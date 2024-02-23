from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship



class Privilege_Role(Base):

    __tablename__ = "privileges_roles"
     
    id = Column(BigInteger, primary_key=True, index=True)
    role_id = Column(BigInteger, default=0)
    privilege_id = Column(BigInteger, default=0)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_privilege_role(db: Session, role_id: int=0, privilege_id: int=0, status: int = 0):
    pr = Privilege_Role(role_id=role_id, privilege_id=privilege_id, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(pr)
    db.commit()
    db.refresh(pr)
    return pr

def update_privilege_role(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Privilege_Role).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_privilege_role(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Privilege_Role).filter_by(id = id).update(values)
    db.commit()
    return True

def get_single_privilege_role_by_id(db: Session, id: int=0):
    return db.query(Privilege_Role).filter_by(id = id).first()

def get_privileges_roles(db: Session):
    return db.query(Privilege_Role).filter(Privilege_Role.deleted_at == None).all()

def count_privileges_roles(db: Session):
    return db.query(Privilege_Role).count()