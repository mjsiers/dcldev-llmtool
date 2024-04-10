import logging

import click

from ..settings import load_config
from .tools_load import load_assessment_files, load_template_file

# configure logging
logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def tools(ctx):
    logger.info("tools:")


# default_folder = "./data/assessments/clients"
# default_zipfile = "./data/assessments/clients-20240410.zip"
@tools.command("load", context_settings={"show_default": True})
@click.pass_context
@click.option(
    "--datapath",
    type=str,
    default="./data/assessments/clients",
    help="Folder or zip file with assessment files.",
)
@click.option(
    "--filepath", type=str, default="./data", help="Default file path for template files."
)
@click.option(
    "--sections", type=str, default="template_sections.json", help="Template sections JSON file."
)
@click.option(
    "--tables", type=str, default="template_tables.json", help="Template tables JSON file."
)
def load(ctx, datapath: str, filepath: str, sections: str, tables: str):
    logger.info("load: DATAPATH[%s]", datapath)
    logger.info("load: FILEPATH[%s]", filepath)
    logger.info("load: SECTIONS[%s]", sections)
    logger.info("load: TABLES[%s]", tables)

    # load the global settings configuration file
    load_config()

    # load the template sections definitions
    sections_data = load_template_file(filepath, sections)
    tables_data = load_template_file(filepath, tables)
    if sections_data is None or tables_data is None:
        logger.error("load: Unable to load the required template files.")
        return

    logger.info("load: SECTIONS[%s]", len(sections_data))
    logger.info("load: TABLES[%s]", len(tables_data))

    # load the assessment files found in the specified location
    load_assessment_files(datapath, sections_data, tables_data)


@tools.command("search", context_settings={"show_default": True})
@click.pass_context
@click.option("--query", type=str, help="Query text.")
@click.option("--table", type=str, help="Table name.")
def search(ctx, query: str, table: str):
    logger.info("search: QUERY[%s]", query)
    logger.info("search: TABLE[%s]", table)
