import os

os.environ["TESTING"] = "1"

import pytest
from database.orm import Base, create_tables, Session, engine, delete_tables
import pytest
from sqlalchemy import MetaData
from fastapi.testclient import TestClient

import datetime

from api.app.main import app


# Fixture to create a new database session for each test
# @pytest.fixture(scope="session", autouse=True)
# def set_env_vars():
    


@pytest.fixture(scope="module")
def client():
    """
    Fixture to provide a FastAPI test client with the database session.
    """
    create_tables()
    db_client = TestClient(app)
    yield db_client
    meta = MetaData()
    delete_tables()

@pytest.fixture(scope="module")
def base_experience(client):
    """A base experience added to the database to work with testing."""
    # Setup: Create the experience and return the ID
    res = client.post("/experience", json={
        "name": "test experience 1",
        "short_description": "dogs and cats eat food.",
        "start": datetime.date(2010, 1, 1).isoformat(),
        "html": "<div>this is a test div.</div>",
        "experience_type": "job"
    })
    return res