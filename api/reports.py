from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime
import os

from config.database import get_db
from config.auth import get_current_user

from services.expense_service import get_user_transactions, transactions_to_dicts
from services.budget_service import get_user_budgets
from services.investment_service import get_user_investments
from services.report_service import save_report_record, save_recommendations, get_report_history

from workflows.finance_graph import finance_graph
from workflows.state import FinanceState

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/generate")
def generate_report(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Runs the complete agent workflow (including the report_generator
    node) and returns the resulting PDF file.
    """
    transactions = get_user_transactions(db, current_user.id)
    transaction_dicts = transactions_to_dicts(transactions)

    current_month = datetime.utcnow().strftime("%Y-%m")
    budgets = get_user_budgets(db, current_user.id, current_month)
    investments = get_user_investments(db, current_user.id)

    initial_state: FinanceState = {
        "user_id": current_user.id,
        "raw_transactions": transaction_dicts,
        "budgets": budgets,
        "investment_accounts": investments,
        "errors": [],
    }

    final_state = finance_graph.invoke(initial_state)

    report_path = final_state.get("report_path")
    if not report_path or not os.path.exists(report_path):
        raise HTTPException(status_code=500, detail="Report generation failed.")

    health_score = final_state.get("budget_analysis", {}).get("financial_health_score", 0)
    save_report_record(db, current_user.id, report_path, health_score)

    if final_state.get("recommendations"):
        save_recommendations(db, current_user.id, final_state["recommendations"])

    return FileResponse(report_path, media_type="application/pdf", filename=os.path.basename(report_path))


@router.get("/history")
def report_history(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Returns metadata for all previously generated reports."""
    reports = get_report_history(db, current_user.id)
    return [
        {
            "id": r.id,
            "file_path": r.file_path,
            "generated_at": r.generated_at,
            "health_score": r.health_score,
        }
        for r in reports
    ]