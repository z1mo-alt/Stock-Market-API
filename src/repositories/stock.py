from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.stock import Stock

async def get_by_ticker(session: AsyncSession, ticker: str) -> Stock | None:
    return await session.scalar(select(Stock).where(Stock.ticker == ticker))


async def list_all(session: AsyncSession) -> list[Stock]:
    result = await session.scalars(select(Stock).order_by(Stock.ticker))
    return list(result.all())

async def create(session: AsyncSession, stock: Stock) -> Stock:
    session.add(stock)
    await session.flush()
    await session.refresh(stock)
    return stock

async def delete(session: AsyncSession, stock: Stock) -> None:
    await session.delete(stock)
    await session.flush()