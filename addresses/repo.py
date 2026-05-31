
"""Address Repo"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from models import Address
from exceptions import ConflictException

async def create(db:AsyncSession, name: str, email: str, password_hash : str)->Address:
    address = Address(name=name, email=email, password_hash=password_hash )
    db.add(address)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"Email '{email}' is already in use")
    await db.refresh(address)
    return address.to_api_dict()

async def get_all_addresss(db: AsyncSession ):
    stmt = select(Address).where(Address.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result

async def get_address_by_id(address_id: int,db: AsyncSession):
    stmt = select(Address).where(Address.id == address_id, Address.deleted_at.is_(None))
    result = await db.scalars(stmt)
    address = result.first()
    return address

async def get_address_by_name(address_name: str,db: AsyncSession):
    stmt = select(Address).where(Address.name == address_name, Address.deleted_at.is_(None))
    result = await db.scalars(stmt)
    address = result.first()
    return address

async def get_by_email(db : AsyncSession, email: str) -> Address | None:
    stmt = select(Address).where(Address.email == email, Address.deleted_at.is_(None))
    address = await db.scalars(stmt)
    return address.first()

async def update_address(address: Address, email: str, db: AsyncSession):
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"Email '{email}' is already in use")
    await db.refresh(address)
    return address

async def soft_delete_address(address : Address, db: AsyncSession):
    await db.refresh(address)
    return