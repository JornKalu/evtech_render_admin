from typing import Dict
from database.model import user_login, get_single_user_by_phone_number, get_single_user_by_email, update_user, get_single_user_by_id, delete_user, update_profile_by_user_id, get_wallet_by_user_id, update_user_active_device, get_profile_by_user_id, get_single_setting_by_user_id, create_user_with_other_rows, registration_unique_field_check, admin_login, create_admin, get_single_admin_by_id, get_single_role_by_id, admin_registration_unique_field_check, update_admin, delete_admin, get_admins, manage_user_device
from modules.utils.net import get_ip_info, process_phone_number
from modules.utils.tools import process_schema_dictionary
from modules.utils.auth import AuthHandler, get_next_few_minutes, check_if_time_as_pass_now
from sqlalchemy.orm import Session
import random
import datetime
import random

auth = AuthHandler()

def login_user(db: Session, phone_number: str=None, password: str=None, device_name: str=None, imei: str=None, mac_address: str=None, fbt: str=None):
    country_code = "NG"
    processed_phone_number = process_phone_number(phone_number=phone_number, country_code=country_code)
    if processed_phone_number['status'] == True:
        phone = processed_phone_number['phone_number']
        user = user_login(db=db, field=phone)
        if user is None:
            return {
                'status': False,
                'message': 'Phone Number Incorrect',
                'data': None
            }
        else:
            if not auth.verify_password(plain_password=password, hashed_password=user.password):
                return {
                    'status': False,
                    'message': 'Password Incorrect',
                    'data': None
                }
            else:
                if user.status == 0:
                    return {
                        'status': False,
                        'message': 'This account has been locked',
                        'data': None
                    }
                else:
                    if user.deleted_at is not None:
                        return {
                            'status': False,
                            'message': 'This account has been deactivated',
                            'data': None
                        }
                    else:
                        user_device = manage_user_device(db=db, user_id=user.id, device_name=device_name, imei=imei, mac_address=mac_address, fbt=fbt)
                        payload = {
                            'id': user.id,
                            'username': user.username,
                            'phone_number': user.phone_number,
                            'email': user.email,
                            'token_type': 2,
                            'device_id': user_device.id
                        }
                        token = auth.encode_token(user=payload)
                        da = {
                            'fbt': fbt
                        }
                        update_user_active_device(db=db, user_id=user.id, values=da)
                        profile = get_profile_by_user_id(db=db, user_id=user.id)
                        setting = get_single_setting_by_user_id(db=db, user_id=user.id)
                        wallet = get_wallet_by_user_id(db=db, user_id=user.id)
                        pin_available = False
                        if user.pin is not None:
                            pin_available = True
                        data = {
                            'access_token': token,
                            'id': user.id,
                            'username': user.username,
                            'phone_number': user.phone_number,
                            'email': user.email,
                            'profile': profile,
                            'setting': setting,
                            'wallet': wallet,
                            'pin_available': pin_available,
                        }
                        return {
                            'status': True,
                            'message': 'Login Success',
                            'data': data,
                        }
            
    else:
        return {
            'status': False,
            'message': processed_phone_number['message'],
            'data': None
        }

def register_user(db: Session, username: str=None, phone_number: str=None, email: str=None, password: str=None, device_name: str=None, imei: str=None, mac_address: str=None, fbt: str=None):
    country_code = "NG"
    processed_phone_number = process_phone_number(phone_number=phone_number, country_code=country_code)
    if processed_phone_number['status'] == True:
        check = registration_unique_field_check(db=db, phone_number=processed_phone_number['phone_number'], username=username, email=email)
        if check['status'] == False:
            return {
                'status': False,
                'message': check['message'],
                'data': None,
            }
        else:
            hashed_password = auth.get_password_hash(password=password)
            user = create_user_with_other_rows(db=db, phone_number=processed_phone_number['phone_number'], email=email, password=hashed_password, username=username, device_name=device_name, imei=imei, mac_address=mac_address, fbt=fbt)
            payload = {
                'id': user.id,
                'username': user.username,
                'phone_number': user.phone_number,
                'email': user.email,
                'fbt': fbt,
                'token_type': 2
            }
            profile = get_profile_by_user_id(db=db, user_id=user.id)
            setting = get_single_setting_by_user_id(db=db, user_id=user.id)
            wallet = get_wallet_by_user_id(db=db, user_id=user.id)
            token = auth.encode_token(user=payload)
            pin_available = False
            data = {
                'access_token': token,
                'id': user.id,
                'username': user.username,
                'phone_number': user.phone_number,
                'email': user.email,
                'profile': profile,
                'setting': setting,
                'wallet': wallet,
                'pin_available': pin_available,
            }
            return {
                'status': True,
                'message': 'Registration successful',
                'data': data,
            }

    else:
        return {
            'status': False,
            'message': processed_phone_number['message'],
            'data': None
        }

def get_loggedin_user_info(db: Session, user_id: int=0):
    user = get_single_user_by_id(db=db, id=user_id)
    if user is None:
        return {
            'status': False,
            'message': 'User not found',
            'data': None
        }
    else:
        profile = get_profile_by_user_id(db=db, user_id=user.id)
        setting = get_single_setting_by_user_id(db=db, user_id=user.id)
        wallet = get_wallet_by_user_id(db=db, user_id=user.id)
        pin_available = False
        if user.pin is not None:
            pin_available = True
        data = {
            'id': user.id,
            'username': user.username,
            'phone_number': user.phone_number,
            'email': user.email,
            'profile': profile,
            'setting': setting,
            'wallet': wallet,
            'pin_available': pin_available,
        }
        return {
            'status': True,
            'message': 'Success',
            'data': data,
        }

def update_user_pin(db: Session, user_id: int=0, pin: str=None):
    pin = auth.get_password_hash(password=pin)
    da = {
        'pin': pin
    }
    update_user(db=db, id=user_id, values=da)
    return {
        'status': True,
        'message': 'Success'
    }

def verify_user_pin(db: Session, user_id: int=0, pin: str=None):
    user_info = get_single_user_by_id(db=db, id=user_id)
    if user_info is None:
        return {
            'status': False,
            'message': 'User not found',
        }
    else:
        if auth.verify_password(plain_password=pin, hashed_password=user_info.pin) == True:
            return {
                'status': True,
                'message': 'Pin Correct'
            }
        else:
            return {
                'status': False,
                'message': 'Pin Incorrect'
            }
                       
def update_user_password(db: Session, user_id: int=0, password: str=None, old_password: str = None):
    user_info = get_single_user_by_id(db=db, id=user_id)
    if user_info is None:
        return {
            'status': False,
            'message': 'User not found',
        }
    else:
        if auth.verify_password(plain_password=old_password, hashed_password=user_info.password) == True:
            password = auth.get_password_hash(password=password)
            da = {
                'password': password
            }
            update_user(db=db, id=user_id, values=da)
            return {
                'status': True,
                'message': 'Success'
            }
        else:
            return {
                'status': False,
                'message': 'Old Password Incorrect'
            }
    
def remove_user(db: Session, user_id: int = 0, password: str = None):
    user = get_single_user_by_id(db=db, id=user_id)
    if user is not None:
        if auth.verify_password(plain_password=password, hashed_password=user.password):
            user_wallet = get_wallet_by_user_id(db=db, user_id=user_id)
            if user_wallet is not None:
                if user_wallet.balance > -1:
                    delete_user(db=db, id=user_id)
                    return {
                        'status': True,
                        'message': 'Success'
                    }
                else:
                    return {
                        'status': False,
                        'message': 'User cannot be deleted due to balance'
                    }
            else:
                return {
                    'status': False,
                    'message': 'Wallet not found'
                }
        else:
            return {
                'status': False,
                'message': 'Incorrect Password'
            }
    else:
        return {
            'status': False,
            'message': 'User does not exist'
        }
    
def login_admin(db: Session, field: str=None, password: str=None):
    return [field, password]
    admin = admin_login(db=db, field=field)
    if admin is None:
        return {
            'status': False,
            'message': 'Username or Email not found',
            'data': None,
        }
    else:
        if not auth.verify_password(plain_password=password, hashed_password=admin.password):
            return {
                'status': False,
                'message': 'Incorrect Password',
                'data': None,
            }
        else:
            if admin.status == 0:
                return {
                    'status': False,
                    'message': 'Admin has been deactivated',
                    'data': None,
                }
            else:
                if admin.deleted_at is not None:
                    return {
                        'status': False,
                        'message': 'Admin has been deleted',
                        'data': None,
                    }
                else:
                    payload = {
                        'id': admin.id,
                        'username': admin.username,
                        'phone_number': admin.phone_number,
                        'email': admin.email,
                        'role_id': admin.role_id,
                        'token_type': 1,
                    }
                    token = auth.encode_token(user=payload)
                    data = {
                        'access_token': token,
                        'id': admin.id,
                        'username': admin.username,
                        'phone_number': admin.phone_number,
                        'email': admin.email,
                        'first_name': admin.first_name,
                        'other_name': admin.other_name,
                        'last_name': admin.last_name,
                        'address': admin.address,
                        'gender': admin.gender,
                        'avatar': admin.avatar,
                        'role': get_single_role_by_id(db=db, id=admin.role_id)
                    }
                    return {
                        'status': True,
                        'message': 'Login Success',
                        'data': data,
                    }

def register_admin(db: Session, role_id: int = 0, username: str = None, email: str = None, phone_number: str = None, password: str = None, created_by: int=0):
    check = admin_registration_unique_field_check(db=db, username=username, email=email)
    if check['status'] == False:
        return {
            'status': False,
            'message': check['message'],
            'data': None,
        }
    else:
        hashed_password = auth.get_password_hash(password=password)
        admin = create_admin(db=db, role_id=role_id, email=email, phone_number=phone_number, username=username, password=hashed_password, status=1, created_by=created_by)
        data = {
            'id': admin.id,
            'username': admin.username,
            'phone_number': admin.phone_number,
            'email': admin.email,
            'first_name': admin.first_name,
            'other_name': admin.other_name,
            'last_name': admin.last_name,
            'address': admin.address,
            'gender': admin.gender,
            'avatar': admin.avatar,
            'role': get_single_role_by_id(db=db, id=admin.role_id),
            'created_at': admin.created_at,
        }
        return {
            'status': True,
            'message': 'Success',
            'data': data,
        }
    
def get_loggedin_admin(db: Session, admin_id: str=None):
    admin = get_single_admin_by_id(db=db, id=admin_id)
    if admin is None:
        return {
            'status': False,
            'message': 'Admin not found',
            'data': None
        }
    else:
        data = {
            'id': admin.id,
            'username': admin.username,
            'phone_number': admin.phone_number,
            'email': admin.email,
            'first_name': admin.first_name,
            'other_name': admin.other_name,
            'last_name': admin.last_name,
            'address': admin.address,
            'gender': admin.gender,
            'avatar': admin.avatar,
            'role': get_single_role_by_id(db=db, id=admin.role_id)
        }
        return {
            'status': True,
            'message': 'Success',
            'data': data,
        }
    
def update_admin_details(db: Session, admin_id: int=0, values: Dict={}, updated_by: int=0):
    values = process_schema_dictionary(info=values)
    if updated_by != admin_id:
        values['updated_by'] = updated_by
    update_admin(db=db, id=admin_id, values=values)
    return {
        'status': True,
        'message': 'Success'
    }

def update_admin_password(db: Session, admin_id: int=0, password: str=None, old_password: str = None):
    admin_info = get_single_admin_by_id(db=db, id=admin_id)
    if admin_info is None:
        return {
            'status': False,
            'message': 'Not found'
        }
    else:
        if auth.verify_password(plain_password=old_password, hashed_password=admin_info.password) == True:
            password = auth.get_password_hash(password=password)
            da = {
                'password': password
            }
            update_admin(db=db, id=admin_id, values=da)
            return {
                'status': True,
                'message': 'Success'
            }
        else:
            return {
                'status': False,
                'message': 'Old Password Incorrect'
            }

def remove_admin(db: Session, admin_id: int=0):
    admin_info = get_single_admin_by_id(db=db, id=admin_id)
    if admin_info is None:
        return {
            'status': False,
            'message': 'Not found'
        }
    else:
        delete_admin(db=db, id=admin_id)
        return {
            'status': True,
            'message': 'Success'
        }