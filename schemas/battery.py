from typing import Optional
from pydantic import BaseModel

class BatteryTypeModel(BaseModel):
    id: int
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    voltage: Optional[str] = None
    power: Optional[str] = None
    fee: Optional[float] = 0
    status: Optional[str] = None
    created_at: str

    class Config:
        orm_mode = True

class CreateBatteryTypeModel(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    voltage: Optional[str] = None
    power: Optional[str] = None
    fee: Optional[float] = 0
    collection_due_days: Optional[int] = 0
    collection_due_fees: Optional[float] = 0

    class Config:
        orm_mode = True

class UpdateBatteryTypeModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    voltage: Optional[str] = None
    power: Optional[str] = None
    fee: Optional[float] = None
    status: Optional[int] = None
    collection_due_days: Optional[int] = None
    collection_due_fees: Optional[float] = None

    class Config:
        orm_mode = True

class CreateBatteryTypeResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[BatteryTypeModel] = None

    class Config:
        orm_mode = True

class CreateBatteryModel(BaseModel):
    type_id: int
    # code: str
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True

class BatteryModel(BaseModel):
    id: int
    type_id: int
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    qr_code: Optional[str] = None
    voltage: Optional[str] = None
    temperature: Optional[str] = None
    charge: Optional[str] = None
    humidity: Optional[str] = None
    electric_current: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    temp_status: Optional[int] = 0
    status: Optional[int] = 0
    customer_id: Optional[int] = None
    customer_full_name: Optional[str] = None
    customer_address: Optional[str] = None
    station_name: Optional[str] = None
    station_address: Optional[str] = None
    station_id: Optional[int] = None
    mobility_device_code: Optional[str] = None
    mobility_device_name: Optional[str] = None
    mobility_device_type: Optional[int] = None
    mobility_device_model: Optional[str] = None
    mobility_device_registration_number: Optional[str] = None
    mobility_device_vin: Optional[str] = None
    mobility_device_id: Optional[int] = None
    battery_type_name: Optional[str] = None
    created_at: str

    class Config:
        orm_mode = True

class CreateBatteryResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[BatteryModel] = None

    class Config:
        orm_mode = True

class UpdateBatteryModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None

    class Config:
        orm_mode = True

class GeneralBatteryResponseModel(BaseModel):
    status: bool
    message: str

    class Config:
        orm_mode = True