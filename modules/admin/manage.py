from typing import Dict
from database.model import get_single_admin_by_id, get_anon_admin_by_id, get_just_admins, get_admins, get_roles, get_single_role_by_id, create_role, update_role, delete_role
from modules.utils.tools import process_schema_dictionary
from sqlalchemy.orm import Session
from fastapi_pagination.ext.sqlalchemy import paginate

def retrieve_admins(db: Session):
    data = get_just_admins(db=db)
    # return paginate(data)
    return str(data)

def retrieve_single_admin(db: Session, admin_id: int=0):
    admin = get_single_admin_by_id(db=db, id=admin_id)
    if admin is None:
        return {
            'status': False,
            'message': 'Admin not found',
            'data': None
        }
    else:
        data = {
            'id': admin.id,
            'username': admin.username,
            'phone_number': admin.phone_number,
            'email': admin.email,
            'first_name': admin.first_name,
            'other_name': admin.other_name,
            'last_name': admin.last_name,
            'address': admin.address,
            'gender': admin.gender,
            'avatar': admin.avatar,
            'role': get_single_role_by_id(db=db, id=admin.role_id)
        }
        return {
            'status': True,
            'message': 'Success',
            'data': data
        }

def retrieve_roles(db: Session):
    data = get_roles(db=db)
    return paginate(data)

def retrieve_single_role(db: Session, id: int=0):
    role = get_single_role_by_id(db=db, id=id)
    if role is None:
        return {
            'status': False,
            'message': 'Role not found',
            'data': None
        }
    else:
        return {
            'status': True,
            'message': 'Success',
            'data': role
        }

def insert_new_role(db: Session, name: str=None, description: str=None, functions: str=None, created_by: int=0):
    role = create_role(db=db, name=name, description=description, functions=functions, status=1, created_by=created_by)
    return {
        'status': True,
        'message': 'Success',
        'data': role
    }

def update_admin_role(db: Session, role_id: int=0, values: Dict={}, updated_by: int=0):
    values = process_schema_dictionary(info=values)
    values['updated_by'] = updated_by
    update_role(db=db, id=role_id, values=values)
    return {
        'status': True,
        'message': 'Success'
    }

def remove_role(db: Session, role_id: int=0):
    delete_role(db=db, id=role_id)
    return {
        'status': True,
        'message': 'Success'
    }