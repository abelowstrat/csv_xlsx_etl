import pandas as pd
import csv

def load_csv(file_path):
    """Load a CSV file with a dynamic delimiter into a DataFrame and remove rows where all entries are null."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read a small portion of the file to guess the delimiter
            dialect = csv.Sniffer().sniff(file.read(5000))
            file.seek(0)  # Reset file read position to the beginning
            df = pd.read_csv(file, dtype=str, delimiter=dialect.delimiter, parse_dates= True)    

        df.dropna(how='all', inplace=True)  # how='all' removes rows where all entries are null
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except pd.errors.EmptyDataError:
        print(f"Empty file: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred while loading the CSV file: {e} \n Please check the csv file format and save it as csv-UTF8.")
        return None

def load_excel(file_path, sheet_name=None):
    """
    Load an Excel file into a DataFrame and remove rows where all entries are null.
    :param file_path: Path to the Excel file.
    :param sheet_name: Name of the sheet to load. If None, loads the first sheet.
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str) # excel parsed automatisch die Dates.
        df.dropna(how='all', inplace=True)
        return df
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except pd.errors.EmptyDataError:
        print(f"Empty file: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred while loading the Excel file: {e}")
        return None