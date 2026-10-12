from fastapi import FastAPI, Depends
from api.routes.stocks import router as stocks_router
from api.routes.forecasts import router as forecasts_router
from core.config import settings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_session

app = FastAPI(
    title="Stock Market", 
    version="0.1.0",
    debug=settings.debug,
)
app.include_router(stocks_router, prefix="/api/stocks")
app.include_router(forecasts_router, prefix="/api/forecasts")


@app.get("/health")
async def health_check(session: AsyncSession = Depends(get_session)):
    await session.execute(text("SELECT 1"))
    return {"status": "ok"}