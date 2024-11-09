from getValuefromAccessJSON import load_and_search
import json, requests

filePath = r"C:\Users\paul\Desktop\Better Pronto\Authentication\JSON\accessTokenResponse.json"
userID = load_and_search(filePath, "id")

url = "https://stanfordohs.pronto.io/api/v3/bubble.list"

# Load the access token
access_token = load_and_search(filePath, "accesstoken")
if not access_token:
    raise ValueError("Access token not found or invalid")

userID = load_and_search(filePath, "id")
if not userID:
    raise ValueError("User ID not found or invalid")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {access_token}",  # Ensure 'Bearer' is included
}

try:
    response = requests.post(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    print("Access Token:", access_token)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err} - Response: {response.text}")
except requests.exceptions.RequestException as req_err:
    print(f"Request exception occurred: {req_err}")
except Exception as err:
    print(f"An unexpected error occurred: {err}")

output_file_path = r"C:\Users\paul\Desktop\Better Pronto\getUsersChatData\json\listofBubbles.json"

try:
    with open(output_file_path, 'w') as outfile:
        json.dump(response.json(), outfile, indent=4)
    print(f"Response successfully written to {output_file_path}")
except IOError as io_err:
    print(f"File write error occurred: {io_err}")
