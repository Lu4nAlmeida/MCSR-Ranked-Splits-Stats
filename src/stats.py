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

    splits_dict = {
        name: [
            pd.to_timedelta(splits_filtered[name]).mean(),
            Timedelta(seconds=standard_deviation(pd.to_timedelta(splits_filtered[name]).tolist()))
        ] for name in splits_name
    }

    splits_dict['Total'] = [
            pd.to_timedelta(splits_filtered['Total']).mean(),
            Timedelta(seconds=standard_deviation(pd.to_timedelta(splits_filtered['Total']).tolist()))
        ]

    splits_dict['Death Rate'] = [
        splits_filtered['Deaths'].mean(),
        standard_deviation(splits_filtered['Deaths'].tolist())
    ]

    splits_dict['Reset Rate'] = [
        splits_filtered['Resets'].mean(),
        standard_deviation(splits_filtered['Resets'].tolist())
    ]


    df = pd.DataFrame.from_dict(
        data=splits_dict,
        orient='index',
        columns=['Mean', 'Standard Deviation']
    )

    return df


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


flawless = statistics(won=True, forfeited=False, deaths=0, resets=0, time=Timedelta(minutes=30))
deathless = statistics(won=True, forfeited=False, deaths=0)
completions = statistics(won=True, forfeited=False)

outplayed = statistics(won=False, forfeited=False, deaths=0, resets=0)

village = statistics(seedType='VILLAGE')
shipwreck = statistics(seedType='SHIPWRECK')
temple = statistics(seedType='DESERT_TEMPLE')
portal = statistics(seedType='RUINED_PORTAL')

selected = deathless

pprint(selected)

mean = selected['Mean']['Total'].total_seconds()
std = selected['Standard Deviation']['Total'].total_seconds()

runs_dist = stat.NormalDist(mu=mean,sigma=std)
probability_of_pb = runs_dist.cdf(1004)
print("Probability of PB: ", (runs_dist.cdf(1004) * 100), '%')



