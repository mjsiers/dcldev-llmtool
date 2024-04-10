import logging
import os
import uuid
from typing import Dict, List

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


def database_embed_sections(db: lancedb.DBConnection, doc_name: str, doc_sections: Dict) -> None:
    # increase the log level for the httpx library to reduce output messages
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # generate a new unique identifier for this document
    doc_uuid = str(uuid.uuid4())

    # create the document type
    tbl_assessment = db.open_table(lancedb_assessment_table)
    doc_data = DocumentSchema(assessment_uuid=doc_uuid, assessment_file=doc_name)
    tbl_assessment.add([doc_data])

    # create the sections for this documment
    list_sections: List[Dict] = []
    for k, v in doc_sections.items():
        # ensure we have at least one text string
        if len(v) == 0:
            logger.warning(
                "database_embed_sections: [%s] section [%s] is empty.",
                doc_name,
                k,
            )
            continue

        # join all the section text strings and compute the vector embedding value for this section text
        section_text = "\n".join(v)
        result = ollama.embeddings(model=ollama_model_embed, prompt=section_text)

        # initialize the section data using the pydantic mode
        # save the model into the local list as a dictionary
        logger.debug(
            "database_embed_sections: [%s] section [%s] has %s text strings.", doc_name, k, len(v)
        )
        section_data = SectionSchema(
            assessment_uuid=doc_uuid,
            client_age=None,
            client_grade=None,
            section=k,
            text=section_text,
            vector=result["embedding"],
        )
        list_sections.append(section_data.model_dump())

    # saving the pydantic model directly into lancedb does not work
    # so converting the section data into a pyarrow table first
    schema = SectionSchema.to_arrow_schema()
    pa_table = pa.Table.from_pylist(list_sections, schema=schema)

    # add all the section data to the database
    tbl_section = db.open_table(lancedb_section_table)
    tbl_section.add(pa_table)
    logger.info(
        "database_embed_sections: [%s] has %s section embeddings.", doc_name, len(list_sections)
    )
