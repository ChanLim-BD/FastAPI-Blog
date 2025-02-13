import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from routes import blog, auth

from utils.common import lifespan
from utils import exc_handler, middleware
from dotenv import load_dotenv


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(CORSMiddleware, 
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"],
                   allow_credentials=True,
                   max_age=-1)
# app.add_middleware(middleware.DummyMiddleware)
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
# signed cookie 적용
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, max_age=3600)
app.add_middleware(middleware.MethodOverrideMiddleware)     # 얘 부터 적용됨...

app.include_router(blog.router)
app.include_router(auth.router)

@app.get("/")
def redirect_to_blogs():
    return RedirectResponse(url="/blogs")

app.add_exception_handler(StarletteHTTPException, exc_handler.custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, exc_handler.validation_exception_handler)