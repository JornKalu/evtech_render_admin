from database.model import get_single_user_by_id, get_single_user_by_username, get_single_user_by_phone_number, get_single_user_by_email, get_users, search_user
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate
from modules.utils.net import process_phone_number

def retrieve_users(db: Session):
    data = get_users(db)
    return paginate(data)

def retrieve_users_by_search(db: Session, query: str=None):
    data = search_user(db, query=query)
    return paginate(data)

def retrieve_user_by_id(db: Session, id: int=0):
    user = get_single_user_by_id(db=db, id=id)
    if user is None:
        return {
            'status': False,
            'message': 'User not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': user
        }
    
def retrieve_user_by_username(db: Session, username: str=None):
    user = get_single_user_by_username(db=db, username=username)
    if user is None:
        return {
            'status': False,
            'message': 'User not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': user
        }
    
def retrieve_user_by_email(db: Session, email: str=None):
    user = get_single_user_by_email(db=db, email=email)
    if user is None:
        return {
            'status': False,
            'message': 'User not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': user
        }
    
def retrieve_user_by_phone_number(db: Session, phone_number: str=None):
    country_code = "NG"
    processed_phone_number = process_phone_number(phone_number=phone_number, country_code=country_code)
    if processed_phone_number['status'] == False:
        return {
            'status': False,
            'message': processed_phone_number['message'],
            'data': None
        }
    else:
        phone = processed_phone_number['phone_number']
        user = get_single_user_by_phone_number(db=db, phone_number=phone)
        if user is None:
            return {
                'status': False,
                'message': 'User not found',
                'data': None
            }
        else:
            return {
                'status': True,
                'message': 'Success',
                'data': user
            }
    