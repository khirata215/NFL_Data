def NFL_BettingInfo(Years = [2022], ToPickle = False, PickleFileLocation = './NFL_PlayByPlay.pkl'):
    import nfl_data_py as nfl
    import pandas as pd
    import numpy as np

    bi = nfl.import_schedules(years = Years)[
        ['game_id',
        'season',
        'game_type',
        'week',
        'gameday',
        'weekday',
        'gametime',
        'away_team',
        'away_score',
        'home_team',
        'home_score',
        'location',
        'result',
        'total',
        'away_moneyline',
        'home_moneyline',
        'spread_line',
        'away_spread_odds',
        'home_spread_odds',
        'total_line',
        'under_odds',
        'over_odds']
    ]
    bi.columns = bi.columns.str.title()
    bi.columns = bi.columns.str.replace('_', '')

    if ToPickle == True:
        bi.to_pickle(PickleFileLocation)
    
    else:
        return(bi)