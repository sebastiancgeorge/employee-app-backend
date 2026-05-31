"""Address Router"""

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from fastapi import Depends, status, Body, APIRouter
from addresses import service
from addresses.schemas import AddressCreate, AddressResponse, AddressResponseId
from auth.dependencies import get_current_user
from auth.schemas import TokenPayload

router = APIRouter(tags=["Addresses"])

@router.post("/employee/{employee_id}/address", status_code=status.HTTP_201_CREATED, response_model=AddressResponse)
async def create_address(employee_id: int, body: AddressCreate, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    address = await service.create(db, body.line1, body.city, body.postal_code, body.country, employee_id)
    return address

@router.get("/employee/{employee_id}/addresses", response_model=list[AddressResponse])
async def get_addresses_by_employee(employee_id: int, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    results = await service.get_addresses_by_employee(employee_id, db)
    return [r for r in results.all()]

@router.get("/address/{address_id}", response_model=AddressResponseId)
async def get_address_by_id(address_id: int,db: AsyncSession = Depends(get_db),  _current_user: TokenPayload = Depends(get_current_user)):
    result = await service.get_address_by_id(address_id, db)
    return result

@router.put("/address/{address_id}", response_model=AddressResponse)
async def update_address(address_id: int,body: AddressCreate, db: AsyncSession = Depends(get_db),  _current_user: TokenPayload = Depends(get_current_user)):
    result = await service.update_address(address_id,body.line1, body.city, body.postal_code, body.country, db)
    return result

@router.delete("/address/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_address(address_id: int,db: AsyncSession = Depends(get_db),_current_user: TokenPayload = Depends(get_current_user)):
    await service.soft_delete_address(address_id, db)
    return {"message": "Address soft deleted"}