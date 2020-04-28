"""
Go through all the gyms to unlock george and compute the energy needed.

It trains for a gym:
1. the best dot bonus
2. the lowest stat

In case of equality it takes what the sorting function gives... so randomish

TODO:
- train different stats of same dot bonus for a same gym to endup with more
balanced stats at the end for the gym (doesn't mean more balanced stats at the end)
- account for (standard) happy evolution throughout the gyms
(start at 250 finish at 4500)

"""

import numpy
import matplotlib.pyplot as plt
import json

from gymlib import bs_s

gyms = json.load(open("../json/gyms.json", 'r'))

# s = bs_s(100, 0, H=250, B=0.0, G=1.0, verbose=2)

stats = {"strength": 0, "defense": 0, "speed": 0, "dexterity": 0}

for k, v in [(k, v) for (k, v) in gyms.items() if v["unlock_e"]]:
    print(f'== Gym {v["name"]}: energy spent {v["unlock_e"]} ==')

    # get gyms dots
    max_gym_dot = 0
    for k in stats:
        max_gym_dot = max(max_gym_dot, int(v[k]))
    max_gym_key = [k for k in stats if int(v[k]) == max_gym_dot]
    for k in stats:
        print(f'\t*{k:>12} = {v[k]:,.0f}{"*" if k in max_gym_key else "":>2}')
    print("")

    # sorted stats for max_gym
    sorted_stats = [k for k, v in sorted(stats.items(), key=lambda x: x[1]) if k in max_gym_key]
    train_stat = sorted_stats[0]

    for k in stats:
        print(f'\t*{k:>10} = {stats[k]:>15,.2f}{"*" if k in max_gym_key else "":>2}{" <- train" if k == train_stat else ""}')
    print("")


    G = 0.1 * max_gym_dot
    ds = bs_s(v["unlock_e"], stats[train_stat], H=4500, B=0.0, G=G)

    print(f'\t*{train_stat:>10}  = {stats[train_stat]:>15,.2f}')
    print(f'\t*{train_stat:>10} += {ds:>15,.2f}')
    print(f'\t*{train_stat:>10}  = {stats[train_stat] + ds:>15,.2f}')
    stats[train_stat] += ds
    print("")


print("== Final stats when unlocking George ==")
sum = 0
for k, v in stats.items():
    sum += v
    print(f'\t*{k:>10} = {v:>15,.2f}')
print(f'\t*{"---":>10}')
print(f'\t*{"total":>10} = {sum:>15,.2f}')
    # break
