from sqlalchemy.orm import Session
from typing import List, Dict, Any
from database.models import Investment


def get_user_investments(db: Session, user_id: int) -> List[Dict[str, Any]]:
    """Fetches investments and converts to plain dicts for the investment agent."""
    investments = db.query(Investment).filter(Investment.user_id == user_id).all()
    return [
        {
            "asset_name": i.asset_name,
            "asset_type": i.asset_type,
            "sector": i.sector,
            "invested_amount": i.invested_amount,
            "current_value": i.current_value,
            "purchase_date": i.purchase_date,
        }
        for i in investments
    ]


def add_investment(db: Session, user_id: int, data: Dict[str, Any]) -> Investment:
    """Creates a new investment record for the user."""
    investment = Investment(
        user_id=user_id,
        asset_name=data["asset_name"],
        asset_type=data.get("asset_type", "stock"),
        sector=data.get("sector", "unclassified"),
        invested_amount=data["invested_amount"],
        current_value=data.get("current_value", data["invested_amount"]),
        purchase_date=data.get("purchase_date"),
    )
    db.add(investment)
    db.commit()
    db.refresh(investment)
    return investment