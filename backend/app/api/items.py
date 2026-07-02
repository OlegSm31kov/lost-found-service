from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.db.session import get_db
from app.services.search_service import find
from app.services.item_management import create_item

router = APIRouter()

@router.get("/items/find")
def find_item(date_lost: date, station: str, summary: str, location = None, db: Session = Depends(get_db)):
    return find(date_lost, station, location, summary, db)

@router.post("/items")
def add_item(date_found: date, station: str, location: str, summary: str, db: Session = Depends(get_db)):
    return create_item(date_found, station, location, summary, db)