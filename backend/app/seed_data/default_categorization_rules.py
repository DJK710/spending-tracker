# Transcribed from the original hardcoded if/elif chain that used to live in
# backend/app/services/camt_parser.py::categorize_transaction. Order matches
# the original branch order except for two changes:
#
# 1. The "zorgtoeslag"/"huurtoeslag" branches originally required
#    "belastingdienst" AND "zorgtoeslag" (or "huurtoeslag") both present, but
#    were placed after a plain "belastingdienst" branch that always matched
#    first — making them permanently unreachable. Rules here only support
#    ANY-of-keywords matching, not AND, so they're transcribed as standalone
#    keyword rules (just "zorgtoeslag" / "huurtoeslag") and moved ahead of the
#    generic "belastingdienst" rule so they're actually reachable.
# 2. The original Entertainment branch was
#    `"efteling" in text or "013 poppodium" in text or "america" in text or "digital art center"`
#    — the last clause is a bare non-empty string (always truthy), so this
#    branch always fired once reached, making every rule after it (OV,
#    Credit Card, Gift received) dead code. Fixed here to properly check
#    `"digital art center" in text`.
DEFAULT_CATEGORIZATION_RULES = [
    {"keywords": ["univé", "unive"], "transaction_type": "Healthcare", "is_subscription": True},
    {"keywords": ["lidl"], "transaction_type": "Groceries"},
    {"keywords": ["zorgtoeslag"], "transaction_type": "Healthcare allowance"},
    {"keywords": ["huurtoeslag"], "transaction_type": "Rent allowance"},
    {"keywords": ["belastingdienst"], "transaction_type": "Belastingdienst"},
    {"keywords": ["dylan van der kuijl", "studentenrekening"], "transaction_type": "Savings"},
    {"keywords": ["paypal"], "transaction_type": "PayPal"},
    {"keywords": ["int card services", "creditcard"], "transaction_type": "Credit Card Payment"},
    {"keywords": ["hollandsnieuwe"], "transaction_type": "Phone Subscription", "is_subscription": True},
    {"keywords": ["dp schoonhoven"], "transaction_type": "Domino's/Food"},
    {"keywords": ["silvester"], "transaction_type": "Freelance income"},
    {"keywords": ["engie", "energielevering"], "transaction_type": "Energy bill", "is_subscription": True},
    {"keywords": ["amazon payments", "amazon eu"], "transaction_type": "Amazon"},
    {"keywords": ["villex"], "transaction_type": "Rent"},
    {"keywords": ["veerdienst"], "transaction_type": "OV"},
    {"keywords": ["zakgeld dylan"], "transaction_type": "Pocket Money"},
    {"keywords": ["etos"], "transaction_type": "Health & Personal Care"},
    {"keywords": ["mcdonalds"], "transaction_type": "McDonalds/Food"},
    {"keywords": ["tebex"], "transaction_type": "Gaming"},
    {"keywords": ["snackhoek"], "transaction_type": "Food"},
    {"keywords": ["teruggaf", "teruggaaf"], "transaction_type": "Tax Refund"},
    {"keywords": ["plus rechtuyt", "plus "], "transaction_type": "Groceries"},
    {"keywords": ["albron"], "transaction_type": "Food"},
    {"keywords": ["e-food"], "transaction_type": "Food"},
    {"keywords": ["geld van opa"], "transaction_type": "Money toward driving license"},
    {"keywords": ["flatex"], "transaction_type": "Investments"},
    {"keywords": ["douglas"], "transaction_type": "Gift/Personal Care"},
    {"keywords": ["dominos", "domino"], "transaction_type": "Domino's/Food"},
    {"keywords": ["temu"], "transaction_type": "Temu"},
    {
        "keywords": ["villa pardoe", "fondswerving", "donatie", "sidemen"],
        "transaction_type": "Donation",
    },
    {"keywords": ["action"], "transaction_type": "Action"},
    {"keywords": ["bonprix"], "transaction_type": "Clothing"},
    {"keywords": ["barber"], "transaction_type": "Barber"},
    {"keywords": ["bruilo", "bruiloft"], "transaction_type": "Gift"},
    {"keywords": ["mvgm", "ikwilhuren"], "transaction_type": "Housing"},
    {"keywords": ["netflix"], "transaction_type": "Netflix", "is_subscription": True},
    {"keywords": ["bigmaid"], "transaction_type": "I dont remember"},
    {"keywords": ["kruidvat"], "transaction_type": "Health & Personal Care"},
    {"keywords": ["jumbo"], "transaction_type": "Groceries"},
    {"keywords": ["stichting woning in zicht"], "transaction_type": "Housing"},
    {"keywords": ["tikkie"], "transaction_type": "Tikkie"},
    {"keywords": ["rente", "creditrente"], "transaction_type": "Interest"},
    {"keywords": ["lunchroom"], "transaction_type": "Food"},
    {"keywords": ["budget energie", "greenchoice"], "transaction_type": "Energy bill", "is_subscription": True},
    {"keywords": ["ziggo"], "transaction_type": "Internet/Ziggo", "is_subscription": True},
    {"keywords": ["oasen"], "transaction_type": "Water bill", "is_subscription": True},
    {"keywords": ["gapph"], "transaction_type": "Housing", "is_subscription": True},
    {"keywords": ["regionale belasting", "svhw", "belastingen"], "transaction_type": "Taxes"},
    {"keywords": ["doe het zelf", "gamma", "brievenbus"], "transaction_type": "Home improvement"},
    {"keywords": ["albert heijn"], "transaction_type": "Groceries"},
    {"keywords": ["mw p alphenaar", "cadeau"], "transaction_type": "Gift"},
    {"keywords": ["unhcr"], "transaction_type": "Donation"},
    {"keywords": ["huishouden", "huishoudkosten"], "transaction_type": "Household money"},
    {
        "keywords": ["jagex", "ea.com", "ea play", "side+ by sidemen"],
        "transaction_type": "Gaming",
        "subscription_keywords": ["recurring", "membership"],
    },
    {
        "keywords": ["amazon marketplace"],
        "transaction_type": "Amazon refund",
        "amount_sign": "positive",
    },
    {
        "keywords": ["amazon marketplace"],
        "transaction_type": "Amazon",
        "amount_sign": "negative",
    },
    {"keywords": ["media markt", "fresh .n rebel"], "transaction_type": "Electronics"},
    {"keywords": ["barbershop", "knippenz"], "transaction_type": "Barber"},
    {"keywords": ["primark"], "transaction_type": "Clothing"},
    {"keywords": ["bol.com"], "transaction_type": "Bol.com"},
    {"keywords": ["hms_host", "hmshost", "kiosk"], "transaction_type": "Food"},
    {"keywords": ["justbite", "thuisbezorgd"], "transaction_type": "Food"},
    {
        "keywords": ["efteling", "013 poppodium", "america", "digital art center"],
        "transaction_type": "Entertainment",
    },
    {"keywords": ["capelsebrug", "ovpay", "ov-chip"], "transaction_type": "OV"},
    {"keywords": ["credit card"], "transaction_type": "Credit Card"},
    {"keywords": ["verjaardag"], "transaction_type": "Gift received"},
]
