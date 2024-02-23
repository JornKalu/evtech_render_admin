from typing import Optional
from pydantic import BaseModel, EmailStr, constr

class LoginModel(BaseModel):
    phone_number: str
    password: str
    device_name: Optional[str] = None
    imei: Optional[str] = None
    mac_address: Optional[str] = None
    fbt: Optional[str] = None

    class Config:
        orm_mode = True
        
class RegisterModel(BaseModel):
    phone_number: str
    email: EmailStr
    username: str
    password: str
    device_name: Optional[str] = None
    imei: Optional[str] = None
    mac_address: Optional[str] = None
    fbt: Optional[str] = None

    class Config:
        orm_mode = True

class AdminLoginModel(BaseModel):
    field: str
    password: str

    class Config:
        orm_mode = True

class AdminRegisterModel(BaseModel):
    role_id: int
    username: str
    email: str
    phone_number: str
    password: str

    class Config:
        orm_mode = True

class RoleModel(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    functions: Optional[str] = None
    status: int

    class Config:
        orm_mode = True

class AdminAuthModel(BaseModel):
    access_token: Optional[str] = None
    id: int
    username: str
    phone_number: str
    email: str
    first_name: Optional[str] = None
    other_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    gender: Optional[str] = None
    avatar: Optional[str] = None
    role: RoleModel

    class Config:
        orm_mode = True
        
class AdminModel(BaseModel):
    id: int
    username: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    role_id: Optional[int] = None
    first_name: Optional[str] = None
    other_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    gender: Optional[str] = None
    avatar: Optional[str] = None
    role_name: Optional[str] = None
    role_description: Optional[str] = None
    role: Optional[RoleModel] = None
    created_at: Optional[str] = None

    class Config:
        orm_mode = True

class AdminAuthResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[AdminAuthModel]

    class Config:
        orm_mode = True
        
class AdminAuthRegisterResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[AdminModel] = None

    class Config:
        orm_mode = True

class AdminAuthUpdateResponseModel(BaseModel):
    status: bool
    message: str

    class Config:
        orm_mode = True

class AdminUpdateDetailsModel(BaseModel):
    role_id: Optional[int]
    first_name: Optional[str]
    other_name: Optional[str]
    last_name: Optional[str]
    address: Optional[str]
    gender: Optional[str]
    avatar: Optional[str]
    status: Optional[int]

    class Config:
        orm_mode = True
        
class AdminDetailsModel(BaseModel):
    id: int
    username: str
    phone_number: str
    email: str
    first_name: str
    other_name: str
    last_name: str
    address: str
    gender: str
    avatar: str
    role: RoleModel

    class Config:
        orm_mode = True

class AdminUpdatePassword(BaseModel):
    password: str
    old_password: str

    class Config:
        orm_mode = True

class UserProfileModel(BaseModel):
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
    nok_first_name: Optional[str] = None
    nok_other_name: Optional[str] = None
    nok_last_name: Optional[str] = None
    nok_phone_number: Optional[str] = None
    nok_email: Optional[str] = None
    nok_address: Optional[str] = None
    nok_city: Optional[str] = None
    nok_state: Optional[str] = None
    nok_postal_code: Optional[str] = None
    id_verification_type: Optional[int] = 0
    id_status: Optional[int] = 0
    status: Optional[int] = 0

    class Config:
        orm_mode = True

class UserSettingModel(BaseModel):
    email_notification: Optional[int] = 0
    sms_notification: Optional[int] = 0

    class Config:
        orm_mode = True

class UserWalletModel(BaseModel):
    account_name: Optional[str] = None
    account_number: Optional[str] = None
    balance: Optional[float] = 0
    status: Optional[int] = 0

    class Config:
        orm_mode = True

class UserAuthModel(BaseModel):
    access_token: str
    id: int
    username: str
    phone_number: str
    email: str
    profile: Optional[UserProfileModel] = None
    setting: Optional[UserSettingModel] = None
    wallet: Optional[UserWalletModel] = None
    pin_available: Optional[bool] = None

    class Config:
        orm_mode = True
        
class UserModel(BaseModel):
    id: int
    username: str
    phone_number: str
    email: str
    profile: Optional[UserProfileModel] = None
    setting: Optional[UserSettingModel] = None
    wallet: Optional[UserWalletModel] = None
    pin_available: Optional[bool] = None

    class Config:
        orm_mode = True

class UserAuthResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[UserAuthModel] = None

    class Config:
        orm_mode = True
        
class UserResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[UserModel] = None

    class Config:
        orm_mode = True
        
class UserMainResponseModel(BaseModel):
    status: bool
    message: str

    class Config:
        orm_mode = True

class UpdateUserPinModel(BaseModel):
    pin: constr(min_length=4, max_length=4)

    class Config:
        orm_mode = True
        
class UpdateUserPasswordModel(BaseModel):
    password: str
    old_password: str

    class Config:
        orm_mode = True

class CreateRoleModel(BaseModel):
    name: str
    description: Optional[str] = None
    functions: str

    class Config:
        orm_mode = True

class UpdateRoleModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    functions: Optional[str] = None

    class Config:
        orm_mode = True

class CreateRoleResponseModel(BaseModel):
    status: bool
    message: str
    data: Optional[RoleModel] = None

    class Config:
        orm_mode = True

class RoleOtherResponse(BaseModel):
    status: bool
    message: str
    data: Optional[RoleModel] = None

    class Config:
        orm_mode = True