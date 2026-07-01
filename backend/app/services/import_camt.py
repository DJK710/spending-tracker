from app.database import SessionLocal
from app.models import Transaction
from app.services.camt_parser import parse_all_camt_files
from app.services.categorization import categorize_parsed_transaction
from app import crud


def import_camt_folder_to_db(data_folder: str):
    db = SessionLocal()

    try:
        rules = crud.get_categorization_rules(db, active_only=True)
        parsed_files = parse_all_camt_files(data_folder)

        for file_transactions in parsed_files:
            for transaction in file_transactions:
                categorized = categorize_parsed_transaction(transaction, rules)

                db_transaction = Transaction(
                    amount=categorized["amount"],
                    type=categorized["type"],
                    description=categorized["description"],
                    is_subscription=categorized["is_subscription"],
                    transaction_date=categorized["transaction_date"],
                )

                db.add(db_transaction)

        db.commit()

    except Exception as e:
        db.rollback()
        print("Error importing CAMT files:", e)

    finally:
        db.close()

# spending-tracker/backend
# python -m app.services.import_camt
import_camt_folder_to_db("data/6-11-2024-tot-05-05-2026")
