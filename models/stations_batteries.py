from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship
from models.stations import Station


class Station_Battery(Base):

    __tablename__ = "stations_batteries"
     
    id = Column(BigInteger, primary_key=True, index=True)
    station_id = Column(BigInteger, default=0)
    battery_id = Column(BigInteger, default=0)
    slot_number = Column(Integer, default=0)
    station_allow_charge = Column(SmallInteger, default=0)
    battery_docked = Column(SmallInteger, default=0)
    battery_eject = Column(SmallInteger, default=0)
    battery_stop_charge = Column(SmallInteger, default=0)
    battery_ejected_by = Column(BigInteger, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_station_battery(db: Session, station_id: int=0, battery_id: int=0, slot_number: int = 0, station_allow_charge: int=None, battery_docked: int=None, battery_eject: int=None, battery_stop_charge: int=None, battery_ejected_by: int=None, status: int = 0):
    sb = Station_Battery(station_id=station_id, battery_id=battery_id, slot_number=slot_number, station_allow_charge=station_allow_charge, battery_docked=battery_docked, battery_eject=battery_eject, battery_stop_charge=battery_stop_charge, battery_ejected_by=battery_ejected_by, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(sb)
    db.commit()
    db.refresh(sb)
    return sb

def update_station_battery(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Station_Battery).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_station_battery(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Station_Battery).filter_by(id = id).update(values)
    db.commit()
    return True

def get_query(db: Session):
    stations = aliased(Station)
    # sb = aliased(Station_Battery)
    subquery_stations_name = db.query(stations.name).filter(stations.id == Station_Battery.station_id).as_scalar()
    subquery_stations_addr = db.query(stations.address).filter(stations.id == Station_Battery.station_id).as_scalar()
    return db.query(Station_Battery.id, Station_Battery.slot_number, Station_Battery.station_id, Station_Battery.battery_id, Station_Battery.station_allow_charge, Station_Battery.battery_docked, Station_Battery.battery_eject, Station_Battery.battery_stop_charge, Station_Battery.status, Station_Battery.created_at, Station_Battery.updated_at, subquery_stations_name.label('station_name'), subquery_stations_addr.label('station_address'))


def get_single_station_battery_by_id(db: Session, id: int=0):
    main_query = get_query(db=db)
    return main_query.filter_by(id = id).first()

def get_stations_batteries(db: Session):
    main_query = get_query(db=db)
    return main_query.filter(Station_Battery.deleted_at == None)

def get_stations_batteries_station_id(db: Session, station_id: int = 0):
    main_query = get_query(db=db)
    return main_query.filter(and_(Station_Battery.station_id == station_id, Station_Battery.deleted_at == None))

def get_stations_batteries_station_id_alias(db: Session, station_id: int = 0):
    main_query = get_query(db=db)
    return main_query.filter(and_(Station_Battery.station_id == station_id, Station_Battery.deleted_at == None)).all()

def get_station_battery_by_slot_number(db: Session, station_id: int = 0, slot_number: int = 0):
    main_query = get_query(db=db)
    return main_query.filter(and_(Station_Battery.station_id == station_id, Station_Battery.slot_number == slot_number, Station_Battery.deleted_at == None)).first()

def count_stations_batteries(db: Session):
    return db.query(Station_Battery).count()