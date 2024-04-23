import logging
from typing import Optional

import pandas as pd

from ..settings import lancedb_assessment_table
from .database import database_connect, embed_text

# configure logging
logger = logging.getLogger(__name__)


def search_embeddings(
    query_text: str, filter_text: Optional[str] = None, limit: int = 10
) -> Optional[pd.DataFrame]:
    # embed the query text
    query_vector = embed_text(query_text)
    if query_vector is None:
        return None

    # connect to the database and get the specified table
    db = database_connect()
    tbl = db.open_table(lancedb_assessment_table)
    list_cols = ["assessment_uuid", "assessment_date", "client_name", "client_grade", "client_age"]

    # build and execute the query
    query = tbl.search(query_vector, query_type="vector")
    if filter_text is not None:
        query = query.where(filter_text, prefilter=True)
    df_result = query.limit(limit).select(list_cols).to_pandas()
    return df_result


def search_keywords(
    query_text: str, filter_text: Optional[str] = None, limit: int = 10
) -> Optional[pd.DataFrame]:
    # connect to the database and get the specified table
    db = database_connect()
    tbl = db.open_table(lancedb_assessment_table)
    list_cols = ["assessment_uuid", "assessment_date", "client_name", "client_grade", "client_age"]

    # build and execute the query
    query = tbl.search(query_text, query_type="fts")
    if filter_text is not None:
        query = query.where(filter_text, prefilter=True)
    df_result = query.limit(limit).select(list_cols).to_pandas()
    return df_result
