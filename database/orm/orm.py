
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://user:password@localhost/project-db"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session factory
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crea te a base class for models
Base = declarative_base()


def create_tables():
    """Create tables in database."""
    Base.metadata.create_all(bind=engine)
