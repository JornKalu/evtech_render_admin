from fastapi import APIRouter, Request, Depends, HTTPException
from modules.authentication.auth import auth
from modules.admin.station import insert_new_station, update_existing_station, remove_station, retrieve_stations, retrieve_stations_by_query, retrieve_stations_slots, retrieve_single_station, retrieve_station_slot_by_number, retrieve_station_slot_by_id
from database.schema import CreateStationModel, StationModel, CreateStationResponseModel, UpdateStationModel, GeneralStationResponse, StationSlotModel, ErrorResponse, GeneralSlotResponse
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page

router = APIRouter(
    prefix="/v1/stations",
    tags=["v1_admin_station"]
)


@router.post("/create", response_model=CreateStationResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def create(request: Request, fields: CreateStationModel, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session)):
    req = insert_new_station(db=db, name=fields.name, description=fields.description, address=fields.address, city=fields.city, state=fields.state, image=fields.image, number_of_slots=fields.number_of_slots, created_by=admin['id'])
    return req

@router.post("/update/{station_id}", response_model=GeneralStationResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def update(request: Request, fields: UpdateStationModel, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), station_id: int=0):
    updict = fields.dict()
    req = update_existing_station(db=db, station_id=station_id, values=updict, updated_by=admin['id'])
    return req

@router.get("/get_all", response_model=Page[StationModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session)):
    return retrieve_stations(db=db)

@router.get("/search/{query}", response_model=Page[StationModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def search(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), query: str = None):
    return retrieve_stations_by_query(db=db, query=query)

@router.get("/get_single/{station_id}", response_model=CreateStationResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_single(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), station_id: int = 0):
    return retrieve_single_station(db=db, id=station_id)

@router.delete("/delete/{station_id}", response_model=GeneralStationResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def delete(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), station_id: int = 0):
    return remove_station(db=db, station_id=station_id)

@router.get("/slots/{station_id}", response_model=Page[StationSlotModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def slots(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), station_id: int = 0):
    return retrieve_stations_slots(db=db, station_id=station_id)

@router.get("/slots_by_number/{station_id}/{slot_number}", response_model=GeneralSlotResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def slots_by_number(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), station_id: int = 0, slot_number: int = 0):
    return retrieve_station_slot_by_number(db=db, station_id=station_id, slot_number=slot_number)

@router.get("/single_slot/{slot_id}", response_model=GeneralSlotResponse, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def single_slot(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), slot_id: int = 0):
    return retrieve_station_slot_by_id(db=db, id=slot_id)

