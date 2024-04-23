# DCL Assessment Tool

The purpose of this project is to evaluate how well open source large language models (LLM)
would work in assisting the generation of text for a client assessment report.  The generated 
text will be reviewed by a user and allow them to correct errors and suggest additional 
improvements.  

This project will be configured to only use locally running LLMs to ensure the confidential client 
data is not exposed to other vendors.

### Project Workflow
Below are the steps of how this project will work.  It will be using the Retreival-Augmented 
Generation (RAG) design pattern to ensure the LLM requests include a detailed context of their expected 
output.

- Existing client assessment reports are parsed, embedded, and saved into local vector database.
- User provides information about the new client.
- Vector database embeddings are searched for clients with similar conditions.
- The retrieved text blocks are then used as the context for generating the text for the new client.
- Multiple AI agents are used to improve the quality of the generated text.
- User can review the generated report text and suggest additional improvements.

### Technology Stack
- Linux/Ubuntu/PopOS
- Makefile
- Poetry
- Python
- LanceDB (Vector Database)
- Ollama (Local LLMs)
  - Embedding Model(s)
  - Text Generation Model(s)
- CrewAI (AI Agents)
- Gradio (Web User Interface)

### CLI
TBD.

### GUI
TBD.
