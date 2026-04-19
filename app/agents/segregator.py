def classify_page(text):
    text_lower = text.lower()

    if any(k in text_lower for k in ["discharge summary", "admission date", "discharge date", "attending physician", "hospital course"]):
        return "discharge_summary"

    if any(k in text_lower for k in ["itemized", "hospital bill", "itemized charges", "subtotal", "total amount", "rate\namount"]):
        return "itemized_bill"

    if any(k in text_lower for k in ["prescription", "dosage", "sig:", "refills", "rx\n", "capsule", "tablet", "take with food"]):
        return "prescription"

    if any(k in text_lower for k in ["cash receipt", "receipt no", "amount paid", "received from", "cashier"]):
        return "cash_receipt"

    if any(k in text_lower for k in ["cheque", "account number", "ifsc", "routing number", "swift", "bank account"]):
        return "cheque_or_bank_details"

    if any(k in text_lower for k in ["government id", "id card", "id number", "date of birth", "blood group", "expiry date", "issue date"]):
        return "identity_document"

    if any(k in text_lower for k in ["claim form", "claim reference", "policy number", "insurance coverage", "total amount claimed"]):
        return "claim_forms"

    if any(k in text_lower for k in ["laboratory report", "lab report", "cbc", "blood count", "pathology", "test result", "reference range"]):
        return "investigation_report"

    if any(k in text_lower for k in ["pharmacy", "invoice", "medication details", "total due"]):
        return "itemized_bill"

    return "other"


def segregator_agent(pages):
    classified = {
        "claim_forms": [],
        "cheque_or_bank_details": [],
        "identity_document": [],
        "itemized_bill": [],
        "discharge_summary": [],
        "prescription": [],
        "investigation_report": [],
        "cash_receipt": [],
        "other": []
    }

    for page in pages:
        text = page["text"] if isinstance(page, dict) else str(page)
        category = classify_page(text)
        classified[category].append(text)
        print(f"✅ PAGE CLASSIFIED: {category}")

    print("\n📦 FINAL CLASSIFICATION:")
    for k, v in classified.items():
        print(f"{k}: {len(v)} pages")

    return classified