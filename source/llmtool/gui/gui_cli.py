import logging

import click
import gradio as gr

from ..data.query import search_embeddings, search_keywords
from ..settings import load_config

# configure logging
logger = logging.getLogger(__name__)


# configure logging
logger = logging.getLogger(__name__)


def launch_gui():
    with gr.Blocks() as demo:
        gr.Markdown(
            """
                    # DCL Assessment Tool
                    This tool provides the ability to search the data extracted from previous DCL Assessment reports. 
                    The data can be searched using either similarity or keywords.
                    """
        )
        with gr.Row():
            client_name = gr.Textbox(placeholder="Client Name", label="Client Name")  # noqa: F841
        with gr.Row():
            client_reasons = gr.Textbox(
                placeholder="Client Reasons", label="Key Reasons for Assessment"
            )
        with gr.Row():
            with gr.Tab("Similarity"):
                button1 = gr.Button("Search Embeddings")
                results1 = gr.DataFrame(type="pandas")
                clear1 = gr.ClearButton(results1)  # noqa: F841

            with gr.Tab("Keywords"):
                button2 = gr.Button("Search Keywords")
                results2 = gr.DataFrame(type="pandas")
                clear2 = gr.ClearButton(results2)  # noqa: F841

        button1.click(search_embeddings, inputs=client_reasons, outputs=[results1])
        button2.click(search_keywords, inputs=client_reasons, outputs=[results2])

        # with gr.Row():
        #    with gr.Tab("Embeddings"):
        #        embedding_text = gr.Textbox(value="low confidence", show_label=False)
        #        b1 = gr.Button("Submit")
        #    with gr.Tab("Keywords"):
        #        keywords_text = gr.Textbox(value="struggles reading", show_label=False)
        #        b2 = gr.Button("Submit")
        # with gr.Row():
        #    query_results = gr.DataFrame(type="pandas")

        # b1.click(search_embeddings, inputs=embedding_text, outputs=[query_results])
        # b2.click(search_keywords, inputs=keywords_text, outputs=[query_results])

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
