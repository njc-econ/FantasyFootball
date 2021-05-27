
import pandas as pd

playerBasisData = pd.read_parquet("data/playerBasisData.parquet.gzip")

playerBasisData.head()

teamBasisData = pd.read_parquet("data/teamBasisData.parquet.gzip")

teamBasisData.head()

playerBasisData = playerBasisData.set_index(["team","team_code"]).join(teamBasisData.set_index(["id","code"]),on=["team","team_code"])


import pickle as pk

pickle_in = open("data/playerData.pickle", "rb")
playerData = pk.load(pickle_in)
pickle_in.close()

weeklyData = playerData['weeklyData']

weeklyDataList = []

for player in weeklyData:
    for week in player:
            weeklyDataList.append(week)

weeklyDataDF = pd.DataFrame(weeklyDataList)

historyDataList = []

historyData = playerData['historyData']

for player in historyData:
    for year in player:
            historyDataList.append(year)

historyDataDF = pd.DataFrame(historyDataList)


historyDataDF = historyDataDF.set_index("element_code").join(playerBasisData.set_index("code"))

weeklyDataDF = weeklyDataDF.set_index("element").join(playerBasisData.set_index("id"))

pointsAgainstTeams = weeklyDataDF[["opponent_team","total_points"]].groupby(by=["opponent_team"]).sum()

pointsAgainstTeams = pointsAgainstTeams.join(teamBasisData.set_index("id")).sort_values(by="total_points", ascending = True)
print(pointsAgainstTeams)


pointsAgainstTeamsByPos = weeklyDataDF[["opponent_team","element_type","total_points"]].groupby(by=["opponent_team","element_type"]).sum()


# %% md

## Identify any players that have changed clubs during the season and set the team for the fixture to the correct value

# %% codecell

noPlayers = weeklyDataDF.groupby(["fixture", "opponent_team","name","short_name"]).size()

noPlayersOver10 = pd.DataFrame(noPlayers[noPlayers>=10],columns=["noPlayers"]).reset_index()
noPlayersOver10.sort_values(by="noPlayers")
weeklyDataDF.keys()

weeklyDataDF_cleanTeam = weeklyDataDF.drop(["name","short_name"],axis=1).set_index(["fixture","opponent_team"]).join(noPlayersOver10.drop("noPlayers",axis=1).set_index(["fixture","opponent_team"]),on=["fixture","opponent_team"])

# %% md

## Which players have changed teams

# %% codecell

playerClubs = weeklyDataDF_cleanTeam.reset_index().groupby(["first_name","second_name","web_name","code"]).agg({"short_name":'nunique'}).rename(columns={'short_name':'no_clubs'})
multipleClubs = playerClubs.loc[playerClubs['no_clubs']>1]

print(multipleClubs)

# %% md
## Order clubs by points earned

# %% codecell

pointsForTeams = weeklyDataDF_cleanTeam.reset_index()[["short_name","name","total_points"]].groupby(["short_name","name"]).sum().sort_values(by="total_points", ascending = False)
print(pointsForTeams)

weeklyDataDF_cleanTeam.keys()

# %% md
## Check how values relate to those seen on the webpage
## Sam Johnstone had a value of 4.6m GBP
## Mo Salah had a value of 12.9m GBP

# %% codecell
print(
    weeklyDataDF_cleanTeam[(weeklyDataDF_cleanTeam['second_name']=='Johnstone') & (weeklyDataDF_cleanTeam['round']==38) ]['value']
)

print(
    weeklyDataDF_cleanTeam[(weeklyDataDF_cleanTeam['second_name']=='Salah') & (weeklyDataDF_cleanTeam['round']==38) ]['value']
)


# %% md
## Values are stored as integer, ten times recorded value

# %% codecell
weeklyDataDF_cleanTeam['value'] = weeklyDataDF_cleanTeam['value'] / 10

# %% md
## Value distribution

# %% codecell

import matplotlib.pyplot as plt

for i in weeklyDataDF_cleanTeam['element_type'].unique():
    plt.hist(weeklyDataDF_cleanTeam[weeklyDataDF_cleanTeam['element_type'] == i]['value'])

for i in weeklyDataDF_cleanTeam['element_type'].unique():
    plt.hist(weeklyDataDF_cleanTeam[weeklyDataDF_cleanTeam['element_type'] == i]['total_points'])

# %% md
## Value per point when players play

# %% codecell

playersPointValue = weeklyDataDF_cleanTeam[weeklyDataDF_cleanTeam['minutes']>0].groupby(['second_name','first_name','element_type']).agg(
    {'total_points':'sum','value':'mean'}
)

playersPointValue['pointPerMillion'] = playersPointValue['total_points']/playersPointValue['value']
playersPointValue = playersPointValue.reset_index()

for i in weeklyDataDF_cleanTeam['element_type'].unique():
    print(playersPointValue[playersPointValue['element_type']==i].sort_values(by='pointPerMillion', ascending=False).head(20))

playersPointValue.sort_values(by='pointPerMillion', ascending=False).head(20)
