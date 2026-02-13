import datetime
import pandas as pd
import json
import csv
import os

achievements = [
    "story.enter_the_nether",
    "nether.find_bastion",
    "nether.find_fortress",
    "projectelo.timeline.blind_travel",
    "story.follow_ender_eye",
    "story.enter_the_end",
    "projectelo.timeline.dragon_death",
    "projectelo.timeline.reset",
]

achievements_detailed = achievements + [
    "story.lava_bucket", # TODO Fix for Ruined Portal seeds
    "nether.obtain_crying_obsidian",
    "nether.obtain_blaze_rod",
    "projectelo.timeline.death"
]

def get_player_timeline(timeline: list, uuid: str):
    output = []

    for achievement in timeline:
        if achievement["uuid"] == uuid:
            output.append(achievement)

    return output


def filter_timeline(timeline: list, uuid: str, detailed: bool = False) -> list:
    output = []

    timeline = get_player_timeline(timeline, uuid)

    for achievement in timeline:
        if detailed:
            if achievement["type"] in achievements_detailed:
                output.append(achievement)
        else:
            if achievement["type"] in achievements:
                output.append(achievement)

    return output


def get_opponent(players: list[dict], uuid: str) -> str:
    opponent = None
    if len(players) > 2:
        opponent = 'MULTIPLE'
    else:
        for player in players:
            if player["uuid"] != uuid:
                opponent = player["nickname"]

    return opponent


def add_match_to_spreadsheet(match: dict, uuid: str, detailed: bool = False):
    timeline = pd.DataFrame(filter_timeline(match["splits"][0], uuid, detailed))
    timeline_timestamps = timeline.get('time').tolist()
    last_time = 0

    # Only gets splits up from most recent reset
    if 'projectelo.timeline.reset' in timeline.get('type').tolist():
        index = timeline.get('type').tolist().index('projectelo.timeline.reset')
        last_time = timeline_timestamps[index]
        timeline_timestamps = timeline_timestamps[:index]

    with open('src/splits.json', 'r') as f:
        fieldnames = json.load(f)['detailed'] if detailed else json.load(f)['splits']

    splits = {name: '' for name in fieldnames}

    for name in fieldnames:
        try:
            current_time = timeline_timestamps.pop()
            splits[name] = str(datetime.timedelta(milliseconds=current_time - last_time))
            last_time = current_time
        except IndexError:
            splits[name] = None

    fieldnames = ["Date", "Opponent", "Won", "Forfeited"] + fieldnames + ["Total", "Seed", "Bastion Type", "Deaths", "Resets"]
    splits["Date"] = str(pd.to_datetime(match["date"], unit="s"))
    splits["Opponent"] = get_opponent(match["players"], uuid)
    splits["Total"] = str(datetime.timedelta(milliseconds=match["result"]["time"]))
    splits["Seed"] = match["seedType"]
    splits["Bastion Type"] = match["bastionType"]
    splits["Won"] = True if match["result"]["uuid"] == uuid else False
    splits["Forfeited"] = match["forfeited"]

    full_timeline = pd.DataFrame(get_player_timeline(match["splits"][0], uuid)).get('type').tolist()

    splits["Deaths"] = full_timeline.count('projectelo.timeline.death')
    splits["Resets"] = full_timeline.count('projectelo.timeline.reset')

    if detailed:
        write_splits(fieldnames, splits, file='splits_detailed.csv')
    else:
        write_splits(fieldnames, splits, file='my_splits.csv')


def write_splits(fieldnames: list, splits: dict, file: str):
    with open(f"splits/{file}", "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only if file is empty
        if os.stat(f"splits/{file}").st_size == 0:
            writer.writeheader()

        writer.writerow(splits)


def update_splits_sheets(user_id: str):
    if os.path.exists("splits/my_splits.csv"):
        os.remove("splits/my_splits.csv")
        os.remove("splits/splits_detailed.csv")

    with open('matches/recent_matches_splits.json', 'r') as f:
        recent_matches = json.load(f)

    for match in recent_matches:
        add_match_to_spreadsheet(match, uuid=user_id)
        add_match_to_spreadsheet(match, uuid=user_id, detailed=True)