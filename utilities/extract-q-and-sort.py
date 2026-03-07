import jsonlines

def extract_and_sort_questions(input_file, output_file):
    questions = []

    # Read the questions from the input JSONL file
    with jsonlines.open(input_file) as reader:
        for obj in reader:
            if "question" in obj:
                questions.append(obj["question"])

    # Sort the questions alphabetically
    questions.sort()

    # Write the sorted questions to a text file
    with open(output_file, 'w') as outfile:
        for question in questions:
            outfile.write(question + '\n')

# Specify the input and output files
input_file = '../data/cleaned2.jsonl'
output_file = '../data/sorted_questions.txt'

# Extract, sort, and save the questions
extract_and_sort_questions(input_file, output_file)