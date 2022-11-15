def NFL_BettingInfo(Years = [2022], ToPickle = False, PickleFileLocation = './NFL_PlayByPlay.pkl'):
    import nfl_data_py as nfl
    import pandas as pd
    import numpy as np

    #   Importing schedule data, keeping relevant betting info
    bi = nfl.import_schedules(years = Years)[
        'game_id',
        'season',
        'game_type',
        'week',
        'gameday',
        'weekday',
        'gametime',
        'away_team',
        'away_score'
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
    
    #   Format column names by capitalizing first letters after underscore
    bi.columns = bi.columns.str.title()
    #   Get rid of underscore to pascal case column names
    bi.columns = bi.columns.str.replace('_', '')

    #   Exporting to a .pkl file if desired
    if ToPickle == True:
        bi.to_pickle(PickleFileLocation)
    
    #   Else just returning it locally as a dataframe
    else:
        return(bi)