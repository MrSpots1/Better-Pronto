import json

# Sample JSON data
with open(r'C:\Users\paul\Desktop\Better Pronto\response.json', 'r') as file:
    data = json.load(file)

def search_key(data, key):
    results = []

    def search(data, key):
        if isinstance(data, dict):
            for k, v in data.items():
                if k == key:
                    results.append(v)
                search(v, key)
        elif isinstance(data, list):
            for item in data:
                search(item, key)

    search(data, key)
    return results

# Example usage
key_to_search = "fullname"
results = search_key(data, key_to_search)
print(f"Values for key '{key_to_search}': {results}")