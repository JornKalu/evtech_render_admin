from typing import Dict
from models.admins import Admin, create_admin, update_admin, delete_admin, get_single_admin_by_id, get_anon_admin_by_id, get_admins, admin_login
from models.auth_tokens import Auth_Token, create_auth_token, update_auth_token, ping_auth_token, logout_except_device, get_auth_token_by_id, get_auth_token_by_token, get_auth_token_by_user_id, get_auth_token_by_admin_id, get_last_login_auth_token_by_user_id, get_last_login_auth_token_by_admin_id
from models.batteries import Battery, create_battery, update_battery, delete_battery, get_single_battery_by_id, get_all_batteries, search_batteries, get_batteries_by_type, get_batteries_by_status, get_batteries_by_user_id, get_batteries_by_user_id_and_status, get_batteries_by_station_id, count_batteries, count_batteries_by_code, check_if_battery_code_exists
from models.battery_images import Battery_Image, create_battery_image, update_battery_image, delete_battery_image, get_single_battery_image_by_id, get_all_battery_images, get_all_battery_images_by_battery_id, count_battery_images
from models.battery_logs import Battery_Log, create_battery_log, update_battery_log, delete_battery_log, get_single_battery_log_by_id, get_all_battery_logs, get_all_battery_logs_by_battery_id, count_battery_logs
from models.battery_types import Battery_Type, create_battery_type, update_battery_type, delete_battery_type, get_all_battery_types, get_single_battery_type_by_id, get_single_battery_type_by_code, count_battery_types, count_battery_type_by_code, check_if_battery_type_code_exist
from models.collections import Collection, create_collections, update_collection, delete_collection, get_single_collection_by_id, get_all_collections
from models.general_settings import General_Setting, create_general_setting, update_general_settings, get_single_general_setting_by_id, get_single_general_setting_by_name, get_all_general_setting, count_general_setting
from models.logs import Log, create_log, update_log, delete_log, get_single_log_by_id, get_logs_by_user_id, get_logs_by_user_id_and_status, get_logs_by_station_id, get_logs_by_station_id_and_status, get_logs_by_mobility_device_id, get_logs_by_mobility_device_id_and_status, get_logs_by_user_device_id, get_logs_by_user_device_id_and_status, get_all_logs, count_logs
from models.mobility_device_types import Mobility_Device_Type, create_mobility_device_type, update_mobility_device_type, delete_mobility_device_type, get_single_mobility_device_type_by_id, get_all_mobility_device_types, count_mobility_device_types
from models.mobility_devices import Mobility_Device, create_mobility_device, update_mobility_device, delete_mobility_device, get_single_mobility_device_by_id, get_single_mobility_devices_by_user_id, get_single_mobility_devices_by_user_id_and_status, get_single_mobility_devices_by_type, get_single_mobility_devices_by_type_id_and_status, get_single_mobility_devices_by_status, get_all_mobility_devices, search_mobility_devices, count_mobility_devices
from models.privileges_roles import Privilege_Role, create_privilege_role, update_privilege_role, delete_privilege_role, get_single_privilege_role_by_id, get_privileges_roles, count_privileges_roles
from models.privileges import create_privilege, update_privilege, delete_privilege, get_single_privilege_by_id, get_privileges, count_privilege
from models.profiles import Profile, create_profile, update_profile, update_profile_by_user_id, delete_profile, get_profile_by_user_id
from models.request_logs import Request_Log, create_request_log, update_request_log, get_single_request_log_by_id, get_all_request_logs, count_request_logs
from models.roles import Role, create_role, update_role, delete_role, get_single_role_by_id, get_roles, count_role
from models.settings import Setting, create_setting, update_setting, delete_setting, get_single_setting_by_id, get_single_setting_by_user_id, get_settings, count_settings
from models.stations_batteries import Station_Battery, create_station_battery, update_station_battery, delete_station_battery, get_single_station_battery_by_id, get_stations_batteries, get_stations_batteries_station_id, get_stations_batteries_station_id_alias, get_station_battery_by_slot_number, count_stations_batteries
from models.stations import Station, create_station, update_station, delete_station, get_single_station_by_id, get_all_stations, search_stations, count_stations
from models.transactions import Transaction, create_transaction, create_deposit_transaction, create_collection_transaction, update_transaction, delete_transaction, get_single_transaction_by_id, get_single_transaction_by_reference, get_single_transaction_by_external_reference, get_transactions_by_user_id, get_transactions_by_user_id_and_status, get_transactions_by_wallet_id, get_transactions_by_wallet_id_and_status, get_deposits_transactions, get_deposits_transactions_by_user_id, get_collections_transactions, get_collections_transactions_by_user_id, get_transactions_by_log_id, get_all_transactions, get_transactions_by_station_id, get_transactions_by_mobility_device_id, search_transactions, get_all_transactions_between_dates, get_transactions_filtered, count_transactions
from models.user_devices import User_Device, create_user_device, update_user_device, update_user_active_device, delete_user_device, get_single_user_device_by_id, get_single_user_device_by_user_id, get_single_user_device_by_user_id_and_status, get_user_active_device, get_all_user_devices, get_user_device_by_imei_and_address, get_user_device_by_fbt
from models.users import User, create_user, update_user, delete_user, get_single_user_by_id, get_single_user_by_username, get_single_user_by_phone_number, get_single_user_by_email, get_users, search_user, user_login
from models.wallets import Wallet, create_wallet, update_wallet, delete_wallet, get_single_wallet_by_id, get_wallets, get_wallet_by_user_id, count_wallets
import string
import random
from sqlalchemy.orm import Session

def id_generator(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def create_user_with_other_rows(db: Session, username: str = None, email: str = None, phone_number: str = None, email_verified_at: str = None, pin: str = None, password: str = None, remember_token: str = None, device_name: str = None, mac_address: str = None, imei: str = None, fbt: str = None):
    user = create_user(db=db, username=username, email=email, phone_number=phone_number, email_verified_at=email_verified_at, pin=pin, password=password, remember_token=remember_token, status=1)
    create_profile(db=db, user_id=user.id)
    create_setting(db=db, user_id=user.id)
    create_wallet(db=db, user_id=user.id)
    create_user_device(db=db, user_id=user.id, name=device_name, mac_address=mac_address, imei=imei, fbt=fbt, status=1)
    return user

def manage_user_device(db: Session, user_id: int =0 , device_name: str = None, mac_address: str = None, imei: str = None, fbt: str = None):
    user_device = get_user_device_by_fbt(db=db, user_id=user_id, fbt=fbt)
    if user_device is not None:
        return user_device
    else:
        return create_user_device(db=db, user_id=user_id, name=device_name, mac_address=mac_address, imei=imei, fbt=fbt, status=1)

def registration_unique_field_check(db: Session, phone_number: str=None, username: str=None, email: str=None):
    phone_number_check = get_single_user_by_phone_number(db=db, phone_number=phone_number)
    username_check = get_single_user_by_username(db=db, username=username)
    email_check = get_single_user_by_email(db=db, email=email)
    if phone_number_check is not None:
        return {
            'status': False,
            'message': 'Phone number already exist',
        }
    elif username_check is not None:
        return {
            'status': False,
            'message': 'Username already exist',
        }
    elif email_check is not None:
        return {
            'status': False,
            'message': 'Email already exist'
        }
    else:
        return {
            'status': True,
            'message': 'Validation successful'
        }
    
def admin_registration_unique_field_check(db: Session, username: str=None, email: str=None):
    username_check = get_single_user_by_username(db=db, username=username)
    email_check = get_single_user_by_email(db=db, email=email)
    if username_check is not None:
        return {
            'status': False,
            'message': 'Username already exist',
        }
    elif email_check is not None:
        return {
            'status': False,
            'message': 'Email already exist'
        }
    else:
        return {
            'status': True,
            'message': 'Validation successful'
        }