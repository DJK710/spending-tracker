from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Transaction
from app.services.ai_service import generate_spending_insights

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)

limiter = Limiter(key_func=get_remote_address)


class AIAnalyzeFilters(BaseModel):
    type: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    subscription_filter: Optional[str] = "all"
    sort_by: Optional[str] = "newest"
    exclude_savings: bool = True


@router.post("/analyze")
@limiter.limit("5/minute")
def analyze_spending(
    request: Request,
    filters: AIAnalyzeFilters,
    db: Session = Depends(get_db),
):
    query = db.query(Transaction)

    if filters.exclude_savings:
        query = query.filter(Transaction.type != "Savings")

    if filters.type and filters.type != "All":
        query = query.filter(Transaction.type == filters.type)

    if filters.start_date:
        query = query.filter(Transaction.transaction_date >= filters.start_date)

    if filters.end_date:
        query = query.filter(Transaction.transaction_date <= filters.end_date)

    if filters.subscription_filter == "subscriptions":
        query = query.filter(Transaction.is_subscription == True)

    if filters.subscription_filter == "non-subscriptions":
        query = query.filter(Transaction.is_subscription == False)

    if filters.sort_by == "amount-high":
        query = query.order_by(Transaction.amount.desc())
    elif filters.sort_by == "amount-low":
        query = query.order_by(Transaction.amount.asc())
    elif filters.sort_by == "oldest":
        query = query.order_by(Transaction.transaction_date.asc())
    else:
        query = query.order_by(Transaction.transaction_date.desc())

    transactions = query.limit(100).all()

    transaction_data = []

    for transaction in transactions:
        transaction_data.append(
            {
                "amount": float(transaction.amount),
                "type": transaction.type,
                "description": transaction.description,
                "is_subscription": transaction.is_subscription,
                "transaction_date": (
                    transaction.transaction_date.isoformat()
                    if hasattr(transaction, "transaction_date")
                    and transaction.transaction_date
                    else None
                ),
                "created_at": (
                    transaction.created_at.isoformat()
                    if transaction.created_at
                    else None
                ),
            }
        )

    insight = generate_spending_insights(transaction_data, filters.model_dump())

    return {
        "insight": insight,
        "transaction_count": len(transaction_data),
    }