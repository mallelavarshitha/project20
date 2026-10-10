import os
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DB_URL = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('DB_HOST', 'db')}:5432/{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class ItemIn(BaseModel):
    name: str


app = FastAPI()


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(engine)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/items")
def list_items():
    with SessionLocal() as db:
        return [{"id": i.id, "name": i.name} for i in db.query(Item).all()]


@app.post("/api/items")
def add_item(item: ItemIn):
    with SessionLocal() as db:
        row = Item(name=item.name)
        db.add(row)
        db.commit()
        return {"id": row.id, "name": row.name}