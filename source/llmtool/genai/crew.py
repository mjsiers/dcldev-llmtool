import logging

from crewai import Crew

from ..settings import AppConfig
from .crew_agents import ReportAgents
from .crew_state import ReportClient, ReportState
from .crew_tasks import ReportTasks

# configure logging
logger = logging.getLogger(__name__)


class ReportCrew:
    def __init__(self, config: AppConfig, client: ReportClient):
        # create the report agents
        agents = ReportAgents(config)
        self.reasons_agent = agents.reasons_agent()
        self.section_agent = agents.section_agent()

        # initialize the report state objects
        self.state: ReportState = ReportState(
            config=config,
            client=client,
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
