from typing import List
from fastapi import APIRouter, Request, Depends, HTTPException
from modules.authentication.auth import auth
from modules.admin.manage import retrieve_roles, retrieve_single_role, insert_new_role, update_admin_role, remove_role
from database.schema import RoleModel, ErrorResponse, CreateRoleModel, UpdateRoleModel, CreateRoleResponseModel, RoleOtherResponse
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page

router = APIRouter(
    prefix="/v1/roles",
    tags=["v1_admin_role"]
)


@router.post("/create", response_model=CreateRoleResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def create(request: Request, fields: CreateRoleModel, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session)):
    req = insert_new_role(db=db, name=fields.name, description=fields.description, functions=fields.functions, created_by=admin['id'])
    return req

@router.post("/update/{role_id}", response_model=RoleOtherResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def create(request: Request, fields: UpdateRoleModel, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), role_id: int=0):
    updict = fields.dict()
    req = update_admin_role(db=db, role_id=role_id, values=updict, updated_by=admin['id'])
    return req

@router.get("/get_all_roles", response_model=Page[RoleModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all_roles(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session)):
    return retrieve_roles(db=db)

@router.get("/get_single/{role_id}", response_model=RoleOtherResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), role_id: int = 0):
    return retrieve_single_role(db=db, id=role_id)

@router.delete("/delete/{role_id}", response_model=RoleOtherResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), role_id: int = 0):
    return remove_role(db=db, role_id=role_id)
