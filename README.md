# 🪵 Structured JSON Logger with Request ID Tracking

A lightweight Python logging utility that outputs structured **JSON logs** and automatically propagates **request IDs** across async request lifecycles using Python's `contextvars`. Built with [Starlette](https://www.starlette.io/) middleware support.

---

## 📌 Features

- ✅ **Structured JSON logs** — every log line is a valid JSON object for easy parsing and ingestion into log aggregators (Datadog, ELK, etc.)
- ✅ **Request ID tracking** — correlate all log lines within a single HTTP request using `X-Request-ID`
- ✅ **Context-safe** — uses `contextvars.ContextVar` for async-safe, per-request isolation (no global state pollution)
- ✅ **Starlette middleware** — plug-and-play `RequestIDMiddleware` for FastAPI / Starlette apps
- ✅ **UTC timestamps** — all log entries include an ISO 8601 UTC timestamp
- ✅ **Zero third-party dependencies** for core logging (stdlib only; Starlette only for the middleware)

---

## 📂 Project Structure

```
logs/
├── config.py        # Logging setup — wires up JSONFormatter to the root logger
├── formatter.py     # Custom logging.Formatter that outputs JSON
├── context.py       # ContextVar helpers for request ID lifecycle management
└── middleware.py    # Starlette middleware that injects / propagates X-Request-ID
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- [Starlette](https://www.starlette.io/) (only if using the middleware)

```bash
pip install starlette
```

> If you're using FastAPI, Starlette is already included as a dependency.

---

### Basic Usage (standalone logging)

```python
from config import setup_logging
import logging

setup_logging(level="INFO")

logger = logging.getLogger("my_app")
logger.info("Application started")
logger.error("Something went wrong")
```

**Sample output:**

```json
{"timestamp": "2026-09-17T18:30:00+00:00", "level": "INFO",  "message": "Application started",  "logger_name": "my_app", "request_id": null}
{"timestamp": "2026-09-17T18:30:01+00:00", "level": "ERROR", "message": "Something went wrong", "logger_name": "my_app", "request_id": null}
```

---

### Usage with FastAPI / Starlette

```python
from fastapi import FastAPI
from middleware import RequestIDMiddleware
from config import setup_logging
import logging

setup_logging()

app = FastAPI()
app.add_middleware(RequestIDMiddleware)

logger = logging.getLogger("api")

@app.get("/hello")
async def hello():
    logger.info("Handling /hello request")
    return {"message": "hello"}
```

**Sample output for a request with `X-Request-ID: abc-123`:**

```json
{"timestamp": "2026-09-17T18:30:00+00:00", "level": "INFO", "message": "Handling /hello request", "logger_name": "api", "request_id": "abc-123"}
```

If no `X-Request-ID` header is provided, a UUID is auto-generated for the request.

---

## 🔧 Configuration

### `setup_logging(level: str = "INFO")`

Call once at application startup. Accepts any standard Python log level string:

| Level      | Description                              |
|------------|------------------------------------------|
| `DEBUG`    | Verbose — everything                     |
| `INFO`     | General operational messages             |
| `WARNING`  | Something unexpected but not fatal       |
| `ERROR`    | A failure occurred                       |
| `CRITICAL` | A severe error that may halt the program |

```python
setup_logging(level="DEBUG")  # Show all log levels
```

> `setup_logging` is idempotent — calling it multiple times will not add duplicate handlers.

---

## 📋 Log Output Format

Every log line is a single JSON object with the following fields:

| Field         | Type            | Description                                           |
|---------------|-----------------|-------------------------------------------------------|
| `timestamp`   | `string` (ISO 8601) | UTC time the log record was created               |
| `level`       | `string`        | Log level: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `message`     | `string`        | The log message                                       |
| `logger_name` | `string`        | Name of the logger that emitted the record            |
| `request_id`  | `string` / `null` | The current request ID from context, or `null`      |

---

## 🧩 Module Reference

### `formatter.py` — `JSONFormatter`

A custom `logging.Formatter` subclass that serializes each `LogRecord` into a JSON string. Automatically reads the current `request_id` from the context.

### `context.py` — Request ID Context

| Function | Description |
|---|---|
| `set_request_id(request_id: str)` | Sets the request ID in the current async context. Returns a `Token` for later reset. |
| `get_request_id() -> Optional[str]` | Returns the current request ID, or `None` if not set. |
| `reset_request_id(token)` | Resets the context variable to its previous value using the token. |

### `middleware.py` — `RequestIDMiddleware`

A Starlette `BaseHTTPMiddleware` that:
1. Reads `X-Request-ID` from incoming request headers, or generates a UUID if absent.
2. Injects the ID into the async context via `set_request_id`.
3. Forwards `X-Request-ID` in the response headers.
4. Safely resets the context after the request completes (even on errors).

### `config.py` — `setup_logging`

Bootstraps the root Python logger with the `JSONFormatter` attached to a `StreamHandler` (stdout/stderr). Safe to call multiple times.

---

## 💡 Why Structured Logging?

Plain text logs are hard to query at scale. Structured JSON logs let you:

- **Filter** by log level, logger name, or request ID instantly
- **Ingest** into tools like **Datadog**, **Elasticsearch (ELK)**, **Google Cloud Logging**, or **AWS CloudWatch** with zero parsing config
- **Correlate** every log line within a single request using `request_id`

---

## 📄 License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).
