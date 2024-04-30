from typing import Dict, List, TypedDict

from ..settings import AppConfig

# https://github.com/joaomdmoura/crewAI-examples/tree/main/landing_page_generator
# https://github.com/joaomdmoura/crewAI-examples/blob/main/CrewAI-LangGraph/src/state.py


class ReportState(TypedDict):
    config: AppConfig
    client_keywords: List[str]
    client_observations: List[str]
    client_sections: List[str]
    client_uuids: List[str]
    section_context: Dict[str, List[str]]
    section_results: Dict[str, str]
