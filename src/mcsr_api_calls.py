import requests
import json
import sys
from src.timesplits import filter_timeline
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry



def mcsr_api_call(url) -> dict | None:
    s = requests.Session()
    retries = Retry(total=5, connect=5, read=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        response = s.get('https://mcsrranked.com/api' + url, timeout=10)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed after retries: {e}")


def get_user():
    global user

    username = input("Enter your Minecraft nickname\nUsername: ")

    response = mcsr_api_call(f'/users/{username}')

    if response["status"] == "success":
        user = response['data']
    else:
        print("Player Not Found.")

    with open('user.json', 'w') as f:
        json.dump(user, f)

    return username


def get_user_matches():
    with open('user.json', 'r') as f:
        user = json.load(f)

    user_id = user["uuid"]
    matches = mcsr_api_call(f'/users/{user_id}/matches?count=80')

    matches_id= []
    for match in matches['data']:
        if match['date'] > 1768578040: # TODO Make time period adjustable
            matches_id.append(match['id'])

    matches_splits = []
    total = len(matches_id)

    for i, id in enumerate(matches_id, start=1):
        splits = []

        match = mcsr_api_call(f'/matches/{id}')['data']

        important_keys = ['id', 'players', 'result', 'forfeited', 'date', 'seedType', 'bastionType']
        match_info = {key: match[key] for key in important_keys if key in match}

        splits.append(
                filter_timeline(timeline=match['timelines'], uuid=user_id, detailed=True)
        )

        match_info["splits"] = splits
        matches_splits.append(match_info)

        print_progress(i, total)

    with open('matches/matches.json', 'w') as matches_file:
        json.dump(matches, matches_file, indent=4)

    with open('matches/recent_matches_splits.json', 'w') as matches_info_file:
        json.dump(matches_splits, matches_info_file, indent=4)


def print_progress(current, total, bar_length=30):
    progress = current / total
    filled = int(bar_length * progress)
    bar = "█" * filled + "-" * (bar_length - filled)
    percent = progress * 100

    sys.stdout.write(f"\r[{bar}] {percent:6.2f}% ({current}/{total})")
    sys.stdout.flush()

    if current == total:
        print()  # newline at end