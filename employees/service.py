"""Employee Service"""

from sqlalchemy.ext.asyncio import AsyncSession
from models import Employee
from fastapi import HTTPException, status
from datetime import datetime

from exceptions import NotFoundException, BadRequestException
from addresses.service import create as create_address
from auth.utils import hash_password
from employees import repo

async def create(db:AsyncSession, name: str, email: str, password: str, age: int | None = None, address = None)->Employee:
    employee_dict = await repo.create(db, name, email, hash_password(password), age)
    if address is not None:
        await create_address(db, address.line1, address.city, address.postal_code, address.country, employee_dict["id"])
    return employee_dict

async def get_all_employees(db: AsyncSession ):
    return await repo.get_all_employees(db)

async def get_employee_by_name(employee_name: str,db: AsyncSession):
    employee = await repo.get_employee_by_name(employee_name,db)
    if employee is None:
        raise NotFoundException("Employees not found")
    return employee

async def get_employee_by_id(employee_id: int,db: AsyncSession):
    employee = await repo.get_employee_by_id(employee_id,db)
    if employee is None:
        raise NotFoundException(f"Employee with id: {employee_id} not found")
    return employee

async def update_employee(employee_id: int, name: str, email: str, age: int | None, db: AsyncSession):
    employee = await repo.get_employee_by_id(employee_id, db)
    if employee is None:
        raise NotFoundException(f"Employee with id {employee_id} not found")
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException("name must be a non-empty string")
    if not isinstance(email, str) or not email.strip():
        raise BadRequestException("email must be a non-empty string")

    employee.name = name.strip()
    employee.email = email.strip()
    
    result = await repo.update_employee(employee, email, db)
    return result

async def soft_delete_employee(employee_id: int, db: AsyncSession):
    employee = await repo.get_employee_by_id(employee_id,db)
    if employee is None:
        raise NotFoundException(f"Employee with id:{employee_id} not found")
    employee.deleted_at = datetime.now()
    await repo.soft_delete_employee(employee, db)
    return