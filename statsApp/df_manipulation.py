import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def get_df(players):
    players_list = []
    for p in list(players):
        players_list.append(p.__dict__)
    return pd.DataFrame(players_list)


def get_erg(players, teams):
    df = get_df(players)

    df = df[df['ab'] > 5]

    team_data = []
    for t in teams:
        num_players = 0
        vals = {'aH': 0, 'aHR' : 0, 'aR' : 0}
        for index, row in df[df['team_id'] == t.pk].iterrows():
            vals['aH'] += row['h']
            vals['aHR'] += row['hr']
            vals['aR'] += row['rbi']
            num_players += 1
        vals['aH'] /= num_players
        vals['aHR'] /= num_players
        vals['aR'] /= num_players
        team_data.append(vals)

    team_data_df = pd.DataFrame(team_data)

    X = team_data_df.drop('aR', axis = 1)

    y = team_data_df['aR']

    lr = LinearRegression()
    lr.fit(X, y)

    simple_players = df[['name','ab','ba', 'hr']]
    simple_players['hr'] = simple_players.apply(lambda x : x['hr']/x['ab'] if x['ab'] > 0 else 0, axis = 1)

    simple_players = simple_players.drop(['name', 'ab'], axis = 1)
    df = df.reset_index().drop('index', axis = 1)
    simple_players.columns = ['aH', 'aHR']
    predictions = lr.predict(simple_players)
    df['E_Runs_Generated'] = pd.DataFrame(predictions)
    df['E_Runs_Generated'] = df.apply(lambda x : x['E_Runs_Generated'] + np.power(x['rbi'], 1/10), axis = 1)

    return df.sort_values('E_Runs_Generated', ascending = False)
