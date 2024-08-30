from datetime import date
from typing import Literal
from pydantic import BaseModel


class ExperienceData(BaseModel):
    """Full experience model with all fields."""
    id: int
    name: str
    short_description: str
    embedding: list[float]
    experience_type: Literal["project", "job"]
    start: date
    complete: date | None
    html: str
    css: str
    images: "list[ImageMetadata]"


class ExperienceMetadata(BaseModel):
    """Partial experience model with important fields."""
    id: int
    name: str
    short_description: str
    experience_type: Literal["project", "job"]
    start: date
    complete: date | None


class InformationSectionData(BaseModel):
    """Section model."""
    id: int
    content: str
    anchor: str
    embedding: list[float]
    experience: ExperienceMetadata


class InformationSectionMetadata(BaseModel):
    """Section model."""
    id: int
    anchor: str
    experience_id: int


class ImageMetadata(BaseModel):
    """Image model."""
    id: int
    filename: str
    experience_id: int


class ImageData(BaseModel):
    """Image model."""
    image_data: bytes
