"""
Collection of ORM classes.

Common column fields:
	•	primary_key=True: Indicates a primary key.
	•	unique=True: Ensures all values in the column are unique.
	•	nullable=False: Ensures the column cannot be NULL.
	•	default: Sets a default value for the column.
"""

from sqlalchemy import (
    Column,
    Integer,
    Float,
    Numeric,
    String,
    Text,
    Date,
    Time,
    DateTime,
    Boolean,
    UUID,
    Enum,
    ARRAY,
    ForeignKey,
    null,
    LargeBinary
)
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from .orm import Base, create_tables, Session
