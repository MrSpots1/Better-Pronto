import json
import requests
from getValuefromAccessJSON import load_and_search

def get_latest_messages(bubble_id):
    file_path = r"C:\Users\tjder\Downloads\Better-Pronto-main\Better-Pronto-main\Authentication\accessTokenResponse.json"
    output_file_path = r"C:\Users\tjder\Downloads\Better-Pronto-main\Better-Pronto-main\getUsersChatData\latestMessages.json"
    #user_id = load_and_search(file_path, "id")
    access_token = load_and_search(file_path, "accesstoken")
    
    if not access_token:
        raise ValueError("Access token not found or invalid")
    
    url = "https://stanfordohs.pronto.io/api/v1/bubble.history"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    payload = {"bubble_id": str(bubble_id)}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()
        
        with open(output_file_path, 'w') as outfile:
            json.dump(response_json, outfile, indent=4)
        
        print(f"Response successfully written to {output_file_path}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Response: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request exception occurred: {req_err}")
    except IOError as io_err:
        print(f"File write error occurred: {io_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")


get_latest_messages(3835617 )
def PrintMessages():
    output_file_path = r"C:\Users\tjder\Downloads\Better-Pronto-main\Better-Pronto-main\getUsersChatData\latestMessages.json"
    with open(output_file_path, 'r') as file:
        data = json.load(file)
    messages = data["messages"]
    for i in range(50):
        print(messages[49-i]["message"])
PrintMessages()