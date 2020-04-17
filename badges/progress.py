import os
import re
from itertools import zip_longest  # in py3, this is renamed zip_longest
from collections import Sequence
import anybadge

regex = re.compile(r"\[(?:( )|([-\/])|([xX]))\]")

with open("README.md") as readme:
    matches = [
        i for i in
        [re.findall(regex, line) for line in readme]
        if len(i) > 0
    ]


def flatten(nested_list):
    return list(zip(*_flattengen(nested_list)))  # in py3, wrap this in list())


def _flattengen(iterable):
    for element in zip_longest(*iterable, fillvalue=""):
        if isinstance(element[0], Sequence) \
                and not isinstance(element[0], str):
            yield from _flattengen(element)
        else:
            yield element


matches = flatten(matches)

total = len(matches)
incomplete = len([i[0] for i in matches if len(i[0]) > 0])
working = len([i[1] for i in matches if len(i[1]) > 0])
done = len([i[2] for i in matches if len(i[2]) > 0])
progress = int((done * 2 + working) / (total * 2) * 100)

print(
    "incomplete: {}\nworking: {}\ndone: {}\n\nProgress: {}%".format(
        incomplete, working, done,
        progress
        ))

# Generate badge

thresholds = {
    10: 'red',
    30: 'orange',
    50: 'yellow',
    80: 'green',
    100: 'lime'
}

badge = anybadge.Badge('progress', progress, thresholds=thresholds,
                       value_suffix='%')

badge_path = 'badges/progress.svg'
if os.path.exists(badge_path):
    os.remove(badge_path)
badge.write_badge(badge_path)
