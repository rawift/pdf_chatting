import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from server2.config import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve PostgreSQL connection string from environment
PG_CONNECTION_STRING = os.getenv("PG_CONNECTION_STRING")

# If not found, raise an error
if PG_CONNECTION_STRING is None:
    raise ValueError("Database connection string is not set")

# Create the SQLAlchemy engine
engine = create_engine(PG_CONNECTION_STRING)

# Define the base class for models
Base = declarative_base()

# Create a session local factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
