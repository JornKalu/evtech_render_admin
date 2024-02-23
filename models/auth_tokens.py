from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import or_, and_
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime
from sqlalchemy.orm import relationship


class Auth_Token(Base):

    __tablename__ = "auth_tokens"
     
    id = Column(BigInteger, primary_key=True, index=True)
    admin_id = Column(BigInteger, default=0)
    user_id = Column(BigInteger, default=0)
    device_id = Column(BigInteger, default=0)
    token = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    ping = Column(String, nullable=True)
    expired_at = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())



def create_auth_token(db: Session, admin_id: int=0, user_id: int=0, device_id: int=0, token: str=None, status: int=0, expired_at: str=None):
    auth_token = Auth_Token(admin_id=admin_id, user_id=user_id, token=token, device_id=device_id, status=status, ping=get_laravel_datetime(), expired_at=expired_at, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(auth_token)
    db.commit()
    db.refresh(auth_token)
    return auth_token
    
def update_auth_token(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Auth_Token).filter_by(id=id).update(values)
    db.commit()
    return True

def ping_auth_token(db: Session, id: int = 0):
    return update_auth_token(db=db, id=id, values={'ping': get_laravel_datetime()})

def logout_except_device(db: Session, user_id: int = 0, device_id: int = 0):
    values = {
        'status': 0,
        'updated_at': get_laravel_datetime(),
    }
    db.query(Auth_Token).filter(and_(Auth_Token.user_id == user_id, Auth_Token.device_id != device_id)).update(values)
    db.commit()
    return True

def get_auth_token_by_id(db: Session, id: int=0):
    return db.query(Auth_Token).filter(Auth_Token.id == id).first()
    
def get_auth_token_by_token(db: Session, token: str=None):
    return db.query(Auth_Token).filter(Auth_Token.token == token).first()
    
def get_auth_token_by_user_id(db: Session, user_id: int=0):
    return db.query(Auth_Token).filter(Auth_Token.user_id == user_id).all()

def get_auth_token_by_admin_id(db: Session, admin_id: int=0):
    return db.query(Auth_Token).filter(Auth_Token.admin_id == admin_id).all()
    
def get_last_login_auth_token_by_user_id(db: Session, user_id: int=0):
    return db.query(Auth_Token).filter(and_(Auth_Token.user_id == user_id, Auth_Token.status == 1)).order_by(desc(Auth_Token.id)).first()

def get_last_login_auth_token_by_admin_id(db: Session, admin_id: int=0):
    return db.query(Auth_Token).filter(and_(Auth_Token.admin_id == admin_id, Auth_Token.status == 1)).order_by(desc(Auth_Token.id)).first()