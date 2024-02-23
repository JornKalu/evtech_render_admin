from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship
from models.profiles import Profile
from models.settings import Setting
from models.wallets import Wallet


class User(Base):

    __tablename__ = "users"
     
    id = Column(BigInteger, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=True)
    phone_number = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=True)
    email_verified_at = Column(TIMESTAMP(timezone=True), nullable=True)
    pin = Column(String, nullable=True)
    password = Column(String, nullable=True)
    remember_token = Column(String, nullable=True)
    status = Column(SmallInteger, default=0)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_user(db: Session, username: str = None, email: str = None, phone_number: str = None, email_verified_at: str = None, pin: str = None, password: str = None,  remember_token: str = None, status: int = 0):
    user = User(username=username, email=email, phone_number=phone_number, email_verified_at=email_verified_at, pin=pin, password=password,  remember_token=remember_token, status=status, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(User).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_user(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(User).filter_by(id = id).update(values)
    db.commit()
    return True

def get_query(db: Session):
    return db.query(User.id, User.email, User.username, User.phone_number, User.status, User.created_at, User.updated_at, Profile.first_name, Profile.other_name, Profile.last_name, Profile.address, Profile.gender, Profile.city, Profile.state, Profile.postal_code, Profile.nationality, Profile.bvn, Profile.nin, Profile.drivers_licence_number, Profile.drivers_licence_photo, Profile.passport, Profile.signature, Setting.email_notification, Setting.sms_notification, Wallet.account_name, Wallet.account_number, Wallet.balance).join(Profile, Profile.user_id == User.id).join(Setting, Setting.user_id == User.id).join(Wallet, Wallet.user_id == User.id).filter(User.deleted_at == None)

def get_single_user_by_id(db: Session, id: int=0):
    return get_query(db=db).filter(User.id == id).first()

def get_single_user_by_username(db: Session, username: str=None):
    return get_query(db=db).filter(User.username == username).first()

def get_single_user_by_phone_number(db: Session, phone_number: str=None):
    return get_query(db=db).filter(User.phone_number == phone_number).first()

def get_single_user_by_email(db: Session, email: str=None):
    return get_query(db=db).filter(User.email == email).first()

def get_users(db: Session):
    return get_query(db=db).order_by(desc(User.id))

def search_user(db: Session, query: str = None):
    main_query = get_query(db=db)
    return main_query.filter(and_(or_(User.username.like('%' + str(query) + '%'), User.email.like('%' + str(query) + '%'), User.phone_number.like('%' + str(query) + '%'), Profile.first_name.like('%' + str(query) + '%'), Profile.other_name.like('%' + str(query) + '%'), Profile.last_name.like('%' + str(query) + '%')), User.deleted_at == None)).order_by(desc(User.id))

def user_login(db: Session, field: str=None):
    return db.query(User).filter(and_(or_(User.email == field, User.username == field, User.phone_number == field), User.deleted_at == None)).first()