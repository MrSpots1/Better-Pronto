import requests
import json
from getValuefromAccessJSON import load_and_search

def get_channel_list(bubble_id, page_number):
    access_token = load_and_search(r"C:\Users\paul\Desktop\Better Pronto\Authentication\getAccessToken\accessTokenResponse.json", "accesstoken")
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
        "orderby":["firstname","lastname"],"includeself":True,"bubble_id": bubble_id,"page":page_number
    }
    
    response = requests.post(url, headers=headers, json=device_info)
    
    # Print the response status and text for debugging
    print(f"Status Code: {response.status_code}")
    print("Response Text:", response.text)
    
    if response.status_code == 200:
        try:
            response_json = response.json()
            with open('bubbleSearchResponse.json', 'a') as json_file:
                json.dump(response_json, json_file, indent=4)
                json_file.write('\n')  # Add a newline for better readability
            return response_json
        except ValueError:
            print("Response is not in JSON format.")
            return None
    else:
        response.raise_for_status()

# Example usage
pageNumber = 1
bubble_id = 3640189

for pageNumber in range(1, 34):
    channels = get_channel_list(bubble_id, pageNumber)
    print(f"Page Number: {pageNumber}")
    print(channels)
