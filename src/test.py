import pprint
import pandas as pd

from src.timesplits import *
import requests
from timesplits import filter_timeline, add_match_to_spreadsheet


my_uuid = '5d851a87545645eb988079ced8ef4a6b'

with open('../matches/recent_matches_splits.json', 'r') as f:
    recent_matches = json.load(f)

add_match_to_spreadsheet(recent_matches[7], uuid=my_uuid)