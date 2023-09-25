import json
import pandas as pd
from pathlib import Path


def read_data(files):
    """
    Reads one or more JSON files and combines the data into a single DataFrame.

    :param files: List of file paths or a single file path.
    :return: A preprocessed DataFrame.
    """
    # Handle single file input.
    if isinstance(files, str) or isinstance(files, Path):
        files = [files]

    # Initialize an empty list to store data from each file.
    combined_data = []

    # Loop through each file and load the data.
    for match_id, file in enumerate(files, 1):  # Starting match_id from 1
        with open(file, 'r') as f:
            data = json.load(f)
            # Adding match_id to each data entry
            for entry in data:
                entry['match_id'] = match_id
            combined_data.extend(data)

    return combined_data

def preprocess_data(combined_data):
    # Convert the combined data to a DataFrame.
    df = pd.DataFrame(combined_data)

    # Extracting norms statistics.
    df['norms_mean'] = df['norm'].apply(lambda x: sum(x) / len(x) if x else 0)
    df['norms_std'] = df['norm'].apply(lambda x: pd.Series(x).std() if x else 0)
    df['norms_len'] = df['norm'].apply(len)
    
    return df

# Example usage:
# files = ['data/match_1.json', 'data/match_2.json']
# combined_data = read_data(files)
# df = preprocess_data(combined_data)