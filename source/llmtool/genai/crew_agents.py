import logging
from textwrap import dedent

from crewai import Agent

from ..settings import AppConfig

# configure logging
logger = logging.getLogger(__name__)


class ReportAgents:
    def __init__(self, config: AppConfig):
        self.config = config

    def reasons_agent(self) -> Agent:
        agent = Agent(
            role="Senior Email Analyst",
            goal="Filter out non-essential emails like newsletters and promotional content",
            backstory=dedent(
                """\
				As a Senior Email Analyst, you have extensive experience in email content analysis.
				You are adept at distinguishing important emails from spam, newsletters, and other
				irrelevant content. Your expertise lies in identifying key patterns and markers that
				signify the importance of an email."""
            ),
            verbose=True,
            allow_delegation=False,
        )
        return agent

    def section_agent(self) -> Agent:
        agent = Agent(
            role="Senior Email Analyst",
            goal="Filter out non-essential emails like newsletters and promotional content",
            backstory=dedent(
                """\
				As a Senior Email Analyst, you have extensive experience in email content analysis.
				You are adept at distinguishing important emails from spam, newsletters, and other
				irrelevant content. Your expertise lies in identifying key patterns and markers that
				signify the importance of an email."""
            ),
            verbose=True,
            allow_delegation=False,
        )
        return agent
