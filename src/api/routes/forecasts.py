from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/forecasts",
    tags=["Forecasts"]
)