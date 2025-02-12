from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from db.database import context_get_conn
from services import auth_svc
from schemas.auth_schema import UserDataPASS
from sqlalchemy import Connection
from pydantic import EmailStr

# router 생성
router = APIRouter(prefix="/auth", tags=["auth"])
# jinja2 Template 엔진 생성
templates = Jinja2Templates(directory="templates")


@router.get("/register")
async def register_user_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register_user.html",
        context={}
    )


@router.get("/login")
async def login_ui(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )

