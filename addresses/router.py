"""Address Router"""

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from fastapi import Depends, status, Body, APIRouter
from addresses import service
from addresses.schemas import AddressCreate, AddressResponse, AddressResponseId
from auth.dependencies import get_current_user
from auth.schemas import TokenPayload

router = APIRouter(prefix="/address",tags=["Address"])

@router.post("",status_code=status.HTTP_201_CREATED,response_model= AddressResponse)
async def create_address(body : AddressCreate, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    address = await service.create(db,body.name, **body)
    return address

@router.get("",response_model= list[AddressResponse])
async def get_all_addresss(db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    results = await service.get_all_addresses(db)
    return [r for r in results.all()]

@router.get("/{address_id}", response_model = AddressResponseId)
async def get_address_by_id(address_id: int, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    result= await service.get_address_by_id(address_id, db)
    return result

@router.put("/{address_id}")
async def update_address(address_id: int, body: dict = AddressCreate, db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    result = await service.update_address(address_id, body.name, body.email, db)
    return result

@router.delete("/{address_id}", status_code= status.HTTP_204_NO_CONTENT)
async def soft_delete_address(address_id: int,db: AsyncSession = Depends(get_db), _current_user: TokenPayload = Depends(get_current_user)):
    await service.soft_delete_address(address_id, db)
    return {"message": "Address soft deleted"}
