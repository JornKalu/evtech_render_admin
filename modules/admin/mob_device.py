from typing import List, Dict
from database.model import create_mobility_device, update_mobility_device, delete_mobility_device, get_single_mobility_device_by_id, get_single_mobility_devices_by_user_id, get_single_mobility_devices_by_user_id_and_status, get_single_mobility_devices_by_type, get_single_mobility_devices_by_type_id_and_status, get_single_mobility_devices_by_status, get_all_mobility_devices, search_mobility_devices, count_mobility_devices
from sqlalchemy.orm import Session
from modules.utils.tools import process_schema_dictionary, generate_host_id
from fastapi_pagination.ext.sqlalchemy import paginate

def generate_mob_device_code(db: Session):
    num = count_mobility_devices(db=db)
    return "MOB_" + str(num + 1)

def insert_new_mobility_device(db: Session, user_id: int = 0, name: str = None, device_type_id: int = 0, model: str = None, registration_number: str = None, vin: str = None, latitude: str = None, longitude: str = None, conversion_date: str = None, front_image: str = None, left_image: str = None, right_image: str = None, back_image: str = None, created_by: int=0):
    num = count_mobility_devices(db=db) + 1
    # code = generate_mob_device_code(db=db)
    code = generate_host_id(first_char="M", number=num)
    mob_device = create_mobility_device(db=db, user_id=user_id, code=code, name=name, device_type_id=device_type_id, model=model, registration_number=registration_number, vin=vin, latitude=latitude, longitude=longitude, conversion_date=conversion_date, front_image=front_image, left_image=left_image, right_image=right_image, back_image=back_image, created_by=created_by)
    mob_device_info = get_single_mobility_device_by_id(db=db, id=mob_device.id)
    return {
        'status': True,
        'message': 'Success',
        'data': mob_device_info,
    }

def update_existing_mobility_device(db: Session, device_id: int = 0, values: Dict = {}, updated_by: int = 0):
    values = process_schema_dictionary(info=values)
    values['updated_by'] = updated_by
    update_mobility_device(db=db, id=device_id, values=values)
    return {
        'status': True,
        'message': 'Sucess'
    }

def remove_mobility_device(db: Session, device_id: int = 0):
    delete_mobility_device(db=db, id=device_id)
    return {
        'status': True,
        'message': 'Sucess'
    }

def retrieve_mob_devices(db: Session):
    data = get_all_mobility_devices(db=db)
    return paginate(data)

def retrieve_mob_devices_by_user_id(db: Session, user_id: int = 0):
    data = get_single_mobility_devices_by_user_id(db=db, user_id=user_id)
    return paginate(data)

def retrieve_mob_devices_by_user_id_and_status(db: Session, user_id: int = 0, status: int = 0):
    data = get_single_mobility_devices_by_user_id_and_status(db=db, user_id=user_id, status=status)
    return paginate(data)

def retrieve_mob_devices_by_type_id(db: Session, type_id: int = 0):
    data = get_single_mobility_devices_by_type(db=db, type_id=type_id)
    return paginate(data)

def retrieve_mob_devices_by_type_id_and_status(db: Session, type_id: int = 0, status: int = 0):
    data = get_single_mobility_devices_by_type_id_and_status(db=db, type_id=type_id, status=status)
    return paginate(data)

def retrieve_mob_devices_by_status(db: Session, status: int = 0):
    data = get_single_mobility_devices_by_status(db=db, status=status)
    return paginate(data)

def retrieve_mob_devices_by_search(db: Session, query: str = None):
    data = search_mobility_devices(db=db, query=query)
    return paginate(data)

def retrieve_single_mob_device_by_id(db: Session, id: int=0):
    mob_device = get_single_mobility_device_by_id(db=db, id=id)
    if mob_device is None:
        return {
            'status': False,
            'message': 'Not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': mob_device
        }