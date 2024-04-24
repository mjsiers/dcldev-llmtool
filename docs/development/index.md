# Development Environment

This is a Python based project (version 3.10) and the development environment can be
setup using the following directions.  Please review the **Makefile** that is in the 
project root directory.  It contains many commands for executing the different development 
tools used by this project.

## Python

1. Install the Python Package Manager [Poetry](https://python-poetry.org/).
2. Clone repository source code into a local directory.
3. Install required packages by running command `poetry install`.

## Ollama

This project was designed to use the Large Language Model (LLM) tool **Ollama** for executing
the different open source models locally.  This tool must be installed and configured for the
application to work properly.  See the [Ollama](https://ollama.com/) website for more information 
and installation instructions.

### Models

The **ollama** tool must be used to download any model that is going to be used by the project.
The following command is used to download a model so it can be run locally.

    ollama pull <model-name> # pulls down the model
    ollama list              # lists which models are locally available

### Custom Models

This project is using the [CrewAI](https://www.crewai.com/) framework to run multiple AI Agents
to see if they can improve the quality of the generated text.  This framework may require the
open source LLM model files to be updated.  The `scripts/ollama` folder contains some updated 
model files and bash scripts to update the local models to work with **CrewAI**.  The
[Ollama Integration](https://docs.crewai.com/how-to/LLM-Connections/#ollama-integration)
documentation on the **CrewAI** website decribes this procedure in more detail.

    cd scripts/ollama             # changes to the ollama scripts directory
    bash create-llama2-model.sh   # creates new model based on llama2
    bash create-llama3-model.sh   # creates new model based on llama3
    bash create-phi3.sh           # creates new model based on phi3
