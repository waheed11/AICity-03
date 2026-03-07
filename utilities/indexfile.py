import jsonlines

def index_jsonl(input_file, output_file):
    with jsonlines.open(input_file) as reader, jsonlines.open(output_file, mode='w') as writer:
        for idx, obj in enumerate(reader, start=1):
            obj['index'] = idx
            writer.write(obj)

# Specify the input and output files
input_file = '../data/ee-ar.jsonl'
output_file = '../data/indexed.jsonl'

# Call the function to index and write the jsonl file
index_jsonl(input_file, output_file)