# Project Documentation

The tool [MkDocs](https://www.mkdocs.org/) is used to build a static website
from all the project documentation markdown files located in the `docs` folder.
The configuration file `mkdocs.yml` is located in the project root directory.

Below are the Makefile commands used to build the project documentation.

    make docs        # Build and serve the project documentation.
    make docs-test   # Build project documentation and check for errors.
