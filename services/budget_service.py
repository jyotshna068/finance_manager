from sqlalchemy.orm import Session
from typing import Dict
from database.models import Budget


def get_user_budgets(db: Session, user_id: int, month: str) -> Dict[str, float]:
    """Returns a {category: planned_amount} dict for the given month."""
    budgets = db.query(Budget).filter(Budget.user_id == user_id, Budget.month == month).all()
    return {b.category: b.planned_amount for b in budgets}


def upsert_budget(db: Session, user_id: int, category: str, month: str, planned_amount: float) -> Budget:
    """Creates or updates a budget entry for a given user/category/month."""
    budget = db.query(Budget).filter(
        Budget.user_id == user_id, Budget.category == category, Budget.month == month
    ).first()

    if budget:
        budget.planned_amount = planned_amount
    else:
        budget = Budget(user_id=user_id, category=category, month=month, planned_amount=planned_amount)
        db.add(budget)

    db.commit()
    db.refresh(budget)
    return budget


def update_actuals(db: Session, user_id: int, month: str, category_spend: Dict[str, float]) -> None:
    """Syncs actual_amount on existing budgets after expense analysis runs."""
    for category, amount in category_spend.items():
        budget = db.query(Budget).filter(
            Budget.user_id == user_id, Budget.category == category, Budget.month == month
        ).first()
        if budget:
            budget.actual_amount = amount

    db.commit()