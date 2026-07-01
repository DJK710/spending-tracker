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

def bulk_update_is_subscription(db: Session, transaction_ids: list[int], is_subscription: bool):
    updated_count = (
        db.query(models.Transaction)
        .filter(models.Transaction.id.in_(transaction_ids))
        .update({"is_subscription": is_subscription}, synchronize_session=False)
    )

    db.commit()

    return updated_count

def get_categorization_rules(db: Session, active_only: bool = False):
    query = db.query(models.CategorizationRule)

    if active_only:
        query = query.filter(models.CategorizationRule.is_active.is_(True))

    return query.order_by(models.CategorizationRule.priority.asc()).all()

def get_categorization_rule(db: Session, rule_id: int):
    return db.query(models.CategorizationRule).filter(models.CategorizationRule.id == rule_id).first()

def create_categorization_rule(db: Session, rule: schemas.CategorizationRuleCreate):
    db_rule = models.CategorizationRule(**rule.model_dump())

    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)

    return db_rule

def update_categorization_rule(db: Session, rule_id: int, rule: schemas.CategorizationRuleUpdate):
    db_rule = get_categorization_rule(db, rule_id)

    if db_rule is None:
        return None

    update_data = rule.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_rule, key, value)

    db.commit()
    db.refresh(db_rule)

    return db_rule

def delete_categorization_rule(db: Session, rule_id: int):
    db_rule = get_categorization_rule(db, rule_id)

    if db_rule is None:
        return None

    db.delete(db_rule)
    db.commit()

    return db_rule

def reorder_categorization_rules(db: Session, ordered_ids: list[int]):
    rules_by_id = {
        rule.id: rule
        for rule in db.query(models.CategorizationRule)
        .filter(models.CategorizationRule.id.in_(ordered_ids))
        .all()
    }

    if len(rules_by_id) != len(set(ordered_ids)):
        return None

    for index, rule_id in enumerate(ordered_ids):
        rules_by_id[rule_id].priority = (index + 1) * 10

    db.commit()

    return get_categorization_rules(db)