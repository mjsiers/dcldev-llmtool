# Workflow

The typical development workflow is list below.

    ...                    # download the client assessment reports
    make install           # ensure project CLI has been installed
    vi config.toml         # update the project configuration values

    llmtool tools load     # parse and save reports into local database
    llmtool tools search   # query local database (optional)
    llmtool gui run        # run the web based GUI


## Configuration File
