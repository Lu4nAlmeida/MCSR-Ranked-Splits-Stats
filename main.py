import requests
import pprint
import json

url = "https://mcsrranked.com/api"

my_uuid = '5d851a87545645eb988079ced8ef4a6b'

response = requests.get(url+'/users/MrLu4n/matches')

# Check HTTP status
response.raise_for_status()

# Parse JSON response
data = response.json()
matches_id= []

for match in data['data']:
    if match['date'] > 1768578040:
        matches_id.append(match['id'])


matches_splits = []
for id in matches_id:
    splits = []

    match = requests.get(url+f'/matches/{id}').json()['data']

    important_keys = ['id', 'players', 'result', 'forfeited', 'date', 'seedType', 'bastionType']
    match_info = {key: match[key] for key in important_keys if key in match}  # Filters non-important keys

    # TODO Filter only the achievements tied to the splits
    for split in match['timelines']:
        if split['uuid'] == my_uuid:
            splits.append(split)

    match_info["splits"] = splits
    matches_splits.append(match_info)

with open('matches.json', 'w') as matches_file:
    json.dump(data, matches_file, indent=4)

with open('recent_matches_splits.json', 'w') as matches_info_file:
    json.dump(matches_splits, matches_info_file, indent=4)

pprint.pprint(matches_splits[0])
