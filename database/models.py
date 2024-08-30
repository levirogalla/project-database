
from datetime import date
from typing import Literal
from sqlalchemy import LargeBinary
from typing import Literal
from database.orm import (
    Base,
    Text,
    Integer,
    String,
    Vector,
    Date,
    ForeignKey,
    create_tables,
    relationship,
    Mapped,
    mapped_column,
    Enum
)


class Experience(Base):
    """experience Table Object."""
    __tablename__ = "experiences"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    experience_type: Mapped[Literal["project", "job"]] = mapped_column(
        Enum("project", "job", name="experience_type"), nullable=False
    )
    short_description: Mapped[str] = mapped_column(
        String(1000), nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector, nullable=False)
    started: Mapped[date] = mapped_column(Date, nullable=False)
    completed: Mapped[date] = mapped_column(Date, nullable=True)
    html: Mapped[str] = mapped_column(Text, nullable=True)
    css: Mapped[str] = mapped_column(Text, nullable=True)

    information_sections: "Mapped[list[InformationSection]]" = relationship(
        "InformationSection", back_populates="experience")
    images: "Mapped[list[Image]]" = relationship(
        "Image", back_populates="experience")

    def __init__(
        self,
        name: str,
        short_description: str,
        embedding: list,
        experience_type: Literal["project", "job"],
        started: date,
        completed: date = None,
        html: str = None,
        css: str = None,
        information_sections: "InformationSection" = [],
        images: "list[Image]" = [],
        uid: int = None
    ):
        super().__init__(
            id=uid,
            name=name,
            short_description=short_description,
            embedding=embedding,
            experience_type=experience_type,
            started=started,
            completed=completed,
            html=html,
            css=css,
            information_sections=information_sections,
            images=images
        )


class InformationSection(Base):
    """Important Sections."""

    __tablename__ = "sections"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    anchor: Mapped[str] = mapped_column(String(100), nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector, nullable=False)
    experience_id: Mapped[int] = mapped_column(Integer, ForeignKey(Experience.id))

    experience: Mapped[Experience] = relationship(
        "Experience", back_populates="information_sections")

    def __init__(
        self,
        content: str,
        anchor: str,
        embedding: list,
        experience: experience,
        uid: int = None
    ):
        super().__init__(
            id=uid,
            content=content,
            anchor=anchor,
            embedding=embedding,
            experience=experience
        )


class Image(Base):
    """Table for images."""

    __tablename__ = "images"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(100), nullable=False)
    image_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    experience_id: Mapped[int] = mapped_column(Integer, ForeignKey(Experience.id))

    experience: Mapped[Experience] = relationship(
        "Experience", back_populates="images")

    def __init__(
        self,
        filename: str,
        image_data: bytes,
        experience: experience,
        uid: str = None
    ):
        super().__init__(
            filename=filename,
            image_data=image_data,
            experience=experience,
            id=uid
        )


# Create the database tables
if __name__ == "__main__":
    create_tables()
