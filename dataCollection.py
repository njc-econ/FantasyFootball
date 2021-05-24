
# %% codecell

import urllib.request, json

teamNo = 5191452

# %% md


## General Team Data

# %% codecell

with urllib.request.urlopen("https://fantasy.premierleague.com/api/entry/"+str(teamNo)+"/") as url:
    teamData = json.loads(url.read().decode())

print(teamData)

# %%md

## Transfer Data

# %%codecell

with urllib.request.urlopen("https://fantasy.premierleague.com/api/entry/"+str(teamNo)+"/transfers/") as url2:
    transferData = json.loads(url2.read().decode())

print(transferData)

# %% md

## Collect Team Picks

# %% codecell

# first identify the start week for the team
firstWeek = teamData['started_event']

teamPicks = []

for i in range(1,39):
    with urllib.request.urlopen("https://fantasy.premierleague.com/api/entry/"+str(teamNo)+"/event/"+str(i)+"/picks/") as url3:
        teamPicks.append(json.loads(url3.read().decode()))

print(teamPicks[37])

# %% md

## Gameweek and Player History

# %% codecell

with urllib.request.urlopen("https://fantasy.premierleague.com/api/entry/"+str(teamNo)+"/history/") as url2:
    historyData = json.loads(url2.read().decode())

print(historyData)
