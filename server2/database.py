import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from server2.config import load_dotenv


load_dotenv()


PG_CONNECTION_STRING = os.getenv("PG_CONNECTION_STRING")


if PG_CONNECTION_STRING is None:
    raise ValueError("Database connection string is not set")


engine = create_engine(PG_CONNECTION_STRING)

Base = declarative_base()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
