import logging
from typing import Dict

from crewai import Crew

from .crew_agents import ReportAgents
from .crew_state import ReportState
from .crew_tasks import ReportTasks

# configure logging
logger = logging.getLogger(__name__)


class ReportCrew:
    def __init__(self):
        agents = ReportAgents()
        self.reasons_agent = agents.reasons_agent()
        self.section_agent = agents.section_agent()

    def kickoff(self, state: ReportState) -> Dict:
        tasks = ReportTasks()
        crew = Crew(
            agents=[self.reasons_agent, self.section_agent],
            tasks=[
                tasks.reasons_task(self.reasons_agent, state["context"]),
                tasks.section_task(self.section_agent),
            ],
            verbose=True,
        )
        result = crew.kickoff()
        return {**state, "action_result": result}
