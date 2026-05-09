from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

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