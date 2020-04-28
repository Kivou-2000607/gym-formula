"""
Just to play arround with the inverse function that gives the energy needed
to reach a stat goal.
"""

import numpy
import matplotlib.pyplot as plt

from gymlib import bs_e

si = 0
sf = sc

# Minimal energy for normalisation
Hmax = 5025
Bmax = 1.02 * 1.1 * 1.02 - 1.
Gmax = 7.5
Emin = bs_e(si, sf, H=Hmax, B=Bmax, G=Gmax)

# Happy
x_tab = numpy.arange(250, 5026, 25)
e_tab = bs_e(si, sf, H=x_tab, B=Bmax, G=Gmax)
eta = e_tab / Emin

plt.xlabel("Happy")
plt.ylabel("Energy factor")
plt.plot(x_tab, eta)
plt.savefig("happy.png")
plt.clf()

# Gym
x_tab = numpy.arange(2.0, 7.6, 0.1)
e_tab = bs_e(si, sf, H=Hmax, B=Bmax, G=x_tab)
eta = e_tab / Emin

plt.xlabel("Gym")
plt.xlabel("Energy factor")
plt.plot(x_tab, eta)
plt.savefig("gym.png")
plt.clf()

# # Bonus
# x_tab = numpy.arange(2.0, 7.6, 0.1)
# e_tab = bs_e(si, sf, H=Hmax, B=Bmax, G=x_tab)
# eta = e_tab / Emin
#
# plt.xlabel("Gym")
# plt.xlabel("Energy factor")
# plt.plot(x_tab, eta)
# plt.savefig("gym.png")
# plt.clf()
