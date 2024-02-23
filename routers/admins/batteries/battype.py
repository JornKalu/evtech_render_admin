from fastapi import APIRouter, Request, Depends, HTTPException
from modules.authentication.auth import auth
from modules.admin.battery import insert_new_battery_type, update_existing_battery_type, remove_battery_type, retrieve_battery_types, retrieve_single_battery_type
from database.schema import BatteryTypeModel, CreateBatteryTypeModel, UpdateBatteryTypeModel, CreateBatteryTypeResponseModel, GeneralBatteryResponseModel, ErrorResponse
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page

router = APIRouter(
    prefix="/v1/battery_types",
    tags=["v1_admin_battery_type"]
)


@router.post("/create", response_model=CreateBatteryTypeResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def create(request: Request, fields: CreateBatteryTypeModel, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session)):
    req = insert_new_battery_type(db=db, code=fields.code, name=fields.name, description=fields.description, voltage=fields.voltage, power=fields.power, fee=fields.fee, collection_due_days=fields.collection_due_days, collection_due_fees=fields.collection_due_fees, created_by=admin['id'])
    return req

@router.post("/update/{type_id}", response_model=GeneralBatteryResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def create(request: Request, fields: UpdateBatteryTypeModel, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), type_id: int=0):
    updict = fields.dict()
    req = update_existing_battery_type(db=db, type_id=type_id, values=updict, updated_by=admin['id'])
    return req

@router.get("/get_all", response_model=Page[BatteryTypeModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session)):
    return retrieve_battery_types(db=db)

@router.get("/get_single/{type_id}", response_model=CreateBatteryTypeResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), type_id: int = 0):
    return retrieve_single_battery_type(db=db, id=type_id)

@router.delete("/delete/{type_id}", response_model=GeneralBatteryResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def delete(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), type_id: int = 0):
    return remove_battery_type(db=db, type_id=type_id)
