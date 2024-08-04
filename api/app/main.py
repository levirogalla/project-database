from datetime import date
from fastapi import FastAPI
from .schemas import ProjectFull, ProjectPartial, Section, Image

app = FastAPI()


@app.get("/project/{project_id}", response_model=ProjectFull)
@app.get("/project/{project_name}", response_model=ProjectFull)
def get_project(
    project_id: int,
    project_name: str,
) -> ProjectFull:
    """
Gets project py id or name.
\n:param project_id: is the projects id.
:type project_id: int
\n:param project_name: is the name of the project.
:type project_name: str
    """


@app.get("/projects", response_model=list[ProjectFull])
def get_projects(
    embedding: list[float],
    start: date,
    complete: date | None
) -> list[ProjectFull]:
    """
Query projects by description embedding, start date, and/or completed date. \n
\n:param embedding: embedding vector for short_description.
:type embedding: list[float]
\n:param start: the start date of the project.
:type start: datetime.date
\n:param complete: the end date of the project.
:type complete: datetime.date
    """


@app.get("/section/{section_id}", response_model=Section)
def get_section(section_id: int) -> Section:
    """
Get section by id.
\n:param section_id: the section id.
:type section_id: int
    """


@app.get("/sections", response_model=list[Section])
def get_sections(
    embedding: list[int] | None,
    project_id: int | None
):
    """
Query sections by content embedding or by project id.
\n:param embedding: the text embedding for the section content.
:type embedding: list[int]
\n:param project_id: the project id the section belongs to.
:type project_id: int
    """


def add_project():

    # makes project
    # makes images
    # makes sections

    # handels embedding stuff
    ...


def update_project():
    # takes id, can change project name
    # updates project
    # updates images
    # updates sections
    ...


def delete_project():
    # deletes all project data
    ...


######################### for later #########################

# make resume function
# resume template getter and setters
# etc
