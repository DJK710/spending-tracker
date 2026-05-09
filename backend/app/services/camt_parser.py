import xml.etree.ElementTree as ET
import os
import re
from datetime import datetime

def categorize_transaction(description, addtl_info, creditor_name, debtor_name, amount):
    text = " ".join([
        description or "",
        addtl_info or "",
        creditor_name or "",
        debtor_name or "",
    ]).lower()

    is_subscription = False
    transaction_type = "Unknown"

    if "univé" in text or "unive" in text:
        transaction_type = "Healthcare"
        is_subscription = True

    elif "lidl" in text:
        transaction_type = "Groceries"

    elif "belastingdienst" in text:
        transaction_type = "Belastingdienst"

    elif "dylan van der kuijl" in text or "studentenrekening" in text:
        transaction_type = "Savings"

    elif "belastingdienst" in text and "zorgtoeslag" in text:
        transaction_type = "Healthcare allowance"

    elif "belastingdienst" in text and "huurtoeslag" in text:
        transaction_type = "Rent allowance"

    elif "paypal" in text:
        transaction_type = "PayPal"

    elif "int card services" in text or "creditcard" in text:
        transaction_type = "Credit Card Payment"

    elif "hollandsnieuwe" in text:
        transaction_type = "Phone Subscription"
        is_subscription = True

    elif "dp schoonhoven" in text:
        transaction_type = "Domino's/Food"

    elif "silvester" in text:
        transaction_type = "Freelance income"

    elif "engie" in text or "energielevering" in text:
        transaction_type = "Energy bill"
        is_subscription = True

    elif "amazon payments" in text or "amazon eu" in text:
        transaction_type = "Amazon"

    elif "villex" in text:
        transaction_type = "Rent"

    elif "veerdienst" in text:
        transaction_type = "OV"

    elif "zakgeld dylan" in text:
        transaction_type = "Pocket Money"

    elif "etos" in text:
        transaction_type = "Health & Personal Care"

    elif "mcdonalds" in text:
        transaction_type = "McDonalds/Food"

    elif "tebex" in text:
        transaction_type = "Gaming"

    elif "snackhoek" in text:
        transaction_type = "Food"

    elif "teruggaf" in text or "teruggaaf" in text:
        transaction_type = "Tax Refund"

    elif "plus rechtuyt" in text or "plus " in text:
        transaction_type = "Groceries"

    elif "albron" in text:
        transaction_type = "Food"

    elif "e-food" in text:
        transaction_type = "Food"

    elif "geld van opa" in text:
        transaction_type = "Money toward driving license"

    elif "flatex" in text:
        transaction_type = "Investments"

    elif "douglas" in text:
        transaction_type = "Gift/Personal Care"

    elif "dominos" in text or "domino" in text:
        transaction_type = "Domino's/Food"

    elif "temu" in text:
        transaction_type = "Temu"

    elif "villa pardoe" in text or "fondswerving" in text or "donatie" in text or "sidemen" in text:
        transaction_type = "Donation"

    elif "action" in text:
        transaction_type = "Action"

    elif "bonprix" in text:
        transaction_type = "Clothing"

    elif "barber" in text:
        transaction_type = "Barber"

    elif "bruilo" in text or "bruiloft" in text:
        transaction_type = "Gift"

    elif "mvgm" in text or "ikwilhuren" in text:
        transaction_type = "Housing"

    elif "netflix" in text:
        transaction_type = "Netflix"
        is_subscription = True

    elif "bigmaid" in text:
        transaction_type = "I dont remember"

    elif "kruidvat" in text:
        transaction_type = "Health & Personal Care"

    elif "jumbo" in text:
        transaction_type = "Groceries"

    elif "stichting woning in zicht" in text:
        transaction_type = "Housing"

    elif "tikkie" in text:
        transaction_type = "Tikkie"

    elif "rente" in text or "creditrente" in text:
        transaction_type = "Interest"

    elif "lunchroom" in text:
        transaction_type = "Food"

    elif "budget energie" in text or "greenchoice" in text:
        transaction_type = "Energy bill"
        is_subscription = True

    elif "ziggo" in text:
        transaction_type = "Internet/Ziggo"
        is_subscription = True

    elif "oasen" in text:
        transaction_type = "Water bill"
        is_subscription = True

    elif "gapph" in text:
        transaction_type = "Housing"
        is_subscription = True

    elif "regionale belasting" in text or "svhw" in text or "belastingen" in text:
        transaction_type = "Taxes"

    elif "doe het zelf" in text or "gamma" in text or "brievenbus" in text:
        transaction_type = "Home improvement"

    elif "albert heijn" in text:
        transaction_type = "Groceries"

    elif "mw p alphenaar" in text or "cadeau" in text:
        transaction_type = "Gift"

    elif "unhcr" in text:
        transaction_type = "Donation"

    elif "huishouden" in text or "huishoudkosten" in text:
        transaction_type = "Household money"

    elif "jagex" in text or "ea.com" in text or "ea play" in text or "side+ by sidemen" in text:
        transaction_type = "Gaming"
        if "recurring" in text or "membership" in text:
            is_subscription = True

    elif "amazon marketplace" in text:
        transaction_type = "Amazon refund" if amount > 0 else "Amazon"

    elif "media markt" in text or "fresh .n rebel" in text:
        transaction_type = "Electronics"

    elif "barbershop" in text or "knippenz" in text:
        transaction_type = "Barber"

    elif "primark" in text:
        transaction_type = "Clothing"

    elif "bol.com" in text:
        transaction_type = "Bol.com"

    elif "hms_host" in text or "hmshost" in text or "kiosk" in text:
        transaction_type = "Food"

    elif "justbite" in text or "thuisbezorgd" in text:
        transaction_type = "Food"

    elif "efteling" in text or "013 poppodium" in text or "america" in text or "digital art center":
        transaction_type = "Entertainment"

    elif "capelsebrug" in text or "ovpay" in text or "ov-chip" in text:
        transaction_type = "OV"

    elif "credit card" in text:
        transaction_type = "Credit Card"

    elif "verjaardag" in text:
        transaction_type = "Gift received"

    return transaction_type, is_subscription

def ErrorHelper(entry, namespace, amount, credit_debit_element, unstructured_element):
            print("\n--- UNKNOWN TRANSACTION ---")

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

        transaction_type, is_subscription = categorize_transaction(
            description=description,
            addtl_info=addtl_info,
            creditor_name=creditor_name,
            debtor_name=debtor_name,
            amount=amount,
        )
            
        
        date_element = entry.find("ns:BookgDt/ns:Dt", namespace)

        if date_element is None:
            date_element = entry.find("ns:BookgDt/ns:DtTm", namespace)

        if date_element is None:
            date_element = entry.find("ns:ValDt/ns:Dt", namespace)

        if date_element is not None:
            transaction_date = date_element.text

        if description == "Unknown" or transaction_type == "Unknown" or transaction_date == "Unknown":
            print("\n--- UNKNOWN TRANSACTION ---")
            print(f"Description = {description}")
            print(f"Transaction Type = {transaction_type}")
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

        if transaction_type == "Donation":
            ErrorHelper(entry, namespace, amount, credit_debit_element, unstructured_element)
            
        transactions.append({
            "amount": amount,
            "type": transaction_type,
            "description": description,
            "is_subscription": is_subscription,
            "transaction_date": date_value
        })

    return transactions