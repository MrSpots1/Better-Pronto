import requests
import time
import json
from dataclasses import dataclass

@dataclass
class DeviceInfo:
    browsername: str
    browserversion: str
    osname: str
    type: str

class BackendError(Exception):
    pass

# Define the API base URL
api_base_url = "https://stanfordohs.pronto.io/"
endpoint = "api/v1/user.tokenlogin"

def search_key(data, target_key):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            elif isinstance(value, dict):
                result = search_key(value, target_key)
                if result is not None:
                    return result
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        result = search_key(item, target_key)
                        if result is not None:
                            return result
    return None

def load_data_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return str(e)

def load_and_search(file_path, target_key):
    data = load_data_from_file(file_path)
    if isinstance(data, dict):
        value = search_key(data, target_key)
        return value if value is not None else f"Key '{target_key}' not found."
    return data

# Load the login token from the response file
login_token = load_and_search(r"C:\Users\paul\Desktop\Better Pronto\Authentication\getLoginToken\LoginToken_Response.json", 'logintoken')
print(f"Login Token: {login_token}")

# Create the payload
device_info = {
    "browsername": "firefox",
    "browserversion": "130.0.0",
    "osname": "macOS",
    "type": "WEB",
    "uuid": "314c9314-d5e5-4ae4-84e2-9f2f3938ca28",
    "osversion": "10.15.6",
    "appversion": "1.0.0",
}

payload = {
    "logintokens": [login_token],
    "device": device_info,
}

# Send the POST request
start_time = time.time()
response = requests.post(f"{api_base_url}{endpoint}", json=payload)
end_time = time.time()
print(f"Request sent in {end_time - start_time} seconds")

# Check the response
if response.status_code == 200:
    response_data = response.json()
    print("Success:", response_data)
else:
    response_data = {"error": response.status_code, "message": response.text}
    print(f"Error: {response.status_code} - {response.text}")

# Save the response to a file in JSON format
response_file_path = r'C:\Users\paul\Desktop\Better Pronto\Authentication\getAccessToken\accessTokenResponse.json'
with open(response_file_path, 'w') as file:
    json.dump(response_data, file, indent=4)
