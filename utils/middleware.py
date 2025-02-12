from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class DummyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print("### request info:", request.url, request.method)
        print("### request type", type(request))

        response = await call_next(request)
        return response
    
"""
INFO:     127.0.0.1:34964 - "GET /blogs/show/2 HTTP/1.1" 200 OK
### request info: http://127.0.0.1:8081/blogs/ GET
### request type <class 'starlette.middleware.base._CachedRequest'>
INFO:     127.0.0.1:34964 - "GET /blogs/ HTTP/1.1" 200 OK
"""