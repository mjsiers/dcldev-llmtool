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
    assessment_initials: Optional[str] = None
    assessment_reasons: Optional[str] = None
    assessment_keywords: Optional[str] = None
    client_name: Optional[str] = None
    client_dob: Optional[str] = None
    client_grade: Optional[int] = None
    client_age: Optional[float] = None
    vector: Vector(EMBEDDING_MODEL_LENGTH)  # type: ignore[valid-type]


class SectionSchema(LanceModel):
    assessment_uuid: str
    client_grade: Optional[int]
    client_age: Optional[float]
    section: str
    text: str
    vector: Vector(EMBEDDING_MODEL_LENGTH)  # type: ignore[valid-type]
