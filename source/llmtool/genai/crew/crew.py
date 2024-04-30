import logging
from typing import List

from crewai import Crew

from ...settings import AppConfig
from .crew_agents import ReportAgents
from .crew_state import ReportState
from .crew_tasks import ReportTasks

# configure logging
logger = logging.getLogger(__name__)

# define list of default section names
default_section_names = ["key-reasons", "summary-impact", "auditory-processing"]


class ReportCrew:
    def __init__(
        self, config: AppConfig, keywords: List[str], observations: List[str], sections: List[str]
    ):
        # create the report agents
        agents = ReportAgents()
        self.reasons_agent = agents.reasons_agent()
        self.section_agent = agents.section_agent()

        # initialize the report state objects
        self.state: ReportState = ReportState(
            config=config,
            client_keywords=keywords,
            client_observations=observations,
            client_sections=sections,
            client_uuids=[],
            section_context={},
            section_results={},
        )

    def kickoff(self) -> ReportState:
        tasks = ReportTasks(self.state)
        crew = Crew(
            agents=[self.reasons_agent, self.section_agent],
            tasks=[
                tasks.reasons_task(self.reasons_agent),
                tasks.section_task(self.section_agent),
            ],
            verbose=True,
        )
        result = crew.kickoff()
        logger.info("kickoff: [%s].", result)
        return self.state
