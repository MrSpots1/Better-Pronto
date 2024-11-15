import json
import time
import requests
from getValuefromAccessJSON import load_and_search

def get_channel_list(bubble_id, page_number):
    access_token = load_and_search(r"C:\Users\tjder\Downloads\Better-Pronto-main\Better-Pronto-main\Authentication\accessTokenResponse.json", "accesstoken")
    url = "https://stanfordohs.pronto.io/api/v1/bubble.membershipsearch"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,es;q=0.8",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
        "X-Time-Zone": "America/Chicago",
        "X-Version": "WEB/1.0.0/770",
    }
    
    device_info = {
        "browsername": "Firefox",
        "browserversion": "130.0.0",
        "osname": "Windows",
        "type": "WEB",
        "orderby": ["firstname", "lastname"],
        "includeself": True,
        "bubble_id": bubble_id,
        "page": page_number
    }
    
    response = requests.post(url, headers=headers, json=device_info)
    
    # Print the response status and text for debugging
    print(f"Status Code: {response.status_code}")
    print("Response Text:", response.text)
    
    if response.status_code == 200:
        try:
            response_json = response.json()
            return response_json
        except ValueError:
            print("Response is not in JSON format.")
            return None
    else:
        response.raise_for_status()

def append_to_json_file(data, filename):
    try:
        with open(filename, 'r+') as json_file:
            try:
                # Try to load existing data
                existing_data = json.load(json_file)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
            except json.JSONDecodeError:
                # If file is empty or invalid, start with an empty list
                existing_data = []
            
            # Append new data
            existing_data.append(data)
            
            # Move file pointer to the beginning
            json_file.seek(0)
            # Write updated data
            json.dump(existing_data, json_file, indent=4)
            json_file.write('\n')  # Add a newline for better readability
    except FileNotFoundError:
        # If file does not exist, create it and write data
        with open(filename, 'w') as json_file:
            json.dump([data], json_file, indent=4)
            json_file.write('\n')  # Add a newline for better readability

# Example usage
pageNumber = 1
bubble_id = 3930501 
filename = 'bubbleSearchResponse.json'

start_time = time.time()

for pageNumber in range(1, 35):
    channels = get_channel_list(bubble_id, pageNumber)
    if channels:
        append_to_json_file(channels, filename)
    print(f"Page Number: {pageNumber}")
    print(channels)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Total time taken: {elapsed_time} seconds")
