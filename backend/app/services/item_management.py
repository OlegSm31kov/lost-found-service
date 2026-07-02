from datetime import date
from sqlalchemy.orm import Session

from app.db.models import Item

from backend.app.services.search_service import get_embedding


def create_item(
    date_found: date,
    station: str,
    found_location: str,
    summary: str,
    db: Session,
):
    item = Item(
        date=date_found,
        station=station,
        location=found_location,
        summary=summary,
        embedding=get_embedding(summary)
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item.id