import json
import logging
import os
from typing import Dict, Optional

import fsspec

from .tools_embed import (
    database_connect,
    database_create_tables,
    database_drop_tables,
    database_embed_sections,
)
from .tools_parse import docx_parse_sections

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


def load_assessment_files(filepath: str, sections_data: Dict, tables_data: Dict) -> None:
    # ensure the specified file exists
    fs = fsspec.filesystem("file")
    file_exists = fs.exists(filepath)
    file_folder = fs.isdir(filepath)
    logger.debug(
        "load_assessment_files: [%s] EXISTS[%s] ISDIR[%s].", filepath, file_exists, file_folder
    )
    if file_exists and file_folder:
        # initialize the database and drop all existing tables
        db = database_connect()
        database_drop_tables(db)
        database_create_tables(db)

        # get a list of all the docx files
        list_files = fs.ls(filepath, details=False)
        logger.info("load_assessment_files: [%s] has [%s] files.", filepath, len(list_files))
        for idx, item in enumerate(list_files):
            file_basename = os.path.basename(item)
            doc_sections = docx_parse_sections(item, sections_data)
            if (doc_sections is not None) and (len(doc_sections) > 0):
                # create all the required embeddings from this document
                database_embed_sections(db, file_basename, doc_sections)
