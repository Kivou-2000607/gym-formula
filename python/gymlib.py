"""
Library for the gym calculations
"""

import numpy
import matplotlib.pyplot as plt

# coefficients
a = 0.0000003480061091
b = 250.
c = 0.000003091619094
d = 0.0000682775184551527
e = -0.0301431777

# stat cap
sc = 50000000


def vladar(energy, so, H=250, B=0.0, G=1.0):

    # states coefficients
    alpha = (a * numpy.log(H + b) + c) * (1. + B) * G
    beta = (d * (H + b) + e) * (1. + B) * G

    stat_cap = float(min(so, sc))

    return (alpha * stat_cap + beta) * energy


def bs_s(energy, so, H=250, B=0.0, G=1.0, verbose=False):
    """Returns the stat given:
        energy: the energy spent in gym
        so: the initial stat
        H: the happy
        B: the gym perks bonus
        G: the gym dot bonus

        note: only works for pre cap (gives 0 gains for post cap)
    """

    # states coefficients
    alpha = (a * numpy.log(H + b) + c) * (1 + B) * G
    beta = (d * (H + b) + e) * (1 + B) * G

    # shortcuts
    ratio = numpy.divide(beta, alpha)
    slope = alpha * sc + beta

    bc = so < sc
    reached_cap = False
    s = 0

    if bc:
        s = numpy.multiply(so + ratio, numpy.exp(energy * alpha)) - ratio
        reached_cap = s > sc
    else:
        return 0

    if verbose == 1:
        print(f"h = {H:.4g}, b = {B:.4g}, g = {G:.4g}")
    elif verbose == 2:
        print("=== Battle stats formula ===")
        print("")
        print("= States variables =")
        print(f"Happy: {H:.4g}")
        print(f"Bonus: {B:.4g}")
        print(f"Gym dot: {G:.4g}")
        print("")
        print("= States coefficients =")
        print(f"alpha: {alpha:.4g}")
        print(f"beta: {beta:.4g}")
        print(f"ratio: {ratio:.4g}")
        print(f"slope: {slope:.4g}")
        print("")
        print("= CAP =")
        print(f"so: {so:,.1f}")
        print(f"Before CAP: {bc}")
        print(f"Reached CAP: {reached_cap}")
        print("= Variables =")
        print(f"e: {energy:,.1f}")
        print(f"s: {s:,.1f}")

    return s

def bs_e(si, sf, H=250, B=0.0, G=1.0, verbose=False):
    """Returns the energy needed given:
        si: the initial stat
        so: the final stat
        H: the happy
        B: the gym perks bonus
        G: the gym dot bonus

        note: it account automatically account for pre/post cap
    """

    # states coefficients
    alpha = (a * numpy.log(H + b) + c) * (1 + B) * G
    beta = (d * (H + b) + e) * (1 + B) * G

    # shortcuts
    minf = min(sc, sf)
    mini = min(sc, si)
    maxf = max(sc, sf)
    maxi = max(sc, si)
    ratio = numpy.divide(beta, alpha)
    slope = alpha * sc + beta

    # energy before cap
    dE_bc = numpy.divide(numpy.log(numpy.divide(minf + ratio, mini + ratio)), alpha)
    # print(dE_bc[0], numpy.log((minf + ratio) / (mini + ratio))[0], alpha[0])
    # energy after cap
    dE_ac = numpy.divide(maxf - minf, slope)
    # energy total
    dE = dE_bc + dE_ac

    if verbose == 1:
        print(f"h = {H:.4g}, b = {B:.4g}, g = {G:.4g}")
    elif verbose == 2:
        print("=== Battle stats formula ===")
        print("")
        print("= States variables =")
        print(f"Happy: {H:.4g}")
        print(f"Bonus: {B:.4g}")
        print(f"Gym dot: {G:.4g}")
        print("")
        print("= States coefficients =")
        print(f"alpha: {alpha:.4g}")
        print(f"beta: {beta:.4g}")
        print("")
        print("= Energy =")
        print(f"Before CAP: {dE_bc:,.1f}")
        print(f"After CAP: {dE_ac:,.1f}")
        print(f"Total: {dE:,.1f}")

    return dE


def normalize_cap(train, type="+"):
    perks_keys = ["perks_faction", "perks_property", "perks_education_stat", "perks_education_all", "perks_company"]

    if type == "x":
        b_perks = [1 + train.get(key) / 100. for key in perks_keys]
        bonus = numpy.prod(b_perks) - 1
    else:
        bonus = numpy.sum([train.get(key) / 100. for key in perks_keys])

    gym_dot = train.get("gym_dot") / 10.

    return (1. + bonus) * gym_dot * float(train["energy_used"])
