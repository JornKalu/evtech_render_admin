from fastapi import APIRouter, Request, Depends, HTTPException
from modules.authentication.auth import auth
from modules.admin.user import retrieve_user_by_id, retrieve_user_by_username, retrieve_user_by_email, retrieve_user_by_phone_number, retrieve_users, retrieve_users_by_search
from database.schema import UserModel, ErrorResponse, UserResponseModel
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page

router = APIRouter(
    prefix="/v1/users",
    tags=["v1_admin_users"]
)

@router.get("/get_all", response_model=Page[UserModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session)):
    return retrieve_users(db=db)

@router.get("/by_username/{username}", response_model=UserResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def by_username(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), username: str=None):
    return retrieve_user_by_username(db=db, username=username)

@router.get("/by_email/{email}", response_model=UserResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def by_email(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), email: str=None):
    return retrieve_user_by_email(db=db, email=email)

@router.get("/by_phone_number/{phone_number}", response_model=UserResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def by_phone_number(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), phone_number: str=None):
    return retrieve_user_by_phone_number(db=db, phone_number=phone_number)

@router.get("/search/{query}", response_model=Page[UserModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def search(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), query: str = None):
    return retrieve_users_by_search(db=db, query=query)

@router.get("/get_single/{user_id}", response_model=UserResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), user_id: int = 0):
    return retrieve_user_by_id(db=db, id=user_id)
