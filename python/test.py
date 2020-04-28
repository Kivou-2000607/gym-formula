"""
Play around
"""

import numpy
import matplotlib.pyplot as plt
import json

from gymlib import bs_s
from gymlib import bs_e

G = 2.0
B = 0.08
H = 4988
e = 5
so = 225613

s = bs_s(e, so, H=H, B=B, G=G, verbose=2)

print(f"dS 1: {s-so:,.1f}")
print(f"dS 2: {18.3399:,.1f}")
