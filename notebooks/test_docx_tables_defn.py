#%%
import json

from docx import Document

#%%
table_defn = [
    {
        'title': "client", 
        'cols': None,
        'rows': None,       
        'cells': ["Date:", "Client:", "Grade:", "Date of Birth:", "Age:", "From:"],
    },
    {
        'title': "gibson-spelling", 
        'cols': ["Raw Score", "Age Equivalent", "Grade Equivalent"],
        'rows': None,
        'cells': None,     
    },
    {
        'title': "test-word-reading-efficency", 
        'cols': ["Age", "Grade", "Percentile", "Scaled Score"],
        'rows': ["Sight Words", "Phonemic Decoding", "Total Word Reading Index"],
        'cells': None,  
    },
    {
        'title': "gardner-reversals-test", 
        'cols': ["Subtest", "Patient Errors"],
        'rows': ["Execution", "Recognition", "Matching"],
        'cells': None,  
    },
    {
        'title': "jordan-left-right-reversal", 
        'cols': None,
        'rows': ["Score Analysis", "Total Raw Score", "Percentile Rank"],
        'cells': None,  
    },
    {
        'title': "visual-test-variables-attention", 
        'cols': None,
        'rows': ["Variability", "Response Time", "Commission Errors", "Omission Errors"],
        'cells': None,  
    },
    {
        'title': "test-auditory-processing-skills-4", 
        'cols': ["", "Age Score", "Percentile", "Standard Score"],
        'rows': ["Number Memory Forward", "Word Memory", "Sentence Memory", "Auditory Memory", "Processing Oral Directions", "Auditory Comprehension", "Listening Comprehension"],
        'cells': None,  
    },
    {
        'title': "test-visual-perceptual-skills-4", 
        'cols': ["Subtest", "Scaled Score", "Age Score", "Percentage"],
        'rows': ["Visual Discrimination", "Visual Memory", "Spatial Relations", "Form Constancy", "Sequential Memory", "Figure Ground", "Visual Closure", "Overall Score"],
        'cells': None,  
    },
    {
        'title': "developmental-test-visual-perception-3", 
        'cols': ["", "Age", "Percentile", "Scaled Score"],
        'rows': ["Eye-Hand Coordination", "Copying", "Visual- Motor Integration"],
        'cells': None,  
    },
    {
        'title': "receptive-expressive-observation", 
        'cols': ["SUBTEST", "Standard Score", "Percentile", "Functional Level"],
        'rows': ["Visual - Vocal", "Visual - Motor", "Auditory - Vocal", "Auditory - Motor"],
        'cells': None,  
    },
    {
        'title': "interactive-metronome-assessment", 
        'cols': ["Task", "Score", "Functional Level"],
        'rows': ["Both Hands", "Both Hands w/Guides", "Right Hand Left Foot", "Left Hand Right Foot"],
        'cells': None,  
    },
    {
        'title': "scan3-auditory-processing-1", 
        'cols': ["Subtest", "Scaled Score", "Percentage", "Functional Level"],
        'rows': ["Auditory Figure Ground +8", "Filtered Word", "Competing Words- Directed Ear", "Competing Sentences", "Competing Words - Free Recall", "Time Compressed Sentences", "Auditory Processing Composite"],
        'cells': None,  
    },
    {
        'title': "scan3-auditory-processing-2", 
        'cols': ["Subtest", "Ear Advantage (Rt/Lft)", "Score", "Typical (Y/N)"],
        'rows': ["Auditory Figure Ground", "Filtered Word", "Competing Words Free Recall", "Competing Words- Directed Right Ear", "Competing Words- Directed Left Ear", "Competing Sentences", "Time Compressed Sentences"],
        'cells': None,  
    },
    {
        'title': "gray-oral-reading-test-v", 
        'cols': ["", "Age Score", "Percentile", "Standard Score"],
        'rows': ["Rate", "Accuracy", "Reading fluency", "Comprehension", "Oral Reading Index"],
        'cells': None,  
    },
    {
        'title': "key-math-3", 
        'cols': ["", "Grade Score", "Age Score", "Standard Score"],
        'rows': ["Numeration", "Algebra", "Geometry", "Measurement", "Data Analysis / Probability", ""],
        'cells': ["Percentile rank =", "Standard Score ="],  
    },
    {
        'title': "behavior-rating-inventory-executive-function-1", 
        'cols': ["Scale/index/composite", "Percentile", "T score"],
        'rows': ["Inhibit", "Self-Monitor", "BRI", "Shift", "Emotional Control", "ERI", "Task Completion", "Working Memory", "Plan/Organize", "CRI", "GEC"],
        'cells': None,  
    },
    {
        'title': "behavior-rating-inventory-executive-function-2", 
        'cols': ["Scale", "Protocol Classification"],
        'rows': ["Negativity Scale", "Infrequency Scale", "Inconsistency Scale"],
        'cells': None,  
    },
]


#%%
json_filename = "../data/template_tables.json"
with open(json_filename, 'w', encoding='utf-8') as f:
    json.dump(table_defn, f, ensure_ascii=True, indent=2)


#%%
