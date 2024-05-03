import logging
from typing import List, Optional

import ollama

# configure logging
logger = logging.getLogger(__name__)


def model_query(model: str, query: str, data: Optional[List[str]] = None):
    model_query = query
    context = None
    if data is not None:
        # update model query to include query data
        context = "\n\n".join(data)
        model_query = (
            f"{query} - Answer that question using the following text as a resource: {context}"
        )

    # make request to the specified model
    stream = ollama.generate(model=model, prompt=model_query, stream=True)
    for chunk in stream:
        if chunk["response"]:
            print(chunk["response"], end="", flush=True)
    print("\n\n")
