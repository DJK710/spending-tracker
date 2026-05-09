from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class TransactionBase(BaseModel):
    amount: float
    type: str
    description: str | None = None
    is_subscription: bool = False
    transaction_date: date | None = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: float | None = None
    type: str | None = None
    description: str | None = None
    is_subscription: bool | None = None
    transaction_date: date | None = None


class TransactionRead(TransactionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)