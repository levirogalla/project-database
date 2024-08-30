from datetime import date
from logging import config
from bs4 import BeautifulSoup
from database.models import InformationSection, ORMProject, Image
from pyvindex import VectorIndex
import yaml
import os
from database.orm import Session

# Set up logging
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def get_file_content(filepath: str):
    with open(filepath, "r") as f:
        return f.read()


def parse_html(filepath: str, project: ORMProject, images_folder: str):
    sections = []
    images = []
    vindex = VectorIndex("sentence-transformers/all-mpnet-base-v2")

    with open(filepath, "rb") as f:
        soup = BeautifulSoup(f, "html.parser")

    paragraphs = soup.find_all('p')
    for p in paragraphs:
        info_sect = InformationSection(
            content=p.text,
            anchor=p.get("id"),
            embedding=vindex.embed_query(p.text),
            project=project
        )
        sections.append(info_sect)

    for img in soup.find_all("img"):
        src = img.get("src")
        filename = os.path.basename(src)
        filepath = os.path.join(images_folder, filename)
        with open(filepath, "rb") as f:
            image_data = f.read()

        image_entry = Image(
            filename=filename,
            image_data=image_data,
            project=project
        )
        images.append(image_entry)

    return sections, images


def main():
    # with open("project")
    vindex = VectorIndex("sentence-transformers/all-mpnet-base-v2")
    print(1)
    with open("projects/projects.yaml", "r") as f:
        config = yaml.safe_load(f)
    print(2)
    for project_config in config["projects"]:
        project = ORMProject(
            name=project_config["name"],
            short_description=project_config["short_description"],
            embedding=vindex.embed_query(project_config["short_description"]),
            started=date(2010, 11, 11),
            html=get_file_content(os.path.join(
                "projects", project_config["html_file"]))
        )
        sections, images = parse_html(
            os.path.join("projects", project_config["html_file"]), project, os.path.join("./projects", project_config["images_folder"]))

        print(3)
        session = Session()

        session.add(project)
        session.add_all(sections)
        session.add_all(images)

        session.commit()


if __name__ == "__main__":
    main()
