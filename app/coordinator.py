from app.agents.segregator import segregator_agent
from app.agents.bill_agent import bill_agent
from app.agents.discharge_agent import discharge_agent
from app.agents.id_agent import id_agent


def run_pipeline(pages):
    classified = segregator_agent(pages)

    patient_pages   = classified.get("identity_document", []) + classified.get("claim_forms", [])
    discharge_pages = classified.get("discharge_summary", []) + classified.get("prescription", []) + classified.get("investigation_report", [])
    billing_pages   = classified.get("itemized_bill", []) + classified.get("cash_receipt", []) + classified.get("cheque_or_bank_details", [])

    return {
        "patient":           id_agent(patient_pages)          if patient_pages   else {},
        "discharge_summary": discharge_agent(discharge_pages) if discharge_pages else {},
        "billing":           bill_agent(billing_pages)        if billing_pages   else {},
    }