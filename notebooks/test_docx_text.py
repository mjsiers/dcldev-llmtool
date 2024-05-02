#%%
import json

from docx import Document

section_defn = [
    {
        'title': "key-reasons", 
        'text': "Key Reason for Assessment", 
        'skip': False, 
        'max_length': -1,
        'text_range': "0:-1",
    },
    {
        'title': "summary-impact", 
        'text': "Summary and Impact of Challenges",
        'skip': True, 
        'max_length': -1,
        'text_range': None,
    },
    {
        'title': "neuro-developmental", 
        'text': "Neurodevelopmental",
        'skip': False, 
        'max_length': -1,
        'text_range': "11:",
    },
    {
        'title': "cognitive-processing", 
        'text': "Cognitive Processing", 
        'skip': False, 
        'max_length': -1,
        'text_range': "12:-1",
    },
    {
        'title': "auditory-processing",
        'text': "Auditory Processing", 
        'skip': False, 
        'max_length': -1,
        'text_range': "13:-1",
    },
    {
        'title': "visual-processing", 
        'text': "Visual Processing", 
        'skip': False, 
        'max_length': -1,
        'text_range': "1:-1",
    },
    {
        'title': "attention-focus", 
        'text': "Attention Focus", 
        'skip': False, 
        'max_length': -1,
        'text_range': "1:-1",
    },
    {
        'title': "executive-function", 
        'text': "Executive Function", 
        'skip': False, 
        'max_length': -1,
        'text_range': "8:-1",
    },
    {
        'title': "phonological-awareness", 
        'text': "Phonological Awareness", 
        'skip': False, 
        'max_length': -1,
        'text_range': "1:-1",
    },
    {
        'title': "dyslexia", 
        'text': "Dyslexia. Reading, and Spelling Skills", 
        'skip': False, 
        'max_length': -1,
        'text_range': "1:-1",
    },
    {
        'title': "dysgraphia", 
        'text': "Dysgraphia", 
        'skip': False, 
        'max_length': -1,
        'text_range': "1:",
    },
    {
        'title': "dysgraphia", 
        'text': "Writing", 
        'skip': False, 
        'max_length': -1,
        'text_range': "1:",
    },    
    {
        'title': "graphomotor", 
        'text': "Graphomotor", 
        'skip': False, 
        'max_length': -1,
        'text_range': "1:",
    },
    {
        'title': "disorientation-neurotiming", 
        'text': "Disorientation and Neuro-timing", 
        'skip': False, 
        'max_length': -1,
        'text_range': None,
    },
    {
        'title': "comprehension", 
        'text': "Comprehension", 
        'skip': False, 
        'max_length': -1,
        'text_range': "7:",
    },
    {
        'title': "expressive-language", 
        'text': "Expressive Language Skills", 
        'skip': False, 
        'max_length': -1,
        'text_range': "1:",
    },
    {
        'title': "math-concepts", 
        'text': "Math Concepts and Skills", 
        'skip': False, 
        'max_length': -1,
        'text_range': "1:",        
    },
    {
        'title': "what-canbe-done", 
        'text': "What Can Be Done?", 
        'skip': True, 
        'max_length': -1,
        'text_range': None,
    },
    {
        'title': "recommendations", 
        'text': "Programming /Recommendations", 
        'skip': False, 
        'max_length': 90,
        'text_range': None,
    },
    {
        'title': "commitment", 
        'text': "Commitment", 
        'skip': False, 
        'max_length': -1,
        'text_range': None,
    },
    {
        'title': "testing-scores", 
        'text': "Testing and Scores", 
        'skip': True, 
        'max_length': -1,
        'text_range': None,
    },
]

# build out list of the section text values
section_text = [item["text"] for item in section_defn]
print(len(section_text))
print(section_text)

json_filename = "../config/template_sections.json"
with open(json_filename, 'w', encoding='utf-8') as f:
    json.dump(section_defn, f, ensure_ascii=True, indent=2)


#%%
def is_section_text(text: str) -> int:
    for idx, item in enumerate(section_text):
        if text.startswith(item):
            return idx
    return -1


#%%
client_filename = "../data/assessments/clients/2021-0001.docx"
client_filename = "../data/assessments/clients/2022-0001.docx"
client_filename = "../data/assessments/clients/2023-0001.docx"
client_filename = "../data/assessments/clients/2024-0001.docx"
client_filename = "../data/assessments/clients/2024-0002.docx"
document = Document(client_filename)

doc_sections = {}
section_index = 0
section_data = None
section_info = None
for idx, paragraph in enumerate(document.paragraphs):
    # remove extra spaces
    # also ensure unicode characters and others are replaced
    text = paragraph.text.strip()
    text = text.replace('\t', "")
    text = text.replace('\n', "")
    text = text.replace('\u2019', "'")
    text = text.replace('\u2013', "-")

    # ignore empty text lines
    if len(text) > 0:
        # determine if text indicates the start of a new section
        new_index = -1
        if (section_info is not None) and (section_info["title"] == "key-reasons"):
            # only end this section when the next section is found
            # this section may contain other section key words
            if text.startswith("Summary and Impact of Challenges"):            
                new_index = is_section_text(text)
        else:
            new_index = is_section_text(text)

        # check to see if we found a new section
        if new_index >= 0:
            # check to see if we have an active section
            if (section_data is not None) and (len(section_data) > 0):
                # persist the current section data
                if not section_info["skip"]:
                    # check to see if the section data should be filtered
                    if section_info["text_range"] is not None:
                        slice_ints = section_info["text_range"].split(':')
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
                    print(section_info["title"], len(section_data), section_length)

            # initialize the new section data
            section_index = new_index
            section_data = []
            section_info = section_defn[section_index]

            # check to see if we have reached the end of the sections
            if section_index >= len(section_text):
                section_data = None
                section_title = None
                break

        elif section_data is not None:
            if section_info["max_length"] < 0:
                # add the text to the current section
                section_data.append(text)
            else: 
                # only add the text if it is less than the max length value
                if len(text) <= section_info["max_length"]:
                    section_data.append(text)

json_filename = "../data/client_text.json"
with open(json_filename, 'w', encoding='utf-8') as f:
    json.dump(doc_sections, f, ensure_ascii=False, indent=2)


#%%
