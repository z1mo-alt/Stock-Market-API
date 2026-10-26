from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, StringConstraints

Ticker = Annotated[str, StringConstraints(strip_whitespace=True, to_upper=True,min_length=1, max_length=10, pattern=r"^[A-Za-z0-9.\-]+$")]
Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
Exchange = Annotated[str, StringConstraints(strip_whitespace=True, to_upper=True, min_length=1, max_length=10)]
Currency = Annotated[str, StringConstraints(strip_whitespace=True, to_upper=True, pattern=r"^[A-Za-z]{3}$")]

class StockBase(BaseModel):
    ticker: Ticker
    name: Name
    exchange: Exchange | None = None
    currency: Currency


class StockCreate(StockBase):
    pass


class StockRead(StockBase):
    model_config = ConfigDict(from_attributes=True)

    created_at: datetime