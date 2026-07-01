from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..services.recurring_detection import detect_recurring_series

router = APIRouter(
    prefix="/recurring",
    tags=["recurring"]
)

@router.get("/detect", response_model=list[schemas.RecurringSeriesRead])
def detect_recurring(db: Session = Depends(get_db)):
    transactions = (
        db.query(models.Transaction)
        .filter(
            models.Transaction.amount < 0,
            models.Transaction.transaction_date.isnot(None),
        )
        .all()
    )

    return detect_recurring_series(transactions)
