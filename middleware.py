from starlette.middleware.base import BaseHTTPMiddleware
from context import set_request_id,get_request_id,reset_request_id
import uuid
from starlette.requests import Request



class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next):
        request_id = request.headers.get("X-Request-ID",None)
        if not request_id:
            request_id = str(uuid.uuid4())
        token = set_request_id(request_id)
        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            return response
        finally:
            reset_request_id(token)




