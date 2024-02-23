from fastapi import APIRouter, Request, Depends, HTTPException
from modules.authentication.auth import auth
from modules.admin.battery import insert_new_battery, update_existing_battery, remove_battery, retrieve_single_battery, retrieve_batteries, retrieve_batteries_by_type, retrieve_batteries_by_status, retrieve_batteries_by_search, retrieve_batteries_by_station_id, retrieve_batteries_by_user_id
from database.schema import CreateBatteryModel, BatteryModel, CreateBatteryResponseModel, UpdateBatteryModel, GeneralBatteryResponseModel, ErrorResponse
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page

router = APIRouter(
    prefix="/v1/batteries",
    tags=["v1_admin_battery"]
)


@router.post("/create", response_model=CreateBatteryResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def create(request: Request, fields: CreateBatteryModel, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session)):
    req = insert_new_battery(db=db, type_id=fields.type_id, name=fields.name, description=fields.description, created_by=admin['id'])
    return req

@router.post("/update/{battery_id}", response_model=GeneralBatteryResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def create(request: Request, fields: UpdateBatteryModel, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), battery_id: int=0):
    updict = fields.dict()
    req = update_existing_battery(db=db, battery_id=battery_id, values=updict, updated_by=admin['id'])
    return req

@router.get("/get_all", response_model=Page[BatteryModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session)):
    return retrieve_batteries(db=db)

@router.get("/by_type/{type_id}", response_model=Page[BatteryModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def search(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), type_id: int = 0):
    return retrieve_batteries_by_type(db=db, type_id=type_id)

@router.get("/by_status/{status}", response_model=Page[BatteryModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def search(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), status: int = 0):
    return retrieve_batteries_by_status(db=db, status=status)

@router.get("/by_station/{station_id}", response_model=Page[BatteryModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def by_station(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), station_id: int = 0):
    return retrieve_batteries_by_station_id(db=db, station_id=station_id)

@router.get("/by_user/{user_id}", response_model=Page[BatteryModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def by_user(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), user_id: int = 0):
    return retrieve_batteries_by_user_id(db=db, user_id=user_id)

@router.get("/search/{query}", response_model=Page[BatteryModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def search(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), query: str = None):
    return retrieve_batteries_by_search(db=db, query=query)

@router.get("/get_single/{battery_id}", response_model=CreateBatteryResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), battery_id: int = 0):
    return retrieve_single_battery(db=db, id=battery_id)

@router.delete("/delete/{battery_id}", response_model=GeneralBatteryResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def delete(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), battery_id: int = 0):
    return remove_battery(db=db, battery_id=battery_id)
