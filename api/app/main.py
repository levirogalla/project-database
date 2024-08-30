# from ast import Bytes
from datetime import date
from fastapi import FastAPI, HTTPException
from sqlalchemy import desc, literal
from .utils import embed_text
# from torch import embedding
from database.models import (
    Experience as ORMExperience,
    InformationSection as ORMInformationSection,
    Image as ORMImage
)
from database.orm import Session
from .response_models import ImageMetadata, ExperienceData, ExperienceMetadata, InformationSectionData, ImageData
from .request_models import PostExperience, PutExperience
from sqlalchemy.orm import joinedload
import sentence_transformers

DEFAULT_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
DEVICE = "cpu"
app = FastAPI()
model = sentence_transformers.SentenceTransformer(
            DEFAULT_MODEL_NAME, device=DEVICE, cache_folder="__embedding_model_cache__")


# TODO: at some point rename to experience instead of experience,
# so can have positions, experiences, and any other experience type.

# TODO: the end points that take embeddings as query parameters should actually take text and
# then embedd it on the back end. They should also take a closeness parameter.

# TODO: update query params to take greater than and smaller than signs

@app.get("/experience/{experience_id}", response_model=ExperienceData)
def get_experience_by_id(experience_id: int) -> ExperienceData:
    """
Gets experience py id or name.
\n:param experience_id: is the experiences id.
:type experience_id: int
\n:param experience_name: is the name of the experience.
:type experience_name: str
    """
    with Session() as session:
        experiences = session.query(ORMExperience).filter(
            ORMExperience.id == experience_id).options(joinedload(ORMExperience.images)).order_by(ORMExperience.started).all()

        experience = experiences[0]
        response = ExperienceData(
            id=experience.id,
            name=experience.name,
            short_description=experience.short_description,
            embedding=experience.embedding,
            experience_type=experience.experience_type,
            start=experience.started,
            complete=experience.completed,
            html=experience.html or "",
            css=experience.css or "",
            images=[
                ImageMetadata(
                    id=image.id,
                    filename=image.filename,
                    experience_id=experience.id
                ) for image in experience.images
            ]
        )

    return response

# UPDATED THE RETURN TYPE HERE MAKE SURE TO FIX THIS IN THE TESTS!!!!
@app.get("/experiences", response_model=list[tuple[ExperienceMetadata, float|None]])
def query_experiences(
    name: str | None = None,
    description: str | None = None,
    started_after: date | None = None,
    complete_before: date | None = None,
    limit: int = 10,
    similarity_cutoff: float = 0
) -> list[tuple[ExperienceMetadata, float|None]]:
    """
    Query experiences by description embedding, start date, and/or completed date.

    :param description: similarity search for short_description.
    :type description: list[float]
    :param start: the start date of the experience.
    :type start: datetime.date
    :param complete: the end date of the experience.
    :type complete: datetime.date
    """


    with Session() as session:
        if description:
            embedding = model.encode(description).tolist()
            similarity_column = 1 - ORMExperience.embedding.cosine_distance(embedding)
        else:
            similarity_column = literal(None)

        query = session.query(
            ORMExperience,
            similarity_column.label("similarity"),
        )

        if name:
            query = query.filter(ORMExperience.name == name)
        if description:
            query = query.filter(
                similarity_column > similarity_cutoff).order_by(desc(similarity_column))
        if started_after:
            query = query.filter(ORMExperience.started >= started_after).order_by(ORMExperience.started)
        if complete_before:
            query = query.filter(ORMExperience.completed <= complete_before).order_by(ORMExperience.completed)

        experiences = query.limit(limit).all()

        result = []
        for experience, similarity in experiences:
            experience_metadata = ExperienceMetadata(
                id=experience.id,
                name=experience.name,
                short_description=experience.short_description,
                experience_type=experience.experience_type,
                embedding=experience.embedding,
                start=experience.started,
                complete=experience.completed,
            )
            result.append((experience_metadata, similarity))

        return result


@app.get("/section/{section_id}", response_model=InformationSectionData)
def get_section(section_id: int) -> InformationSectionData:
    """
    Get section by id.

    :param section_id: the section id.
    :type section_id: int
    """
    with Session() as session:
        section = session.query(ORMInformationSection).filter(
            ORMInformationSection.id == section_id).first()

        if not section:
            raise HTTPException(status_code=404, detail="Section not found")

        section_metadata = InformationSectionData(
            id=section.id,
            content=section.content,
            anchor=section.anchor,
            embedding=section.embedding,
            experience=ExperienceMetadata(
                id=section.experience.id,
                name=section.experience.name,
                short_description=section.experience.short_description,
                start=section.experience.started,
                complete=section.experience.completed
            ),
            images=[
                ImageMetadata(
                    id=image.id,
                    filename=image.filename,
                    experience_id=image.experience_id
                ) for image in section.experience.images
            ]
        )

        return section_metadata


@app.get("/sections", response_model=list[InformationSectionData])
def get_sections(
    experience_id: int | None = None,
    text: str | None = None,
):
    """
    Query sections by content embedding or by experience id.

    :param text: the text similarity for the section content.
    :type text: str
    :param experience_id: the experience id the section belongs to.
    :type experience_id: int
    """

    with Session() as session:
        query = session.query(ORMInformationSection).options(joinedload(
            ORMInformationSection.experience))

        if text:
            embedding = object(text)
            query = query.filter(ORMInformationSection.embedding == embedding)
        if experience_id:
            query = query.filter(
                ORMInformationSection.experience_id == experience_id)

        sections = query.all()

        if not sections:
            raise HTTPException(status_code=404, detail="No sections found")

        result = []
        for section in sections:
            section_metadata = InformationSectionData(
                id=section.id,
                content=section.content,
                anchor=section.anchor,
                embedding=section.embedding,
                experience=ExperienceMetadata(
                    id=section.experience.id,
                    name=section.experience.name,
                    short_description=section.experience.short_description,
                    start=section.experience.started,
                    complete=section.experience.completed
                )
            )
            result.append(section_metadata)

    return result


@app.get("/image/{image_id}", response_model=ImageData)
def get_image(image_id: int):
    """
    Get image by id.

    :param image_id: the image id.
    :type image_id: int
    """
    with Session() as session:
        image = session.query(ORMImage).filter(ORMImage.id == image_id).first()

        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        image_data = ImageData(
            image_data=image.image_data
        )

        return image_data


@app.post("/experience", response_model=ExperienceData)
def add_experience(
    experience_data: PostExperience
):
    """
    Adds a new experience.

    :param name: the name of the experience.
    :type name: str
    :param short_description: the short description of the experience.
    :type short_description: str
    :param start: the start date of the experience.
    :type start: datetime.date
    :param complete: the end date of the experience.
    :type complete: datetime.date
    :param html: the HTML content for the experience.
    :type html: str
    :param css: the CSS content for the experience.
    :type css: str
    """
    embedding = model.encode(experience_data.short_description).tolist()
    with Session() as session:
        new_experience = ORMExperience(
            name=experience_data.name,
            short_description=experience_data.short_description,
            experience_type=experience_data.experience_type,
            started=experience_data.start,
            embedding=embedding,
            completed=experience_data.complete,
            html=experience_data.html,
            css=experience_data.css
        )

        session.add(new_experience)
        session.commit()
        session.refresh(new_experience)

        experience_data = ExperienceData(
            id=new_experience.id,
            name=new_experience.name,
            experience_type=new_experience.experience_type,
            short_description=new_experience.short_description,
            embedding=new_experience.embedding,
            start=new_experience.started,
            complete=new_experience.completed,
            html=new_experience.html or "",
            css=new_experience.css or "",
            images=new_experience.images
        )
        return experience_data


@app.put("/experience/{experience_id}", response_model=ExperienceData)
def update_experience(
    experience_id: int,
    experience_data: PutExperience
):
    """
    Updates a experience.

    :param experience_id: the id of the experience to update.
    :type experience_id: int
    :param name: the new name of the experience.
    :type name: str
    :param short_description: the new short description of the experience.
    :type short_description: str
    :param start: the new start date of the experience.
    :type start: datetime.date
    :param complete: the new end date of the experience.
    :type complete: datetime.date
    :param html: the new HTML content of the experience.
    :type html: str
    :param css: the new CSS content of the experience.
    :type css: str
    """
    with Session() as session:
        experience = session.query(ORMExperience).filter(
            ORMExperience.id == experience_id).first()

        if not experience:
            raise HTTPException(status_code=404, detail="experience not found")

        if experience_data.name is not None:
            experience.name = experience_data.name
        if experience_data.short_description is not None:
            experience.short_description = experience_data.short_description
        if experience_data.start is not None:
            experience.started = experience_data.start
        if experience_data.complete is not None:
            experience.completed = experience_data.complete
        if experience_data.html is not None:
            experience.html = experience_data.html
        if experience_data.css is not None:
            experience.css = experience_data.css
        if experience_data.experience_type is not None:
            experience.experience_type = experience_data.experience_type

        session.commit()
        session.refresh(experience)

        experience_data = ExperienceData(
            id=experience.id,
            name=experience.name,
            short_description=experience.short_description,
            experience_type=experience.experience_type,
            embedding=experience.embedding,
            start=experience.started,
            complete=experience.completed,
            html=experience.html or "",
            css=experience.css or "",
            images=[
                ImageMetadata(
                    id=image.id,
                    filename=image.filename,
                    experience_id=image.experience_id
                ) for image in experience.images
            ]
        )

        return experience_data


@app.delete("/experience/{experience_id}")
def delete_experience(experience_id: int):
    """
    Deletes a experience.

    :param experience_id: the id of the experience to delete.
    :type experience_id: int
    """
    with Session() as session:
        experience = session.query(ORMExperience).filter(
            ORMExperience.id == experience_id).first()

        if not experience:
            raise HTTPException(status_code=404, detail="experience not found")

        session.delete(experience)
        session.commit()

    return {"message": "experience deleted successfully"}


@app.post("/experience/{experience_id}/section", response_model=InformationSectionData)
def add_section(
    experience_id: int,
    content: str,
    anchor: str,
):
    """
    Adds a new section to the experience.

    :param content: the content of the section.
    :type content: str
    :param anchor: the anchor of the section.
    :type anchor: str
    :param experience_id: the id of the experience to which the section belongs.
    :type experience_id: int
    """
    embedding = []
    with Session() as session:
        experience = session.query(ORMExperience).filter(
            ORMExperience.id == experience_id).first()

        if not experience:
            raise HTTPException(status_code=404, detail="experience not found")

        new_section = ORMInformationSection(
            content=content,
            anchor=anchor,
            embedding=embedding,
            experience=experience
        )

        session.add(new_section)
        session.commit()
        session.refresh(new_section)

        section_data = InformationSectionData(
            id=new_section.id,
            content=new_section.content,
            anchor=new_section.anchor,
            embedding=new_section.embedding,
            experience=ExperienceMetadata(
                id=experience.id,
                name=experience.name,
                short_description=experience.short_description,
                start=experience.started,
                complete=experience.completed
            ),
            images=[
                ImageMetadata(
                    id=image.id,
                    filename=image.filename,
                    experience_id=image.experience_id
                ) for image in experience.images
            ]
        )

        return section_data


@app.put("/section/{section_id}", response_model=InformationSectionData)
def update_section(
    section_id: int,
    name: str | None = None,
    description: str | None = None,
    start: date | None = None,
    complete: date | None = None,
):
    """
Updates a section.
:param section_id: the id of the section to update.
:type section_id: int
\n:param name: the new name of the section.
:type name: str
\n:param description: the new description of the section.
:type description: str
\n:param start: the new start date of the section.
:type start: datetime.date
\n:param complete: the new end date of the section.
:type complete: datetime.date
    """


@app.delete("/section/{section_id}")
def delete_section(section_id: int):
    """
Deletes a section.
:param section_id: the id of the section to delete.
:type section_id: int
    """

# def upload_image(experience_id)


######################### for later #########################

# make resume function
# resume template getter and setters
# etc
