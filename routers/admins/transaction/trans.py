from fastapi import APIRouter, Request, Depends, HTTPException
from modules.authentication.auth import auth
from modules.admin.trans import retrieve_single_transaction_by_id, retrieve_single_transaction_by_reference, retrieve_single_transaction_by_external_reference, retrieve_transactions, retrieve_user_transactions, retrieve_user_transactions_by_status, retrieve_deposit_transactions, retrieve_user_deposit_transactions, retrieve_collection_transactions, retrieve_user_collection_transactions, retrieve_search_transactions, retrieve_transactions_between_dates, retrieve_station_transactions, retrieve_mobility_device_transactions, retrive_filtered_transactions
from database.schema import TransactionModel, ErrorResponse, GeneralTransactionResponseModel
from database.db import get_session
from sqlalchemy.orm import Session
from fastapi_pagination import LimitOffsetPage, Page

router = APIRouter(
    prefix="/v1/transactions",
    tags=["v1_admin_transactions"]
)

@router.get("/get_all", response_model=Page[TransactionModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_all(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session)):
    return retrieve_transactions(db=db)

@router.get("/get_user/{user_id}", response_model=Page[TransactionModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_users(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), user_id: int=0):
    return retrieve_user_transactions(db=db, user_id=user_id)

@router.get("/get_user_by_status/{user_id}/{status}", response_model=Page[TransactionModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_users_by_status(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), user_id: int=0, status: int=0):
    return retrieve_user_transactions_by_status(db=db, user_id=user_id, status=status)

@router.get("/get_deposits", response_model=Page[TransactionModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_deposits(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session)):
    return retrieve_deposit_transactions(db=db)

@router.get("/get_user_deposits/{user_id}", response_model=Page[TransactionModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_user_deposits(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), user_id: int=0):
    return retrieve_user_deposit_transactions(db=db, user_id=user_id)

@router.get("/get_collections", response_model=Page[TransactionModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_collections(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session)):
    return retrieve_collection_transactions(db=db)

@router.get("/get_user_collections/{user_id}", response_model=Page[TransactionModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_user_collections(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), user_id: int=0):
    return retrieve_user_collection_transactions(db=db, user_id=user_id)

@router.get("/get_station/{station_id}", response_model=Page[TransactionModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_station(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), station_id: int=0):
    return retrieve_station_transactions(db=db, station_id=station_id)

@router.get("/get_mobility_device/{mobility_device_id}", response_model=Page[TransactionModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def get_mobility_device(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), mobility_device_id: int=0):
    return retrieve_mobility_device_transactions(db=db, mobility_device_id=mobility_device_id)

@router.get("/search/{query}", response_model=Page[TransactionModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def search(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), query: str=None):
    return retrieve_search_transactions(db=db, query=query)

@router.get("/filtered", response_model=Page[TransactionModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def search(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), user_id: int = None, station_id: int = None, mobility_device_id: int = None, from_date: str = None, to_date: str = None):
    return retrive_filtered_transactions(db=db, user_id=user_id, station_id=station_id, mobility_device_id=mobility_device_id, from_date=from_date, to_date=to_date)

@router.get("/between_dates/{from_date}/{to_date}", response_model=Page[TransactionModel], responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def between_dates(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), from_date: str=None, to_date: str=None):
    return retrieve_transactions_between_dates(db=db, from_date=from_date, to_date=to_date)

@router.get("/by_id/{id}", response_model=GeneralTransactionResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def by_id(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), id: int=0):
    return retrieve_single_transaction_by_id(db=db, id=id)

@router.get("/by_reference/{reference}", response_model=GeneralTransactionResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def by_reference(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), reference: str=None):
    return retrieve_single_transaction_by_reference(db=db, reference=reference)

@router.get("/by_external_reference/{external_reference}", response_model=GeneralTransactionResponseModel, responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}})
async def by_external_reference(request: Request, admin=Depends(auth.auth_admin_wrapper), db: Session = Depends(get_session), external_reference: str=None):
    return retrieve_single_transaction_by_external_reference(db=db, external_reference=external_reference)
