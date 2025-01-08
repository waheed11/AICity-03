import jsonlines

def remove_index_key(input_file, output_file):
    with jsonlines.open(input_file) as reader, jsonlines.open(output_file, mode='w') as writer:
        for obj in reader:
            if "index" in obj:
                del obj["index"]
            writer.write(obj)

# Specify the input and output files
input_file = '../data/cleaned.jsonl'
output_file = '../data/cleaned2.jsonl'

# Call the function to remove the index key from each item and write the modified items to a new jsonl file
remove_index_key(input_file, output_file)