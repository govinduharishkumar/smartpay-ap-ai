from fastapi import FastAPI

app = FastAPI(
    title="SmartPay AP AI",
    version="1.0"
)

@app.get("/")
def health_check():

    return {
        "status": "running",
        "service": "SmartPay AP AI"
    }


@app.get("/workflow-status")
def workflow_status():

    return {
        "workflow": "LangGraph AP Workflow",
        "status": "active"
    }