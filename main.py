from typing import Union
from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str

DB_DRIVER = os.getenv("DB_DRIVER", default="postgresql")
DB_USER = os.getenv("DB_USER", default="postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", default="postgres")
DB_HOST = os.getenv("DB_HOST", default="postgres-fastapi")
DB_PORT = os.getenv("DB_PORT", default="5432")
DB_NAME = os.getenv("DB_NAME", default="postgres")


connection_string = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(connection_string)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/heroes/")
def create_hero(hero: Hero) -> Hero:
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero

@app.get("/heroes/")
def get_all_hero():
    with Session(engine) as session:
        stmt = select(Hero)
        return session.exec(stmt).all()