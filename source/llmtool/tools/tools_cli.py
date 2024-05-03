import logging
from typing import Optional

import click

from ..data.query import search_embeddings, search_keywords, search_sections
from ..genai.generate import model_query
from ..settings import load_config
from .tools_load import (
    load_assessment_files,
    load_template_file,
    load_template_keywords,
    save_dataframe,
)

# configure logging
logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def tools(ctx):
    logger.info("tools:")


# default_folder = "./data/assessments/clients"
# default_zipfile = "./data/assessments/clients-20240410.zip"
# default_zipfile = "./data/assessments/drive-download-20240409.zip"
@tools.command("load", context_settings={"show_default": True})
@click.pass_context
@click.option(
    "--datapath",
    type=str,
    default="./data/assessments/drive-download-20240409.zip",
    help="Folder or zip file with assessment files.",
)
@click.option(
    "--clients", type=str, default="client_info.csv", help="Clients output info CSV file."
)
@click.option(
    "--reasons",
    type=str,
    default="client_reasons_info.csv",
    help="Client reasons output info CSV file.",
)
def load(
    ctx,
    datapath: str,
    clients: str,
    reasons: str,
):
    # load the global settings configuration file
    config = load_config()
    if config is None:
        logger.error("load: Unable to load the configuration file.")
        return

    # load the template sections definitions
    sections_data = load_template_file(
        config.template.template_path, config.template.template_sections
    )
    tables_data = load_template_file(config.template.template_path, config.template.template_tables)
    if sections_data is None or tables_data is None:
        logger.error("load: Unable to load the required template files.")
        return

    logger.info("load: SECTIONS[%s]", len(sections_data))
    logger.info("load: TABLES[%s]", len(tables_data))

    # load the template keywords definitions
    list_keywords = load_template_keywords(
        config.template.template_path, config.template.template_keywords
    )
    if list_keywords is None:
        logger.error("load: Unable to load the required keywords template file.")
        return

    # load the assessment files found in the specified location
    logger.info("load: DATAPATH[%s]", datapath)
    results = load_assessment_files(config, datapath, list_keywords, sections_data, tables_data)
    if results is not None:
        # unpack the results tuple
        df_clients = results[0]
        df_reasons = results[1]

        # check to see if the different dataframes can be persisted
        if (clients is not None) and (df_clients is not None):
            # save the clients into a CSV file
            save_dataframe("./", clients, df_clients)
        if (reasons is not None) and (df_reasons is not None):
            # save the client reasons into a CSV file
            save_dataframe("./", reasons, df_reasons, index=True)


@tools.command("search", context_settings={"show_default": True})
@click.pass_context
@click.option("--query", default="self-esteem", type=str, help="Query text.")
def search(ctx, query: str):
    logger.info("search: QUERY[%s]", query)

    # load the global settings configuration file
    config = load_config()
    if config is None:
        logger.error("search: Unable to load the configuration file.")
        return

    # first search using the embeddings
    filter: Optional[str] = None
    filter = "client_age < 19.0"
    df = search_embeddings(config, query, filter_text=filter)
    if df is None:
        logger.info("search: No result found.")
        return

    logger.info("search: Found [%s] embedding results.", df.shape)
    print(df.head(10))
    list_uuids = df["assessment_uuid"].tolist()
    print(list_uuids[0:4])

    # now search using the keywords
    df = search_keywords(config, query, filter_text=filter)
    if df is None:
        logger.info("search: No result found.")
        return

    logger.info("search: Found [%s] keyword results.", df.shape)
    print(df.head(10))

    # now search for the sections
    list_sections = ["auditory-processing", "dyslexia", "dysgraphia"]
    for item in list_sections:
        df = search_sections(config, item, list_uuids[0:4])
        print(df.head(10))


@tools.command("chat", context_settings={"show_default": True})
@click.pass_context
@click.option("--model", type=str, help="Model name.")
@click.option("--query", type=str, help="Query text.")
def chat(ctx, model: str, query: str):
    logger.info("chat: MODEL[%s] QUERY[%s]", model, query)
    model_query(model, query)
