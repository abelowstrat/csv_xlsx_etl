import tkinter as tk
from tkinter import filedialog
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def update_config_with_files(file_paths, config_path='Config/config.json'):
    # Load the existing configuration
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Update the configuration with new file paths
    for file_path in file_paths:
        # Extract the filename without the extension
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # Find a matching file configuration and update its input file path
        found = False
        for file_config in config:
            if file_config['file_name'].startswith(file_name):
                old_path = file_config.get('input_file_path', 'not previously set')
                file_config['input_file_path'] = file_path
                logging.info(f"Updated input file path for '{file_name}': '{old_path}' to '{file_path}'")
                found = True
                break
        if not found:
            logging.warning(f"No configuration found for file: {file_name}")

    # Save the updated configuration
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
        logging.info("Configuration file updated successfully.")

def select_files():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Show the file dialog and get the selected file paths
    file_paths = filedialog.askopenfilenames(
        title='Select input files',
        filetypes=[('CSV files', '*.csv'), ('Excel files', '*.xlsx')]
    )

    # Call the function to update the configuration with the selected file paths
    update_config_with_files(file_paths)

# Run the GUI
select_files()