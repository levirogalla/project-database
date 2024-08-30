from datetime import date
import math
import os
import numpy as np
from sqlalchemy import desc
os.environ["TESTING"] = "0"


from api.app.request_models import PostExperience
from database.orm import Session, create_tables, delete_tables
from database.models import InformationSection, Image, Experience as ORMExperience
from pyvindex import VectorIndex
from api.app.main import add_experience

def cosine_dist(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dist = 1 - (np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
    return dist

session = Session()

# print(session.bind.engine)

delete_tables()
create_tables()
add_experience(PostExperience(
    name="test experience 1",
    short_description="animals live in the jungle and hunt",
    experience_type="job",
    start=date.today()
))
add_experience(PostExperience(
    name="test experience 2",
    short_description="computers use transitors to process info",
    experience_type="job",
    start=date.today()
))


vindex = VectorIndex("sentence-transformers/all-mpnet-base-v2")

# Retrieve users with a specific name
# sections = session.query(InformationSection).filter( 
#     func.vector_cosine_similarity(InformationSection.embedding, vindex.embed_query("newtons method")) < 0.2).all()
vec = vindex.embed_query("computer engineering")
# sections = session.query(InformationSection).filter(
#     InformationSection.embedding.cosine_distance(vec) < 0.9
# ).order_by(InformationSection.embedding.cosine_distance(vec)).all()

similarity_column = 1 - ORMExperience.embedding.cosine_distance(vec)
l2_column = ORMExperience.embedding.l2_distance(vec)

# Query to get both the section and the similarity
sections = session.query(
    ORMExperience,
    similarity_column.label("similarity"),
    l2_column.label("l2")
).order_by(
    desc(similarity_column)
).all()

# Printing section names and their corresponding similarity
for sec, similarity, l2 in sections:
    print(f"Name: {sec.name}, Similarity: {math.acos(similarity)*(360/(2*math.pi))}, l2: {1/l2}")
  

# results = session.query(Item).filter(
#     func.vector_cosine_similarity(Item.embedding, query_vector) < 0.1
# ).all()
