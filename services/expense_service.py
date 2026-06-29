from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Dict, Any
from database.models import Transaction, Merchant


def save_transactions(db: Session, user_id: int, account_id: int, transactions: List[Dict[str, Any]]) -> int:
    """
    Persists cleaned transactions into the database, resolving or
    creating merchant records as needed. Returns count of rows inserted.
    """
    inserted = 0

    for txn in transactions:
        merchant_name = txn.get("merchant") or txn.get("description", "Unknown")[:255]

        merchant = db.query(Merchant).filter(Merchant.normalized_name == merchant_name).first()
        if not merchant:
            merchant = Merchant(
                raw_name=merchant_name,
                normalized_name=merchant_name,
                category=txn.get("category", "uncategorized"),
            )
            db.add(merchant)
            db.flush()  # get merchant.id without full commit

        transaction = Transaction(
            user_id=user_id,
            account_id=account_id,
            merchant_id=merchant.id,
            date=txn["date"],
            description=txn.get("description", ""),
            amount=txn["amount"],
            transaction_type=txn.get("transaction_type", "debit"),
            category=txn.get("category", merchant.category),
            payment_method=txn.get("payment_method", "unknown"),
            confidence_score=txn.get("confidence_score", 0.5),
        )
        db.add(transaction)
        inserted += 1

    db.commit()
    return inserted


def get_user_transactions(db: Session, user_id: int, start_date: datetime = None, end_date: datetime = None) -> List[Transaction]:
    """Fetches a user's transactions, optionally filtered by date range."""
    query = db.query(Transaction).filter(Transaction.user_id == user_id)

    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)

    return query.order_by(Transaction.date.desc()).all()


def transactions_to_dicts(transactions: List[Transaction]) -> List[Dict[str, Any]]:
    """Converts ORM transaction rows into plain dicts for agent consumption."""
    return [
        {
            "date": t.date,
            "description": t.description,
            "amount": t.amount,
            "transaction_type": t.transaction_type,
            "category": t.category,
            "merchant": t.merchant.normalized_name if t.merchant else None,
            "payment_method": t.payment_method,
        }
        for t in transactions
    ]