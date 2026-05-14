from typing import TypedDict
from langgraph.graph import StateGraph, END

# -----------------------------
# Workflow State Definition
# -----------------------------

class WorkflowState(TypedDict):
    invoice_id: str
    vendor: str
    amount: float
    po_number: str
    match_status: str
    explanation: str
    dispute_email: str
    approved: bool


# -----------------------------
# Intake Agent
# -----------------------------

def intake_agent(state):

    print("\n[ Intake Agent ]")
    print(f"Processing Invoice: {state['invoice_id']}")

    return state


# -----------------------------
# Reconciliation Agent
# -----------------------------

def reconciliation_agent(state):

    print("\n[ Reconciliation Agent ]")

    # Simulated matching logic
    if state["amount"] > 12000:
        state["match_status"] = "Mismatch"
    else:
        state["match_status"] = "Matched"

    print(f"Match Status: {state['match_status']}")

    return state


# -----------------------------
# Explanation Agent
# -----------------------------

def explanation_agent(state):

    print("\n[ Explanation Agent ]")

    if state["match_status"] == "Mismatch":

        state["explanation"] = (
            "Invoice amount exceeds approved PO threshold."
        )

    else:

        state["explanation"] = (
            "Invoice successfully matched with PO."
        )

    print(f"Explanation: {state['explanation']}")

    return state


# -----------------------------
# Dispute Email Agent
# -----------------------------

def dispute_email_agent(state):

    print("\n[ Dispute Email Agent ]")

    if state["match_status"] == "Mismatch":

        email = f'''
Subject: Invoice Discrepancy Notification

Dear {state["vendor"]},

We identified a discrepancy during invoice reconciliation.

Invoice ID: {state["invoice_id"]}
PO Number: {state["po_number"]}

Reason:
{state["explanation"]}

Please review and provide clarification.

Regards,
Accounts Payable Team
'''

        state["dispute_email"] = email

        print(email)

    else:

        state["dispute_email"] = "No dispute email required."

    return state


# -----------------------------
# Human Approval Node
# -----------------------------

def human_approval_node(state):

    print("\n[ Human Approval Node ]")

    # Simulated human approval
    if state["match_status"] == "Mismatch":

        print("Mismatch detected.")
        print("Escalating for manual review.")

        state["approved"] = False

    else:

        print("Invoice Approved.")

        state["approved"] = True

    return state


# -----------------------------
# Guardrail Node
# -----------------------------

def guardrail_node(state):

    print("\n[ Guardrail Validation ]")

    # Example Guardrail
    if state["amount"] > 50000:

        raise Exception(
            "Guardrail Triggered: High-value invoice requires executive approval."
        )

    return state


# -----------------------------
# ERP Trigger Node
# -----------------------------

def erp_trigger_node(state):

    print("\n[ ERP Workflow Trigger ]")

    if state["approved"]:

        print("Triggering SAP/Oracle payment workflow.")

    else:

        print("Workflow stopped pending human approval.")

    return state


# -----------------------------
# LangGraph Workflow Definition
# -----------------------------

workflow = StateGraph(WorkflowState)

workflow.add_node("intake", intake_agent)
workflow.add_node("reconcile", reconciliation_agent)
workflow.add_node("explain", explanation_agent)
workflow.add_node("dispute_email", dispute_email_agent)
workflow.add_node("guardrail", guardrail_node)
workflow.add_node("approval", human_approval_node)
workflow.add_node("erp_trigger", erp_trigger_node)

workflow.set_entry_point("intake")

workflow.add_edge("intake", "reconcile")
workflow.add_edge("reconcile", "explain")
workflow.add_edge("explain", "dispute_email")
workflow.add_edge("dispute_email", "guardrail")
workflow.add_edge("guardrail", "approval")
workflow.add_edge("approval", "erp_trigger")
workflow.add_edge("erp_trigger", END)

# Compile Workflow
app = workflow.compile()

# -----------------------------
# Execute Workflow
# -----------------------------

result = app.invoke({

    "invoice_id": "INV-1004",
    "vendor": "ABC Corporation",
    "amount": 15000,
    "po_number": "PO-2201",
    "match_status": "",
    "explanation": "",
    "dispute_email": "",
    "approved": False
})

print("\n FINAL WORKFLOW OUTPUT ")
print(result)