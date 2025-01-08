import os
import jsonlines

# Define the data folder path
data_folder = '../data'

# Get list of all JSONL files in the data folder
jsonl_files = [file for file in os.listdir(data_folder) if file.endswith('.jsonl')]

for jsonl_file in jsonl_files:
    # Determine the output TXT file name
    file_name_parts = jsonl_file.replace('.jsonl', '').split('-')
    output_txt_file = f"{file_name_parts[0]}-qa-{file_name_parts[1]}.txt"

    # Open the JSONL file and extract questions
    questions = []
    with jsonlines.open(os.path.join(data_folder, jsonl_file)) as reader:
        for index, question in enumerate(reader):
            indexed_question = f"Q{index + 1}: {question['question']}\n"
            questions.append(indexed_question)

    # Write the indexed questions to the output TXT file
    with open(os.path.join(data_folder, output_txt_file), 'w', encoding='utf-8') as writer:
        writer.writelines(questions)

print("Questions have been extracted and saved to TXT files.")