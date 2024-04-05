from lancedb.pydantic import LanceModel, Vector

# define which embedding model we are using
EMBEDDING_MODEL: str = "nomic-embed-text"
EMBEDDING_MODEL_LENGTH: int = 768


class DocumentSchema(LanceModel):
    assessment_uuid: str
    assessment_file: str
    assessment_date: str
    assessment_author: str
    client_grade: str
    client_age: str


class SectionSchema(LanceModel):
    assessment_uuid: str
    assessment_author: str
    section: str
    text: str
    vector: Vector(EMBEDDING_MODEL_LENGTH)
