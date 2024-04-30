import logging
from typing import List, Optional

from langchain.tools import tool

from ....data.query import search_embeddings, search_sections
from ....settings import AppConfig

# configure logging
logger = logging.getLogger(__name__)


class QueryTools:
    def __init__(self, config: AppConfig):
        self.config = config

    @tool("Fetch documents from database")
    def get_documents(self, query: str, limit: int = 10) -> List[str]:
        results: List[str] = []
        df = search_embeddings(self.config, query, filter_text=None, limit=limit)
        if df is None:
            logger.info("get_documents: No results found.")
            return results

        logger.info("get_documents: Embeddings search results [%s].", df.shape)
        results = df["assessment_uuid"].tolist()
        return results

    @tool("Fetch document sections from database")
    def get_sections(
        self, section: str, filter_uuids: Optional[List[str]] = None, limit: int = 10
    ) -> List[str]:
        results: List[str] = []
        df = search_sections(self.config, section, filter_uuids=filter_uuids, limit=limit)
        if df is None:
            logger.info("get_sections: No results found.")
            return results

        logger.info("get_sections: Search results [%s].", df.shape)
        results = df["text"].tolist()
        return results
