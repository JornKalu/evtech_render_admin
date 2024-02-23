from typing import Optional, List
from pydantic import BaseModel


class StationSlotModel(BaseModel):
    id: int
    station_id: int
    battery_id: int
    slot_number: int
    status: int
    created_at: str
    updated_at: Optional[str] = None
    station_name: Optional[str] = None
    station_address: Optional[str] = None
    battery_name: Optional[str] = None
    battery_code: Optional[str] = None
    battery_description: Optional[str] = None
    battery_voltage: Optional[str] = None
    battery_temperature: Optional[str] = None
    battery_charge: Optional[str] = None
    battery_humidity: Optional[str] = None
    battery_electric_current: Optional[str] = None
    battery_status: Optional[int] = None

    class Config:
        orm_mode = True

class CreateStationModel(BaseModel):
    name: str
    description: str
    address: str
    city: str
    state: str
    number_of_slots: int
    image: Optional[str] = None

    class Config:
        orm_mode = True

class StationModel(BaseModel):
    id: int
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    image: Optional[str] = None
    autonomy_charge: Optional[str] = None
    autonomy_charge_time: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    number_of_slots: Optional[int] = 0
    slots: Optional[List[StationSlotModel]] = None
    status: int
    created_by: int
    created_at: str

    class Config:
        orm_mode = True

class CreateStationResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[StationModel] = None

    class Config:
        orm_mode = True

class UpdateStationModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    image: Optional[str] = None
    status: Optional[int] = None

    class Config:
        orm_mode = True

class GeneralStationResponse(BaseModel):
    status: bool
    message: str

    class Config:
        orm_mode = True

class GeneralSlotResponse(BaseModel):
    status: bool
    message: str
    data: Optional[StationSlotModel] = None

    class Config:
        orm_mode = True