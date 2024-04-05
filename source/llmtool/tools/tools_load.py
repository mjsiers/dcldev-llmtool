import logging
import os
from typing import Dict, List, Optional

import fsspec

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

    return json_data
