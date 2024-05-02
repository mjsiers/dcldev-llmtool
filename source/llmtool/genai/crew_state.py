import dataclasses
from typing import Dict, List

from ..settings import AppConfig

# https://github.com/joaomdmoura/crewAI-examples/tree/main/landing_page_generator
# https://github.com/joaomdmoura/crewAI-examples/blob/main/CrewAI-LangGraph/src/state.py


# define list of default section names
default_section_names = ["key-reasons", "summary-impact", "auditory-processing"]


@dataclasses.dataclass
class ReportClient:
    name: str
    keywords: List[str]
    facts: List[str]
    observations: List[str]
    sections: List[str] = default_section_names


@dataclasses.dataclass
class ReportState:
    config: AppConfig
    client: ReportClient
    client_uuids: List[str]
    section_context: Dict[str, List[str]]
    section_results: Dict[str, str]
