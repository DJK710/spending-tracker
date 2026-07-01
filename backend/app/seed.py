from .database import SessionLocal
from .models import CategorizationRule
from .seed_data.default_categorization_rules import DEFAULT_CATEGORIZATION_RULES


def seed_categorization_rules_if_empty() -> None:
    db = SessionLocal()

    try:
        if db.query(CategorizationRule).count() > 0:
            return

        rules = [
            CategorizationRule(
                priority=(index + 1) * 10,
                keywords=rule["keywords"],
                transaction_type=rule["transaction_type"],
                is_subscription=rule.get("is_subscription", False),
                subscription_keywords=rule.get("subscription_keywords"),
                amount_sign=rule.get("amount_sign", "any"),
            )
            for index, rule in enumerate(DEFAULT_CATEGORIZATION_RULES)
        ]

        db.add_all(rules)
        db.commit()
    finally:
        db.close()
