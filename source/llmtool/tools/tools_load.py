import json
import logging
import os
import zipfile
from typing import Any, Dict, List, Optional, Tuple

import fsspec
import pandas as pd
from docx import Document

from ..data.models import DocumentSchema, SectionSchema
from .tools_embed import (
    database_connect,
    database_create_fts,
    database_create_tables,
    database_drop_tables,
    database_embed_sections,
)
from .tools_parse import docx_parse_client, docx_parse_sections, parse_key_reasons

# configure logging
logger = logging.getLogger(__name__)


def verify_filename(filepath: str, filename: str) -> Optional[str]:
    # determine what file system type to use
    fs = fsspec.filesystem("file")
    if filepath.startswith("s3"):
        fs = fsspec.filesystem("s3")
        filepath = filepath.replace("s3://", "")

    # ensure the specified file resource exists
    file_resource = os.path.join(filepath, filename)
    file_exists = fs.exists(file_resource)
    file_valid = fs.isfile(file_resource)
    if not file_exists or not file_valid:
        logger.error("verify_filename: [%s] was not found.", file_resource)
        return None

    return file_resource


def load_json_data(filepath: str, filename: str) -> Optional[str]:
    # determine what file system type to use
    fs = fsspec.filesystem("file")
    if filepath.startswith("s3"):
        fs = fsspec.filesystem("s3")
        filepath = filepath.replace("s3://", "")

    # ensure the specified file resource exists
    file_resource = os.path.join(filepath, filename)
    file_exists = fs.exists(file_resource)
    file_valid = fs.isfile(file_resource)
    if not file_exists or not file_valid:
        logger.error("verify_filename: [%s] was not found.", file_resource)
        return None

    # read the text date
    with fs.open(file_resource) as fdata:
        json_data = fdata.read()

    return json_data


def load_template_file(filepath: str, filename: str) -> Optional[Dict]:
    # load the department info from the specified JSON file
    json_data = load_json_data(filepath, filename)
    if json_data is None:
        return None

    # load python dictionary from string
    json_dict = json.loads(json_data)
    return json_dict


def load_template_keywords(filepath: str, filename: str) -> Optional[List[str]]:
    # determine what file system type to use
    fs = fsspec.filesystem("file")
    if filepath.startswith("s3"):
        fs = fsspec.filesystem("s3")
        filepath = filepath.replace("s3://", "")

    # ensure the specified file resource exists
    file_resource = os.path.join(filepath, filename)
    file_exists = fs.exists(file_resource)
    file_valid = fs.isfile(file_resource)
    if not file_exists or not file_valid:
        logger.error("load_template_keywords: [%s] was not found.", file_resource)
        return None

    # read the keywords template CSV file
    list_keywords: Optional[List[str]] = None
    with fs.open(file_resource) as fdata:
        df_keywords = pd.read_csv(fdata)
        logger.info("load_template_keywords: [%s] read in.", df_keywords.shape)
        if not df_keywords.empty and "keywords" in df_keywords:
            list_keywords = df_keywords["keywords"].tolist()

    return list_keywords


def save_dataframe(filepath: str, filename: str, df_data: pd.DataFrame, index: bool = False):
    # save the dataframe to a CSV file
    file_resource = os.path.join(filepath, filename)
    df_data.to_csv(file_resource, index=index)
    logger.info("save_dataframe: [%s] [%s].", file_resource, df_data.shape)


def load_document(
    file_basename: str,
    file_obj: Any,
    dict_keywords: Dict[str, int],
    sections_data: Dict,
    tables_data: Dict,
) -> Optional[Tuple[DocumentSchema, Dict]]:
    # get the document basename and load the document
    document = Document(file_obj)

    # parse out the different sections
    doc_sections = docx_parse_sections(document, sections_data)
    if (doc_sections is None) or (len(doc_sections) == 0):
        logger.warning("load_document: [%s] unable to parse sections.", file_basename)
        return None

    # skip over any file that does not have the key reasons section
    # first data retrival will be done using this information
    if "key-reasons" not in doc_sections:
        logger.warning("load_document: [%s] unable to parse key reasons.", file_basename)
        return None

    # get the key reasons for the assessment
    reasons, keywords = parse_key_reasons(dict_keywords, doc_sections["key-reasons"])
    if not reasons or not keywords:
        logger.warning("load_document: [%s] key reasons are not specified.", file_basename)
        return None

    # try parsing out the client info
    doc_client = docx_parse_client(file_basename, document, reasons, keywords)
    if doc_client is None:
        logger.warning("load_document: [%s] was unable to parse client info.", file_basename)
        return None

    # ensure the client has a valid age
    if (doc_client.client_age is None) or (doc_client.client_age < 4):
        logger.warning(
            "load_document: [%s] was unable to parse client age [%s].",
            file_basename,
            doc_client.client_age,
        )
        return None

    # update the client assessment reasons and keywords and return results

    return (doc_client, doc_sections)


def load_assessment_files(
    filepath: str, list_keywords: List[str], sections_data: Dict, tables_data: Dict
) -> Optional[Tuple[pd.DataFrame, pd.DataFrame]]:
    # ensure the specified file exists
    fs = fsspec.filesystem("file")
    file_exists = fs.exists(filepath)
    if not file_exists:
        logger.error("load_assessment_files: [%s] does not exist.", filepath)
        return None

    # check to see we are processing a zip archive file or a folder of files
    file_iszip = filepath.lower().endswith(".zip")
    file_folder = fs.isdir(filepath)
    logger.debug(
        "load_assessment_files: [%s] ISZIP[%s] ISDIR[%s].", filepath, file_iszip, file_folder
    )
    if (not file_iszip) and (not file_folder):
        logger.error("load_assessment_files: [%s] is not a zip archive or folder.", filepath)
        return None

    # initialize the database and drop all existing tables
    db = database_connect()
    database_drop_tables(db)
    database_create_tables(db)
    total_files = 0
    valid_files = 0

    # initialize the dictionary of keywords
    # the dictionary will hold the number of times each keyword was found
    dict_keywords: Dict[str, int] = dict.fromkeys(list_keywords, 0)

    list_clients = []
    if file_folder:
        # get a list of all the docx files
        list_files = fs.ls(filepath, details=False)
        logger.info("load_assessment_files: [%s] has [%s] files.", filepath, len(list_files))
        for idx, item in enumerate(list_files):
            # load the current document
            file_basename = os.path.basename(item)
            total_files += 1
            results = load_document(file_basename, item, dict_keywords, sections_data, tables_data)
            if results is None:
                continue

            # create all the required embeddings from this document
            doc_client = results[0]
            doc_sections = results[1]
            database_embed_sections(db, doc_client, doc_sections)
            valid_files += 1
            list_clients.append(doc_client.model_dump())

    elif file_iszip:
        # get a list of all the files in the zip archive
        with zipfile.ZipFile(filepath, "r") as zf:
            for f in zf.namelist():
                # ensure only try and parse the docx files
                if f.endswith(".docx"):
                    # get the document
                    with zf.open(f, "r") as fp:
                        # load the current document
                        file_basename = os.path.basename(f)
                        total_files += 1
                        results = load_document(
                            file_basename, fp, dict_keywords, sections_data, tables_data
                        )
                        if results is None:
                            continue

                        # create all the required embeddings from this document
                        doc_client = results[0]
                        doc_sections = results[1]
                        database_embed_sections(db, doc_client, doc_sections)
                        valid_files += 1
                        list_clients.append(doc_client.model_dump())

    logger.info(
        "load_assessment_files: Loaded [%s / %s] assessment files.", valid_files, total_files
    )
    if len(list_clients) == 0:
        return None

    # create the full text search index on the keywords column
    database_create_fts(db)

    # determine the total number of times the keywords were found
    total_words = 0
    for k, v in dict_keywords.items():
        total_words += v

    # convert the dictionary of keywords into a pandas dataframe
    df_keywords = pd.DataFrame.from_dict(dict_keywords, orient="index", columns=["count"])
    df_keywords.sort_values(by=["count"], ascending=False, inplace=True)
    df_keywords.index.name = "keyword"
    df_keywords["percent"] = (df_keywords["count"] / total_words) * 100

    # build up dataframe with the client info
    df_clients = pd.DataFrame.from_dict(list_clients)
    df_clients.drop(columns=["assessment_file", "assessment_author", "client_name"], inplace=True)
    logger.info("load_assessment_files: Client dataframe [%s].", df_clients.shape)
    return (df_clients, df_keywords)
