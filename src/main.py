from fastapi import FastAPI
from api.routes.stocks import router as stocks_router

app = FastAPI(
    title="Stock Market", 
    version="0.1.0",
)
app.include_router(stocks_router, prefix="/api/stocks")