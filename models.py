
from sqlalchemy import LargeBinary
from database.orm import (
    Base,
    Column,
    Text,
    Integer,
    String,
    Vector,
    Date,
    ForeignKey,
    create_tables,
    relationship
)


class Project(Base):
    """Project Table Object."""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    short_description = Column(String(1000), nullable=False)
    embedding = Column(Vector, nullable=False)
    started = Column(Date, nullable=False)
    completed = Column(Date, nullable=True)
    html = Column(Text, nullable=True)
    css = Column(Text, nullable=True)

    information_sections = relationship(
        "InformationSection", back_populates="project")
    images = relationship(
        "Image", back_populates="project")

    def __init__(
        self,
        name: str,
        short_description: str,
        embedding: list,
        started: Date,
        completed: Date = None,
        html: str = None,
        css: str = None,
        information_sections: "InformationSection" = [],
        images: "Image" = [],
        uid: int = None
    ):
        super().__init__(
            id=uid,
            name=name,
            short_description=short_description,
            embedding=embedding,
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

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    anchor = Column(String(100), nullable=False)
    embedding = Column(Vector, nullable=False)
    project_id = Column(Integer, ForeignKey(Project.id))

    project = relationship("Project", back_populates="information_sections")

    def __init__(
        self,
        content: str,
        anchor: str,
        embedding: list,
        project: Project,
        uid: int = None
    ):
        super().__init__(
            id=uid,
            content=content,
            anchor=anchor,
            embedding=embedding,
            project=project
        )


class Image(Base):
    """Table for images."""

    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(100), nullable=False)
    image_data = Column(LargeBinary, nullable=False)
    project_id = Column(Integer, ForeignKey(Project.id))

    project = relationship("Project", back_populates="images")

    def __init__(
        self,
        filename: str,
        image_data: bytes,
        project: Project,
        uid: str = None
    ):
        super().__init__(
            filename=filename,
            image_data=image_data,
            project=project,
            id=uid
        )


# Create the database tables
if __name__ == "__main__":
    create_tables()
