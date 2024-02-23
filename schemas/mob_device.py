from typing import Optional
from pydantic import BaseModel

class CreateMobDeviceTypeModel(BaseModel):
    name: str
    description: Optional[str] = None
    number_of_wheels: int
    number_of_batteries: int
    number_required_without_return: Optional[int] = 0

    class Config:
        orm_mode = True

class MobDeviceTypeModel(BaseModel):
    id: int
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    number_of_wheels: Optional[int] = None
    number_of_batteries: Optional[int] = None
    number_required_without_return: Optional[int] = None
    created_by: Optional[int] = None
    created_at: str

    class Config:
        orm_mode = True

class CreateMobDevTypeResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[MobDeviceTypeModel] = None

    class Config:
        orm_mode = True

class UpdateMobDevTypeModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    number_of_wheels: Optional[int] = None
    number_of_batteries: Optional[int] = None
    number_required_without_return: Optional[int] = None

    class Config:
        orm_mode = True

class GeneralMobDevTypeResponse(BaseModel):
    status: bool
    message: str

    class Config:
        orm_mode = True

class CreateMobDeviceModel(BaseModel):
    user_id: int
    name: str
    device_type_id: int
    model: Optional[str] = None
    registration_number: Optional[str] = None
    vin: Optional[str] = None
    # latitude: Optional[str] = None
    # longitude: Optional[str] = None
    conversion_date: Optional[str] = None
    front_image: Optional[str] = None
    left_image: Optional[str] = None
    right_image: Optional[str] = None
    back_image: Optional[str] = None

    class Config:
        orm_mode = True

class MobilityDeviceModel(BaseModel):
    id: int
    user_id: int
    device_type_id: int
    code: Optional[str] = None
    name: Optional[str] = None
    model: Optional[str] = None
    registration_number: Optional[str] = None
    vin: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    charge: Optional[str] = None
    speed: Optional[str] = None
    conversion_date: Optional[str] = None
    front_image: Optional[str] = None
    left_image: Optional[str] = None
    right_image: Optional[str] = None
    back_image: Optional[str] = None
    status: Optional[int] = 0
    created_at: Optional[str] = None
    type_name: Optional[str] = None
    type_code: Optional[str] = None
    type_description: Optional[str] = None
    number_of_wheels: Optional[int] = 0
    number_of_batteries: Optional[int] = 0
    username: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    customer_full_name: Optional[str] = None
    customer_address: Optional[str] = None
    created_by: Optional[str] = None

    class Config:
        orm_mode = True

class CreateMobDeviceResponse(BaseModel):
    status: bool
    message: str
    data: Optional[MobilityDeviceModel] = None

    class Config:
        orm_mode = True

class UpdateMobDeviceModel(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    registration_number: Optional[str] = None
    vin: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    conversion_date: Optional[str] = None
    front_image: Optional[str] = None
    left_image: Optional[str] = None
    right_image: Optional[str] = None
    back_image: Optional[str] = None

    class Config:
        orm_mode = True