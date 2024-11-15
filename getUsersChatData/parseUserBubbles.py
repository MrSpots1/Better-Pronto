import json
from datetime import datetime, timezone

# Sample JSON data
with open(r"C:\Users\tjder\Downloads\Better-Pronto-main\Better-Pronto-maingetUsersChatData\json\listofBubbles.json", 'r') as file:
    data = json.load(file)

def search_key(data, key):
    dms = []
    non_dms = {}

    def search(data, key, parent_key=None, is_dm=False, category=None):
        if isinstance(data, dict):
            if 'isdm' in data:
                is_dm = data['isdm']
            if 'category' in data and data['category'] is not None:
                category = str(data['category'].get('title', 'Unknown'))
            for k, v in data.items():
                if k == key and parent_key != "category":
                    if is_dm:
                        if 'dmpartner' in data and 'lastseen' in data['dmpartner']:
                            last_seen = data['dmpartner']['lastseen']
                            try:
                                if last_seen.endswith('Z'):
                                    last_seen = last_seen.replace('Z', '+00:00')
                                last_seen_time = datetime.fromisoformat(last_seen)
                                if last_seen_time.tzinfo is None:
                                    try:
                                        last_seen_time = datetime.strptime(last_seen, "%Y-%m-%dT%H:%M:%S.%f%z")
                                    except ValueError:
                                        last_seen_time = datetime.strptime(last_seen, "%Y-%m-%d %H:%M:%S")
                                        last_seen_time = last_seen_time.replace(tzinfo=timezone.utc)
                                if last_seen_time.tzinfo is None:
                                    last_seen_time = last_seen_time.replace(tzinfo=timezone.utc)
                            except ValueError:
                                last_seen_time = datetime.strptime(last_seen, "%Y-%m-%dT%H:%M:%S.%f%z")
                            current_time = datetime.now(timezone.utc)
                            minutes_ago = int((current_time - last_seen_time).total_seconds() / 60)
                            dms.append((v, minutes_ago))
                        else:
                            dms.append((v, None))
                    else:
                        if category not in non_dms:
                            non_dms[category] = []
                        non_dms[category].append(v)
                search(v, key, k, is_dm, category)
        elif isinstance(data, list):
            for item in data:
                search(item, key, parent_key, is_dm, category)

    search(data, key)
    return dms, non_dms

# Example usage
key_to_search = "title"
dms, non_dms = search_key(data, key_to_search)

# Sort DMs alphabetically by the first name
dms_sorted = sorted(dms, key=lambda x: str(x[0]).split()[0])

print(f"Direct Messages")
for dm, minutes_ago in dms_sorted:
    if minutes_ago is not None:
        print(f" - {dm} (last seen {minutes_ago} minutes ago)")
    else:
        print(f" - {dm} (last seen time not available)")

print(f"\nNon-DMs for key '{key_to_search}':")
for category, titles in non_dms.items():
    print(f"Category: {category}")
    for title in sorted(titles):
        print(f" - {title}")
