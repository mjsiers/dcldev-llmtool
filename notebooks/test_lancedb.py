#%%
import ollama
import lancedb
import pyarrow as pa
import pandas as pd


#%%
test_docs = [
    "A Table is a collection of Records in a LanceDB Database.",
    "Tables in Lance have a schema that defines the columns and their types.",
    "These schemas can include nested columns and can evolve over time.",
    "A deeper integration between LanceDB Tables and Polars DataFrames is on the way.",
    "You can also create LanceDB tables directly from Arrow tables.",
    "LanceDB supports float16 data type!",
]

vector_data = []
for doc in test_docs:
    # compute the document embeding
    result = ollama.embeddings(model="nomic-embed-text", prompt=doc)

    # add document embedding and text to the vector data
    doc_info = {
        'vector': result['embedding'],
        'text': doc
    }
    vector_data.append(doc_info)

print(len(vector_data))
for idx,item in enumerate(vector_data):
    print(idx, len(item["vector"]), item["vector"][0:4])



#%%
vector_store = "../data/vectors/test-lancedb"
db = lancedb.connect(vector_store)

table_name = "lancedb_info"
list_tables = db.table_names()
if table_name in list_tables:
    db.drop_table(table_name)

tbl = db.create_table(table_name, data=vector_data)
#tbl.create_index(vector_column_name="vector", num_partitions=1, replace=True)
print(db.table_names())


#%%
list_queries = [
    "Does lancedb support the float16 data type?",
    "Does lancedb work with the polars dataframe?",
]

for query in list_queries:
    result = ollama.embeddings(model="nomic-embed-text", prompt=query)
    df_result = tbl.search(result['embedding']).limit(2).to_pandas()
    df_result.drop(columns="vector", inplace=True)
    print(df_result.head)


#%%
