# %% codecell

import urllib.request, json

with urllib.request.urlopen("https://fantasy.premierleague.com/api/bootstrap-static/") as url:
    playerData = json.loads(url.read().decode())

print(playerData.keys())

print(playerData['teams'][0].keys())
print(len(playerData['teams']))


# %% md

### No of players with data

# %% codecell

print(len(playerData['elements']))

print(playerData['elements'][301])

for element in playerData['elements']:
    if element['id'] == 302:
        print(element)
