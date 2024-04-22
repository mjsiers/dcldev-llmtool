import logging
import os
from typing import Any, Optional

import lancedb
import ollama
import pandas as pd

from ..data.models import DocumentSchema, SectionSchema
from ..settings import (
    lancedb_assessment_table,
    lancedb_database_name,
    lancedb_database_path,
    ollama_model_embed,
)

# configure logging
logger = logging.getLogger(__name__)


# configure logging
logger = logging.getLogger(__name__)


def embed_text(input_text: str) -> Optional[Any]:
    result = ollama.embeddings(model=ollama_model_embed, prompt=input_text)
    if (result is None) or ("embedding" not in result):
        logger.error("embed_text: Embedding model [%s] failed.", ollama_model_embed)
        return None

    return result["embedding"]


def database_connect() -> lancedb.DBConnection:
    vector_store = os.path.join(lancedb_database_path, lancedb_database_name)
    db = lancedb.connect(vector_store)
    return db


def search_embeddings(query: str) -> Optional[pd.DataFrame]:
    # embed the query text
    query_vector = embed_text(query)
    if query_vector is None:
        return None

    # connect to the database and get the specified table
    db = database_connect()
    tbl = db.open_table(lancedb_assessment_table)
    df_result = tbl.search(query_vector).limit(10).to_df()
    df_result.drop(
        columns=[
            "assessment_file",
            "assessment_author",
            "assessment_initials",
            "assessment_reasons",
            "assessment_keywords",
            # "client_name",
            "client_dob",
            "vector",
        ],
        inplace=True,
    )
    return df_result
