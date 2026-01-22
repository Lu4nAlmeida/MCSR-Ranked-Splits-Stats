import datetime
import csv
import os

achievements = [
    "story.enter_the_nether",
    "nether.find_bastion",
    "nether.find_fortress",
    "projectelo.timeline.blind_travel",
    "story.follow_ender_eye",
    "story.enter_the_end",
    "projectelo.timeline.dragon_death"
]

achievements_detailed = achievements + [
    "story.lava_bucket",
    "nether.obtain_crying_obsidian",
    "nether.obtain_blaze_rod",
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


def get_opponent(players: list, uuid: str) -> str:
    opponent = None
    if len(players) > 2:
        opponent = 'MULTIPLE'
    else:
        for player in players:
            if player["uuid"] != uuid:
                opponent = player["nickname"]

    return opponent


def add_match_to_spreadsheet(match: dict, uuid: str, detailed: bool = False) -> dict:
    timeline = filter_timeline(match["splits"][0], uuid, detailed)

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
            current_time = timeline.pop()["time"]
            splits[name] = current_time - last_time
            last_time = current_time
        except IndexError:
            splits[name] = None

    fieldnames = ["Date", "Opponent", "Won", "Forfeited"] + fieldnames + ["Total", "Seed", "Bastion Type"] # TODO Add deaths and resets
    splits["Date"] = match["date"]
    splits["Opponent"] = get_opponent(match["players"], uuid)
    splits["Total"] = match["result"]["time"]
    splits["Seed"] = match["seedType"]
    splits["Bastion Type"] = match["bastionType"]
    splits["Won"] = True if match["result"]["uuid"] == uuid else False
    splits["Forfeited"] = match["forfeited"]

    # TODO Make the detailed version be saved on a separate file
    with open("my_splits.csv", "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only if file is empty
        if os.stat("my_splits.csv").st_size == 0:
            writer.writeheader()

        writer.writerow(splits)

    return splits