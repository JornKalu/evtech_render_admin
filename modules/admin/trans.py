from database.model import get_single_transaction_by_id, get_single_transaction_by_reference, get_single_transaction_by_external_reference, get_transactions_by_user_id, get_transactions_by_user_id_and_status,  get_deposits_transactions, get_deposits_transactions_by_user_id, get_collections_transactions, get_collections_transactions_by_user_id, get_all_transactions, search_transactions, get_all_transactions_between_dates, get_transactions_by_station_id, get_transactions_by_mobility_device_id, get_transactions_filtered
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from modules.utils.tools import process_datetime_string

def retrieve_transactions(db: Session):
    data = get_all_transactions(db)
    return paginate(data)

def retrieve_user_transactions(db: Session, user_id: int=0):
    data = get_transactions_by_user_id(db, user_id=user_id)
    return paginate(data)

def retrieve_station_transactions(db: Session, station_id: int=0):
    data = get_transactions_by_station_id(db, station_id=station_id)
    return paginate(data)

def retrieve_mobility_device_transactions(db: Session, mobility_device_id: int=0):
    data = get_transactions_by_mobility_device_id(db, mobility_device_id=mobility_device_id)
    return paginate(data)

def retrieve_user_transactions_by_status(db: Session, user_id: int=0, status: int=0):
    data = get_transactions_by_user_id_and_status(db, user_id=user_id, status=status)
    return paginate(data)

def retrieve_deposit_transactions(db: Session):
    data = get_deposits_transactions(db)
    return paginate(data)

def retrieve_user_deposit_transactions(db: Session, user_id: int=0):
    data = get_deposits_transactions_by_user_id(db, user_id=user_id)
    return paginate(data)

def retrieve_collection_transactions(db: Session):
    data = get_collections_transactions(db)
    return paginate(data)

def retrieve_user_collection_transactions(db: Session, user_id: int=0):
    data = get_collections_transactions_by_user_id(db, user_id=user_id)
    return paginate(data)

def retrieve_search_transactions(db: Session, query: str=None):
    data = search_transactions(db, query=query)
    return paginate(data)

def retrieve_transactions_between_dates(db: Session, from_date: str = None, to_date: str = None):
    from_date = process_datetime_string(time_str=from_date)
    to_date = process_datetime_string(time_str=to_date)
    data = get_all_transactions_between_dates(db, from_date=from_date, to_date=to_date)
    return paginate(data)

def retrive_filtered_transactions(db: Session, user_id: int = None, station_id: int = None, mobility_device_id: int = None, from_date: str = None, to_date: str = None):
    from_date = process_datetime_string(time_str=from_date)
    to_date = process_datetime_string(time_str=to_date)
    data = get_transactions_filtered(db, user_id=user_id, station_id=station_id, mobility_device_id=mobility_device_id, from_date=from_date, to_date=to_date)
    return paginate(data)

def retrieve_single_transaction_by_id(db: Session, id: int=0):
    transaction = get_single_transaction_by_id(db=db, id=id)
    if transaction is None:
        return {
            'status': False,
            'message': 'Not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': transaction
        }

def retrieve_single_transaction_by_reference(db: Session, reference: str=None):
    transaction = get_single_transaction_by_reference(db=db, reference=reference)
    if transaction is None:
        return {
            'status': False,
            'message': 'Not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': transaction
        }

def retrieve_single_transaction_by_external_reference(db: Session, external_reference: str=None):
    transaction = get_single_transaction_by_external_reference(db=db, external_reference=external_reference)
    if transaction is None:
        return {
            'status': False,
            'message': 'Not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': transaction
        }