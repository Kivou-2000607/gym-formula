"""
Play around
"""

import numpy
import matplotlib.pyplot as plt
import json
import requests

from gymlib import vladar

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
# trains = requests.get("http://yata.alwaysdata.net/tmp/gym?export=json").json()["trains"]


print(len(trains))
xy = numpy.array([[t["energy_used"], t["happy_delta"]] for t in trains if t["stat_before"] > 49999999])
# for train in trains:
#     delta_happy.append(train[""])
#     print(train)

# plt.xlabel("energy_used")
# plt.ylabel("happy_delta")
# plt.plot(xy[:, 0], xy[:, 1], "*")
# plt.savefig("plot_happydrop_vs_energyused.png")
# plt.clf()
#
# happydrop_per_e = -xy[:, 0] / xy[:, 1]
# bins = numpy.linspace(0, 5, 100)
#
# p, _ = numpy.histogram(happydrop_per_e, bins=bins)
# h = [0.5 * (a + b) for a, b in zip(bins[0:-1], bins[1:])]
#
# plt.xlabel("Happy drop / e")
# plt.ylabel("Frequency")
# plt.plot(h, p, "*")
# plt.savefig("hist_happydrop_per_e.png")
# plt.clf()
#
#
# x = []
# y = []
# z = []
# for train in trains:
#     energy = train.get("energy_used")
#     stat_before = train.get("stat_before")
#     happy_before = train.get("happy_before")
#     perks_keys = ["perks_faction", "perks_property", "perks_education_stat", "perks_education_all", "perks_company"]
#     b_perks = [1 + train.get(key) / 100. for key in perks_keys]
#     bonus = numpy.prod(b_perks) - 1
#     # bonus = numpy.sum([train.get(key) / 100. for key in perks_keys])
#     # print(bonus)
#     gym_dot = train.get("gym_dot") / 10.
#     gains = vladar(energy, stat_before, H=happy_before, B=bonus, G=gym_dot)
#     stat_delta = train.get("stat_delta")
#     error = abs(gains - stat_delta) / stat_delta
#
#     x.append(stat_before)
#     y.append(happy_before)
#     z.append(error * 100.)
# #
# # plt.xlabel("Stat")
# # plt.ylabel("Happy")
# # plt.scatter(x, y, c=z, alpha=0.5, vmin=0.0, vmax=1.)
# # plt.savefig("error_map.png", dpi=720)
# # plt.clf()
#
# plt.xlabel("Stat")
# plt.ylabel("Happy")
# plt.hist2d(x, y, bins=25, cmin=1)
# plt.colorbar().set_label("Frequency")
# plt.savefig("joint_histogram.png", dpi=720)
# plt.clf()
