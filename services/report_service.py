from sqlalchemy.orm import Session
from database.models import Report, Recommendation
from typing import Dict, Any, List


def save_report_record(db: Session, user_id: int, file_path: str, health_score: float) -> Report:
    """Logs a generated report's metadata for history/tracking."""
    report = Report(user_id=user_id, file_path=file_path, health_score=health_score)
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def save_recommendations(db: Session, user_id: int, recommendations: List[Dict[str, Any]]) -> int:
    """Persists the recommendation agent's output for future reference/notifications."""
    count = 0
    for rec in recommendations:
        record = Recommendation(
            user_id=user_id,
            title=rec["title"],
            reasoning=rec["reasoning"],
            impact_score=rec.get("impact_score", 0),
            urgency=rec.get("urgency", "low"),
        )
        db.add(record)
        count += 1

    db.commit()
    return count


def get_report_history(db: Session, user_id: int) -> List[Report]:
    return db.query(Report).filter(Report.user_id == user_id).order_by(Report.generated_at.desc()).all()