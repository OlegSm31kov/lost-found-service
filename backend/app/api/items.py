import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.db.session import get_db
from app.services.search_service import find
from app.services.item_management import create_item

router = APIRouter()

@router.get("/items/find")
def find_item(date_lost: str, station: str, summary: str, location = None, db: Session = Depends(get_db)):
    return find(datetime.datetime.strptime(date_lost, '%d.%m.%y').date(), station, summary, location, db)

@router.post("/items")
def add_item(date_found: str, station: str, location: str, summary: str, db: Session = Depends(get_db)):
    return create_item(datetime.datetime.strptime(date_found, '%d.%m.%y').date(), station, location, summary, db)