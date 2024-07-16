from pydantic import BaseModel
from datetime import datetime
from typing import List


class Operation(BaseModel):
    book: str
    price: float
    amount: float


class OrderBook(BaseModel):
    updated_at: datetime
    sequence: int
    bids: List[Operation]
    asks: List[Operation]
