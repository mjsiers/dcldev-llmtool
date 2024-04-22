import logging
import os
from typing import Any, Optional

import click
import gradio as gr
import lancedb
import ollama
import pandas as pd

from ..data.models import DocumentSchema, SectionSchema
from ..settings import (
    lancedb_assessment_table,
    lancedb_database_name,
    lancedb_database_path,
    load_config,
    ollama_model_embed,
)

# configure logging
logger = logging.getLogger(__name__)


# configure logging
logger = logging.getLogger(__name__)


def embed_text(input_text: str) -> Optional[Any]:
    result = ollama.embeddings(model=ollama_model_embed, prompt=input_text)
    if (result is None) or ("embedding" not in result):
        logger.error("embed_text: Embedding model [%s] failed.", ollama_model_embed)
        return None

    return result["embedding"]


def database_connect() -> lancedb.DBConnection:
    vector_store = os.path.join(lancedb_database_path, lancedb_database_name)
    db = lancedb.connect(vector_store)
    return db


def search_embeddings(query: str) -> Optional[pd.DataFrame]:
    # embed the query text
    query_vector = embed_text(query)
    if query_vector is None:
        return None

    # connect to the database and get the specified table
    db = database_connect()
    tbl = db.open_table(lancedb_assessment_table)
    df_result = tbl.search(query_vector).limit(9).to_df()
    return df_result


def launch_gui():
    with gr.Blocks() as demo:
        gr.Markdown(
            """
                    # DCL Assessment Search with LanceDB
                    The GUI provides the ability to search the data extracted from DCL Assessment reports. 
                    The data can be searched using either embeddings or keywords.
                    """
        )
        with gr.Row():
            with gr.Tab("Embeddings"):
                vector_query = gr.Textbox(value="low self-esteem", show_label=False)
                b1 = gr.Button("Submit")
            with gr.Tab("Keywords"):
                keyword_query = gr.Textbox(value="low self-esteem", show_label=False)
                b2 = gr.Button("Submit")
        with gr.Row():
            query_results = gr.DataFrame()
        # with gr.Row():
        #    code = gr.Code(label="Code", language="python")
        # with gr.Row():
        #    gallery = gr.HTML()

        b1.click(search_embeddings, inputs=vector_query, outputs=[query_results])
        # b2.click(find_video_keywords, inputs=keyword_query, outputs=[gallery, code])
        # 3.click(find_video_sql, inputs=sql_query, outputs=[gallery, code])

    demo.launch()


@click.group()
@click.pass_context
def gui(ctx):
    logger.info("gui:")


@gui.command("run", context_settings={"show_default": True})
@click.pass_context
def run(ctx):
    # load the global settings configuration file
    load_config()

    # run the gui
    launch_gui()
