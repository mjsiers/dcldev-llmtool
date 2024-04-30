# Design

## Report Parsing

The client assessment reports are saved in the `.docx` file format.  The document
contains multiple sections.  Each section contains common descriptive text and client
specific text.  Only the client specific text needs to be extracted for this project.

The report also contains sections with data tables that contain specific test results.
The code has been written to extract this client tabular data but it is currently not
being used by the project.

## Vector Database

After the client specific information has been extracted from the report, it will be
persisted into a local vector database.  The project is currently using the 
[LanceDB](https://lancedb.com/) vector database.  This local database supports both
vector embedding simularity searching along with full text search.

The client data is saved into two different tables.  These tables provide a parent-child
type relationship.  The initial strategy is to find all the existing clients with
similar keywords.  The text from each of these client report sections will then be used
as contextual input for the generation of text for the new client.

The database table schemas are defined using PyDantic model classes which are defined
in the followin source code file.

    source/llmtool/data/models.py

### Document Table

The **Document** table holds the client information along with the keywords used to 
describe the client.  The keyword text values are saved along with a vector embedding
of the keywords.  This allows this table to support both simularity/vector and full text
searches.  

### Section Table

The **Section** table holds the extracted text from each of the sections that were defined
in the parsed client assessment report.  The sections extracted text is also embedded as a 
vector into the table but this is not currently being used.


## Retrieval-Augmented Generation (RAG)

### Single Prompt Text Generation

### Multi-Agent Text Generation

#### Agents
- Reasons Writer
- Section Writer
- Editor

#### Tools
- Query LanceDB for similar clients
- Query LanceDB for specific section text and filtering by specified client list

#### Tasks
- Get similar clients to the current client
- Generate key reason text for client
- Generate section text for client
- Correct any errors or mistakes in generated text
- 