import os
import tempfile

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db
from ..services.camt_parser import parse_camt_file
from ..services.categorization import categorize_parsed_transaction

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)

@router.get("/", response_model=list[schemas.TransactionRead])
def read_transactions(db: Session = Depends(get_db)):
    return crud.get_transactions(db)

@router.get("/{transaction_id}", response_model=schemas.TransactionRead)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = crud.get_transaction(db, transaction_id)

    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction

@router.post("/", response_model=schemas.TransactionRead)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db, transaction)

@router.post("/import/camt", response_model=schemas.CamtImportResult)
async def import_camt_files(files: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    camt_files = [
        file for file in files
        if (file.filename or "").lower().endswith(".xml")
    ]

    if not camt_files:
        raise HTTPException(status_code=400, detail="Please upload a folder with CAMT XML files.")

    temp_paths = []

    try:
        parsed_transactions = []

        for file in camt_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as temp_file:
                temp_paths.append(temp_file.name)
                temp_file.write(await file.read())

            parsed_transactions.extend(parse_camt_file(temp_paths[-1]))

        rules = crud.get_categorization_rules(db, active_only=True)

        db_transactions = [
            models.Transaction(
                amount=categorized["amount"],
                type=categorized["type"],
                description=categorized["description"],
                is_subscription=categorized["is_subscription"],
                transaction_date=categorized["transaction_date"],
            )
            for categorized in (
                categorize_parsed_transaction(transaction, rules)
                for transaction in parsed_transactions
            )
        ]

        db.add_all(db_transactions)
        db.commit()

        return schemas.CamtImportResult(imported_count=len(db_transactions))

    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Could not import CAMT file: {exc}") from exc
    finally:
        for temp_path in temp_paths:
            if os.path.exists(temp_path):
                os.remove(temp_path)

@router.put("/{transaction_id}", response_model=schemas.TransactionRead)
def update_transaction(
    transaction_id: int,
    transaction: schemas.TransactionUpdate,
    db: Session = Depends(get_db)
):
    updated_transaction = crud.update_transaction(db, transaction_id, transaction)

    if updated_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return updated_transaction

@router.delete("/{transaction_id}", response_model=schemas.TransactionRead)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    deleted_transaction = crud.delete_transaction(db, transaction_id)

    if deleted_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return deleted_transaction

@router.post("/bulk-subscription-flag", response_model=schemas.BulkUpdateResult)
def bulk_subscription_flag(request: schemas.BulkSubscriptionUpdate, db: Session = Depends(get_db)):
    updated_count = crud.bulk_update_is_subscription(db, request.transaction_ids, request.is_subscription)

    return schemas.BulkUpdateResult(updated_count=updated_count)
