import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from docx import Document

from ..data.models import DocumentSchema

# configure logging
logger = logging.getLogger(__name__)


def is_section_text(text: str, sections_text: List[str]) -> int:
    for idx, item in enumerate(sections_text):
        if text.startswith(item):
            return idx
    return -1


def get_age(date: str, birth_date: str) -> float:
    today = datetime.strptime(date, "%Y-%m-%d")
    dob = datetime.strptime(birth_date, "%Y-%m-%d")
    delta_days = (today - dob).days
    age_value = delta_days / 365.25
    return age_value


def get_grade(grade: str) -> int:
    if not grade[-1].isdigit():
        grade = grade[:-2]
    return int(grade)


def docx_parse_client(file_name: str, document: Document) -> Optional[DocumentSchema]:
    if len(document.tables) == 0:
        logger.error("docx_parse_client: [%s] does not have any tables.", file_name)
        return None

    # initialize values used to parse the first table in the document
    table = document.tables[0]
    num_rows = len(table.rows)
    num_cols = len(table.columns)
    logger.info("docx_parse_client: [%s] table size [%s][%s].", file_name, num_rows, num_cols)

    # initialize the document schema values
    doc_uuid = str(uuid.uuid4())
    doc_data = DocumentSchema(assessment_uuid=doc_uuid, assessment_file=file_name)

    # get list of the unique strings from each cell in the table
    list_info = []
    for r in range(num_rows):
        for c in range(num_cols):
            # parse out the text for the current cell
            text = table.cell(r, c).text.strip()
            text = text.replace("\t", "")
            text = text.replace("\n", "")
            text = text.replace("\u2019", "'")
            text = text.replace("\u2013", "-")

            # ensure the text is not empty
            item_text = text.strip()
            if len(item_text) > 0:
                # if the string contains a comma, only take the first part of it
                if "," in item_text:
                    item_text = item_text.split(",")[0]

                # ensure the string is not a duplicate
                if item_text not in list_info:
                    list_info.append(item_text)

    # loop through the list of strings
    for item in list_info:
        # split the string on the colon and get the key and value
        item_split = item.split(":", 1)
        item_key = item_split[0].strip()
        item_value = item_split[1].strip()

        # update the output value based on the key value
        if item_key.startswith("Date"):
            # ensure date is in correct format
            date_info = item_value.split("-")
            date_value = datetime(int(date_info[2]), int(date_info[0]), int(date_info[1]))
            if "Birth" not in item_key:
                # update the assessment date
                doc_data.assessment_date = datetime.strftime(date_value, "%Y-%m-%d")
            else:
                # update the client birth date and compute age value
                doc_data.client_dob = datetime.strftime(date_value, "%Y-%m-%d")
                doc_data.client_age = get_age(
                    str(doc_data.assessment_date), str(doc_data.client_dob)
                )

        elif item_key.startwith("Client"):
            doc_data.client_name = item_value
        elif item_key.startwith("Grade"):
            doc_data.client_grade = get_grade(item_value)
        elif item_key.startwith("From"):
            doc_data.assessment_author = item_value

    return doc_data


def docx_parse_sections(file_name: str, sections_defn: Dict) -> Dict:
    sections_text = [item["text"] for item in sections_defn]
    document = Document(file_name)

    doc_sections = {}
    section_index: int = 0
    section_data: Optional[List] = None
    section_info: Optional[Dict[str, Any]] = None
    for idx, paragraph in enumerate(document.paragraphs):
        # remove extra spaces
        # also ensure unicode characters and others are replaced
        text = paragraph.text.strip()
        text = text.replace("\t", "")
        text = text.replace("\n", "")
        text = text.replace("\u2019", "'")
        text = text.replace("\u2013", "-")

        # ignore empty text lines
        if len(text) > 0:
            # determine if text indicates the start of a new section
            new_index = -1
            if (section_info is not None) and (section_info["title"] == "key-reasons"):
                # only end this section when the next section is found
                # this section may contain other section key words
                if text.startswith("Summary and Impact of Challenges"):
                    new_index = is_section_text(text, sections_text)
            else:
                new_index = is_section_text(text, sections_text)

            # check to see if we found a new section
            if new_index >= 0:
                # check to see if we have an active section
                if (
                    (section_data is not None)
                    and (len(section_data) > 0)
                    and (section_info is not None)
                ):
                    # persist the current section data
                    if not section_info["skip"]:
                        # check to see if the section data should be filtered
                        if section_info["text_range"] is not None:
                            slice_ints = section_info["text_range"].split(":")
                            start_idx = int(slice_ints[0])
                            if (len(slice_ints) == 2) and ((len(slice_ints[1]) > 0)):
                                end_idx = int(slice_ints[1])
                                section_data = section_data[start_idx:end_idx]
                            else:
                                section_data = section_data[start_idx:]

                        # save out the section data
                        section_length = 0
                        for item in section_data:
                            section_length += len(item)
                        doc_sections[section_info["title"]] = section_data
                        # print(section_info["title"], len(section_data), section_length)

                # initialize the new section data
                section_index = new_index
                section_data = []
                section_info = sections_defn[section_index]

                # check to see if we have reached the end of the sections
                if section_index >= len(sections_text):
                    section_data = None
                    break

            elif (section_data is not None) and (section_info is not None):
                if section_info["max_length"] < 0:
                    # add the text to the current section
                    section_data.append(text)
                else:
                    # only add the text if it is less than the max length value
                    if len(text) <= section_info["max_length"]:
                        section_data.append(text)

    return doc_sections


def docx_parse_tables(file_name: str, tables_defn: Dict) -> Optional[Dict]:
    return None
