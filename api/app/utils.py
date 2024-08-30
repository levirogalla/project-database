
from datetime import date


def embed_text(text: str):
    return [1, 1, 1]


def get_project_by_id(project_id: int):
    ...


def get_project_by_name(project_name: str):
    ...


def query_projects(
    embeding: list[float],
    start: date,
    complete: date
):
    ...


def get_section_by_id(section_id: int):
    ...


def query_sections(
        embedding: list[int],
        project_id: int
):
    ...


def get_image_by_id(image_id: int):
    ...


def query_images(project_id: int, section_id: int):
    ...


def add_project(
    name: str,
    description: str,
    start: date,
    complete: date
):
    ...
