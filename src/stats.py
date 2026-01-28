import csv
import pprint
from typing import Literal

import pandas as pd
import datetime


splits = pd.read_csv('../splits/my_splits.csv')
splits_detailed = pd.read_csv('../splits/splits_detailed.csv')

SEEDS = Literal['VILLAGE', 'SHIPWRECK', 'DESERT_TEMPLE', 'RUINED_PORTAL', 'BURIED_TREASURE']
BASTIONS = Literal['BRIDGE', 'TREASURE', 'STABLES', 'HOUSING']

def statistics(won: bool=None,
               forfeited: bool=None,
               time: datetime.timedelta=None,
               seedType: SEEDS=None,
               bastionType: BASTIONS=None,
               deaths: int=None,
               resets: int=None
               ):
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

    stats = {
        'Overworld':  pd.to_timedelta(splits_filtered['Overworld']).mean(),
        'Nether Nav': pd.to_timedelta(splits_filtered['Nether Nav']).mean(),
        'Bastion':    pd.to_timedelta(splits_filtered['Bastion']).mean(),
        'Fortress':   pd.to_timedelta(splits_filtered['Fortress']).mean(),
        'Blind':      pd.to_timedelta(splits_filtered['Blind']).mean(),
        'Stronghold': pd.to_timedelta(splits_filtered['Stronghold']).mean(),
        'End':        pd.to_timedelta(splits_filtered['End']).mean(),
        'Total':      pd.to_timedelta(splits_filtered['Total']).mean(),
        'Death Rate': splits_filtered['Deaths'].sum() / len(splits_filtered['Deaths']),
        'Reset Rate': splits_filtered['Resets'].sum() / len(splits_filtered['Resets']),
    }

    return stats

flawless = statistics(won=True, forfeited=False, deaths=0, resets=0)
deathless = statistics(won=True, forfeited=False, deaths=0)
wins = statistics(won=True, forfeited=False)

outplayed = statistics(won=False, forfeited=False, deaths=0, resets=0)

pprint.pp(statistics(seedType='VILLAGE'))
pprint.pp(statistics(seedType='SHIPWRECK'))
pprint.pp(statistics(seedType='DESERT_TEMPLE'))
pprint.pp(statistics(seedType='RUINED_PORTAL'))
