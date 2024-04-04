import logging

import click


# configure logging
logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def tools(ctx):
    logger.info("tools:")


@tools.command("load", context_settings={"show_default": True})
@click.pass_context
@click.option("--dept", type=str, default="mn_stlou_nsfd.json", help="Department JSON file.")
@click.option(
    "--events",
    type=str,
    default="mn_stlou_nsfd_rules.csv",
    help="Department event rules CSV file.",
)
@click.option(
    "--members", type=str, default="mn_stlou_nsfd_members.csv", help="Department members CSV file."
)
@click.option("--filepath", type=str, default="./data", help="Default file path.")
def load(ctx, dept: str, events: str, members: str, filepath: str):
    logger.info("load: DEPT[%s]", dept)


@tools.command("welcome", context_settings={"show_default": True})
@click.pass_context
@click.option("--dept", type=str, default="mn-stlou-northstar", help="Department identifier.")
def welcome(ctx, dept: str):
    # fetch the department record and members
    logger.info("welcome: DEPT[%s]", dept)


@tools.command("trigger", context_settings={"show_default": True})
@click.pass_context
@click.option("--dept", type=str, default="mn-stlou-northstar", help="Department identifier.")
def trigger(ctx, dept: str):
    # fetch the department event rules
    logger.info("trigger: RULES")


list_replies = ["START", "STOP", "NO", "YES", "STATUS"]


@tools.command("reply", context_settings={"show_default": True})
@click.pass_context
@click.option("--text", required=True, type=click.Choice(list_replies, case_sensitive=False))
@click.option("--mobile", type=str, default="+12183935621", help="Mobile number.")
def reply(ctx, text: str, mobile: str):
    # fetch the mobile record
    logger.info("reply: TEXT[%s] MOBILE[%s]", text, mobile)
