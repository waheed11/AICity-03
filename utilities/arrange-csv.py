import os
import csv

def reorder_and_filter_csv_fields(csv_file, field_order):
    # Read the CSV file with the correct encoding
    with open(csv_file, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)

    # Define the new fieldnames order, filtering out any fields not in the order
    fieldnames = [field for field in field_order if field in reader.fieldnames]

    # Write the reordered and filtered CSV file with the correct encoding
    with open(csv_file, mode='w', newline='', encoding='utf-8-sig') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            # Write row with only the filtered fieldnames, defaulting to empty string if field not found
            writer.writerow({field: row.get(field, "") for field in fieldnames})

def process_csv_folder(csv_folder):
    # The desired field order
    field_order = ["question", "A", "B", "C", "D", "answer"]

    # Iterate over all files in the csv folder
    for filename in os.listdir(csv_folder):
        if filename.endswith('.csv'):
            csv_file = os.path.join(csv_folder, filename)
            reorder_and_filter_csv_fields(csv_file, field_order)
            print(f"Reordered and filtered fields in {csv_file}")

# Specify the CSV folder
csv_folder = '../data/data-csv'

# Call the function to process the CSV folder
process_csv_folder(csv_folder)