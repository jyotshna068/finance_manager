from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from config.database import get_db
from config.auth import get_current_user

from services.expense_service import get_user_transactions, transactions_to_dicts
from services.budget_service import get_user_budgets, update_actuals
from services.investment_service import get_user_investments
from services.subscription_service import sync_detected_subscriptions

from workflows.finance_graph import finance_graph
from workflows.state import FinanceState

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/analysis")
def run_analysis(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Runs the full LangGraph multi-agent workflow for the current user
    and returns all analytical outputs for dashboard visualizations.
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

    # Persist derived data back to DB
    if final_state.get("expense_analysis"):
        update_actuals(db, current_user.id, current_month, final_state["expense_analysis"]["category_distribution"])

    if final_state.get("subscription_analysis"):
        sync_detected_subscriptions(db, current_user.id, final_state["subscription_analysis"]["subscriptions"])

    return {
        "expense_analysis": final_state.get("expense_analysis"),
        "budget_analysis": final_state.get("budget_analysis"),
        "investment_analysis": final_state.get("investment_analysis"),
        "subscription_analysis": final_state.get("subscription_analysis"),
        "recommendations": final_state.get("recommendations"),
        "errors": final_state.get("errors", []),
    }