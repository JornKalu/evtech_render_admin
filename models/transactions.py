from typing import Dict
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, DECIMAL, Float, TIMESTAMP, SmallInteger, Text, Date, desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import and_, or_, cast
from sqlalchemy.sql.schema import ForeignKey
from database.db import Base, get_laravel_datetime, get_added_laravel_datetime, compare_laravel_datetime_with_today
from sqlalchemy.orm import relationship
from settings.constants import TRANSACTION_TYPES
from models.profiles import Profile
from models.users import User
from models.stations import Station
from models.mobility_devices import Mobility_Device

class Transaction(Base):

    __tablename__ = "transactions"
     
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, default=0)
    wallet_id = Column(BigInteger, default=0)
    log_id = Column(BigInteger, default=0)
    station_id = Column(BigInteger, default=0)
    mobility_device_id = Column(BigInteger, default=0)
    reference = Column(String, nullable=True)
    external_reference = Column(String, nullable=True)
    external_source = Column(String, nullable=True)
    transaction_type = Column(Integer, default=0)
    amount = Column(Float, default=0)
    fee = Column(Float, default=0)
    total_amount = Column(Float, default=0)
    balance = Column(Float, default=0)
    battery_quantity = Column(Integer, default=0)
    battery_quantity_taken = Column(Integer, default=0)
    battery_taken_status = Column(SmallInteger, default=0)
    is_battery = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=0)
    misc_data = Column(String, nullable=True)
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


def create_transaction(db: Session, user_id: int = 0, wallet_id: int = 0, log_id: int = 0, station_id: int = 0, mobility_device_id: int = 0, reference: str = None, external_reference: str = None, external_source: str = None, transaction_type: int = 0, amount: float = 0, fee: float = 0, total_amount: float = 0, balance: float = 0, battery_quantity: int = 0, battery_quantity_taken: int = 0, battery_taken_status: int = 0, is_battery: int = 0, status: int = 0, misc_data: str = None):
    trans = Transaction(user_id=user_id, wallet_id=wallet_id, log_id=log_id, station_id=station_id, mobility_device_id=mobility_device_id, reference=reference, external_reference=external_reference, external_source=external_source, transaction_type=transaction_type, amount=amount, fee=fee, total_amount=total_amount, balance=balance, battery_quantity=battery_quantity, battery_quantity_taken=battery_quantity_taken, battery_taken_status=battery_taken_status, is_battery=is_battery, status=status, misc_data=misc_data, created_at=get_laravel_datetime(), updated_at=get_laravel_datetime())
    db.add(trans)
    db.commit()
    db.refresh(trans)
    return trans

def create_deposit_transaction(db: Session, user_id: int = 0, wallet_id: int = 0, log_id: int = 0, station_id: int = 0, mobility_device_id: int = 0, reference: str = None, external_reference: str = None, external_source: str = None, amount: float = 0, fee: float = 0, total_amount: float = 0, balance: float = 0, battery_quantity: int = 0, battery_quantity_taken: int = 0, battery_taken_status: int = 0, is_battery: int = 0, status: int = 0, misc_data: str = None):
    return create_transaction(db=db, user_id=user_id, wallet_id=wallet_id, log_id=log_id, station_id=station_id, mobility_device_id=mobility_device_id, reference=reference, external_reference=external_reference, external_source=external_source, transaction_type=TRANSACTION_TYPES['DEPOSIT'], amount=amount, fee=fee, total_amount=total_amount, balance=balance, battery_quantity=battery_quantity, battery_quantity_taken=battery_quantity_taken, battery_taken_status=battery_taken_status, is_battery=is_battery, status=status, misc_data=misc_data)

def create_collection_transaction(db: Session, user_id: int = 0, wallet_id: int = 0, log_id: int = 0, station_id: int = 0, mobility_device_id: int = 0, reference: str = None, external_reference: str = None, external_source: str = None, amount: float = 0, fee: float = 0, total_amount: float = 0, balance: float = 0, battery_quantity: int = 0, battery_quantity_taken: int = 0, battery_taken_status: int = 0, is_battery: int = 0, status: int = 0, misc_data: str = None):
    return create_transaction(db=db, user_id=user_id, wallet_id=wallet_id, log_id=log_id, station_id=station_id, mobility_device_id=mobility_device_id, reference=reference, external_reference=external_reference, external_source=external_source, transaction_type=TRANSACTION_TYPES['COLLECTION'], amount=amount, fee=fee, total_amount=total_amount, balance=balance, battery_quantity=battery_quantity, battery_quantity_taken=battery_quantity_taken, battery_taken_status=battery_taken_status, is_battery=is_battery, status=status, misc_data=misc_data)

def update_transaction(db: Session, id: int=0, values: Dict={}):
    values['updated_at'] = get_laravel_datetime()
    db.query(Transaction).filter_by(id = id).update(values)
    db.commit()
    return True

def delete_transaction(db: Session, id: int=0):
    values = {
        'updated_at': get_laravel_datetime(),
        'deleted_at': get_laravel_datetime(),
    }
    db.query(Transaction).filter_by(id = id).update(values)
    db.commit()
    return True

def get_query(db: Session):
    return db.query(Transaction.id, Transaction.user_id, Transaction.wallet_id, Transaction.log_id, Transaction.station_id, Transaction.mobility_device_id, Transaction.reference, Transaction.external_reference, Transaction.external_source, Transaction.transaction_type, Transaction.amount, Transaction.fee, Transaction.total_amount, Transaction.balance, Transaction.battery_quantity, Transaction.battery_quantity_taken, Transaction.battery_taken_status, Transaction.is_battery, Transaction.status, Transaction.misc_data, Transaction.created_at, Transaction.updated_at, Transaction.deleted_at, User.username, User.email, User.phone_number, Profile.first_name, Profile.other_name, Profile.last_name, Profile.address, Profile.gender, Profile.city, Profile.state, Profile.postal_code, Profile.nationality, Profile.bvn, Profile.nin, Profile.drivers_licence_number, Profile.drivers_licence_photo, Profile.passport, Profile.signature, Station.code.label('station_code'), Station.name.label('station_name'), Station.description.label('station_description'), Station.address.label('station_address'), Station.city.label('station_city'), Station.state.label('station_state'), Station.latitude.label('station_latitude'), Station.longitude.label('station_longitude'), Station.number_of_slots.label('station_number_of_slots'), Mobility_Device.code.label('mobility_device_code'), Mobility_Device.name.label('mobility_device_name'), Mobility_Device.model.label('mobility_device_model'), Mobility_Device.registration_number.label('mobility_device_registration_number'), Mobility_Device.vin.label('mobility_device_vin'), Mobility_Device.latitude.label('mobility_device_latitude'), Mobility_Device.longitude.label('mobility_device_longitude'), Mobility_Device.conversion_date.label('mobility_device_conversion_date')).join(User, User.id == Transaction.user_id, isouter=True).join(Profile, Profile.user_id == Transaction.user_id, isouter=True).join(Station, Station.id == Transaction.station_id, isouter=True).join(Mobility_Device, Mobility_Device.id == Transaction.mobility_device_id, isouter=True)

def get_single_transaction_by_id(db: Session, id: int=0):
    return get_query(db=db).filter(Transaction.id == id).first()

def get_single_transaction_by_reference(db: Session, reference: str=None):
    return get_query(db=db).filter_by(reference = reference).first()

def get_single_transaction_by_external_reference(db: Session, external_reference: str=None):
    return get_query(db=db).filter_by(external_reference = external_reference).first()

def get_transactions_by_user_id(db: Session, user_id: int=0):
    return get_query(db=db).filter(and_(Transaction.user_id == user_id, Transaction.deleted_at == None)).order_by(desc(Transaction.id))

def get_transactions_by_user_id_and_status(db: Session, user_id: int=0, status: int=0):
    return get_query(db=db).filter(and_(Transaction.user_id == user_id, Transaction.status == status, Transaction.deleted_at == None)).order_by(desc(Transaction.id))

def get_transactions_by_wallet_id(db: Session, wallet_id: int=0):
    return get_query(db=db).filter(and_(Transaction.wallet_id == wallet_id, Transaction.deleted_at == None)).order_by(desc(Transaction.id))

def get_transactions_by_wallet_id_and_status(db: Session, wallet_id: int=0, status: int=0):
    return get_query(db=db).filter(and_(Transaction.wallet_id == wallet_id, Transaction.status == status, Transaction.deleted_at == None)).order_by(desc(Transaction.id))

def get_deposits_transactions(db: Session):
    return get_query(db=db).filter(Transaction.transaction_type == TRANSACTION_TYPES['DEPOSIT']).order_by(desc(Transaction.id))

def get_deposits_transactions_by_user_id(db: Session, user_id: int = 0):
    return get_query(db=db).filter(and_(Transaction.transaction_type == TRANSACTION_TYPES['DEPOSIT'], Transaction.user_id == user_id)).order_by(desc(Transaction.id))

def get_collections_transactions(db: Session):
    return get_query(db=db).filter(Transaction.transaction_type == TRANSACTION_TYPES['COLLECTION']).order_by(desc(Transaction.id))

def get_collections_transactions_by_user_id(db: Session, user_id: int = 0):
    return get_query(db=db).filter(and_(Transaction.transaction_type == TRANSACTION_TYPES['COLLECTION'], Transaction.user_id == user_id)).order_by(desc(Transaction.id))

def get_transactions_by_log_id(db: Session, log_id: int=0):
    return get_query(db=db).filter(Transaction.log_id == log_id).order_by(desc(Transaction.id))

def get_all_transactions(db: Session):
    return get_query(db=db).filter(Transaction.deleted_at == None).order_by(desc(Transaction.id))

def get_transactions_by_station_id(db: Session, station_id: int = 0):
    return get_query(db=db).filter(and_(Transaction.station_id == station_id, Transaction.deleted_at == None)).order_by(desc(Transaction.id))

def get_transactions_by_mobility_device_id(db: Session, mobility_device_id: int = 0):
    return get_query(db=db).filter(and_(Transaction.mobility_device_id == mobility_device_id, Transaction.deleted_at == None)).order_by(desc(Transaction.id))

def search_transactions(db: Session, query: str = None):
    return get_query(db=db).filter(and_(or_(Transaction.reference.like('%' + str(query) + '%'), Transaction.external_source.like('%' + str(query) + '%'), User.username.like('%' + str(query) + '%'), User.email.like('%' + str(query) + '%'), User.phone_number.like('%' + str(query) + '%'), Profile.first_name.like('%' + str(query) + '%'), Profile.other_name.like('%' + str(query) + '%'), Profile.last_name.like('%' + str(query) + '%'), Mobility_Device.code.like('%' + str(query) + '%'), Mobility_Device.code.like('%' + str(query) + '%'), Mobility_Device.model.like('%' + str(query) + '%'), Mobility_Device.registration_number.like('%' + str(query) + '%'), Mobility_Device.vin.like('%' + str(query) + '%'), Station.code.like('%' + str(query) + '%'), Station.name.like('%' + str(query) + '%')), Transaction.deleted_at == None)).order_by(desc(Transaction.id))

def get_all_transactions_between_dates(db: Session, from_date: str = None, to_date: str = None):
    return get_query(db=db).filter(and_(or_(cast(Transaction.created_at, Date).between(from_date, to_date)), Transaction.deleted_at == None)).order_by(desc(Transaction.id))

def get_transactions_filtered(db: Session, user_id: int = None, station_id: int = None, mobility_device_id: int = 0, from_date: str = None, to_date: str = None):
    main_query = get_query(db=db)
    if user_id is not None:
        main_query = main_query.filter(Transaction.user_id == user_id)
    if station_id is not None:
        main_query = main_query.filter(Transaction.station_id == station_id)
    if mobility_device_id is not None:
        main_query = main_query.filter(Transaction.mobility_device_id == mobility_device_id)
    if from_date is not None and to_date is not None:
        main_query = main_query.filter(cast(Transaction.created_at, Date).between(from_date, to_date))
    main_query = main_query.filter(Transaction.deleted_at == None).order_by(desc(Transaction.id))
    return main_query

def count_transactions(db: Session):
    return db.query(Transaction).count()