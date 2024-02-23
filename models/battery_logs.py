from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship


class Battery_Log(Base):

    __tablename__ = "battery_logs"
     
    id = Column(BigInteger, primary_key=True, index=True)
    battery_id = Column(BigInteger, default=0)
    instruction_count = Column(Integer, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_battery_log(db: Session, battery_id: int=0, instruction_count: int=0, status: int=0):
    battery_log = Battery_Log(battery_id=battery_id, instruction_count=instruction_count, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(battery_log)
    db.commit()
    db.refresh(battery_log)
    return battery_log

def update_battery_log(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Battery_Log).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_battery_log(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Battery_Log).filter_by(id = id).update(values)
    db.commit()
    return True

def get_single_battery_log_by_id(db: Session, id: int=0):
    return db.query(Battery_Log).filter_by(id = id).first()

def get_all_battery_logs(db: Session):
    return db.query(Battery_Log).filter(Battery_Log.deleted_at == None).all()

def get_all_battery_logs_by_battery_id(db: Session, battery_id: int=0):
    return db.query(Battery_Log).filter(and_(Battery_Log.battery_id == battery_id, Battery_Log.deleted_at == None)).all()

def count_battery_logs(db: Session):
    return db.query(Battery_Log).count()