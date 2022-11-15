# Building play-by-play data function
def NFL_GameInfo(Years = [2022], ToPickle = False, PickleFileLocation = './NFL_PlayByPlay.pkl'):
    import nfl_data_py as nfl
    import pandas as pd
    import numpy as np

    # Importing schedule, only keeping relevant game info, scores and betting info will be in another function
    gi = nfl.import_schedules(years = Years)[
        [
        'game_id',
        'season',
        'game_type',
        'week',
        'gameday',
        'weekday',
        'gametime',
        'away_team',
        'home_team',
        'location',
        'old_game_id',
        'gsis',
        'nfl_detail_id',
        'pfr',
        'pff',
        'espn',
        'away_rest',
        'home_rest',
        'div_game',
        'roof',
        'surface',
        'temp',
        'wind',
        'away_qb_id',
        'home_qb_id',
        'away_qb_name',
        'home_qb_name',
        'away_coach',
        'home_coach',
        'referee',
        'stadium_id',
        'stadium']
    ]
    
    #   Format column names by capitalizing first letters after underscore
    gi.columns = gi.columns.str.title()
    #   Get rid of underscore to pascal case column names
    gi.columns = gi.columns.str.replace('_', '')
    #   Force rename some columns with abbreviations that I want capitalized
    gi = (gi
        .rename(columns = {
            'Gsis'  :   'GSIS',
            'Pfr'   :   'PFR',
            'Pff'   :   'PFF',
            'Espn'  :   'ESPN'
            }
        )
    )

    #   Exporting to a .pkl file if desired
    if ToPickle == True:
        gi.to_pickle(PickleFileLocation)
    
    #   Else just returning it locally as a dataframe
    else:
        return(gi)