import os

def save_to_csv(data, output_dir, file_name):
    """Save a DataFrame to a CSV file in the specified directory with UTF-8 encoding."""
    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Construct the full file path
    file_path = os.path.join(output_dir, file_name)
    
    # Save the DataFrame to CSV with UTF-8 encoding
    data.to_csv(file_path, index=False, encoding='utf-8-sig', sep=';')
