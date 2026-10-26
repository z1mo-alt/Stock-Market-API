from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session
from services import stock as stock_service
from schemas.stock import StockCreate, StockRead

router = APIRouter(
    tags=["Stocks"]
)

@router.post("", response_model=StockRead, status_code=status.HTTP_201_CREATED)
async def create_stock(data: StockCreate, session: AsyncSession = Depends(get_session)):
    try:
        return await stock_service.create_stock(session, data)
    except stock_service.StockAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("", response_model=list[StockRead])
async def list_stocks(session: AsyncSession = Depends(get_session)):
    return await stock_service.list_stocks(session)

@router.get("/{ticker}", response_model=StockRead)
async def get_stock(ticker: str, session: AsyncSession = Depends(get_session)):
    try:
        return await stock_service.get_stock(session, ticker)
    except stock_service.StockNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("/{ticker}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_stock(ticker: str, session: AsyncSession = Depends(get_session)):
    try:
        await stock_service.delete_stock(session, ticker)
    except stock_service.StockNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))