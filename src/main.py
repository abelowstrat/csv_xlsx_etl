import argparse
import os
from data_loader import load_csv, load_excel
from data_transformer import load_config, transform_data
from data_saver import save_to_csv
import tkinter as tk
from tkinter import simpledialog
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def user_choice_interface():
    """ Create a simple GUI to allow the user to choose to process all files or a selection. """
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    # Ask the user for their choice
    choice = simpledialog.askstring("File Processing", "Enter 'all' to process all files, or file names separated by commas for specific files:")

    if choice is not None:
        if choice.lower().strip() == 'all':
            return 'all'
        else:
            return [file.strip() for file in choice.split(',')]

def process_file(config):
    """Process a file based on the configuration."""
    input_path = config.get('input_file_path')
    output_dir = config.get('output_dir')
    output_file_name = config.get('output_file_name')
    sheet_name = config.get('sheet_name', None)  # Default to None for non-Excel files

    try:
        # Load the data
        logging.info("Loading data...")
        if input_path.endswith('.csv'):
            data = load_csv(input_path)
        elif input_path.endswith('.xlsx'):
            data = load_excel(input_path, sheet_name)
            if not sheet_name:
                logging.warning("No sheet specified in the config. Using the first sheet.")
        else:
            raise ValueError(f"Unsupported file format: {input_path}")
        if data is None:
                raise ValueError(f"Data could not be loaded from file: {input_path}")
        
        # Transform the data
        logging.info("Applying transformations:")
        transformed_data = transform_data(data, config)
        if transformed_data is None:
                raise ValueError("Data transformation resulted in no data.")
        
        # Save the transformed data
        logging.info("Saving the transformed data...")
        save_to_csv(transformed_data, output_dir, output_file_name)
        logging.info("Processing complete for this file.")
        logging.info("-" * 50)
    
    except ValueError as e:
        logging.error(e)
    except Exception as e:
        logging.error(f"An unexpected error occurred while processing the file: {config.get('file_name')}. Error: {e}")


    

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    user_choice = user_choice_interface()

    config_path = 'Config/config.json'
    configs = load_config(config_path)

    if user_choice == 'all':
        logging.info("Processing all files.")
        for index, config in enumerate(configs, start=1):
            logging.info(f"Processing file {index}/{len(configs)}: {config.get('file_name')}")
            process_file(config)
    elif user_choice:
        logging.info("Processing selected files.")
        for file_name in user_choice:
            found = False
            for config in configs:
                if config.get('file_name') == file_name:
                    logging.info(f"Processing file: {file_name}")
                    process_file(config)
                    found = True
                    break
            if not found:
                logging.error(f"No configuration found for file: {file_name}")
    else:
        logging.info("No choice made. Exiting.")

    logging.info("Processing complete.")
    logging.info("=" * 50)

if __name__ == "__main__":
    main()