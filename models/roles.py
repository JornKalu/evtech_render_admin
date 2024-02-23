from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship



class Role(Base):

    __tablename__ = "roles"
     
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    functions = Column(Text, nullable=True)
    status = Column(SmallInteger, default=0)
    created_by = Column(BigInteger, default=0)
    updated_by = Column(BigInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_role(db: Session, name: str=None, description: str=None, functions: str=None, status: int = 0, created_by: int = 0, updated_by: int = 0):
    role = Role(name=name, description=description, functions=functions, status=status, created_by=created_by, updated_by=updated_by, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def update_role(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Role).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_role(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Role).filter_by(id = id).update(values)
    db.commit()
    return True

def get_single_role_by_id(db: Session, id: int=0):
    return db.query(Role).filter_by(id = id).first()

def get_roles(db: Session):
    return db.query(Role).filter(Role.deleted_at == None).order_by(Role.id)

def count_role(db: Session):
    return db.query(Role).count()