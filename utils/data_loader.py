import json
import os

def load_test_data():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, "data", "test_data.json")
    
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"ERROR: {file_path} is empty or contains invalid JSON syntax.")
        raise