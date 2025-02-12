from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse

from routes import blog

from utils.common import lifespan
from utils import exc_handler, middleware

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(middleware.DummyMiddleware)
app.add_middleware(middleware.MethodOverrideMiddleware)     # 얘 부터 적용됨...

app.include_router(blog.router)

@app.get("/")
def redirect_to_blogs():
    return RedirectResponse(url="/blogs")

app.add_exception_handler(StarletteHTTPException, exc_handler.custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, exc_handler.validation_exception_handler)