"""
Play around
"""

import numpy
import matplotlib.pyplot as plt
import json
import requests
from scipy.optimize import curve_fit

from gymlib import normalize_cap

#
# G = 2.0
# B = 0.08
# H = 4988
# e = 5
# so = 225613
#
# s = bs_s(e, so, H=H, B=B, G=G, verbose=2)
#
# print(f"dS 1: {s-so:,.1f}")
# print(f"dS 2: {18.3399:,.1f}")

# trains = requests.get("http://yata.alwaysdata.net/tmp/gym?export=json").json()["trains"]
trains = json.load(open("../json/trains.json", 'r'))["trains"]

data = []

def trial(happy, stat):
    # return 18 * numpy.log(x + 275) + 150
    return (stat * (1. + 0.07 * numpy.log(1. + happy / 250.)) + 12.75 * happy ) / 200000.

for train in [t for t in trains if t["stat_before"] > 49999999]:

    t = []
    t.append(train["happy_before"])
    t.append(train["normalized_gain_mul"])

    data.append(t)


data = numpy.array(data)

def fit1(x, a, b, c):
    return a * (numpy.log(b * (x + 250)) + c)


def fit2(x, a):
    return (50000000. * (1. + 0.07 * numpy.log(1. + x / 250.)) + a * x ) / 200000.


# FIT
popt1, _ = curve_fit(fit1, data[:, 0], data[:, 1])
popt2, _ = curve_fit(fit2, data[:, 0], data[:, 1])

str_fit1 = "FIT: {:.4g} * (numpy.log({:.4g} * (x + 250)) + {:.4g})".format(*popt1)
str_fit2 = "FIT: 250. * (1. + 0.07 * numpy.log(1. + x / 250.)) + {:.6g} * x".format(*popt2)
print(str_fit2)

xfit = numpy.linspace(0, 10000, 100)
yfit1 = fit1(xfit, *popt1)
yfit2 = fit2(xfit, *popt2)

# trial
a = 12.75
str_trial = "TRIAL: 250. * (1. + 0.07 * numpy.log(1. + x / 250.) + {:.6g} * x)".format(a)
tri1 = fit2(xfit, a)
dif1 = abs(data[:, 1] - fit2(data[:, 0], a))

# plt.title("ds_normalized = 18 ln(h + 275) + 150")
plt.plot(data[:, 0], data[:, 1], "x", xfit, yfit2, xfit, tri1)
plt.legend(["data", str_fit2, str_trial], fontsize='xx-small')
plt.xlabel("happy")
plt.ylabel("gains")
plt.savefig("bs_formula_gains_vs_happy.png", dpi=320)
plt.clf()


plt.title(str_trial)
plt.plot(data[:, 0], dif1, "x")
plt.legend([f"mean: {numpy.mean(dif1):.4f} stats, std {numpy.std(dif1):.4f} stats"])
plt.xlabel("happy")
plt.ylabel("Difference in gains: data - trial")
plt.yscale("log")
plt.savefig("bs_formula_diff_vs_happy.png", dpi=320)
plt.clf()
