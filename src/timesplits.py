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
    "story.lava_bucket",
    "nether.obtain_crying_obsidian",
    "nether.obtain_blaze_rod",
    "projectelo.timeline.death"
]

def filter_timeline(timeline: list, uuid: str, detailed: bool = False) -> list:
    output = []

    for achievement in timeline:
        if detailed:
            if achievement["uuid"] == uuid and achievement["type"] in achievements_detailed:
                output.append(achievement)
        else:
            if achievement["uuid"] == uuid and achievement["type"] in achievements:
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


def add_match_to_spreadsheet(match: dict, uuid: str, detailed: bool = False) -> dict:
    timeline = pd.DataFrame(filter_timeline(match["splits"][0], uuid, detailed)).get('time').tolist()

    # Only gets splits up from most recent reset
    if 'projectelo.timeline.reset' in timeline:
        timeline.reverse()
        timeline = timeline[:timeline.index('projectelo.timeline.reset')]
        timeline.reverse()

    if detailed:
        fieldnames = [
            "Overworld",
            "Portal",
            "Nether Nav",
            "Bastion Route",
            "Bartering",
            "Fortress Nav",
            "Blazes",
            "Blind",
            "Stronghold",
            "End",
        ]
    else:
        fieldnames = [
            "Overworld",
            "Nether Nav",
            "Bastion",
            "Fortress",
            "Blind",
            "Stronghold",
            "End",
        ]

    splits = {name: 0 for name in fieldnames}

    last_time = 0

    for name in fieldnames:
        try:
            current_time = timeline.pop()
            splits[name] = current_time - last_time
            last_time = current_time
        except IndexError:
            splits[name] = None

    fieldnames = ["Date", "Opponent", "Won", "Forfeited"] + fieldnames + ["Total", "Seed", "Bastion Type", "Deaths", "Resets"]
    splits["Date"] = match["date"]
    splits["Opponent"] = get_opponent(match["players"], uuid)
    splits["Total"] = match["result"]["time"]
    splits["Seed"] = match["seedType"]
    splits["Bastion Type"] = match["bastionType"]
    splits["Won"] = True if match["result"]["uuid"] == uuid else False
    splits["Forfeited"] = match["forfeited"]
    splits["Deaths"] = pd.DataFrame(match["splits"][0]).get('type').tolist().count('projectelo.timeline.death') # TODO Correct issue where opponent's death and resets are also counted
    splits["Resets"] = pd.DataFrame(match["splits"][0]).get('type').tolist().count('projectelo.timeline.reset')

    # TODO Make the detailed version be saved on a separate file
    with open("../splits/my_splits.csv", "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only if file is empty
        if os.stat("../splits/my_splits.csv").st_size == 0:
            writer.writeheader()

        writer.writerow(splits)

    return splits


def update_splits_sheets(user_id: str):
    if os.path.exists("../splits/my_splits.csv"):
        os.remove("../splits/my_splits.csv")

    with open('../matches/recent_matches_splits.json', 'r') as f:
        recent_matches = json.load(f)

    for match in recent_matches:
        add_match_to_spreadsheet(match, uuid=user_id)