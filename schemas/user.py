from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class UserModel(BaseModel):
    id: int
    username: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    status: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[str] = None
    first_name: Optional[str] = None
    other_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    gender: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    nationality: Optional[str] = None
    bvn: Optional[str] = None
    nin: Optional[str] = None
    drivers_licence_number: Optional[str] = None
    drivers_licence_photo: Optional[str] = None
    passport: Optional[str] = None
    email_notification: Optional[int] = None
    sms_notification: Optional[int] = None
    account_name: Optional[str] = None
    account_number: Optional[str] = None
    balance: Optional[float] = None

    class Config:
        orm_mode = True

class UserResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[UserModel] = None

    class Config:
        orm_mode = True