import logging
from typing import List, Optional

import pandas as pd

from ..settings import AppConfig
from .database import database_connect, embed_text

# configure logging
logger = logging.getLogger(__name__)


def search_embeddings(
    config: AppConfig, query_text: str, filter_text: Optional[str] = None, limit: int = 10
) -> Optional[pd.DataFrame]:
    # embed the query text
    query_vector = embed_text(config.models.embedding, query_text)
    if query_vector is None:
        return None

    # connect to the database and get the specified table
    db = database_connect(config.lancedb)
    tbl = db.open_table(config.lancedb.assessment_table)
    list_cols = ["assessment_uuid", "assessment_date", "client_name", "client_grade", "client_age"]

    # build and execute the query
    query = tbl.search(query_vector, query_type="vector")
    if filter_text is not None:
        query = query.where(filter_text, prefilter=True)
    df_result = query.limit(limit).select(list_cols).to_pandas()
    return df_result


def search_keywords(
    config: AppConfig, query_text: str, filter_text: Optional[str] = None, limit: int = 10
) -> Optional[pd.DataFrame]:
    # connect to the database and get the specified table
    db = database_connect(config.lancedb)
    tbl = db.open_table(config.lancedb.assessment_table)
    list_cols = ["assessment_uuid", "assessment_date", "client_name", "client_grade", "client_age"]

    # build and execute the query
    query = tbl.search(query_text, query_type="fts")
    if filter_text is not None:
        query = query.where(filter_text, prefilter=True)
    df_result = query.limit(limit).select(list_cols).to_pandas()
    return df_result


def search_sections(
    config: AppConfig, section: str, filter_uuids: Optional[List[str]] = None, limit: int = 10
) -> Optional[pd.DataFrame]:
    # connect to the database and get the specified table
    db = database_connect(config.lancedb)
    tbl = db.open_table(config.lancedb.section_table)
    list_cols = ["assessment_uuid", "section", "text"]

    # build the query - include filter if specified
    query_section = f"section = '{section}'"
    if filter_uuids is not None:
        limit = len(filter_uuids)
        item_uuids = ",".join("'{0}'".format(x) for x in filter_uuids)
        query_section = f"(section = '{section}') AND (assessment_uuid IN ({item_uuids}))"

    # execute the query
    query = tbl.search().where(query_section, prefilter=True)
    df_result = query.limit(limit).select(list_cols).to_pandas()
    return df_result
