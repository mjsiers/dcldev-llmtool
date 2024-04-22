import logging
import os
from typing import Any, Optional

import lancedb
import ollama

from ..data.models import DocumentSchema, SectionSchema
from ..settings import (
    lancedb_assessment_table,
    lancedb_database_name,
    lancedb_database_path,
    lancedb_section_table,
    ollama_model_embed,
)

# configure logging
logger = logging.getLogger(__name__)


def database_connect() -> lancedb.DBConnection:
    vector_store = os.path.join(lancedb_database_path, lancedb_database_name)
    db = lancedb.connect(vector_store)
    return db


def database_drop_tables(db: lancedb.DBConnection) -> None:
    list_tables = db.table_names()
    if lancedb_assessment_table in list_tables:
        db.drop_table(lancedb_assessment_table)
    if lancedb_section_table in list_tables:
        db.drop_table(lancedb_section_table)


def database_create_tables(db: lancedb.DBConnection) -> None:
    list_tables = db.table_names()
    if lancedb_assessment_table not in list_tables:
        db.create_table(lancedb_assessment_table, schema=DocumentSchema)
    if lancedb_section_table not in list_tables:
        db.create_table(lancedb_section_table, schema=SectionSchema)


def database_create_fts(db: lancedb.DBConnection) -> None:
    tbl_assessment = db.open_table(lancedb_assessment_table)
    tbl_assessment.create_fts_index("assessment_keywords")


def embed_text(input_text: str) -> Optional[Any]:
    result = ollama.embeddings(model=ollama_model_embed, prompt=input_text)
    if (result is None) or ("embedding" not in result):
        logger.error("embed_text: Embedding model [%s] failed.", ollama_model_embed)
        return None

    return result["embedding"]
