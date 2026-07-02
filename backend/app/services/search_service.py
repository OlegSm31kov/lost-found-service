from datetime import date, timedelta
from sqlalchemy.orm import Session
from sentence_transformers import SentenceTransformer, util

from app.db.models import Item

model = SentenceTransformer("intfloat/multilingual-e5-base")

def get_embedding(text: str) -> list[float]:
    return model.encode(
        text,
        normalize_embeddings=True
    ).tolist()

def find(
        date_lost: date,
        station: str,
        summary: str,
        location: str | None,
        db: Session
):
    embedding = get_embedding(summary)
    date_from = date_lost - timedelta(days=2)
    date_to = date_lost + timedelta(days=2)

    distance = Item.embedding.cosine_distance(embedding)

    query = (
        db.query(Item)
        .filter(
            Item.station == station,
            Item.date.between(date_from, date_to),
            distance <= 0.4,
        )
    )

    if location is not None:
        query = query.filter(Item.location == location)

    return (
        query
        .order_by(distance)
        .limit(5)
        .all()
    )