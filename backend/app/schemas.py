from datetime import date, datetime
from typing import Literal
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


class CamtImportResult(BaseModel):
    imported_count: int


class CategorizationRuleBase(BaseModel):
    keywords: list[str]
    transaction_type: str
    is_subscription: bool = False
    subscription_keywords: list[str] | None = None
    amount_sign: Literal["any", "positive", "negative"] = "any"
    is_active: bool = True


class CategorizationRuleCreate(CategorizationRuleBase):
    priority: int


class CategorizationRuleUpdate(BaseModel):
    keywords: list[str] | None = None
    transaction_type: str | None = None
    is_subscription: bool | None = None
    subscription_keywords: list[str] | None = None
    amount_sign: Literal["any", "positive", "negative"] | None = None
    is_active: bool | None = None
    priority: int | None = None


class CategorizationRuleRead(CategorizationRuleBase):
    id: int
    priority: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class RuleReorderRequest(BaseModel):
    ordered_ids: list[int]


class ReapplyResult(BaseModel):
    updated_count: int


class RecurringSeriesRead(BaseModel):
    description: str
    type: str
    avg_amount: float
    occurrence_count: int
    first_date: date
    last_date: date
    predicted_next_date: date
    transaction_ids: list[int]
    all_marked_subscription: bool


class BulkSubscriptionUpdate(BaseModel):
    transaction_ids: list[int]
    is_subscription: bool = True


class BulkUpdateResult(BaseModel):
    updated_count: int
