from app.database import SessionLocal
from app.models import Transaction
from app.services.camt_parser import parse_all_camt_files


def import_camt_folder_to_db(data_folder: str):
    db = SessionLocal()

    try:
        parsed_files = parse_all_camt_files(data_folder)

        for file_transactions in parsed_files:
            for transaction in file_transactions:
                db_transaction = Transaction(
                    amount=transaction["amount"],
                    type=transaction["type"],
                    description=transaction["description"],
                    is_subscription=transaction["is_subscription"],
                    transaction_date=transaction["transaction_date"],
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