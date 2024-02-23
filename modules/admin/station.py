from typing import List, Dict
from database.model import create_station, update_station, delete_station, get_single_station_by_id, get_all_stations, search_stations, delete_station, create_station_battery, get_stations_batteries_station_id, get_station_battery_by_slot_number, get_single_station_battery_by_id, count_stations, get_stations_batteries_station_id_alias
from sqlalchemy.orm import Session
from modules.utils.tools import process_schema_dictionary, generate_host_id
from fastapi_pagination.ext.sqlalchemy import paginate

def insert_new_station(db: Session, name: str = None, description: str = None, address: str = None, city: str = None, state: str = None, image: str = None, number_of_slots: int = 0, created_by: int=0):
    if number_of_slots < 1:
        return {
            'status': False,
            'message': 'Number of slot cannot be empty',
            'data': None
        }
    else:
        num = count_stations(db=db) + 1
        code = generate_host_id(first_char="S", number=num)
        station = create_station(db=db, code=code, name=name, description=description, address=address, city=city, state=state, image=image, number_of_slots=number_of_slots, created_by=created_by)
        if number_of_slots > 0:
            for i in range(number_of_slots):
                num = i + 1
                create_station_battery(db=db, station_id=station.id, slot_number=num)
        return {
            'status': True,
            'message': 'Success',
            'data': station
        }

def update_existing_station(db: Session, station_id: int=0, values: Dict={}, updated_by: int=0):
    values = process_schema_dictionary(info=values)
    values['updated_by'] = updated_by
    update_station(db=db, id=station_id, values=values)
    return {
        'status': True,
        'message': 'Success'
    }

def remove_station(db: Session, station_id: int=0):
    delete_station(db=db, id=station_id)
    return {
        'status': True,
        'message': 'Success'
    }

def retrieve_stations(db: Session):
    data = get_all_stations(db=db)
    return paginate(data)

def retrieve_single_station(db: Session, id: int=0):
    station = get_single_station_by_id(db=db, id=id)
    if station is None:
        return {
            'status': False,
            'message': 'Not found',
            'data': None
        }
    else:
        data = {
            'id': station.id,
            'code': station.code,
            'name': station.name,
            'description': station.description,
            'address': station.address,
            'city': station.city,
            'state': station.state,
            'image': station.image,
            'autonomy_charge': station.autonomy_charge,
            'autonomy_charge_time': station.autonomy_charge_time,
            'latitude': station.latitude,
            'longitude': station.longitude,
            'number_of_slots': station.number_of_slots,
            'status': station.status,
            'created_by': station.created_by,
            'updated_by': station.updated_by,
            'created_at': station.created_at,
            'updated_at': station.updated_at,
            'slots': get_stations_batteries_station_id_alias(db=db, station_id=id),
        }
        return {
            'status': True,
            'message': 'Success',
            'data': data
        }

def retrieve_stations_by_query(db: Session, query: str=None):
    data = search_stations(db=db, query=query)
    return paginate(data)

def retrieve_stations_slots(db: Session, station_id: int=0):
    data = get_stations_batteries_station_id(db=db, station_id=station_id)
    return paginate(data)

def retrieve_station_slot_by_number(db: Session, station_id: int=0, slot_number: int=0):
    slot = get_station_battery_by_slot_number(db=db, station_id=station_id, slot_number=slot_number)
    if slot is None:
        return {
            'status': False,
            'message': 'Not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': slot
        }
    
def retrieve_station_slot_by_id(db: Session, id: int=0):
    slot = get_single_station_battery_by_id(db=db, id=id)
    if slot is None:
        return {
            'status': False,
            'message': 'Not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': slot
        }