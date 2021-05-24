# %% md

## Generate ranked list of participating teams with the code needed to collected their data

# %% codecell

import urllib.request, json


team_ids = []

for i in range(1,164424):
    with urllib.request.urlopen("https://fantasy.premierleague.com/api/leagues-classic/314/standings/?page_new_entries=1&page_standings="+str(i)+"&phase=1") as url:
        pageData = json.loads(url.read().decode())
    for team in pageData['standings']['results']:
        team_ids.append(team['entry'])

import numpy as np

ranked_ids = np.array(team_ids)
ranked_ids.tofile("ranked_ids_all")
ranked_ids[0:9999].tofile("ranked_ids_top10000")

# %% md

## remove the first 10000 then randomly sort the results
## can then use this randomly sorted list to

rest_ids = ranked_ids[10000:]

from numpy.random import default_rng

rng = default_rng(256)
rng.shuffle(rest_ids)

rest_ids.tofile("random_ids_not_top10000")
