# Building weekly player data function
def NFL_WeeklyPlayer(Years = [2022], ToPickle = False, PickleFileLocation = './NFL_WeeklyPlayer.pkl'):
    import nfl_data_py as nfl
    import pandas as pd
    import numpy as np

    #   Import weekly data, already at the offensive player level
    wp = nfl.import_weekly_data(years = Years)

    #   Format column names by capitalizing first letters after underscore
    wp.columns = wp.columns.str.title()
    #   Get rid of underscore to pascal case column names
    wp.columns = wp.columns.str.replace('_', '')
    #   Force rename some columns with abbreviations that I want capitalized
    wp = (wp
        .rename(columns = {
            'PassingEpa'    :   'PassingEPA',
            'RushingEpa'    :   'RushingEPA',
            'ReceivingEpa'  :   'ReceivingEPA',
            'Pacr'          :   'PACR',
            'Racr'          :   'RACR',
            'Wopr'          :   'WOPR',
            }
        )
    )

    #   Exporting to a .pkl file if desired
    if ToPickle == True:
        wp.to_pickle(PickleFileLocation)
    
    #   Else just returning it locally as a dataframe
    else:
        return(wp)