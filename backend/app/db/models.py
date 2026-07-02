from uuid import UUID, uuid4
from datetime import date
from sqlalchemy import Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from pgvector.sqlalchemy import Vector

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "founditems"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    date: Mapped[date]
    station: Mapped[str]
    location: Mapped[str]
    summary: Mapped[str]
    embedding = mapped_column(Vector(768))