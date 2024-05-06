import logging
import os
from typing import Any, Optional

import lancedb
import ollama

from ..data.models import DocumentSchema, SectionSchema
from ..settings import LanceDbConfig

# configure logging
logger = logging.getLogger(__name__)


def database_connect(config: LanceDbConfig) -> lancedb.DBConnection:
    vector_store = os.path.join(config.database_path, config.database_name)
    db = lancedb.connect(vector_store)
    return db


def database_drop_tables(config: LanceDbConfig, db: lancedb.DBConnection) -> None:
    list_tables = db.table_names()
    if config.assessment_table in list_tables:
        db.drop_table(config.assessment_table)
    if config.section_table in list_tables:
        db.drop_table(config.section_table)


def database_create_tables(config: LanceDbConfig, db: lancedb.DBConnection) -> None:
    list_tables = db.table_names()
    if config.assessment_table not in list_tables:
        db.create_table(config.assessment_table, schema=DocumentSchema)
    if config.section_table not in list_tables:
        db.create_table(config.section_table, schema=SectionSchema)


def database_create_fts(config: LanceDbConfig, db: lancedb.DBConnection) -> None:
    tbl_assessment = db.open_table(config.assessment_table)
    tbl_assessment.create_fts_index("assessment_keywords")


def embed_text(embed_model: str, input_text: str) -> Optional[Any]:
    result = ollama.embeddings(model=embed_model, prompt=input_text)
    if (result is None) or ("embedding" not in result):
        logger.error("embed_text: Embedding model [%s] failed.", embed_model)
        return None

    return result["embedding"]
