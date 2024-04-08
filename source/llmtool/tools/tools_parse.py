import json
from typing import Any, Dict, List, Optional

from docx import Document


def is_section_text(text: str, sections_text: List[str]) -> int:
    for idx, item in enumerate(sections_text):
        if text.startswith(item):
            return idx
    return -1


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
