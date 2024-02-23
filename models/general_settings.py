from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship



class General_Setting(Base):

    __tablename__ = "general_settings"
     
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=True)
    value = Column(String, nullable=True)
    multi_value = Column(Text, nullable=True)


def create_general_setting(db: Session, name: str = None, value: str = None, multi_value: str = None):
    gs = General_Setting(name=name, value=value, multi_value=multi_value)
    db.add(gs)
    db.commit()
    db.refresh(gs)
    return gs

def update_general_settings(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(General_Setting).filter_by(id = id).update(values)
    db.commit()
    return True

def get_single_general_setting_by_id(db: Session, id: int=0):
    return db.query(General_Setting).filter_by(id = id).first()

def get_single_general_setting_by_name(db: Session, name: str=None):
    return db.query(General_Setting).filter_by(name = name).first()

def get_all_general_setting(db: Session):
    return db.query(General_Setting).all()

def count_general_setting(db: Session):
    return db.query(General_Setting).count()