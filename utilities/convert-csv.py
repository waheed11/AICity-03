import os
import jsonlines
import csv

def convert_jsonl_to_csv(jsonl_file, csv_file):
    with jsonlines.open(jsonl_file) as reader:
        all_fieldnames = set()
        rows = list(reader)

        # Collect all unique field names
        for row in rows:
            all_fieldnames.update(row.keys())

        with open(csv_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=list(all_fieldnames))
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

def process_data_folder(data_folder):
    # Path for the new folder
    csv_folder = os.path.join(data_folder, 'data-csv')

    # Create the new folder if it doesn't exist
    os.makedirs(csv_folder, exist_ok=True)

    # Iterate over all files in the data folder
    for filename in os.listdir(data_folder):
        if filename.endswith('.jsonl'):
            jsonl_file = os.path.join(data_folder, filename)
            csv_file = os.path.join(csv_folder, filename.replace('.jsonl', '.csv'))
            convert_jsonl_to_csv(jsonl_file, csv_file)
            print(f"Converted {jsonl_file} to {csv_file}")

# Specify the data folder
data_folder = '../data'

# Call the function to process the data folder
process_data_folder(data_folder)