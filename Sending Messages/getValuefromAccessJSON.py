import json

def load_and_search(file_path, target_key):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return {"error": str(e)}

    def search_key(data):
        if isinstance(data, dict):
            return data.get(target_key) or next((search_key(v) for v in data.values() if isinstance(v, (dict, list))), None)
        elif isinstance(data, list):
            return next((search_key(item) for item in data if isinstance(item, (dict, list))), None)
        return None

    return search_key(data) or f"Key '{target_key}' not found."

# Example usage
if __name__ == "__main__":
    file_path = r"C:\Users\tjder\Downloads\Better-Pronto-main\Better-Pronto-main\Authentication\accessTokenResponse.json"
    key_to_search = "accesstoken"
    result = load_and_search(file_path, key_to_search)
    print(result)
