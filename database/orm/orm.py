
import os
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, MetaData

DATABASE_URL = "postgresql://user:password@localhost/project-db"
TEST_DATABASE_URL = "postgresql://user:password@localhost/test-db"

# use testing db by defualt
print(os.environ.get("TESTING"))
engine = create_engine(DATABASE_URL if os.environ.get(
    "TESTING", "1") != "1" else TEST_DATABASE_URL)

# Create a session factory
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Crea te a base class for models
Base = declarative_base()


def create_tables(bind=engine):
    """Create tables in database."""
    Base.metadata.create_all(bind=bind)


def delete_tables(bind=engine):
    """Delete all tables in database."""
    meta = MetaData()
    meta.reflect(bind=bind)
    meta.drop_all(bind=bind)