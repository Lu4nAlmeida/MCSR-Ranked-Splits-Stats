import pprint
import pandas as pd

from src.timesplits import *
import requests
from timesplits import filter_timeline


my_uuid = '5d851a87545645eb988079ced8ef4a6b'


yea = [
    {
        "a": 0,
        "b": 'hello'
    },
    {
        "a": 1,
        "b": 'hello'
    },
    {
        "a": 1,
        "b": 'hello'
    },
]
df = pd.DataFrame(yea)
print(df['a'].tolist().count(1))

a=[1,2,3,4,3,1,3]
print(a.count(3))