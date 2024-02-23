from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship



class Battery_Image(Base):

    __tablename__ = "battery_images"
     
    id = Column(BigInteger, primary_key=True, index=True)
    battery_id = Column(BigInteger, default=0)
    name = Column(String, nullable=True)
    value = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_battery_image(db: Session, battery_id: int=0, name: str=None, value: str=None, status: int=0):
    battery_image = Battery_Image(battery_id=battery_id, name=name, value=value, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(battery_image)
    db.commit()
    db.refresh(battery_image)
    return battery_image

def update_battery_image(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Battery_Image).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_battery_image(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Battery_Image).filter_by(id = id).update(values)
    db.commit()
    return True

def get_single_battery_image_by_id(db: Session, id: int=0):
    return db.query(Battery_Image).filter_by(id = id).first()

def get_all_battery_images(db: Session):
    return db.query(Battery_Image).filter(Battery_Image.deleted_at == None).all()

def get_all_battery_images_by_battery_id(db: Session, battery_id: int=0):
    return db.query(Battery_Image).filter(and_(Battery_Image.battery_id == battery_id, Battery_Image.deleted_at == None)).all()

def count_battery_images(db: Session):
    return db.query(Battery_Image).count()