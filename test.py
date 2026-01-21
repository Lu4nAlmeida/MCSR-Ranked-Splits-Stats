import json
from timesplits import *


my_uuid = '5d851a87545645eb988079ced8ef4a6b'

with open('recent_matches_splits.json', 'r') as f:
    recent_matches = json.load(f)

for match in recent_matches:
    add_match_to_spreadsheet(match["splits"][0], uuid=my_uuid)