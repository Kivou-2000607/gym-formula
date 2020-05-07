"""
Play around
"""

import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import requests
from scipy.optimize import curve_fit
from scipy.optimize import minimize

from gymlib import normalize_cap

trains = json.load(open("../json/trains.json", 'r'))["trains"]


a = 12.75
def trial(happy, stat, a):
    # return (min(stat, 50000000) * numpy.round(1. + 0.07 * numpy.log(1. + happy / 250.), 4) + a * happy) / 200000.
    return (min(stat, 50000000) * (1. + 0.07 * numpy.log(1. + happy / 250.)) + a * happy) / 200000.

for train in trains:
    error = abs(train["normalized_gain_mul"] - trial(train["happy_before"], train["stat_before"], a))
    if error > 0.1:
        print(f'Train {train["pk"]:04d} with error {error:.4f}')
        for k, v in train.items():
            print(f"    {k}: {v}")
