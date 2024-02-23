from typing import List, Dict
from database.model import create_battery_type, update_battery_type,delete_battery_type, get_all_battery_types, get_single_battery_type_by_id, create_battery, update_battery, delete_battery, get_single_battery_by_id, get_all_batteries, get_batteries_by_type, get_batteries_by_status, search_batteries, check_if_battery_code_exists, count_batteries, get_batteries_by_station_id, get_batteries_by_user_id, check_if_battery_type_code_exist
from sqlalchemy.orm import Session
from modules.utils.tools import process_schema_dictionary, rand_upper_string_generator, generate_battery_code
from fastapi_pagination.ext.sqlalchemy import paginate
import segno
import json
import io

def insert_new_battery_type(db: Session, code: str=None, name: str=None, description: str=None, voltage: str=None, power: str=None, fee: float=0, collection_due_days: int=0, collection_due_fees: float=0, created_by: int=0):
    if check_if_battery_type_code_exist(db=db, code=code) == True:
        return {
            'status': False,
            'message': 'Battery Type Code Already Exist',
            'data': None,
        }
    else:
        battery_type = create_battery_type(db=db, name=name, description=description, voltage=voltage, power=power, fee=fee, collection_due_days=collection_due_days, collection_due_fees=collection_due_fees, status=1, created_by=created_by, updated_by=created_by)
        return {
            'status': True,
            'message': 'Success',
            'data': battery_type
        }

def update_existing_battery_type(db: Session, type_id: int=0, values: Dict={}, updated_by: int=0):
    values = process_schema_dictionary(info=values)
    values['updated_by'] = updated_by
    update_battery_type(db=db, id=type_id, values=values)
    return {
        'status': True,
        'message': 'Success',
    }

def remove_battery_type(db: Session, type_id: int=0):
    delete_battery_type(db=db, id=type_id)
    return {
        'status': True,
        'message': 'Success',
    }

def insert_new_battery(db: Session, type_id: int = 0, name: str = None, description: str = None, created_by: int = 0):
        num = count_batteries(db=db) + 1
        # code = rand_upper_string_generator(size=num)
        code = generate_battery_code(number=num, length=8)
        battery = create_battery(db=db, type_id=type_id, code=code, name=name, description=description, created_by=created_by)
        battery_info = get_single_battery_by_id(db=db, id=battery.id)
        ba_data = {
            'id': battery_info.id,
            'name': battery_info.name,
            'code': battery_info.code,
            'battery_type_name': battery_info.battery_type_name,
        }
        data_dump = json.dumps(ba_data)
        buff = io.BytesIO()
        segno.make(data_dump, error='h').save(buff, kind="svg", xmldecl=False, svgns=False, svgclass=None, lineclass=None, omitsize=True, nl=False)
        val = buff.getvalue().decode('utf-8')
        update_battery(db=db, id=battery_info.id, values={'qr_code': val})
        return {
            'status': True,
            'message': 'Success',
            'data': battery_info
        }

def update_existing_battery(db: Session, battery_id: int=0, values: Dict={}, updated_by: int=0):
    values = process_schema_dictionary(info=values)
    # if 'status' in values:
    #     if values['status'] is not None:
    #         battery_status = values['status']
    #         new_dict = {key: val for key, val in values.items() if key != 'status'}
    #         values = new_dict
    #         values['temp_status'] = battery_status
    values['updated_by'] = updated_by
    update_battery(db=db, id=battery_id, values=values)
    return {
        'status': True,
        'message': 'Success',
    }

def remove_battery(db: Session, battery_id: int=0):
    delete_battery(db=db, id=battery_id)
    return {
        'status': True,
        'message': 'Success'
    }

def retrieve_battery_types(db: Session):
    data = get_all_battery_types(db)
    return paginate(data)

def retrieve_single_battery_type(db: Session, id: int=0):
    battery_type = get_single_battery_type_by_id(db=db, id=id)
    if battery_type is None:
        return {
            'status': False,
            'message': 'Not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': battery_type
        }

def retrieve_batteries(db: Session):
    data = get_all_batteries(db=db)
    return paginate(data)

def retrieve_single_battery(db: Session, id: int=0):
    battery = get_single_battery_by_id(db=db, id=id)
    if battery is None:
        return {
            'status': False,
            'message': 'Not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': battery
        }

def retrieve_batteries_by_type(db: Session, type_id: int=0):
    data = get_batteries_by_type(db=db, type_id=type_id)
    return paginate(data)

def retrieve_batteries_by_status(db: Session, status: int=0):
    data = get_batteries_by_status(db=db, status=status)
    return paginate(data)

def retrieve_batteries_by_search(db: Session, query: str=None):
    data = search_batteries(db=db, query=query)
    return paginate(data)

def retrieve_batteries_by_station_id(db: Session, station_id: int=0):
    data = get_batteries_by_station_id(db=db, station_id=station_id)
    return paginate(data)

def retrieve_batteries_by_user_id(db: Session, user_id: int=0):
    data = get_batteries_by_user_id(db=db, user_id=user_id)
    return paginate(data)
