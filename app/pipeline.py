from langgraph.graph import StateGraph
from typing import TypedDict, Dict, List
from app.utils.ocr import extract_pages
from app.agents.segregator import segregator_agent
from app.agents.id_agent import id_agent
from app.agents.discharge_agent import discharge_agent
from app.agents.bill_agent import bill_agent
from app.utils.aggregator import aggregate_results


# ---------------- STATE ---------------- #
class ClaimState(TypedDict, total=False):
    pages: List[dict]
    classified: Dict
    id_data: Dict
    discharge_data: Dict
    bill_data: Dict
    result: Dict


# ---------------- PIPELINE ---------------- #
def run_pipeline(file_path, claim_id):
    pages = extract_pages(file_path)

    graph = StateGraph(ClaimState)

    # -------- Nodes -------- #

    def segregate(state: ClaimState):
        try:
            result = segregator_agent(state.get("pages", []))
            print("✅ SEGREGATOR OUTPUT:", result)
            return {"classified": result}
        except Exception as e:
            print("❌ SEGREGATOR ERROR:", e)
            return {
                "classified": {
                    "identity_document": [],
                    "discharge_summary": [],
                    "itemized_bill": []
                }
            }

    def id_node(state: ClaimState):
        classified = state.get("classified", {})
        pages = (
            classified.get("identity_document", [])
            + classified.get("claim_forms", [])          # ← added
        )
        return {"id_data": id_agent(pages)}

    def discharge_node(state: ClaimState):
        classified = state.get("classified", {})
        pages = (
            classified.get("discharge_summary", [])
            + classified.get("prescription", [])          # ← added
            + classified.get("investigation_report", [])  # ← added
        )
        return {"discharge_data": discharge_agent(pages)}

    def bill_node(state: ClaimState):
        classified = state.get("classified", {})
        pages = (
            classified.get("itemized_bill", [])
            + classified.get("cash_receipt", [])           # ← added
            + classified.get("cheque_or_bank_details", []) # ← added
        )
        return {"bill_data": bill_agent(pages)}

    def aggregate(state: ClaimState):
        return {
            "result": aggregate_results(
                claim_id,
                state.get("id_data"),
                state.get("discharge_data"),
                state.get("bill_data"),
            )
        }

    # -------- Add Nodes -------- #

    graph.add_node("segregator", segregate)
    graph.add_node("id", id_node)
    graph.add_node("discharge", discharge_node)
    graph.add_node("bill", bill_node)
    graph.add_node("aggregate", aggregate)

    # -------- Flow (SEQUENTIAL) -------- #

    graph.set_entry_point("segregator")

    graph.add_edge("segregator", "id")
    graph.add_edge("id", "discharge")
    graph.add_edge("discharge", "bill")
    graph.add_edge("bill", "aggregate")

    graph.set_finish_point("aggregate")

    # -------- Compile -------- #

    app = graph.compile()

    # -------- Run -------- #

    result = app.invoke({"pages": pages})

    return result.get("result", {"error": "Processing failed"})