from typing import Optional

from lancedb.pydantic import LanceModel, Vector

# define which embedding model we are using
EMBEDDING_MODEL: str = "nomic-embed-text"
EMBEDDING_MODEL_LENGTH: int = 768


class DocumentSchema(LanceModel):
    assessment_uuid: str
    assessment_file: str
    assessment_date: Optional[str] = None
    assessment_author: Optional[str] = None
    client_grade: Optional[str] = None
    client_age: Optional[str] = None


class SectionSchema(LanceModel):
    assessment_uuid: str
    # assessment_author: Optional[str]
    section: str
    text: str
    vector: Vector(EMBEDDING_MODEL_LENGTH)
