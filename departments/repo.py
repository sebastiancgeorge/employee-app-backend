"""Department Repo"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models import Department, Employee
from exceptions import ConflictException


async def create(db: AsyncSession, name: str, employee_ids: list[int] | None = None) -> Department:
    department = Department(name=name)
    if employee_ids:
        stmt = select(Employee).where(Employee.id.in_(employee_ids), Employee.deleted_at.is_(None))
        res = await db.scalars(stmt)
        department.employees = list(res.all())

    db.add(department)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"Department name '{name}' is already in use")

    stmt = select(Department).options(selectinload(Department.employees)).where(Department.id == department.id)
    res = await db.scalars(stmt)
    department = res.first()
    return department


async def get_all_departments(db: AsyncSession):
    stmt = select(Department).options(selectinload(Department.employees)).where(Department.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result


async def get_department_by_id(department_id: int, db: AsyncSession):
    stmt = (
        select(Department)
        .options(selectinload(Department.employees))
        .where(Department.id == department_id, Department.deleted_at.is_(None))
    )
    result = await db.scalars(stmt)
    department = result.first()
    return department


async def get_department_by_name(department_name: str, db: AsyncSession):
    stmt = (
        select(Department)
        .options(selectinload(Department.employees))
        .where(Department.name == department_name, Department.deleted_at.is_(None))
    )
    result = await db.scalars(stmt)
    department = result.first()
    return department


async def update_department(department: Department, name: str, employee_ids: list[int] | None, db: AsyncSession):
    department.name = name
    if employee_ids is not None:
        if employee_ids:
            stmt = select(Employee).where(Employee.id.in_(employee_ids), Employee.deleted_at.is_(None))
            res = await db.scalars(stmt)
            department.employees = list(res.all())
        else:
            department.employees = []

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"Department name '{name}' is already in use")

    stmt = select(Department).options(selectinload(Department.employees)).where(Department.id == department.id)
    res = await db.scalars(stmt)
    department = res.first()
    return department


async def soft_delete_department(department: Department, db: AsyncSession):
    await db.commit()
    return
