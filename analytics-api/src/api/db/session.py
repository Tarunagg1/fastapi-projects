import sqlmodel
from sqlmodel import Session, SQLModel
import timescaledb
from .config import DATABASE_URL

if DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL is not set in the configuration.")

engin = sqlmodel.create_engine(DATABASE_URL, echo=True)

def init_db():
    print("Initializing database...")
    SQLModel.metadata.create_all(engin)


def get_session():
    with Session(engin) as session:
        yield session