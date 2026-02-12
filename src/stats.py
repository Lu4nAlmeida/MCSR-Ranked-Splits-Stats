import json
import math
from pprint import pprint
from typing import Literal
import statistics as stat
import scipy.stats as sci
import matplotlib.pyplot as plt
import seaborn as sns

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
        splits_filtered = splits[pd.to_timedelta(splits['Total']) <= time]
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
    splits_std['Death Rate'] = standard_deviation(splits_filtered['Deaths'].tolist())
    splits_std['Reset Rate'] = standard_deviation(splits_filtered['Resets'].tolist())

    return splits_mean, splits_std


def standard_deviation(sample: list) -> float:
    filtered_sample = []
    if contains_type(sample, Timedelta):
        for value in sample:
            if isinstance(value, Timedelta):
                filtered_sample.append(value.total_seconds())
    else:
        filtered_sample = sample

    return math.sqrt(stat.variance(filtered_sample))


def contains_type(input_list, target_type):
    """Checks if input_list contains any element of target_type."""
    return any(isinstance(item, target_type) for item in input_list)


flawless_mean, flawless_std = statistics(won=True, forfeited=False, deaths=0, resets=0, time=Timedelta(minutes=30))
deathless = statistics(won=True, forfeited=False, deaths=0)
completions_mean, completions_std = statistics(won=True, forfeited=False)

outplayed = statistics(won=False, forfeited=False, deaths=0, resets=0)

village_mean, village_std = statistics(seedType='VILLAGE')
ship_mean, ship_std = statistics(seedType='SHIPWRECK')
temple_mean, temple_std = statistics(seedType='DESERT_TEMPLE')
portal_mean, portal_std = statistics(seedType='RUINED_PORTAL')

pprint(completions_mean)
pprint(completions_std)

runs_dist = stat.NormalDist(mu=1609,sigma=346)
probability_of_pb = runs_dist.cdf(1004)
print(runs_dist.cdf(1004))
num_runs = stat.NormalDist(mu=1/probability_of_pb,sigma=math.sqrt(1-probability_of_pb)/probability_of_pb)
print(num_runs.inv_cdf(0.95))



