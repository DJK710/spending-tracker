from sqlalchemy.orm import Session
from . import models, schemas

def get_transactions(db: Session):
    return db.query(models.Transaction).order_by(models.Transaction.created_at.desc()).all()

def get_transaction(db: Session, transaction_id: int):
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(**transaction.model_dump())

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction

def update_transaction(db: Session, transaction_id: int, transaction: schemas.TransactionUpdate):
    db_transaction = get_transaction(db, transaction_id)

    if db_transaction is None:
        return None

    update_data = transaction.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_transaction, key, value)

    db.commit()
    db.refresh(db_transaction)

    return db_transaction

def delete_transaction(db: Session, transaction_id: int):
    db_transaction = get_transaction(db, transaction_id)

    if db_transaction is None:
        return None

    db.delete(db_transaction)
    db.commit()

    return db_transaction