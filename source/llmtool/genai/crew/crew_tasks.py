import logging
from textwrap import dedent

from crewai import Agent, Task

# configure logging
logger = logging.getLogger(__name__)


class ReportTasks:
    # def __init__(self):
    #   pass

    def reasons_task(self, agent: Agent, context: str) -> Task:
        task = Task(
            description=dedent(
                f"""\
				Analyze a batch of emails and filter out
				non-essential ones such as newsletters, promotional content and notifications.

			  Use your expertise in email content analysis to distinguish
				important emails from the rest, pay attention to the sender and avoind invalid emails.

				Make sure to filter for the messages actually directed at the user and avoid notifications.

				EMAILS
				-------
				{context}

				Your final answer MUST be a the relevant thread_ids and the sender, use bullet points.
				"""
            ),
            agent=agent,
        )
        return task

    def section_task(self, agent: Agent) -> Task:
        task = Task(
            description=dedent(
                """\
				For each email thread, pull and analyze the complete threads using only the actual Thread ID.
				understand the context, key points, and the overall sentiment
				of the conversation.

				Identify the main query or concerns that needs to be
				addressed in the response for each

				Your final answer MUST be a list for all emails with:
				- the thread_id
				- a summary of the email thread
				- a highlighting with the main points
				- identify the user and who he will be answering to
				- communication style in the thread
				- the sender's email address
				"""
            ),
            agent=agent,
        )
        return task
