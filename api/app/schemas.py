from datetime import date
from pydantic import BaseModel


class ProjectFull(BaseModel):
    """Full project model with all fields."""
    id: int
    name: str
    short_description: str
    embedding: list[float]
    started: date
    completed: date | None
    images: dict[str, bytes]


class ProjectPartial(BaseModel):
    """Partial project model with important fields."""
    id: int
    name: str
    short_description: str
    started: date
    completed: date | None


class Section(BaseModel):
    """Section model."""
    id: int
    content: str
    anchor: str
    embedding: list[int]
    project: ProjectPartial


class Image(BaseModel):
    """Image model."""
    id: int
    filename: str
    image_data: bytes
    project: ProjectPartial
