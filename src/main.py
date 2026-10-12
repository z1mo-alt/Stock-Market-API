from fastapi import FastAPI
from api.routes.stocks import router as stocks_router
from api.routes.forecasts import router as forecasts_router
from core.config import settings

app = FastAPI(
    title="Stock Market", 
    version="0.1.0",
    debug=settings.debug,
)
app.include_router(stocks_router, prefix="/api/stocks")
app.include_router(forecasts_router, prefix="/api/forecasts")


@app.get("/health")
async def health_check():
    return {"status": "ok"}