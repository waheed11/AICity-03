import jsonlines

def delete_specific_indices(input_file, output_file, indices_to_delete):
    with jsonlines.open(input_file) as reader, jsonlines.open(output_file, mode='w') as writer:
        for obj in reader:
            if obj.get("index") not in indices_to_delete:
                writer.write(obj)

# Specify the input and output files
input_file = '../data/indexed.jsonl'
output_file = '../data/cleaned.jsonl'

# List of indices to delete
indices_to_delete = {40, 59, 64, 83, 43, 60, 80, 53, 77, 67, 86, 56, 63, 82,
                     37, 57, 66, 85, 69, 88, 45, 62, 81, 87, 65, 84, 55, 58,
                     52, 70, 74, 89, 44, 61, 99}

# Call the function to delete specified indices and write the rest to a new jsonl file
delete_specific_indices(input_file, output_file, indices_to_delete)