"""
Play around
    id: 319
    id_key: x
    timestamp: 1588322707
    time_diff: 0
    happy_before: 180
    happy_after: 165
    happy_delta: -15
    energy_used: 25
    single_train: 1
    stat_type: speed
    stat_before: 50000000
    stat_after: 50000000
    stat_delta: 55647.1946
    gym_id: 26
    gym_dot: 75
    perks_faction: 10
    perks_property: 2
    perks_education_stat: 1
    perks_education_all: 1
    perks_company: 0
    perks_company_happy_red: 0
    perks_gym_book: 0
    perks_happy_book: 0
    error: 42.9330838465321
    req: {}
    pk: 319
    normalized_gain_add: 259.32773921452116
    normalized_gain_mul: 259.30231741869585
    vladar: 55816.63874624658
    vladar_diff: -169.44414624657657
    current: 55690.127683846535
    current_diff: -42.9330838465321
"""

import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import requests
from scipy.optimize import curve_fit
from scipy.optimize import minimize

from gymlib import normalize_cap

trains_row = json.load(open("../json/trains.json", 'r'))["trains"]
gyms = json.load(open("../json/gyms.json", 'r'))
ignore = [487, 319, 4764]
# ignore = [4764]
trains = [train for train in trains_row if train["pk"] not in ignore]

a = 12.75
b = 200000. * 0.015
b = 0
str_trial = "dS = (S * (1. + 0.07 * ln(1. + h / 250.)) + {:.4g} * h ) / 200000.".format(a)


def trial(happy, stat, a=12.75, b=0):
    return (min(stat, 50000000) * numpy.round(1. + 0.07 * numpy.log(1. + happy / 250.), 4) + a * happy + b) / 200000.
    # return (min(stat, 50000000) * (1. + 0.07 * numpy.log(1. + happy / 250.)) + a * happy) / 200000.


def diff(train, a=12.75, b=0):
    return train["normalized_gain_mul"] - trial(train["happy_before"], train["stat_before"], a=a, b=b)
    # return train["normalized_gain_mul"] - iter_ds(train["happy_before"], train["stat_before"], train["energy_used"], a=a, b=b)


def n_train(t):
    gyms = json.load(open("../json/gyms.json", 'r'))["gyms"]
    print(gyms[t["gym_id"]])


def iter_ds(train):
    inc_stat = train["stat_before"]
    inc_happy = train["happy_before"]
    energy_used = float(train["energy_used"])
    energy_gym = float(gyms[str(train["gym_id"])]["energy"])
    n_train = int(energy_used / energy_gym)
    total_ds = 0
    for i, _ in enumerate(range(n_train)):
        ds = trial(inc_happy, inc_stat, a)
        inc_happy -= 0.5 * energy_gym
        inc_stat += ds
        total_ds += ds
    return total_ds


trains_gym = [t for t in trains if t["gym_id"] == 24 and t["single_train"] == 0]
print(iter_ds(trains_gym[0]), trial(trains_gym[0]["happy_before"], trains_gym[0]["stat_before"]))
exit()

trains_spe = numpy.array([[t["happy_before"], diff(t, a=a, b=b)] for t in trains_gym if t["stat_type"] == "speed"])
trains_dex = numpy.array([[t["happy_before"], diff(t, a=a, b=b)] for t in trains_gym if t["stat_type"] == "dexterity"])
trains_def = numpy.array([[t["happy_before"], diff(t, a=a, b=b)] for t in trains_gym if t["stat_type"] == "defense"])
trains_str = numpy.array([[t["happy_before"], diff(t, a=a, b=b)] for t in trains_gym if t["stat_type"] == "strength"])

plt.title("Multiple trains")
plt.plot(trains_spe[:, 0], trains_spe[:, 1], "x", alpha=0.5)
plt.plot(trains_def[:, 0], trains_def[:, 1], "x", alpha=0.5)
plt.plot(trains_dex[:, 0], trains_dex[:, 1], "x", alpha=0.5)
plt.plot(trains_str[:, 0], trains_str[:, 1], "x", alpha=0.5)
# plt.legend([f"PRE: mean={numpy.mean(diffPRE):.4f} / std={numpy.std(diffPRE):.4f}", f"CAP: mean={numpy.mean(diffCAP):.4f} stats / std={numpy.std(diffCAP):.4f}"])
plt.xlabel("happy")
plt.ylabel("Difference in gains: data - trial")
plt.xlim([0, 12000])
# plt.ylim([-0.02, 0.02])
plt.grid()
plt.legend(["Speed", "Defense", "Dexterity", "Stength"])
plt.savefig(f"bs_formula_diff_vs_happy.png", dpi=320)
plt.clf()


# ext = ""
# xyCAP = numpy.array([[t["happy_before"], t["normalized_gain_mul"], trial(t["happy_before"], t["stat_before"], a), t["stat_before"], t["energy_used"]] for t in trains if t["stat_before"] > 49999999])
# xyPRE = numpy.array([[t["happy_before"], t["normalized_gain_mul"], trial(t["happy_before"], t["stat_before"], a), t["stat_before"], t["energy_used"]] for t in trains if t["stat_before"] < 50000000])
# # ext = "__iter"
# # xyCAP = numpy.array([[t["happy_before"], t["normalized_gain_mul"], iter_ds(t["happy_before"], t["stat_before"], a, t["energy_used"]), t["stat_before"], t["energy_used"]] for t in trains if t["stat_before"] > 49999999])
# # xyPRE = numpy.array([[t["happy_before"], t["normalized_gain_mul"], iter_ds(t["happy_before"], t["stat_before"], a, t["energy_used"]), t["stat_before"], t["energy_used"]] for t in trains if t["stat_before"] < 50000000])
#
# diffCAP = numpy.abs(xyCAP[:, 1] - xyCAP[:, 2])
# diffPRE = numpy.abs(xyPRE[:, 1] - xyPRE[:, 2])
# plt.title(str_trial)
# plt.plot(xyPRE[:, 0], diffPRE, "x", xyCAP[:, 0], diffCAP, "+", alpha=0.5)
# plt.legend([f"PRE: mean={numpy.mean(diffPRE):.4f} / std={numpy.std(diffPRE):.4f}", f"CAP: mean={numpy.mean(diffCAP):.4f} stats / std={numpy.std(diffCAP):.4f}"])
# plt.xlabel("happy")
# plt.ylabel("Difference in gains: data - trial")
# plt.yscale("log")
# plt.savefig(f"bs_formula_absdiff_vs_happy{ext}.png", dpi=320)
# plt.clf()
#
# plt.title(str_trial)
# plt.plot(xyPRE[:, 3], diffPRE, "x", xyCAP[:, 3], diffCAP, "+", alpha=0.5)
# plt.legend([f"PRE: mean={numpy.mean(diffPRE):.4f} / std={numpy.std(diffPRE):.4f}", f"CAP: mean={numpy.mean(diffCAP):.4f} stats / std={numpy.std(diffCAP):.4f}"])
# plt.xlabel("total stat")
# plt.ylabel("Difference in gains: data - trial")
# plt.yscale("log")
# plt.savefig(f"bs_formula_absdiff_vs_stat{ext}.png", dpi=320)
# plt.clf()
#
# diffCAP = xyCAP[:, 1] - xyCAP[:, 2]
# diffPRE = xyPRE[:, 1] - xyPRE[:, 2]
# plt.title(str_trial)
# plt.plot(xyPRE[:, 0], diffPRE, "x", xyCAP[:, 0], diffCAP, "+", alpha=0.5)
# plt.legend([f"PRE: mean={numpy.mean(diffPRE):.4f} / std={numpy.std(diffPRE):.4f}", f"CAP: mean={numpy.mean(diffCAP):.4f} stats / std={numpy.std(diffCAP):.4f}"])
# plt.xlabel("happy")
# plt.ylabel("Difference in gains: data - trial")
# plt.savefig(f"bs_formula_diff_vs_happy{ext}.png", dpi=320)
# plt.clf()
#
# plt.title(str_trial)
# plt.plot(xyPRE[:, 3], diffPRE, "x", xyCAP[:, 3], diffCAP, "+", alpha=0.5)
# plt.legend([f"PRE: mean={numpy.mean(diffPRE):.4f} / std={numpy.std(diffPRE):.4f}", f"CAP: mean={numpy.mean(diffCAP):.4f} stats / std={numpy.std(diffCAP):.4f}"])
# plt.xlabel("total stat")
# plt.ylabel("Difference in gains: data - trial")
# plt.savefig(f"bs_formula_diff_vs_stat{ext}.png", dpi=320)
# plt.clf()
#
# plt.title(str_trial)
# plt.plot(xyPRE[:, 4], diffPRE, "x", xyCAP[:, 4], diffCAP, "+", alpha=0.5)
# plt.legend([f"PRE: mean={numpy.mean(diffPRE):.4f} / std={numpy.std(diffPRE):.4f}", f"CAP: mean={numpy.mean(diffCAP):.4f} stats / std={numpy.std(diffCAP):.4f}"])
# plt.xlabel("Energy spent")
# plt.ylabel("Difference in gains: data - trial")
# plt.savefig(f"bs_formula_diff_vs_energy{ext}.png", dpi=320)
# plt.clf()
#
# plt.title(str_trial)
# plt.plot(xyPRE[:, 0], xyPRE[:, 1], "s", xyCAP[:, 0], xyCAP[:, 1], "sg", xyCAP[:, 0], xyCAP[:, 2], "r.", xyPRE[:, 0], xyPRE[:, 2], "r.")
# plt.legend([f"data pre", "data cap", "trial"])
# plt.xlabel("happy")
# plt.ylabel("Normalized gains dS")
# # plt.yscale("log")
# plt.savefig(f"bs_formula_gains_vs_happy{ext}.png", dpi=320)
# plt.clf()
#
#
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# # ax.title(str_trial, fontsize="small")
# ax.scatter(xyPRE[:, 3] / 1e6, xyPRE[:, 0], diffPRE, c=diffPRE)
# # ax.scatter(xyCAP[:, 3] / 1e6, xyCAP[:, 0], diffCAP)
# ax.set_ylabel("happy")
# ax.set_xlabel("Total stats [x1e6]")
# ax.set_zlabel("error = dS - trial")
# # ax.set_colorbar().set_label("dS - trial")
# # ax.set_zscale("log")
# fig.savefig(f"bs_formula_error_3D{ext}.png", dpi=320)
# # fig.show()
