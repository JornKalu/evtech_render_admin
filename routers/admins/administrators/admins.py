from typing import List
from fastapi import APIRouter, Request, Depends, HTTPException
from modules.authentication.auth import auth
from modules.admin.manage import retrieve_admins, retrieve_single_admin
from database.schema import AdminModel, AdminNeoModel, AdminDetailResponseModel, ErrorResponse
from database.db import get_session, get_db
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page

router = APIRouter(
    prefix="/v1",
    tags=["v1_admin"]
)

@router.get("/get_all", response_model=Page[AdminNeoModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_db)):
    return retrieve_admins(db=db)

@router.get("/get_single/{admin_id}", response_model=AdminDetailResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), admin_id: int = 0):
    return retrieve_single_admin(db=db, admin_id=admin_id)

