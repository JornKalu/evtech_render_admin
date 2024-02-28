from logging import log
from fastapi import APIRouter, Request, Depends, HTTPException
from modules.authentication.auth import auth, login_admin, register_admin, get_loggedin_admin, update_admin_details, update_admin_password
from database.schema import AdminLoginModel, AdminRegisterModel, AdminAuthResponseModel, AdminAuthRegisterResponseModel, AdminAuthUpdateResponseModel, AdminUpdateDetailsModel, AdminDetailsModel, AdminDetailResponseModel, AdminUpdatePassword, ErrorResponse
from database.db import get_session
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/v1/auth",
    tags=["v1_admin_auth"]
)

@router.post("/register/", response_model=AdminAuthRegisterResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def register(request: Request, fields: AdminRegisterModel, db: Session = Depends(get_session), admin=Depends(auth.auth_wrapper)):
    ip = request.client.host
    req = register_admin(db=db, role_id=fields.role_id, username=fields.username, email=fields.email, phone_number=fields.phone_number, password=fields.password, created_by=admin['id'])
    return req

@router.post("/login/", response_model=AdminAuthResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def login(request: Request, fields: AdminLoginModel, db: Session = Depends(get_session)):
    ip = request.client.host
    req = login_admin(db=db, field=fields.field, password=fields.password)
    return req

@router.get("/details", response_model=AdminDetailResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_details(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session)):
    return get_loggedin_admin(db=db, admin_id=admin['id'])

@router.post("/update/{admin_id}", response_model=AdminAuthUpdateResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update_admin(request: Request, fields: AdminUpdateDetailsModel, db: Session = Depends(get_session), admin=Depends(auth.auth_admin_wrapper), admin_id: int=0):
    updict = fields.dict()
    req = update_admin_details(db=db, admin_id=admin_id, values=updict, updated_by=admin['id'])
    return req

@router.post("/update_password/", response_model=AdminAuthUpdateResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update_password_admin(request: Request, fields: AdminUpdatePassword, db: Session = Depends(get_session), admin=Depends(auth.auth_admin_wrapper)):
    req = update_admin_password(db=db, admin_id=admin['id'], password=fields.password, old_password=fields.old_password)
    return req
