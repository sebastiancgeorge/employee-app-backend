"""Employee Repo"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from models import Employee
from exceptions import ConflictException

async def create(db:AsyncSession, name: str, email: str, password_hash : str, age: int | None = None)->Employee:
    employee = Employee(name=name, email=email, password_hash=password_hash, age=age)
    db.add(employee)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"Email '{email}' is already in use")
    await db.refresh(employee)
    return employee.to_api_dict()

async def get_all_employees(db: AsyncSession ):
    stmt = select(Employee).where(Employee.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result

async def get_employee_by_id(employee_id: int,db: AsyncSession):
    stmt = select(Employee).where(Employee.id == employee_id, Employee.deleted_at.is_(None))
    result = await db.scalars(stmt)
    employee = result.first()
    return employee

async def get_employee_by_name(employee_name: str,db: AsyncSession):
    stmt = select(Employee).where(Employee.name == employee_name, Employee.deleted_at.is_(None))
    result = await db.scalars(stmt)
    employee = result.first()
    return employee

async def get_by_email(db : AsyncSession, email: str) -> Employee | None:
    stmt = select(Employee).where(Employee.email == email, Employee.deleted_at.is_(None))
    employee = await db.scalars(stmt)
    return employee.first()

async def update_employee(employee: Employee, email: str, db: AsyncSession):
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"Email '{email}' is already in use")
    await db.refresh(employee)
    return employee

async def soft_delete_employee(employee : Employee, db: AsyncSession):
    await db.commit()
    return