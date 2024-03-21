import itertools
import random

_debug = False # * Set to True to print combinations
players = 3  # * Number of players from 2 to 6

factions = [
    {"name": "Marquise de Cat", "reach": 10},
    {"name": "Lord of the Hundreds", "reach": 9},
    {"name": "Keepers in Iron", "reach": 8},
    {"name": "Underground Duchy", "reach": 8},
    {"name": "Eyrie Dynasties", "reach": 7},
    {"name": "Vagabond (1st)", "reach": 5},
    {"name": "Riverfolk Company", "reach": 5},
    {"name": "Woodland Alliance", "reach": 3},
    {"name": "Corvid Conspiracy", "reach": 3},
    {"name": "Lizard Cult", "reach": 2},
]

viable = [17, 18, 21, 25, 28]


def generate_combinations(data_list, key, n, allow_repeats=False):
    combinations = []
    if allow_repeats:
        comb_func = itertools.combinations_with_replacement
    else:
        comb_func = itertools.combinations

    for indices in comb_func(range(len(data_list)), n):
        combination_names = [data_list[i][key] for i in indices]
        combination_reach = sum(data_list[i]["reach"] for i in indices)
        combination = {key: combination_names, "reach": combination_reach}
        combinations.append(combination)
    return combinations


if __name__ == "__main__":
    while True:
        selection = []
        tempPool = factions.copy()
        i = 0
        while len(selection) < players:
            if i > 0 and i < players - 1:
                combinations = generate_combinations(
                    tempPool, "name", players - len(selection)
                )
                if _debug:
                    print("Combinations:")
                    for comb in combinations:
                        print(comb)
                    print("")
                saved = []
                for comb in combinations:
                    if (
                        comb["reach"] + sum([faction["reach"] for faction in selection])
                        >= viable[players - 2]
                    ):
                        for faction in comb["name"]:
                            if faction not in saved:
                                saved.append(faction)
                for faction in tempPool:
                    if faction["name"] not in saved:
                        tempPool.remove(faction)
            faction = random.choice(tempPool)
            if faction["name"] == "Vagabond (1st)":
                tempPool.append({"name": "Vagabond (2nd)", "reach": 2})
            if faction not in selection:
                selection.append(
                    {
                        "player": i + 1,
                        "faction": faction["name"],
                        "reach": faction["reach"],
                    }
                )
                i += 1
                tempPool.remove(faction)

        if sum([faction["reach"] for faction in selection]) >= viable[players - 2]:
            # only print last selection
            if True:  # rep == reps-1:
                print(f"Results:")
                for faction in selection:
                    print(f"Player {faction['player']}: {faction['faction']}")
                print(
                    f"Total reach: {sum([faction['reach'] for faction in selection])}"
                )
                print("")
            break
