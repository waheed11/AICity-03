import jsonlines

def filter_keys(input_file, output_file, keys_to_keep):
    with jsonlines.open(input_file) as reader, jsonlines.open(output_file, mode='w') as writer:
        for obj in reader:
            filtered_obj = {key: obj[key] for key in keys_to_keep if key in obj}
            writer.write(filtered_obj)

# Specify the input and output files
input_file = '../data/ph-ar.jsonl'
output_file = '../data/filtered_ph-ar.jsonl'

# Specify the keys to keep
keys_to_keep = ["question", "A", "B", "C", "D", "answer"]

# Call the function to filter the keys and write to a new JSONL file
filter_keys(input_file, output_file, keys_to_keep)