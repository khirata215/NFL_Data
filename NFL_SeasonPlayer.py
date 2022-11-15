# Building weekly player data function
def NFL_SeasonPlayer(Years = [2022], IncludePostseason = False, ToPickle = False, PickleFileLocation = './NFL_SeasonPlayer.pkl'):
    import nfl_data_py as nfl
    import pandas as pd
    import numpy as np

    #   If postseason rows are desired, just pull in data as is
    if IncludePostseason == True:
        wk = nfl.import_weekly_data(years = Years)
    
    #   If not, we'll only keep those for the regular season
    else:
        wk = nfl.import_weekly_data(years = Years)
        wk = wk.loc[wk['season_type'] == 'REG']

    #   Data is at the player/season/week level, aggregating to be at the player/season level  
    sp = (wk
        .groupby(
            ['player_id',
            'player_name',
            'player_display_name',
            'position', 
            'position_group', 
            'headshot_url', 
            'recent_team', 
            'season']
        )
            ['completions',
            'attempts',
            'passing_yards',
            'passing_air_yards',
            'passing_yards_after_catch',
            'passing_tds',
            'passing_2pt_conversions',
            'interceptions',
            'passing_first_downs',
            'sacks',
            'sack_yards',
            'sack_fumbles',
            'sack_fumbles_lost',
            'carries',
            'rushing_yards',
            'rushing_tds',
            'rushing_2pt_conversions',
            'rushing_fumbles',
            'rushing_fumbles_lost',
            'rushing_first_downs',
            'targets',
            'receptions',
            'receiving_yards',
            'receiving_tds',
            'receiving_2pt_conversions',
            'receiving_fumbles',
            'receiving_fumbles_lost',
            'receiving_air_yards',
            'receiving_yards_after_catch',
            'receiving_first_downs',
            # 'target_share',
            # 'air_yards_share',
            'special_teams_tds',
            'passing_epa',
            'rushing_epa',
            'receiving_epa',
            'pacr',
            'dakota',
            'racr',
            'wopr',
            'fantasy_points',
            'fantasy_points_ppr'
            ]
        .sum()
        .reset_index()
        )

    #   Format column names by capitalizing first letters after underscore
    sp.columns = sp.columns.str.title()
    #   Get rid of underscore to pascal case column names
    sp.columns = sp.columns.str.replace('_', '')
    #   Force rename some columns with abbreviations that I want capitalized
    sp = (sp
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
        sp.to_pickle(PickleFileLocation)
    
    #   Else just returning it locally as a dataframe
    else:
        return(sp)