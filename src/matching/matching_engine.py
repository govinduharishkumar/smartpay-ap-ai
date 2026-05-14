import pandas as pd
from difflib import SequenceMatcher
from sklearn.metrics import classification_report

# Load datasets
invoices = pd.read_csv("data/raw/invoices.csv")
po_data = pd.read_csv("data/raw/po_data.csv")

results = []

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

for _, invoice in invoices.iterrows():

    po_match = po_data[po_data["po_number"] == invoice["po_number"]]

    if len(po_match) == 0:
        results.append({
            "invoice_id": invoice["invoice_id"],
            "status": "Mismatch",
            "reason": "PO not found"
        })
        continue

    po = po_match.iloc[0]

    vendor_score = similarity(invoice["vendor"], po["vendor"])
    amount_difference = abs(invoice["amount"] - po["amount"])

    status = "Matched"
    reasons = []

    if vendor_score < 0.8:
        status = "Mismatch"
        reasons.append("Vendor mismatch")

    if amount_difference > 100:
        status = "Mismatch"
        reasons.append("Amount mismatch")

    if invoice["currency"] != po["currency"]:
        status = "Mismatch"
        reasons.append("Currency mismatch")

    results.append({
        "invoice_id": invoice["invoice_id"],
        "status": status,
        "reason": ", ".join(reasons) if reasons else "Valid Match"
    })

results_df = pd.DataFrame(results)

print(results_df)

# Sample evaluation labels
y_true = [1,1,1,0,1]
y_pred = [1 if s=="Matched" else 0 for s in results_df["status"]]

print(classification_report(y_true, y_pred))