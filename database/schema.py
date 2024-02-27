from schemas.auth import LoginModel, RegisterModel, AdminLoginModel, AdminRegisterModel, RoleModel, AdminAuthModel, AdminModel, AdminAuthResponseModel, AdminAuthRegisterResponseModel, AdminAuthUpdateResponseModel, AdminUpdateDetailsModel, AdminDetailsModel, AdminUpdatePassword, UserAuthResponseModel, UserResponseModel, UserMainResponseModel, UpdateUserPinModel, UpdateUserPasswordModel, CreateRoleModel, UpdateRoleModel, CreateRoleResponseModel, RoleOtherResponse
from schemas.battery import BatteryTypeModel, CreateBatteryTypeModel, UpdateBatteryTypeModel, CreateBatteryTypeResponseModel, CreateBatteryModel, BatteryModel, CreateBatteryResponseModel, UpdateBatteryModel, GeneralBatteryResponseModel
from schemas.mob_device import CreateMobDeviceTypeModel, MobDeviceTypeModel, CreateMobDevTypeResponseModel, UpdateMobDevTypeModel, GeneralMobDevTypeResponse, CreateMobDeviceModel, MobilityDeviceModel, CreateMobDeviceResponse, UpdateMobDeviceModel
from schemas.resp import ErrorResponse
from schemas.station import CreateStationModel, StationModel, CreateStationResponseModel, UpdateStationModel, GeneralStationResponse, StationSlotModel, GeneralSlotResponse
from schemas.tran import TransactionModel, GeneralTransactionResponseModel
from schemas.user import UserModel, UserResponseModel