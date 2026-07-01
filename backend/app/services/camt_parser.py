import xml.etree.ElementTree as ET
import os
import re
from datetime import datetime

def parse_all_camt_files(data_folder):
    results = []
    for filename in os.listdir(data_folder):
        full_path = os.path.join(data_folder, filename)
        if os.path.isfile(full_path) and filename.lower().endswith(".xml"):
            try:
                parsed = parse_camt_file(full_path)
                results.append(parsed)
            except Exception as e:
                print(f"Error parsing {filename}: {e}")

    return results

def parse_camt_file(file_path: str) -> list[dict]:
    tree = ET.parse(file_path)
    root = tree.getroot()

    namespace = {
        "ns": root.tag.split("}")[0].strip("{")
    }

    transactions = []

    entries = root.findall(".//ns:Ntry", namespace)

    for entry in entries:
        transaction_date = "Unknown"

        amount_element = entry.find("ns:Amt", namespace)
        credit_debit_element = entry.find("ns:CdtDbtInd", namespace)


        if amount_element is None or credit_debit_element is None:
            continue

        amount = float(amount_element.text)

        if credit_debit_element.text == "DBIT":
            amount *= -1

        description = "Bank import"

        unstructured_element = entry.find(
            "ns:AddtlNtryInf",
            namespace
        )

        creditor_element = entry.find(".//ns:Cdtr/ns:Nm", namespace)
        debtor_element = entry.find(".//ns:Dbtr/ns:Nm", namespace)
        creditor_name = creditor_element.text if creditor_element is not None else ""
        debtor_name = debtor_element.text if debtor_element is not None else ""
        addtl_info = unstructured_element.text if unstructured_element is not None else ""
        


        if unstructured_element is not None:
            if "remi" in (unstructured_element.text or "").lower() or "eref" in (unstructured_element.text or "").lower():
                if credit_debit_element.text == "DBIT":
                    description_element = entry.find(".//ns:Cdtr/ns:Nm", namespace)
                    description = description_element.text if description_element is not None else "Unknown"
                elif credit_debit_element.text == "CRDT":
                    description_element = entry.find(".//ns:Dbtr/ns:Nm", namespace)
                    description = description_element.text if description_element is not None else "Unknown"
                else:
                    description = ""
            else:   
                if len([p.strip() for p in unstructured_element.text.split("  ") if p.strip()]) > 1:
                    candidate = [p.strip() for p in unstructured_element.text.split("  ") if p.strip()]
                    if "www.ovpay.nl" in candidate:
                        description = "ovpay"
                        transaction_type = "ovpay"
                    elif candidate[1] == "VILLEX,PAS254":
                        description = "Rent"
                    elif re.match(r"^[A-Z0-9]+,PAS\d+$", candidate[1]):
                        description = "Unknown"
                    else:
                        description = [p.strip() for p in unstructured_element.text.split("  ") if p.strip()][1]
                elif unstructured_element.text:
                    description = unstructured_element.text

        date_element = entry.find("ns:BookgDt/ns:Dt", namespace)

        if date_element is None:
            date_element = entry.find("ns:BookgDt/ns:DtTm", namespace)

        if date_element is None:
            date_element = entry.find("ns:ValDt/ns:Dt", namespace)

        if date_element is not None:
            transaction_date = date_element.text

        if description == "Unknown" or transaction_date == "Unknown":
            print("\n--- UNKNOWN TRANSACTION ---")
            print(f"Description = {description}")
            print(f"Transaction Date = {transaction_date}")
            # Basic info
            print("Amount:", amount)
            print("Direction:", credit_debit_element.text)

            # Raw description
            if unstructured_element is not None and unstructured_element.text:
                print("AddtlNtryInf:", unstructured_element.text)

            # Try structured remittance
            rmt = entry.find(".//ns:RmtInf/ns:Ustrd", namespace)
            if rmt is not None and rmt.text:
                print("RmtInf/Ustrd:", rmt.text)

            # Creditor / Debtor
            cdtr = entry.find(".//ns:Cdtr/ns:Nm", namespace)
            if cdtr is not None and cdtr.text:
                print("Cdtr:", cdtr.text)

            dbtr = entry.find(".//ns:Dbtr/ns:Nm", namespace)
            if dbtr is not None and dbtr.text:
                print("Dbtr:", dbtr.text)

            # IBANs (very useful sometimes)
            cdtr_iban = entry.find(".//ns:CdtrAcct/ns:Id/ns:IBAN", namespace)
            if cdtr_iban is not None and cdtr_iban.text:
                print("Cdtr IBAN:", cdtr_iban.text)

            dbtr_iban = entry.find(".//ns:DbtrAcct/ns:Id/ns:IBAN", namespace)
            if dbtr_iban is not None and dbtr_iban.text:
                print("Dbtr IBAN:", dbtr_iban.text)

            print("--- END ---\n")
        
        date_value = transaction_date

        if date_value != "Unknown":
            date_value = datetime.fromisoformat(date_value).date()
        else:
            date_value = None

        transactions.append({
            "amount": amount,
            "description": description,
            "addtl_info": addtl_info,
            "creditor_name": creditor_name,
            "debtor_name": debtor_name,
            "transaction_date": date_value
        })

    return transactions