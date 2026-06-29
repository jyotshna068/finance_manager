from sqlalchemy.orm import Session
from typing import List, Dict, Any
from database.models import Subscription


def sync_detected_subscriptions(db: Session, user_id: int, detected: List[Dict[str, Any]]) -> int:
    """
    Persists subscriptions detected by the subscription agent.
    Updates existing records (by merchant name) rather than duplicating.
    """
    synced = 0
    for sub in detected:
        existing = db.query(Subscription).filter(
            Subscription.user_id == user_id, Subscription.service_name == sub["merchant"]
        ).first()

        if existing:
            existing.billing_cycle = sub["billing_interval"]
            existing.amount = sub["average_amount"]
            existing.last_billed_date = sub["last_billed"]
            existing.is_active = sub["is_active"]
        else:
            new_sub = Subscription(
                user_id=user_id,
                service_name=sub["merchant"],
                billing_cycle=sub["billing_interval"],
                amount=sub["average_amount"],
                last_billed_date=sub["last_billed"],
                is_active=sub["is_active"],
            )
            db.add(new_sub)

        synced += 1

    db.commit()
    return synced


def get_active_subscriptions(db: Session, user_id: int) -> List[Subscription]:
    return db.query(Subscription).filter(
        Subscription.user_id == user_id, Subscription.is_active == True  # noqa: E712
    ).all()