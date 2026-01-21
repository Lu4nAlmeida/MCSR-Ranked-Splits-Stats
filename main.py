import requests
import json
from timesplits import filter_timeline, add_match_to_spreadsheet
import os


url = "https://mcsrranked.com/api"

def get_user():
    global user

    username = input("Enter your Minecraft nickname\nUsername: ")
    response = requests.get(url + f'/users/{username}').json()

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
    matches = requests.get(url + f'/users/{user_id}/matches?count=50').json()

    matches_id= []
    for match in matches['data']:
        if match['date'] > 1768578040: # TODO Make time period adjustable
            matches_id.append(match['id'])


    matches_splits = []
    for id in matches_id:
        splits = []

        match = requests.get(url+f'/matches/{id}').json()['data']

        important_keys = ['id', 'players', 'result', 'forfeited', 'date', 'seedType', 'bastionType']
        match_info = {key: match[key] for key in important_keys if key in match}  # Filters non-important keys

        # Filters only relevant achievements
        splits.append(
                filter_timeline(timeline=match['timelines'], uuid=user_id, detailed=True)
        )

        match_info["splits"] = splits
        matches_splits.append(match_info)


    with open('matches.json', 'w') as matches_file:
        json.dump(matches, matches_file, indent=4)

    with open('recent_matches_splits.json', 'w') as matches_info_file:
        json.dump(matches_splits, matches_info_file, indent=4)


def update_splits_sheets(user_id: str):
    if os.path.exists("my_splits.csv"):
        os.remove("my_splits.csv")

    with open('recent_matches_splits.json', 'r') as f:
        recent_matches = json.load(f)

    for match in recent_matches:
        add_match_to_spreadsheet(match, uuid=user_id)



if __name__ == '__main__':
    if not os.path.exists("user.json"):
        username = get_user()
    else:
        with open("user.json", "r") as f:
            user = json.load(f)
        username = user['nickname']


    print(f"Accessing {username}'s matches...")
    get_user_matches()

    print("Updating spreadsheets...")
    update_splits_sheets(user['uuid'])

    print("Done.")
