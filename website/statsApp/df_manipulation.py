import numpy as np
import pandas as pd

def get_df(players):
    players_list = []
    for p in list(players):
        players_list.append(p.__dict__)
    return pd.DataFrame(players_list)
