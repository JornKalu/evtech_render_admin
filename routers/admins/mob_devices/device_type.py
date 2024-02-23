from fastapi import APIRouter, Request, Depends, HTTPException
from modules.authentication.auth import auth
from modules.admin.mob_device_type import insert_new_mob_device_type, update_existing_mob_device_type, remove_mob_device_type, retrieve_mob_device_type, retrieve_single_mob_device_type
from database.schema import CreateMobDeviceTypeModel, MobDeviceTypeModel, CreateMobDevTypeResponseModel, UpdateMobDevTypeModel, GeneralMobDevTypeResponse, ErrorResponse
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page

router = APIRouter(
    prefix="/v1/mobility_device_types",
    tags=["v1_admin_mobility_device_type"]
)


@router.post("/create", response_model=CreateMobDevTypeResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def create(request: Request, fields: CreateMobDeviceTypeModel, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session)):
    req = insert_new_mob_device_type(db=db, name=fields.name, description=fields.description, number_of_wheels=fields.number_of_wheels, number_of_batteries=fields.number_of_batteries, number_required_without_return=fields.number_of_batteries, created_by=admin['id'])
    return req

@router.post("/update/{type_id}", response_model=GeneralMobDevTypeResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update(request: Request, fields: UpdateMobDevTypeModel, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), type_id: int=0):
    updict = fields.dict()
    req = update_existing_mob_device_type(db=db, type_id=type_id, values=updict, updated_by=admin['id'])
    return req

@router.get("/get_all", response_model=Page[MobDeviceTypeModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session)):
    return retrieve_mob_device_type(db=db)

@router.get("/get_single/{type_id}", response_model=CreateMobDevTypeResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), type_id: int = 0):
    return retrieve_single_mob_device_type(db=db, id=type_id)

@router.delete("/delete/{type_id}", response_model=GeneralMobDevTypeResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def delete(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), type_id: int = 0):
    return remove_mob_device_type(db=db, type_id=type_id)
