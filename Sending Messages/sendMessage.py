import requests
from datetime import datetime
from getValuefromAccessJSON import load_and_search
import uuid, random

def send_message(message, bubble_id):
    url = "https://stanfordohs.pronto.io/api/v1/message.create"
    file_path = r"C:\Users\paul\Desktop\Better Pronto\Authentication\JSON\accessTokenResponse.json"

    # Load the access token
    access_token = load_and_search(file_path, "accesstoken")
    if not access_token:
        raise ValueError("Access token not found or invalid")

    userID = load_and_search(file_path, "id")
    if not userID:
        raise ValueError("User ID not found or invalid")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",  # Ensure 'Bearer' is included
    }

    unique_uuid = str(uuid.uuid4())
    created_message_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "id": "Null",
        "uuid": unique_uuid,
        "bubble_id": bubble_id,
        "message": message,
        "created_at": created_message_at,
        "user_id": userID,
        "messagemedia": []
    }

    try:
        response = requests.post(url, headers=headers, json=data)
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

# Example usage
send_message("Hello, this is a test message", 3536226)
