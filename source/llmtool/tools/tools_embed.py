import logging
import os
from typing import Any, Dict, List, Optional

import lancedb
import numpy as np
import ollama
import pyarrow as pa

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


def embed_text(input_text: str) -> Optional[Any]:
    result = ollama.embeddings(model=ollama_model_embed, prompt=input_text)
    if (result is None) or ("embedding" not in result):
        logger.error("embed_text: Embedding model [%s] failed.", ollama_model_embed)
        return None

    return result["embedding"]


def database_embed_sections(
    db: lancedb.DBConnection, doc_data: DocumentSchema, doc_sections: Dict
) -> None:
    # increase the log level for the httpx library to reduce output messages
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # create the document type
    tbl_assessment = db.open_table(lancedb_assessment_table)
    tbl_assessment.add([doc_data])

    # create the sections for this documment
    list_sections: List[Dict] = []
    for k, v in doc_sections.items():
        # ensure we have at least one text string
        if len(v) == 0:
            logger.debug(
                "database_embed_sections: [%s] section [%s] is empty.",
                doc_data.assessment_file,
                k,
            )
            continue

        # join all the section text strings and compute the vector embedding value for this section text
        section_text = "\n".join(v)
        # result = ollama.embeddings(model=ollama_model_embed, prompt=section_text)
        vector = embed_text(section_text)
        if vector is None:
            logger.error(
                "database_embed_sections: Embedding of [%s] section [%s] failed.",
                doc_data.assessment_file,
                k,
            )
            continue

        # initialize the section data using the pydantic mode
        # save the model into the local list as a dictionary
        logger.debug(
            "database_embed_sections: [%s] section [%s] has %s text strings.",
            doc_data.assessment_file,
            k,
            len(v),
        )
        section_data = SectionSchema(
            assessment_uuid=doc_data.assessment_uuid,
            client_age=doc_data.client_age,
            client_grade=doc_data.client_grade,
            section=k,
            text=section_text,
            vector=vector,
        )
        list_sections.append(section_data.model_dump())

    # saving the pydantic model directly into lancedb does not work
    # so converting the section data into a pyarrow table first
    schema = SectionSchema.to_arrow_schema()
    pa_table = pa.Table.from_pylist(list_sections, schema=schema)

    # add all the section data to the database
    tbl_section = db.open_table(lancedb_section_table)
    tbl_section.add(pa_table)
    logger.debug(
        "database_embed_sections: [%s] has %s section embeddings.",
        doc_data.assessment_file,
        len(list_sections),
    )
