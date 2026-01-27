from mcsr_api_calls import get_user, get_user_matches
from timesplits import update_splits_sheets
import json
import os


if __name__ == '__main__':
    if not os.path.exists("../user.json"):
        username = get_user()
    else:
        with open("../user.json", "r") as f:
            user = json.load(f)
        username = user['nickname']


    print(f"Accessing {username}'s matches...")
    #get_user_matches()

    print("Updating spreadsheets...")
    update_splits_sheets(user['uuid'])

    print("Done.")
