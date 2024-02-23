from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship



class Privilege(Base):

    __tablename__ = "privileges"
     
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_privilege(db: Session, name: str=None, description: str=None, status: int = 0):
    privilege = Privilege(name=name, description=description, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(privilege)
    db.commit()
    db.refresh(privilege)
    return privilege

def update_privilege(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Privilege).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_privilege(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Privilege).filter_by(id = id).update(values)
    db.commit()
    return True

def get_single_privilege_by_id(db: Session, id: int=0):
    return db.query(Privilege).filter_by(id = id).first()

def get_privileges(db: Session):
    return db.query(Privilege).filter(Privilege.deleted_at == None).all()

def count_privilege(db: Session):
    return db.query(Privilege).count()