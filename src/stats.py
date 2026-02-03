import json
import math
from pprint import pprint
from typing import Literal
import statistics as s

import pandas as pd
import datetime

from pandas import Timedelta

SEEDS = Literal['VILLAGE', 'SHIPWRECK', 'DESERT_TEMPLE', 'RUINED_PORTAL', 'BURIED_TREASURE']
BASTIONS = Literal['BRIDGE', 'TREASURE', 'STABLES', 'HOUSING']

def statistics(won: bool=None,
               forfeited: bool=None,
               time: datetime.timedelta=None,
               seedType: SEEDS=None,
               bastionType: BASTIONS=None,
               deaths: int=None,
               resets: int=None,
               detailed: bool=False,
               ):
    global splits

    if detailed:
        splits = pd.read_csv('../splits/splits_detailed.csv')
    else:
        splits = pd.read_csv('../splits/my_splits.csv')

    splits_filtered = None
    if won != None:
        splits_filtered = splits[splits['Won'] == won]
    if forfeited != None:
        splits_filtered = splits[splits['Forfeited'] == forfeited]
    if time != None:
        splits_filtered = splits[splits['Total'] <= time]
    if seedType != None:
        splits_filtered = splits[splits['Seed'] == seedType]
    if bastionType != None:
        splits_filtered = splits[splits['Bastion Type'] == bastionType]
    if deaths != None:
        splits_filtered = splits[splits['Deaths'] <= deaths]
    if resets != None:
        splits_filtered = splits[splits['Resets'] <= resets]

    if splits_filtered.empty:
        splits_filtered = splits

    with open('../src/splits.json', 'r') as f:
        splits_name = json.load(f)['detailed'] if detailed else json.load(f)['splits']

    splits_mean = {name: pd.to_timedelta(splits_filtered[name]).mean() for name in splits_name}

    splits_mean['Total'] = pd.to_timedelta(splits_filtered['Total']).mean()
    splits_mean['Death Rate'] = splits_filtered['Deaths'].mean()
    splits_mean['Reset Rate'] = splits_filtered['Resets'].mean()

    splits_std = {name: standard_deviation(pd.to_timedelta(splits_filtered[name]).tolist()) for name in splits_name}

    splits_std['Total'] = standard_deviation(pd.to_timedelta(splits_filtered['Total']).tolist())
    splits_std['Death Rate'] = standard_deviation(splits_filtered['Deaths'])
    splits_std['Reset Rate'] = standard_deviation(splits_filtered['Resets'])

    return splits_mean, splits_std


def standard_deviation(sample: list) -> float:
    if contains_type(sample, Timedelta):
        sample = [value.total_seconds() if type(value) == Timedelta else math.nan for value in sample]

    return math.sqrt(s.variance(sample))


def contains_type(input_list, target_type):
    """Checks if input_list contains any element of target_type."""
    return any(isinstance(item, target_type) for item in input_list)


flawless = statistics(won=True, forfeited=False, deaths=0, resets=0)
deathless = statistics(won=True, forfeited=False, deaths=0)
wins = statistics(won=True, forfeited=False)

outplayed = statistics(won=False, forfeited=False, deaths=0, resets=0)

village_mean, village_std = statistics(seedType='VILLAGE')
ship_mean, ship_std = statistics(seedType='SHIPWRECK')
temple_mean, temple_std = statistics(seedType='DESERT_TEMPLE')
portal_mean, portal_std = statistics(seedType='RUINED_PORTAL')

pprint(portal_mean)
pprint(portal_std)
