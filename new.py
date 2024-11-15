import json

# Step 2: Create your data
data = {
    "message": "paul this is friggen ez xd"
}

# Step 3: Write the data to a JSON file
with open('new_data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("Data has been written to new_data.json")


with open('new_data.json', 'r') as json_file: 
    data = json.load(json_file) 

print(data['message']) 
