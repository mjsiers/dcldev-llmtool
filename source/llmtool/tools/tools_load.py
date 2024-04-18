import json
import logging
import os
import zipfile
from typing import Dict, List, Optional, Tuple

import fsspec
import pandas as pd
from docx import Document

from ..data.models import DocumentSchema
from .tools_embed import (
    database_connect,
    database_create_tables,
    database_drop_tables,
    database_embed_sections,
)
from .tools_parse import docx_parse_client, docx_parse_sections

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


def save_dataframe(filepath: str, filename: str, df_data: pd.DataFrame):
    # save the dataframe to a CSV file
    file_resource = os.path.join(filepath, filename)
    df_data.to_csv(file_resource, index=False)
    logger.info("save_dataframe: [%s] [%s].", file_resource, df_data.shape)


def parse_key_reasons(list_keywords: List[str], list_reasons: List[str]) -> Tuple[str, str]:
    key_reasons: List[str] = []
    missing_words: List[str] = []
    ignore_words: List[str] = [
        "and",
        "or",
        "of",
        "in",
        "to",
        "too",
        "at",
        "when",
        "with",
        "for",
        "her",
        "him",
        "while",
    ]
    delimiter: str = ""

    # loop through all the lines of text in the key reasons section
    # skip over the first line since it does not contain any keywords
    full_text = ""
    for line in list_reasons[1:]:
        # check to see if the current line contains a period
        if "." in line:
            break

        # add the current line to the full text variable
        full_text += line + "\n"

        # split the reason into separate words
        if "," in line:
            list_words = []
            list_items = line.split(",")
            for item in list_items:
                if " " in item:
                    list_words.extend(item.split(" "))
                else:
                    list_words.append(item)
        elif "/" in line:
            list_words = []
            list_items = line.split("/")
            for item in list_items:
                if " " in item:
                    list_words.extend(item.split(" "))
                else:
                    list_words.append(item)
        else:
            list_words = line.split(" ")

        for word in list_words:
            # convert word to lower case
            word = word.lower().strip()
            if word.startswith("and"):
                word.replace("and", "")
                word = word.strip()

            if len(word) > 1:
                # check to see if the word is in the list of keywords
                if word in list_keywords:
                    key_reasons.append(word)
                else:
                    if word not in ignore_words:
                        missing_words.append(word)

    # compute the reasons text string
    reasons_text = "|".join(key_reasons)
    logger.debug("parse_key_reasons: full text length [%s].", len(full_text))
    logger.debug(
        "parse_key_reasons: key words [%s] with length [%s].", len(key_reasons), len(reasons_text)
    )

    # check to see if we were missing any words
    if len(missing_words) > 0:
        missing_text = "|".join(missing_words)
        logger.info("parse_key_reasons: Missing [%s] words [%s].", len(missing_words), missing_text)

    return (full_text, reasons_text)


def load_assessment_files(
    filepath: str, list_keywords: List[str], sections_data: Dict, tables_data: Dict
) -> Optional[pd.DataFrame]:
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

    list_clients = []
    if file_folder:
        # get a list of all the docx files
        list_files = fs.ls(filepath, details=False)
        logger.info("load_assessment_files: [%s] has [%s] files.", filepath, len(list_files))
        for idx, item in enumerate(list_files):
            # get the document basename and load the document
            file_basename = os.path.basename(item)
            document = Document(item)
            total_files += 1

            # try parsing out the client info
            doc_client = docx_parse_client(file_basename, document)
            if doc_client is None:
                logger.warning("load_assessment_files: [%s] was unable to parse client info.", item)
                continue

            # ensure the client has a valid age
            if (doc_client.client_age is None) or (doc_client.client_age < 4):
                logger.warning(
                    "load_assessment_files: [%s] was unable to parse client age [%s].",
                    item,
                    doc_client.client_age,
                )
                continue

            # parse out the different sections
            doc_sections = docx_parse_sections(document, sections_data)
            if (doc_sections is not None) and (len(doc_sections) > 0):
                # skip over any file that does not have the key reasons section
                # first data retrival will be done using this information
                if "key-reasons" not in doc_sections:
                    logger.warning("load_assessment_files: [%s] unable to parse key reasons.", item)
                    continue

                # get the key reasons for the assessment
                reasons, keywords = parse_key_reasons(list_keywords, doc_sections["key-reasons"])
                if not reasons or not keywords:
                    logger.warning(
                        "load_assessment_files: [%s] key reasons are not specified.", item
                    )
                    continue

                # update the client assessment reasons and keywords
                doc_client.assessment_reasons = reasons
                doc_client.assessment_keywords = keywords

                # create all the required embeddings from this document
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
                        # get the document basename and load the document
                        file_basename = os.path.basename(f)
                        document = Document(fp)
                        total_files += 1

                        # try parsing out the client info
                        doc_client = docx_parse_client(file_basename, document)
                        if doc_client is None:
                            logger.warning(
                                "load_assessment_files: [%s] was unable to parse client info.",
                                file_basename,
                            )
                            continue

                        # ensure the client has a valid age
                        if (doc_client.client_age is None) or (doc_client.client_age < 4):
                            logger.warning(
                                "load_assessment_files: [%s] was unable to parse client age [%s].",
                                file_basename,
                                doc_client.client_age,
                            )
                            continue

                        # parse out the different sections
                        doc_sections = docx_parse_sections(document, sections_data)
                        if (doc_sections is not None) and (len(doc_sections) > 0):
                            # skip over any file that does not have the key reasons section
                            # first data retrival will be done using this information
                            if "key-reasons" not in doc_sections:
                                logger.warning(
                                    "load_assessment_files: [%s] unable to parse key reasons.", item
                                )
                                continue

                            # get the key reasons for the assessment
                            reasons, keywords = parse_key_reasons(
                                list_keywords, doc_sections["key-reasons"]
                            )
                            if not reasons or not keywords:
                                logger.warning(
                                    "load_assessment_files: [%s] key reasons are not specified.",
                                    file_basename,
                                )
                                continue

                            # update the client assessment reasons and keywords
                            doc_client.assessment_reasons = reasons
                            doc_client.assessment_keywords = keywords

                            # create all the required embeddings from this document
                            database_embed_sections(db, doc_client, doc_sections)
                            valid_files += 1
                            list_clients.append(doc_client.model_dump())

    logger.info(
        "load_assessment_files: Loaded [%s / %s] assessment files.", valid_files, total_files
    )
    if len(list_clients) == 0:
        return None

    # build up dataframe with the client info
    df_clients = pd.DataFrame.from_dict(list_clients)
    df_clients.drop(columns=["assessment_file", "assessment_author", "client_name"], inplace=True)
    logger.info("load_assessment_files: Client dataframe [%s].", df_clients.shape)
    return df_clients
