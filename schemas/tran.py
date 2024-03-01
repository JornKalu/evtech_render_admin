from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class TransactionModel(BaseModel):
    id: int
    user_id: Optional[int] = None
    wallet_id: Optional[int] = None
    log_id: Optional[int] = None
    station_id: Optional[int] = None
    mobility_device_id: Optional[int] = None
    reference: Optional[str] = None
    external_reference: Optional[str] = None
    external_source: Optional[str] = None
    transaction_type: Optional[int] = None
    amount: Optional[float] = None
    fee: Optional[float] = None
    total_amount: Optional[float] = None
    balance: Optional[float] = None
    is_battery: Optional[int] = None
    status: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    other_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    gender: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    nationality: Optional[str] = None
    bvn: Optional[str] = None
    nin: Optional[str] = None
    drivers_licence_number: Optional[str] = None
    drivers_licence_photo: Optional[str] = None
    passport: Optional[str] = None
    signature: Optional[str] = None
    station_code: Optional[str] = None
    station_name: Optional[str] = None
    station_description: Optional[str] = None
    station_address: Optional[str] = None
    station_city: Optional[str] = None
    station_state: Optional[str] = None
    station_latitude: Optional[str] = None
    station_longitude: Optional[str] = None
    station_number_of_slots: Optional[int] = None
    mobility_device_code: Optional[str] = None
    mobility_device_name: Optional[str] = None
    mobility_device_model: Optional[str] = None
    mobility_device_registration_number: Optional[str] = None
    mobility_device_vin: Optional[str] = None
    mobility_device_latitude: Optional[str] = None
    mobility_device_longitude: Optional[str] = None
    mobility_device_conversion_date: Optional[str] = None

    class Config:
        orm_mode = True

class GeneralTransactionResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[TransactionModel] = None

    class Config:
        orm_mode = True