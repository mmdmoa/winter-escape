import json
import os
here = os.path.abspath(".") + "/"

def load_level(level_n):
    with open(here+f"assets/levels/level {level_n}.json", "r") as file:
        level = json.loads("".join(file.readlines()))

    return level
