"""Department Router"""

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from fastapi import Depends, status, Body, APIRouter
from departments import service
from departments.schemas import DepartmentCreate, DepartmentUpdate, DepartmentResponse, DepartmentResponseId
from auth.dependencies import get_current_user
from auth.schemas import TokenPayload

router = APIRouter(prefix="/department", tags=["Departments"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=DepartmentResponse)
async def create_department(body: DepartmentCreate, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    department = await service.create(db, body.name, body.employee_ids)
    return department

@router.get("", response_model=list[DepartmentResponse])
async def get_all_departments(db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    results = await service.get_all_departments(db)
    return [r for r in results.all()]

@router.get("/search/{department_name}", response_model=DepartmentResponse)
async def get_department_by_name(department_name: str, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    result = await service.get_department_by_name(department_name, db)
    return result

@router.get("/{department_id}", response_model=DepartmentResponseId)
async def get_department_by_id(department_id: int, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    result = await service.get_department_by_id(department_id, db)
    return result

@router.put("/{department_id}", response_model=DepartmentResponse)
async def update_department(department_id: int, body: DepartmentUpdate, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    result = await service.update_department(department_id, body.name, body.employee_ids, db)
    return result

@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_department(department_id: int, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    await service.soft_delete_department(department_id, db)
    return {"message": "Department soft deleted"}