"""Address Repo"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from models import Address
from exceptions import ConflictException

async def create(db: AsyncSession, line1: str, city: str, postal_code: str, country: str, employee_id: int) -> Address:
    address = Address(line1=line1, city=city, postal_code=postal_code, country=country, employee_id=employee_id)
    db.add(address)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException("Address could not be created due to database conflict")
    await db.refresh(address)
    return address.to_api_dict()

async def get_all_addresses(db: AsyncSession):
    stmt = select(Address).where(Address.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result

async def get_address_by_id(address_id: int, db: AsyncSession):
    stmt = select(Address).where(Address.id == address_id, Address.deleted_at.is_(None))
    result = await db.scalars(stmt)
    address = result.first()
    return address

async def get_addresses_by_employee(employee_id: int, db: AsyncSession):
    stmt = select(Address).where(Address.employee_id == employee_id, Address.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result

async def update_address(address: Address, db: AsyncSession):
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException("Address update failed due to database conflict")
    await db.refresh(address)
    return address

async def soft_delete_address(address: Address, db: AsyncSession):
    await db.commit()
    return