from fastapi import APIRouter, Request, Depends, HTTPException
from modules.authentication.auth import auth
from modules.admin.mob_device import insert_new_mobility_device, update_existing_mobility_device, remove_mobility_device, retrieve_mob_devices, retrieve_mob_devices_by_user_id, retrieve_mob_devices_by_user_id_and_status, get_single_mobility_devices_by_user_id_and_status, retrieve_mob_devices_by_type_id, retrieve_mob_devices_by_type_id_and_status, retrieve_mob_devices_by_status, retrieve_mob_devices_by_search, retrieve_single_mob_device_by_id
from database.schema import CreateMobDeviceModel, MobilityDeviceModel, CreateMobDeviceResponse, UpdateMobDeviceModel, GeneralMobDevTypeResponse, ErrorResponse
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page

router = APIRouter(
    prefix="/v1/mobility_devices",
    tags=["v1_admin_mobility_device"]
)


@router.post("/create", response_model=CreateMobDeviceResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def create(request: Request, fields: CreateMobDeviceModel, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session)):
    req = insert_new_mobility_device(db=db, user_id=fields.user_id, device_type_id=fields.device_type_id, name=fields.name, model=fields.model, registration_number=fields.registration_number, vin=fields.vin, conversion_date=fields.conversion_date, front_image=fields.front_image, left_image=fields.left_image, right_image=fields.right_image, back_image=fields.back_image, created_by=admin['id'])
    return req

@router.post("/update/{device_id}", response_model=GeneralMobDevTypeResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update(request: Request, fields: UpdateMobDeviceModel, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), device_id: int=0):
    updict = fields.dict()
    req = update_existing_mobility_device(db=db, device_id=device_id, values=updict, updated_by=admin['id'])
    return req

@router.get("/get_all", response_model=Page[MobilityDeviceModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session)):
    return retrieve_mob_devices(db=db)

@router.get("/get_user/{user_id}", response_model=Page[MobilityDeviceModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_user(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), user_id: int = 0):
    return retrieve_mob_devices_by_user_id(db=db, user_id=user_id)

@router.get("/get_user_by_status/{user_id}/{status}", response_model=Page[MobilityDeviceModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_user_by_status(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), user_id: int = 0, status: int = 0):
    return retrieve_mob_devices_by_user_id_and_status(db=db, user_id=user_id, status=status)

@router.get("/get_type/{type_id}", response_model=Page[MobilityDeviceModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_type(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), type_id: int = 0):
    return retrieve_mob_devices_by_type_id(db=db, type_id=type_id)

@router.get("/get_type_by_status/{type_id}/{status}", response_model=Page[MobilityDeviceModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_type_by_status(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), type_id: int = 0, status: int = 0):
    return retrieve_mob_devices_by_type_id_and_status(db=db, type_id=type_id, status=status)

@router.get("/get_by_status/{status}", response_model=Page[MobilityDeviceModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_by_status(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), status: int = 0):
    return retrieve_mob_devices_by_status(db=db, status=status)

@router.get("/search/{query}", response_model=Page[MobilityDeviceModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def search(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), query: str = None):
    return retrieve_mob_devices_by_search(db=db, query=query)

@router.get("/get_single/{device_id}", response_model=CreateMobDeviceResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), device_id: int = 0):
    return retrieve_single_mob_device_by_id(db=db, id=device_id)

@router.delete("/delete/{device_id}", response_model=GeneralMobDevTypeResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def delete(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), device_id: int = 0):
    return remove_mobility_device(db=db, device_id=device_id)
