"""Department Service"""

from sqlalchemy.ext.asyncio import AsyncSession
from models import Department
from datetime import datetime

from exceptions import NotFoundException, BadRequestException
from departments import repo

async def create(db: AsyncSession, name: str, employee_ids: list[int] | None = None) -> Department:
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException("name must be a non-empty string")
    department = await repo.create(db, name.strip(), employee_ids)
    return department

async def get_all_departments(db: AsyncSession):
    return await repo.get_all_departments(db)

async def get_department_by_name(department_name: str, db: AsyncSession):
    department = await repo.get_department_by_name(department_name, db)
    if department is None:
        raise NotFoundException(f"Department '{department_name}' not found")
    return department

async def get_department_by_id(department_id: int, db: AsyncSession):
    department = await repo.get_department_by_id(department_id, db)
    if department is None:
        raise NotFoundException(f"Department with id: {department_id} not found")
    return department

async def update_department(department_id: int, name: str, employee_ids: list[int] | None, db: AsyncSession):
    department = await repo.get_department_by_id(department_id, db)
    if department is None:
        raise NotFoundException(f"Department with id {department_id} not found")
    if not isinstance(name, str) or not name.strip():
        raise BadRequestException("name must be a non-empty string")

    result = await repo.update_department(department, name.strip(), employee_ids, db)
    return result

async def soft_delete_department(department_id: int, db: AsyncSession):
    department = await repo.get_department_by_id(department_id, db)
    if department is None:
        raise NotFoundException(f"Department with id:{department_id} not found")
    department.deleted_at = datetime.now()
    await repo.soft_delete_department(department, db)
    return