from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class DummyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print("##<DummyMiddleware>## request info:", request.url, request.method)
        print("##<DummyMiddleware>## request type", type(request))

        response = await call_next(request)
        return response
    
"""
INFO:     127.0.0.1:34964 - "GET /blogs/show/2 HTTP/1.1" 200 OK
##<DummyMiddleware>## request info: http://127.0.0.1:8081/blogs/ GET
##<DummyMiddleware>## request type <class 'starlette.middleware.base._CachedRequest'>
INFO:     127.0.0.1:34964 - "GET /blogs/ HTTP/1.1" 200 OK
"""


class MethodOverrideMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print("##<MethodOverrideMiddleware>## request url, query_params, method",
              request.url, request.query_params, request.method)
        if request.method == "POST":
            query = request.query_params
            if query:
                method_override = query["_method"]
                if method_override:
                    method_override = method_override.upper()
                    if method_override in ("PUT", "DELETE"):
                        request.scope["method"] = method_override
        response = await call_next(request)
        return response