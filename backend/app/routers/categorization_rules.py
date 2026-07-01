from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..services.categorization import reapply_rules_to_transactions

router = APIRouter(
    prefix="/categorization-rules",
    tags=["categorization-rules"]
)

@router.get("/", response_model=list[schemas.CategorizationRuleRead])
def read_categorization_rules(db: Session = Depends(get_db)):
    return crud.get_categorization_rules(db)

@router.post("/", response_model=schemas.CategorizationRuleRead)
def create_categorization_rule(rule: schemas.CategorizationRuleCreate, db: Session = Depends(get_db)):
    return crud.create_categorization_rule(db, rule)

@router.put("/{rule_id}", response_model=schemas.CategorizationRuleRead)
def update_categorization_rule(
    rule_id: int,
    rule: schemas.CategorizationRuleUpdate,
    db: Session = Depends(get_db)
):
    updated_rule = crud.update_categorization_rule(db, rule_id, rule)

    if updated_rule is None:
        raise HTTPException(status_code=404, detail="Categorization rule not found")

    return updated_rule

@router.delete("/{rule_id}", response_model=schemas.CategorizationRuleRead)
def delete_categorization_rule(rule_id: int, db: Session = Depends(get_db)):
    deleted_rule = crud.delete_categorization_rule(db, rule_id)

    if deleted_rule is None:
        raise HTTPException(status_code=404, detail="Categorization rule not found")

    return deleted_rule

@router.post("/reorder", response_model=list[schemas.CategorizationRuleRead])
def reorder_categorization_rules(request: schemas.RuleReorderRequest, db: Session = Depends(get_db)):
    reordered_rules = crud.reorder_categorization_rules(db, request.ordered_ids)

    if reordered_rules is None:
        raise HTTPException(status_code=400, detail="ordered_ids must match existing rule ids exactly")

    return reordered_rules

@router.post("/reapply", response_model=schemas.ReapplyResult)
def reapply_categorization_rules(db: Session = Depends(get_db)):
    updated_count = reapply_rules_to_transactions(db)

    return schemas.ReapplyResult(updated_count=updated_count)
