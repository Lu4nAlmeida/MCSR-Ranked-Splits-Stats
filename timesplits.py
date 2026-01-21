import pprint
import json


achievements = [
    "story.lava_bucket",
    "story.enter_the_nether",
    "nether.find_bastion",
    "nether.obtain_crying_obsidian",
    "nether.find_fortress",
    "nether.obtain_blaze_rod",
    "projectelo.timeline.blind_travel",
    "story.follow_ender_eye",
    "story.enter_the_end"
]

def format_splits(timeline: list) -> list:
    return timeline