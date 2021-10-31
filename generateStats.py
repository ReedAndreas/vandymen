import numpy as np
import pandas as pd

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

import django
django.setup()

stats = pd.read_csv('data/vandymen_stats.csv')
stats = stats.drop(['Unnamed: 11', 'League Leader'], axis = 1)

teams = '''Bishop Sycamore
Captains and Civilians
Daddy Day Care
Flaming Balls, The
Gus Bus, The
Hole Patrol, The
Hojat's Heroes
Killas, The
Rooks, The
Seatte Seamen, The
Silly Salmon, The
Southside Sluggers, The
Wiffle House
Wiffle Women, The'''
teams = teams.split('\n')

abvs = 'BS CAC DAD FB GB HP HH K R SSM SAL SSL WH WW'.split()

abvs_dict = {a[0]:a[1] for a in list(zip(teams, abvs))}

df = pd.read_csv('data/vandymen_teams.csv')

df.columns = ['Division', 'NL', 'W1', 'L1', 'WP', 'nothing' , 'Division2', 'AL', 'W2', 'L2', 'WP2']

team_data = []

for index, row in df.iterrows():
    if row['NL'] in teams:
        team_data.append({'name': row['NL'], 'W': float(row['W1']), 'L': float(row['L1']), 'division': 'NL', 'gp': float(row['L1']) + float(row['W1'])})
        print(row['NL'])

    if row['AL'] in teams:
        team_data.append({'name': row['AL'], 'W': float(row['W2']), 'L': float(row['L2']), 'division': 'AL', 'gp': float(row['L2']) + float(row['W2'])})
        print(row['AL'])

stats = stats.rename(columns={'Unnamed: 0': 'name'})

curr_team = teams[0]
stats['team'] = stats['name'].apply(lambda x : '')
for index, row in stats.iterrows():
    if row['name'] in teams:
        curr_team = row['name']
    else:
        row['team'] = curr_team

for index, row in stats.iterrows():
    if row['name'] in teams:
        stats.drop(index, inplace = True)

stats = stats[stats['name'].notna()]

columns = list(stats.columns)

columns.remove('team')
columns.remove('name')
for index, row in stats.iterrows():
    for c in columns:
        row[c] = float(row[c])

stats = stats.fillna(0)

def calculateOBS(hits, walks, ab):
    if ab == 0:
        return 0
    return round((hits + walks) / (ab + walks), 3)

def calculateSlug(single, double, triple, hr, ab):
    if (ab == 0):
        return 0
    return round ((single + 2*double + 3*triple + 4*hr) / ab, 3)

stats['OBP'] = stats.apply(lambda x : calculateOBS(x['H'], x['BB'], x['AB']), axis = 1)
stats['SP'] = stats.apply(lambda x : calculateSlug(x['H'] - x['HR'] - x['3B'] - x['2B'], x['2B'], x['3B'], x['HR'], x['AB']), axis = 1)
stats['OPS'] = stats.apply(lambda x : x['OBP'] + x['SP'], axis = 1)

week1 = pd.read_csv('data/week1copy.csv')
week1 = week1[week1['Team'].notna()]

teams1 = '''Bishop Sycamore
Captains and Civilians
Daddy Day Care
Flaming Balls
Gus Bus
Hole Patrol
Hojat's Heroes
Killas
Rooks
Seatte Seamen
Silly Salmon
Southside Sluggers
Wiffle House
Wiffle Women'''
teams1 = teams1.split('\n')

teams2 = '''Bishop Sycamore
Captains and Civilians
Daddy Day Care
Flaming Balls, The
Gus Bus, The
Hole Patrol, The
Hojat's Heroes
Killas, The
Rooks, The
Seatte Seamen, The
Silly Salmon, The
Southside Sluggers, The
Wiffle House
Wiffle Women, The'''
teams2 = teams2.split('\n')

teamKeys = {x: y for x, y in zip(teams1, teams2)}

def convertInt(s):
    possible_runs = [str(x) for x in range(0,20)]
    if s in possible_runs:
        return int(s)
    else:
        return None

week1['R'] = week1['R'].apply(convertInt)

def calcAvgRuns(teamName):
    n = 0
    runs = 0
    for index, row in week1.iterrows():
        if row['Team'] == teamName:
            if row['R'] != None:
                n += 1
                runs += row['R']
    if n == 0:
        return 0
    return runs/n

def calcAvgRunsAllowed(teamName):
    n = 0
    ra = 0
    matchup = False
    for index, row in week1.iterrows():
        if '@' in row['Team']:
            splitNames = row['Team'].split('@')
            if splitNames[0][:len(splitNames[0])-1] == teamName or splitNames[1][1:] == teamName:
                matchup = True
            else:
                matchup = False
        if row['Team'] != teamName and row['Team'] in teams and matchup:
            if row['R'] != None:
                n += 1
                ra += row['R']
    if n == 0:
        return 0
    return ra/n

avgRunsAllowed = {}
avgRuns = {}
for t, y in teamKeys.items():
    avgRunsAllowed[y] = calcAvgRunsAllowed(t)
    avgRuns[y] = calcAvgRuns(t)




from statsApp.models import Player, Team
print('generating')
for t in team_data:
    Team.objects.get_or_create(name = t['name'], wins = t['W'], losses = t['L'], division = t['division'], gp = t['gp'], abv = abvs_dict[t['name']])

for index, row in stats.iterrows():
    Player.objects.get_or_create(name = row['name'], gp = row['GP'], ab = row['AB'], h = row['H'], db = row['2B'], tr = row['3B'],
                                hr = row['HR'], rbi = row['RBI'], k = row['K'], bb = row['BB'], ba = row['BA'], obp = row['OBP'],
                                sp = row['SP'], ops = row['OPS'], team = Team.objects.get(name = row['team']))
