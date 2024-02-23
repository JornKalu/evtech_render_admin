from typing import List, Dict
from database.model import create_mobility_device_type, update_mobility_device_type, delete_mobility_device_type, get_single_mobility_device_type_by_id, get_all_mobility_device_types, count_mobility_device_types
from sqlalchemy.orm import Session
from modules.utils.tools import process_schema_dictionary
from fastapi_pagination.ext.sqlalchemy import paginate

def generate_mob_device_type_code(db: Session):
    num = count_mobility_device_types(db=db)
    return "MOBTYPE_" + str(num + 1)

def insert_new_mob_device_type(db: Session, name: str = None, description: str = None, number_of_wheels: int = 0, number_of_batteries: int = 0, number_required_without_return: int = 0, created_by: int = 0):
    code = generate_mob_device_type_code(db=db)
    mob_device_type = create_mobility_device_type(db=db, name=name, code=code, description=description, number_of_wheels=number_of_wheels, number_of_batteries=number_of_batteries, number_required_without_return=number_required_without_return, created_by=created_by)
    return {
        'status': True,
        'message': 'Success',
        'data': mob_device_type
    }

def update_existing_mob_device_type(db: Session, type_id: int = 0, values: Dict = {}, updated_by: int = 0):
    values = process_schema_dictionary(info=values)
    values['updated_by'] = updated_by
    update_mobility_device_type(db=db, id=type_id, values=values)
    return {
        'status': True,
        'message': 'Sucess'
    }

def remove_mob_device_type(db: Session, type_id: int=0):
    delete_mobility_device_type(db=db, id=type_id)
    return {
        'status': True,
        'message': 'Success'
    }

def retrieve_mob_device_type(db: Session):
    data = get_all_mobility_device_types(db=db)
    return paginate(data)

def retrieve_single_mob_device_type(db: Session, id: int=0):
    mob_device_type = get_single_mobility_device_type_by_id(db=db, id=id)
    if mob_device_type is None:
        return {
            'status': False,
            'message': 'Not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': mob_device_type
        }