import pandas as pd
import json
import re
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_path):
    """Load configuration from a JSON file."""
    with open(config_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def apply_transformations(data, transformations):
    """Apply a series of transformations based on the configuration."""
    for transform in transformations:
        if transform['type'] == 'rename':
            data = data.rename(columns=transform['details'])
        elif transform['type'] == 'clean_numeric':
            for column in transform['columns']:
                if column in data.columns:
                    logging.info(f"Cleaning numeric column '{column}'...")
                    data = clean_numeric_column(data, [column])
                else:
                    logging.warning(f"Column '{column}' not found in data...")
        elif transform['type'] == 'transform_date':
            for date_column in transform['date_columns']:
                column = date_column['column']
                if column in data.columns:
                    logging.info(f"Transforming date column '{column}'...")
                    data = transform_date_column(data, column, date_column)
                else:
                    logging.warning(f"Column '{column}' not found in data...")
        elif transform['type'] == 'melt':
            data = melt_data(data, transform)
    # Replace NaN with empty strings
    return data

def transform_data(data, config):
    """Transform data according to the configuration."""
    logging.info("Starting data transformation...")
    if 'transformations' in config:
        data = apply_transformations(data, config['transformations'])
    if 'new_columns' in config:
        data = add_new_columns(data, config['new_columns'])
        # Reorder columns if specified in the configuration
    if 'output_column_order' in config:
        logging.info("Reordering columns...")
        data = reorder_columns(data, config['output_column_order'])

    return data

# ... other functions ...

def clean_numeric_column(data, columns):
    """
    Clean numeric columns from string to float, handling European number formats.
    Round the numeric columns to 2 decimal places.
    :param data: DataFrame
    :param columns: list of columns to clean
    """
    for column in columns:
        if column in data.columns:
            try:
                # Replace any non-numeric characters with 0
                data[column] = data[column].fillna(0)
                # Ensure the column is treated as a string
                data[column] = data[column].astype(str)
                # Replace the European thousand separator (period not preceded by a digit) with nothing
                data[column] = data[column].str.replace(r'(?<!\d)\.(?=\d{3})', '', regex=True)
                # Replace the European decimal separator (comma) with a period
                data[column] = data[column].str.replace(',', '.', regex=False)
                # change decimal spaces to two decimal places
                data[column] = data[column].apply(lambda x: '{0:.2f}'.format(float(x)))
                # Convert the cleaned column to numeric, coercing errors to NaN
                #data[column] = pd.to_numeric(data[column], errors='coerce').round(2)
                
            except Exception as e:
                print(f"Error processing column '{column}': {e}")
        else:
            print(f"Column '{column}' not found in data")
    return data

def reorder_columns(data, column_order):
    """
    Reorder DataFrame columns based on a specified order.
    
    :param data: pandas DataFrame.
    :param column_order: List of column names in the desired order.
    :return: DataFrame with columns reordered.
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Log existing column names for debugging
    logging.info("Existing columns before reordering: %s", data.columns.tolist())

    # Filter out any column names that are not in the DataFrame
    column_order = [col for col in column_order if col in data.columns]

    # Log the final column order for debugging
    logging.info("Final column order: %s", column_order)

    # Reorder the DataFrame
    data = data[column_order]

    return data

def add_new_columns(data, new_columns):
    """
    Add new empty columns to the DataFrame with logging and error handling.
    
    :param data: pandas DataFrame.
    :param new_columns: List of new column names to add.
    :return: DataFrame with new columns added.
    """
    for column in new_columns:
        try:
            if column not in data.columns:
                data[column] = pd.NA  # or pd.NA for newer pandas versions
                logging.info(f"Added new empty column: {column}")
            else:
                logging.warning(f"Column '{column}' already exists in the DataFrame. Skipped adding new column.")
        except Exception as e:
            logging.error(f"Error adding new column '{column}': {e}")

    return data

def transform_date_column(data, column, date_transform):
    """
    Transform dates in a column to the specified format as per configuration.
    :param data: DataFrame
    :param column: name of the column to transform
    :param date_transform: dict containing 'input_format' and 'output_format'
    """
    input_format = date_transform.get('input_format', '%Y-%m-%d %H:%M:%S')  # default format if not specified
    output_format = date_transform.get('output_format', '%Y-%m-%d')         # default format if not specified

    for idx, value in enumerate(data[column]):
        if pd.notnull(value):  # Skip transformation if value is null
            try:
                # Parse the date using the input format
                date_obj = datetime.strptime(value, input_format)
                # Format it to the desired output format
                data.at[idx, column] = date_obj.strftime(output_format)
            except ValueError as e:
                # If there's a parsing error, print it and leave the value as is
                print(f"Error processing date '{value}' in column '{column}': {e}")
    logging.info(f"Date format changed from {input_format} to {output_format} in column {column}")  # Add logging
    return data

def melt_data(data, config):
    """
    Melt the DataFrame to a long format based on the configuration.

    :param data: pandas DataFrame.
    :param config: Configuration for the melt operation, including 'id_vars' and 'value_vars'.
    :return: Melted DataFrame with 'ORGANR', 'Attribut', and 'Wert'.
    """
    id_vars = config['id_vars']
    value_vars = config['value_vars']

    # Perform the melt operation
    melted_df = pd.melt(
        data,
        id_vars=id_vars,
        value_vars=value_vars,
        var_name='Attribut',
        value_name='Wert'
    )

    return melted_df