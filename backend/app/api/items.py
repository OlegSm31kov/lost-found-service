from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.db.session import get_db
from app.services.search_service import find

router = APIRouter()

@router.get("/items/find")
def find_item(_date: date, station: str, summary: str, db: Session = Depends(get_db)):
    return find(_date, station, summary, db)