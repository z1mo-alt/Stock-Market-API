from collections.abc import Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.stock import Stock
from repositories import stock as stock_repo
from schemas.stock import StockCreate

class StockNotFoundError(Exception):
    pass

class StockAlreadyExistsError(Exception):
    pass

async def get_stock(session: AsyncSession, ticker: str) -> Stock:
    stock = await stock_repo.get_by_ticker(session, ticker.strip().upper())
    if stock is None:
        raise StockNotFoundError(f"Stock with ticker '{ticker}' not found.")
    return stock

async def list_stocks(session: AsyncSession) -> Sequence[Stock]:
    return await stock_repo.list_all(session)

async def create_stock(session: AsyncSession, stock_create: StockCreate) -> Stock:
    try:
        stock = await stock_repo.create(session, Stock(**stock_create.model_dump()))
    except IntegrityError:
        await session.rollback()
        raise StockAlreadyExistsError(f"Stock with ticker '{stock_create.ticker}' already exists.")
    await session.commit()
    return stock

async def delete_stock(session: AsyncSession, ticker: str) -> None:
    stock = await get_stock(session, ticker)
    await stock_repo.delete(session, stock)
    await session.commit()
    