from camt_parser import parse_all_camt_files

transactions = parse_all_camt_files("../../data/6-11-2024-tot-05-05-2026")
count = 0

for transaction in transactions:
    for entry in transaction:

        if entry["transaction_date"] is None:
            print(entry)
            count += 1


print(f"Amount of Unknown's = {count}")