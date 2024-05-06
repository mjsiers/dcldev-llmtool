#%%
import os

import faker
import pandas as pd
from llmtool.data.database import database_connect
from llmtool.settings import LanceDbConfig

#%%
# connect to the database and get the specified table
config = LanceDbConfig(
    database_path="../data/vectors/lancedb",
    database_name="dcl-llmtool",
    assessment_table="dcl-assessment",
    section_table="dcl-section",
)
db = database_connect(config)
list_names = db.table_names()
print(list_names)


#%%
tbl = db.open_table(config.section_table)
list_cols_assessment = ["assessment_uuid", "assessment_date", "client_name", "client_grade", "client_age"]
list_cols_section = ["assessment_uuid", "section", "text"]

limit = 10
section = "key-reasons"
filter_uuids = None
query_section = f"section = '{section}'"
if filter_uuids is not None:
    limit = len(filter_uuids)
    item_uuids = ",".join("'{0}'".format(x) for x in filter_uuids)
    query_section = f"(section = '{section}') AND (assessment_uuid IN ({item_uuids}))"

query = tbl.search().where(query_section, prefilter=True)
df_result = query.limit(limit).select(list_cols_section).to_pandas()
print(df_result.shape)


#%%
faker.Faker.seed(2024)
set_female = set(["she", "her"])
set_mail = set(["he", "him", "his"])
fake = faker.Faker()

tbl = db.open_table(config.assessment_table)
list_uuids = df_result["assessment_uuid"].tolist()
list_text = df_result["text"].tolist()
for i, uuid in enumerate(list_uuids):
    df_client = tbl.search().where("assessment_uuid = '{0}'".format(uuid)).select(list_cols_assessment).to_pandas()
    client_info = df_client.iloc[0].to_dict() 
    print(f"{i}: {client_info['client_name']}, {client_info['client_grade']}, {client_info['client_age']}")

    faker_first_name = fake.first_name()
    faker_last_name = fake.last_name()
    print(f"{i}: {faker_first_name} {faker_last_name}")

    client_name = client_info['client_name'].split()
    client_text = list_text[i].replace(client_name[0], "<CLIENT>")
    #print(client_name[0])
    print(f"{i}: {client_text}")


#%%
