# Building play-by-play data function
def NFL_PlayByPlay(Years = [2022], ToPickle = False, PickleFileLocation = './NFL_PlayByPlay.pkl'):
    import nfl_data_py as nfl
    import pandas as pd
    import numpy as np

    #   Import play by play data
    pbp = nfl.import_pbp_data(years = Years)
    
    #   Format column names by capitalizing first letters after underscore
    pbp.columns = pbp.columns.str.title()
    #   Get rid of underscore to pascal case column names
    pbp.columns = pbp.columns.str.replace('_', '')

    #   Exporting to a .pkl file if desired
    if ToPickle == True:
        pbp.to_pickle(PickleFileLocation)

    #   Else just returning it locally as a dataframe
    else:
        return(pbp)