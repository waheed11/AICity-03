import os
import jsonlines
from Levenshtein import distance  # Ensure you have python-Levenshtein installed

# Define the data folder path and the new folder for unique questions
data_folder = '../data'
unique_folder = os.path.join(data_folder, 'unique')

# Ensure the unique folder exists
os.makedirs(unique_folder, exist_ok=True)

# Get list of all JSONL files in the data folder
jsonl_files = [file for file in os.listdir(data_folder) if file.endswith('.jsonl')]

# Function to check if a question is similar to any in a set using Levenshtein distance
def is_similar(existing_questions, new_question, threshold=2):
    return any(distance(existing_question, new_question) <= threshold for existing_question in existing_questions)

# Function to add question to the similarity group map
def add_to_similarity_group(similarity_groups, question_text, index):
    for key in similarity_groups.keys():
        if is_similar([key], question_text):
            similarity_groups[key].append((index, question_text))
            return
    similarity_groups[question_text] = [(index, question_text)]

# Function to process each JSONL file
def process_jsonl_file(jsonl_file):
    questions_set = set()
    unique_questions = []
    duplicates = []
    similarity_groups = {}

    # Read the JSONL file and identify unique questions based only on the "question" field
    with jsonlines.open(os.path.join(data_folder, jsonl_file)) as reader:
        for index, question in enumerate(reader, start=1):  # Start index from 1
            question_text = question['question']
            if not is_similar(questions_set, question_text):
                questions_set.add(question_text)
                unique_questions.append(question)
            else:
                add_to_similarity_group(similarity_groups, question_text, index)
                duplicates.append((index, question_text))

    # Write the unique questions to a new JSONL file in the unique folder
    unique_file_path = os.path.join(unique_folder, jsonl_file)
    with jsonlines.open(unique_file_path, mode='w') as writer:
        writer.write_all(unique_questions)

    # Print number of duplicates and unique questions
    print(f"File: {jsonl_file}")
    print(f"Duplicate questions: {len(duplicates)}")

    # Print grouped similar questions
    for key, group in similarity_groups.items():
        if len(group) > 1:
            print(f"\"{group[0][1]}\" Index: [{group[0][0]}] is similar to:")
            for idx, question in group[1:]:
                print(f"\"{question}\" Index: [{idx}]")
            print(".")

    print(f"Unique questions: {len(unique_questions)}\n")

# Process each JSONL file
for jsonl_file in jsonl_files:
    process_jsonl_file(jsonl_file)

print("Processing completed.")