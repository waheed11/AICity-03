import os
import jsonlines

# Define the source and target directories
source_dir = '../data'
target_dir = os.path.join(source_dir, 'data-temp')

# Ensure the target directory exists
os.makedirs(target_dir, exist_ok=True)

# Iterate over all files in the source directory
for filename in os.listdir(source_dir):
    if filename.endswith('.jsonl'):
        # Create full file paths
        source_file = os.path.join(source_dir, filename)
        target_file = os.path.join(target_dir, f'{os.path.splitext(filename)[0]}.txt')

        # Read JSONL file and write to TXT file
        with jsonlines.open(source_file) as reader, open(target_file, 'w') as writer:
            for obj in reader:
                writer.write(f'{obj}\n')

print("Conversion completed.")