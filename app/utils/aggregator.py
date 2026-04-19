def aggregate_results(claim_id, id_data, discharge_data, bill_data):
    return {
        "claim_id": claim_id,
        "patient": id_data,
        "discharge_summary": discharge_data,
        "billing": bill_data
    }