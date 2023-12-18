# This script defines a function, get_formatted_column_names, that extracts column names from a CSV or Excel file and formats them for JSON configuration.
# The function takes a file path and an optional sheet name as input and returns a JSON string containing the formatted column names.
# The output is in a format that can be easily copied and pasted into a JSON configuration.

import pandas as pd
import json

import csv

def get_formatted_column_names(file_path, sheet_name=None):
    """
    Extracts column names from a CSV or Excel file and formats them for JSON configuration.

    Args:
        file_path (str): The path to the file.
        sheet_name (str, optional): The name of the sheet in case of an Excel file. Defaults to None.

    Returns:
        str: A JSON string containing the formatted column names and their inferred data types.
    """
    # Load the file based on the extension
    if file_path.endswith('.csv'):
        with open(file_path, 'r') as f:
            delimiter = csv.Sniffer().sniff(f.read(5000)).delimiter
        df = pd.read_csv(file_path, delimiter=delimiter)
    elif file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    else:
        raise ValueError("Unsupported file format")

    # Extract column names and their inferred data types
    columns_dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}
    columns_names = {col: col for col in df.columns}
    # Format for JSON configuration
    formatted_columns = {col: col for col, col in columns_names.items()}
    formatted_columns2 = {col: dtype for col, dtype in columns_dtypes.items()}
    return json.dumps([formatted_columns, formatted_columns2] , indent=4)

def main():
    file_path = r"Data\Input\FactInternetSales.csv"
    sheet_name = "BO_GESAMT"
    formatted_columns = get_formatted_column_names(file_path, sheet_name)

    # Output in a format easy to copy-paste into a JSON config
    print("\nFormatted column names for config:")
    print(formatted_columns)

if __name__ == "__main__":
    main()