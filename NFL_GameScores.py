def NFL_GameScores(Years = [2022], ToPickle = False, PickleFileLocation = './NFL_PlayByPlay.pkl'):
    import nfl_data_py as nfl
    import pandas as pd
    import numpy as np

    #   Importing schedule, only keeping relevant score data
    gs = nfl.import_schedules(years = Years)[
        [
        'game_id',
        'season',
        'game_type',
        'week',
        'gameday',
        'away_team',
        'away_score',
        'home_team',
        'home_score']
    ]
    
    #   Format column names by capitalizing first letters after underscore
    gs.columns = gs.columns.str.title()
    #   Get rid of underscore to pascal case column names
    gs.columns = gs.columns.str.replace('_', '')

    #   Exporting to a .pkl file if desired
    if ToPickle == True:
        gs.to_pickle(PickleFileLocation)
    
    #   Else just returning it locally as a dataframe
    else:
        return(gs)