from sqlalchemy.orm import Session

from .. import crud
from ..models import CategorizationRule, Transaction


def apply_rules(text: str, amount: float, rules: list[CategorizationRule]) -> tuple[str, bool]:
    text = (text or "").lower()

    for rule in rules:
        if rule.amount_sign == "positive" and amount <= 0:
            continue

        if rule.amount_sign == "negative" and amount >= 0:
            continue

        if not any(keyword.lower() in text for keyword in rule.keywords):
            continue

        is_subscription = rule.is_subscription or (
            bool(rule.subscription_keywords)
            and any(keyword.lower() in text for keyword in rule.subscription_keywords)
        )

        return rule.transaction_type, is_subscription

    return "Unknown", False


def categorize_parsed_transaction(parsed: dict, rules: list[CategorizationRule]) -> dict:
    text = " ".join(
        [
            parsed.get("description") or "",
            parsed.get("addtl_info") or "",
            parsed.get("creditor_name") or "",
            parsed.get("debtor_name") or "",
        ]
    )

    transaction_type, is_subscription = apply_rules(text, parsed["amount"], rules)

    return {**parsed, "type": transaction_type, "is_subscription": is_subscription}


def reapply_rules_to_transactions(db: Session) -> int:
    rules = crud.get_categorization_rules(db, active_only=True)
    updated_count = 0

    for transaction in db.query(Transaction).all():
        new_type, new_is_subscription = apply_rules(
            transaction.description or "", float(transaction.amount), rules
        )

        if new_type != transaction.type or new_is_subscription != transaction.is_subscription:
            transaction.type = new_type
            transaction.is_subscription = new_is_subscription
            updated_count += 1

    db.commit()

    return updated_count
