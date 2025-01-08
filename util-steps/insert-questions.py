import os
import jsonlines
from Levenshtein import distance  # Ensure you have python-Levenshtein installed

# New unique questions to insert
new_questions = [
    {"question": "What is the formula for calcium carbonate?", "A": "CaCO3", "B": "CaO", "C": "Ca(OH)2", "D": "CaCl2", "answer": "A"},
    {"question": "Which element has the highest electronegativity?", "A": "Fluorine", "B": "Chlorine", "C": "Oxygen", "D": "Nitrogen", "answer": "A"},
    {"question": "What is the chemical formula for ammonia?", "A": "NH3", "B": "NH4+", "C": "N2H4", "D": "NO", "answer": "A"},
    {"question": "What is the electron configuration of potassium?", "A": "1s2 2s2 2p6 3s1", "B": "1s2 2s2 2p6 3s2 3p6", "C": "1s2 2s2 2p6 3s2 3p6 4s1", "D": "1s2 2s2 2p6 3s2 3p6 4s2", "answer": "C"},
    {"question": "Which gas is commonly known as laughing gas?", "A": "Nitrogen dioxide", "B": "Nitrous oxide", "C": "Carbon monoxide", "D": "Sulfur dioxide", "answer": "B"},
    {"question": "What is the pH of a neutral solution?", "A": "1", "B": "7", "C": "14", "D": "0", "answer": "B"},
    {"question": "What element is diamond primarily composed of?", "A": "Carbon", "B": "Oxygen", "C": "Sulfur", "D": "Silicon", "answer": "A"},
    {"question": "Which element is represented by the symbol 'Fe'?", "A": "Fluorine", "B": "Iron", "C": "Francium", "D": "Fermium", "answer": "B"},
    {"question": "What is the main use of chlorine in water treatment?", "A": "To remove hardness", "B": "To add nutrients", "C": "To disinfect", "D": "To remove color", "answer": "C"},
    {"question": "Which element is a liquid at room temperature?", "A": "Mercury", "B": "Bromine", "C": "Gallium", "D": "Both A and B", "answer": "D"}
]

def is_similar(existing_question, new_question, threshold=2):
    return distance(existing_question, new_question) <= threshold

def insert_new_questions(file_path, new_questions):
    existing_questions = []
    questions_set = []

    # Read existing questions
    if os.path.exists(file_path):
        with jsonlines.open(file_path) as reader:
            for question in reader:
                questions_set.append(question['question'])
                existing_questions.append(question)

    # Filter out non-unique questions
    unique_new_questions = []
    for q in new_questions:
        is_unique = True
        for existing_question in questions_set:
            if is_similar(existing_question, q['question']):
                is_unique = False
                print(f"Question \"{q['question']}\" is similar to \"{existing_question}\"")
                break
        if is_unique:
            questions_set.append(q['question'])
            unique_new_questions.append(q)

    if not unique_new_questions:
        print("No new unique questions to insert.")
    else:
        # Append new unique questions
        existing_questions.extend(unique_new_questions)

        # Write updated list back to the file
        with jsonlines.open(file_path, mode='w') as writer:
            writer.write_all(existing_questions)

        print(f"Inserted {len(unique_new_questions)} new unique questions into {file_path}")

# File path to the target JSONL file
file_path = '../data/unique/ch-en.jsonl'

# Call the function to insert new questions
insert_new_questions(file_path, new_questions)