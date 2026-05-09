from camt_parser import parse_all_camt_files

transactions = parse_all_camt_files("../../data/6-11-2024-tot-05-05-2026")
count = 0

for transaction in transactions:
    for entry in transaction:
        
        if entry["type"] == "Donation":
            print(entry)
            count += 1
    #transaction[0]["transaction_date"] == "Unknown" or
    


print(f"Amount of Unknown's = {count}")