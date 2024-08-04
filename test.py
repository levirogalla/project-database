from database.orm import Session
from database.models import InformationSection, Image, Project
from pyvindex import VectorIndex

session = Session()

vindex = VectorIndex("sentence-transformers/all-mpnet-base-v2")

# Retrieve users with a specific name
# sections = session.query(InformationSection).filter(
#     func.vector_cosine_similarity(InformationSection.embedding, vindex.embed_query("newtons method")) < 0.2).all()
vec = vindex.embed_query("uses tutorial to make neural networks")
# sections = session.query(InformationSection).filter(
#     InformationSection.embedding.cosine_distance(vec) < 0.9
# ).order_by(InformationSection.embedding.cosine_distance(vec)).all()
sections = session.query(InformationSection).order_by(
    InformationSection.embedding.cosine_distance(vec)).all()

for sec in sections:
    print(sec.content)

# results = session.query(Item).filter(
#     func.vector_cosine_similarity(Item.embedding, query_vector) < 0.1
# ).all()
