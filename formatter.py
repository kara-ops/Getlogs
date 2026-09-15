import logging 
import json 
from datetime import datetime, timezone
from context import get_request_id

class JSONFormatter(logging.Formatter):
    def format(self,record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger_name": record.name,
            "request_id": get_request_id()

        }
        return json.dumps(log_data)

        
