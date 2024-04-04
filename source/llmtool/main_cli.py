import logging
import sys

import click

from .tools.tools_cli import tools

# configure logging
logging.basicConfig(
    level=logging.getLevelName(logging.INFO),
    handlers=[logging.StreamHandler(sys.stdout)],
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# define command group for the CLI
@click.group()
def cli():
    pass


cli.add_command(tools)
