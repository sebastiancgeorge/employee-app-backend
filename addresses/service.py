"""Address Service"""

from sqlalchemy.ext.asyncio import AsyncSession
from models import Address
from datetime import datetime

from exceptions import NotFoundException
from employees import service as employee_service
from addresses import repo


async def create(db: AsyncSession, line1: str, city: str, postal_code: str, country: str, employee_id: int) -> Address:
    await employee_service.get_employee_by_id(employee_id, db)
    address = await repo.create(db, line1, city, postal_code, country, employee_id)
    return address


async def get_addresses_by_employee(employee_id: int, db: AsyncSession):
    await employee_service.get_employee_by_id(employee_id, db)
    return await repo.get_addresses_by_employee(employee_id, db)


async def get_address_by_id(address_id: int, db: AsyncSession):
    address = await repo.get_address_by_id(address_id, db)
    if address is None:
        raise NotFoundException(f"Address with id: {address_id} not found")
    return address


async def update_address(address_id: int, line1: str, city: str, postal_code: str, country: str, db: AsyncSession):
    address = await repo.get_address_by_id(address_id, db)
    if address is None:
        raise NotFoundException(f"Address with id {address_id} not found")

    address.line1 = line1.strip()
    address.city = city.strip()
    address.postal_code = postal_code.strip()
    address.country = country.strip()

    result = await repo.update_address(address, db)
    return result


async def soft_delete_address(address_id: int, db: AsyncSession):
    address = await repo.get_address_by_id(address_id, db)
    if address is None:
        raise NotFoundException(f"Address with id:{address_id} not found")
    address.deleted_at = datetime.now()
    await repo.soft_delete_address(address, db)
    return
