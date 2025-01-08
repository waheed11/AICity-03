import jsonlines

def add_id_to_questions(file_paths):
    for file_path in file_paths:
        modified_questions = []  # To store the modified questions with an id
        with jsonlines.open(file_path) as reader:
            # Iterate over each question, adding an 'id' key
            for index, question in enumerate(reader):
                question['id'] = index  # Use the current index as the id
                modified_questions.append(question)

        # Write the modified questions back to the file
        with jsonlines.open(file_path, mode='w') as writer:
            writer.write_all(modified_questions)

# Path to the files that need to be updated
file_paths = ['data/ch-ar.jsonl', 'data/ch-en.jsonl']

# Run the function to add 'id' to each question
add_id_to_questions(file_paths)

print("Updated files with question IDs.")