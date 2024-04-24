# Environment Variables

Use the following environment variables to allow the project software to connect
to the local models running inside **ollama**.

    OPENAI_API_BASE='http://localhost:11434/v1'
    OPENAI_MODEL_NAME='llama3:8b'
    OPENAI_API_KEY=''

The project has been configured to support the use of a `.env` file to hold all
the required environment variables.  This file is included in the `.gitignore` file
and will not be checked into the Git repository. It can be loaded into the local active
shell by executing the following command.

    source scripts/setup.sh
