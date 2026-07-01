from fastapi import FastAPI

from app.api.items import router as items_router

from app.db.models import Base
from app.db.session import engine

app = FastAPI()
app.include_router(items_router)

Base.metadata.create_all(bind=engine)