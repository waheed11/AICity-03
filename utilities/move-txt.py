import os
import shutil

def move_txt_files_to_folder(data_folder):
    # Path for the new folder
    new_folder = os.path.join(data_folder, 'data-txt')

    # Create the new folder if it doesn't exist
    os.makedirs(new_folder, exist_ok=True)

    # Iterate over all files in the data folder
    for filename in os.listdir(data_folder):
        if filename.endswith('.txt'):
            # Construct full file path
            file_path = os.path.join(data_folder, filename)
            # Construct new file path
            new_file_path = os.path.join(new_folder, filename)
            # Move the file
            shutil.move(file_path, new_file_path)
            print(f"Moved {filename} to {new_folder}")

# Specify the data folder
data_folder = '../data'

# Call the function to move .txt files to the new folder
move_txt_files_to_folder(data_folder)