from datetime import date
from typing import Literal
from pydantic import BaseModel


class PostExperience(BaseModel):
    name: str
    short_description: str
    experience_type: Literal["project", "job"]
    start: date
    complete: date | None = None
    html: str | None = None
    css: str | None = None


class PutExperience(BaseModel):
    name: str | None = None
    short_description: str | None = None
    experience_type: Literal["project", "job"] | None = None
    start: date | None = None
    complete: date | None = None
    html: str | None = None
    css: str | None = None
