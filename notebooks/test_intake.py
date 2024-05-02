#%%
import pandas as pd

#%%
# define list of concerns from the intake document
list_concerns = [
    "Reading",
    "Math",
    "Comprehension",
    "Processing Speed",
    "CORE",
    "Spelling",
    "Writing",
    "Memory",
    "Auditory Processing",
    "Speech/Language",
    "Visual Processing",
    "Attention/Focus",
    "Executive Function",
    "Dyslexia",
    "Sensory Issues",
    "Test Taking",
    "Study Skills",
    "Organization",
    "Grades",
    "Coordination/Balance",
]

list_examples = [
    "impulsiveness",
    "procrastination",
    "reversals",
    "concentration",
    "listening",
    "difficulty",
    "overload",
    "anxiety",
    "poor",
    "low",
    "slow",
    "work",
    "school",
    "schoolwork",
    "motivation",
    "behavior",
    "behaviors",
    "avoidance",
    "emotional",
    "avoidance",
    "self",
    "esteem",
    "self-esteem",
    "overly",
    "active",
    "fluency",
    "loses",
    "place",
    "skips", 
    "lines",
    "works", 
    "hard",
    "understanding", 
    "focusing",
    "letter",
    "letters",
    "number",
    "numbers",
    "words",
    "delayed",
    "regulation",
    "phonics",
    "social",
    "falling",
    "behind",
    "skipping",
    "distractibility",
    "verbal",
    "expression",
    "struggles",
    "blending",
    "oral",
    "communication",
    "not",
    "coordinated",
    "messy",
    "unsafe",
    "time",
    "management",
    "academics",
    "starting",
    "missing",
    "assignments",
    "learning",
    "grasping",
    "new",
    "motivation",
    "completing",
    "follow-through",
    "concepts",
    "functioning",
    "organizing",
    "planning",
    "prioritization",
    "struggle",
    "frustration",
    "concerning",
    "causing",
    "strengthen",
    "eye",
    "tracking",
    "excessive",
    "self-motivation",
    "independently",
    "independence",
    "habits",
    "overall",
    "answering",
    "questions",
    "self-starting",
    "losing",
    "beginning",
    "reflexes",
    "dyslexic",
    "tendencies",
    "extreme"
]


#%%
# loop through concerns and create a list of all the key words
list_keywords = []
for item in list_concerns:
    if ' ' in item:
        item_words = item.split(' ')
    elif '/' in item:
        item_words = item.split('/')
    else:
        item_words = [item]

    # loop through the item words
    for word in item_words:
        word = word.strip().lower()
        if (len(word) > 0) and not (word in list_keywords):
            list_keywords.append(word)

print(len(list_concerns))
print(len(list_keywords))
print(list_keywords[0:5])


#%%
# add in the extra example words taken from assessement files
for word in list_examples:
    word = word.strip().lower()
    if (len(word) > 0) and not (word in list_keywords):
        list_keywords.append(word)


#%%
df_keywords = pd.DataFrame(data=list_keywords, columns=["keywords"])
df_keywords.sort_values(by=["keywords"], inplace=True)
df_keywords.reset_index(drop=True, inplace=True)
print(df_keywords.shape)
print(df_keywords.head(10))

csv_filename = "../config/template_keywords.csv"
df_keywords.to_csv(csv_filename, index_label="index")


#%%
