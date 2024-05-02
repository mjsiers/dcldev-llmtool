# Client Assessment Report Tool

The purpose of this project is to evaluate how well open source large language models (LLM)
would work in assisting the generation of text for a client assessment report.  The generated 
text will be reviewed by a user and allow them to correct errors and suggest additional 
improvements.  

This project will be configured to only use locally running LLMs to ensure the confidential client 
data is not exposed to other vendors.

## Project Layout

    .github/       # Project Github actions and workflows.
    data/          # Project data files used for parsing reports.
    docs/          # Project documentation files.
    notebooks/     # Project Jupyter notebook files.
    scripts/       # Project script files.
    source/        # Python source files.
    tests/         # Python test source files.

    .env           # Environment variables file.
    config.toml    # Project configuration file.
    Makefile       # Project makefile containing developer commands.
    mkdocs.yml     # Project documentation configuration file.
    poetry.lock    # Poetry python dependencies files.
    poetry.toml    # Poetry configuration file.
    pyproject.toml # Python project file.

## Project Source Code

The source code for this project is available at [Github](https://github.com/mjsiers/dcldev-llmtool).