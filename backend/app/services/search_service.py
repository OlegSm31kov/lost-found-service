from datetime import date
from sqlalchemy.orm import Session

from app.db.models import Item

def find(
        _date: date,
        station: str,
        summary: str,
        db: Session
):
    return (db.query(Item.id)
            .filter(Item.date == _date,
                    Item.station == station,
                    Item.summary == summary)
                    .scalar()
            )