from fastapi import APIRouter

router = APIRouter(
    prefix="/stocks",
    tags=["Stocks"]
)
