import json

def save_json(data, file_path):
    """
    Save data to a JSON file.

    Args:
        data (any): The data to save, typically a dictionary or a list.
        file_path (str): The path to the JSON file where the data will be saved.

    Returns:
        None
    """
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def load_json(file_path):
    """
    Load data from a JSON file.

    Args:
        file_path (str): The path to the JSON file to read from.

    Returns:
        any: The data read from the JSON file. If the file does not exist, returns None.
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
