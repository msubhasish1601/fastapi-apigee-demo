from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database import get_db
from app.models import Customer
from app.schemas import CustomerOut
from app.deps import get_current_user

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("/", response_model=List[CustomerOut])
async def read_customers(
    skip: int = 0, 
    limit: int = 10, 
    db: AsyncSession = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    result = await db.execute(select(Customer).offset(skip).limit(limit))
    customers = result.scalars().all()
    return customers
