"""Employee Router"""

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from fastapi import Depends, status, Body, APIRouter
from employees import service
from employees.schemas import EmployeeCreate, EmployeeResponse, EmployeeResponseId
from auth.dependencies import get_current_user
from auth.schemas import TokenPayload

router = APIRouter(prefix="/employee",tags=["Employees"])

@router.post("",status_code=status.HTTP_201_CREATED,response_model= EmployeeResponse)
async def create_employee(body : EmployeeCreate, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    employee = await service.create(db, body.name, body.email, body.password, body.age, body.address)
    return employee

@router.get("",response_model= list[EmployeeResponse])
async def get_all_employees(db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    results = await service.get_all_employees(db)
    return [r for r in results.all()]

@router.get("/search/{employee_name}")
async def get_employee_by_name(employee_name: str, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    result= await service.get_employee_by_name(employee_name, db)
    return result


@router.get("/{employee_id}", response_model = EmployeeResponseId)
async def get_employee_by_id(employee_id: int, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    result= await service.get_employee_by_id(employee_id, db)
    return result

@router.put("/{employee_id}")
async def update_employee(employee_id: int, body: EmployeeCreate, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    name = body.name
    email = body.email
    age = body.age
    result = await service.update_employee(employee_id, name, email, age, db)
    return result

@router.delete("/{employee_id}", status_code= status.HTTP_204_NO_CONTENT)
async def soft_delete_employee(employee_id: int,db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    await service.soft_delete_employee(employee_id, db)
    return {"message": "Employee soft deleted"}