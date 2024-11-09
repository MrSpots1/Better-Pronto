import json

def search_key(data, target_key):
    if isinstance(data, dict):
        if target_key in data:
            return data[target_key]
        for key, value in data.items():
            result = search_key(value, target_key)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = search_key(item, target_key)
            if result is not None:
                return result
    return None

def load_data_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"error": "File not found."}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON."}

def load_and_search(file_path, target_key):
    data = load_data_from_file(file_path)
    if isinstance(data, dict):
        value = search_key(data, target_key)
        return value if value is not None else f"Key '{target_key}' not found."
    return data

# Example usage
if __name__ == "__main__":
    file_path = r"C:\Users\paul\Desktop\Better Pronto\Authentication\JSON\accessTokenResponse.json"
    key_to_search = "accesstoken"
    result = load_and_search(file_path, key_to_search)
    print(result)
