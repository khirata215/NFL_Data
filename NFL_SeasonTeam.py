# Building weekly team data function
def NFL_SeasonTeam(Years = [2022], IncludePostseason = False, ToPickle = False, PickleFileLocation = './NFL_WeeklyTeam.pkl'):
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
    
    #   Data is at the player/season/week level, aggregating to be at the team/season level  
    st = (wk
            .groupby(['recent_team','season'])
                [   'completions',
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

    #   We also want some info on the game, notably things like the final score
    sch = nfl.import_schedules(years = [2022])
    #   We have a row for each matchup, but if we want a row for each team, the away and home teams need their own rows
    #   Here we take the schedule and rename it so the away team is the focus
    sch_away = (sch
        .rename(columns = {
            'away_team':        'team',
            'home_team':        'opponent',
            'away_score':       'points_scored',
            'home_score':       'points_allowed',
            'away_moneyline':   'team_moneyline',
            'home_moneyline':   'opponent_moneyline',   
            'away_spread_odds': 'team_spread_odds',
            'home_spread_odds': 'opponent_spread_odds',
            'away_qb_id':       'team_qb_id',
            'home_qb_id':       'opponent_qb_id',
            'away_qb_name':     'team_qb_name',
            'home_qb_name':     'opponent_qb_name',
            'away_coach':       'team_coach',
            'home_coach':       'opponent_coach'
            }
        )
        .assign(team_home_away = 'Away')
    )

    #   Same thing again, but the home team is the focus
    sch_home = (sch
        .rename(columns = {
            'away_team':        'opponent',
            'home_team':        'team',
            'away_score':       'points_allowed',
            'home_score':       'points_scored',
            'away_moneyline':   'opponent_moneyline',
            'home_moneyline':   'team_moneyline',   
            'away_spread_odds': 'opponent_spread_odds',
            'home_spread_odds': 'team_spread_odds',
            'away_qb_id':       'opponent_qb_id',
            'home_qb_id':       'team_qb_id',
            'away_qb_name':     'opponent_qb_name',
            'home_qb_name':     'team_qb_name',
            'away_coach':       'opponent_coach',
            'home_coach':       'team_coach'
            }
        )
        .assign(team_home_away = 'Home')
    )

    #   Now we stack the home and away tables are combined
    sch  = pd.concat([
        sch_away[sch_away['points_scored'].notna()],
        sch_home[sch_home['points_scored'].notna()]
        ])

    #   Now we have to aggregate the game info data so that it's at the same level as our season/team level data
    #   If postseason is desired, we'll group by and aggregate without filtering
    if IncludePostseason == True:
        tm = (sch
            .assign(scoring_margin = sch.points_scored - sch.points_allowed)
            .groupby(['team', 'season'], sort = 'False')['points_scored','points_allowed','scoring_margin']
            .agg(
                games_played = ('points_scored', 'count'),
                points_scored = ('points_scored', 'sum'),
                points_allowed = ('points_allowed', 'sum'),
                scoring_margin = ('scoring_margin', 'sum')
                # 'points_scored' :  ['count','sum'],
                # 'points_allowed' : 'sum',
                # 'scoring_margin' : 'sum'
                )
            .reset_index()
            )
    #   Otherwise, we'll only keep regular season rows first before aggregating
    else:    
        tm = (sch
            .loc[sch['game_type'] == 'REG']
            .assign(scoring_margin = sch.points_scored - sch.points_allowed)
            .groupby(['team', 'season'], sort = 'False')['points_scored','points_allowed','scoring_margin']
            .agg(
                games_played = ('points_scored', 'count'),
                points_scored = ('points_scored', 'sum'),
                points_allowed = ('points_allowed', 'sum'),
                scoring_margin = ('scoring_margin', 'sum')
                # 'points_scored' :  ['count','sum'],
                # 'points_allowed' : 'sum',
                # 'scoring_margin' : 'sum'
                )
            .reset_index()
            )

    #   Take the team stats, left joining the game info
    final_df = (st
            .merge(
                tm, 
                how = 'left', 
                left_on = ['recent_team','season'],
                right_on = ['team', 'season']
            )
        )
    
    #   Format column names by capitalizing first letters after underscore
    final_df.columns = final_df.columns.str.title()
    #   Get rid of underscore to pascal case column names
    final_df.columns = final_df.columns.str.replace('_', '')
    #   Force rename some columns with abbreviations that I want capitalized
    final_df = (final_df
        .rename(columns = {
            'PassingEpa'    :   'PassingEPA',
            'RushingEpa'    :   'RushingEPA',
            'ReceivingEpa'  :   'ReceivingEPA',
            'Pacr'          :   'PACR',
            'Racr'          :   'RACR',
            'Wopr'          :   'WOPR',
            'Gsis'          :   'GSIS',
            'Pfr'           :   'PFR',
            'Pff'           :   'PFF',
            'Espn'          :   'ESPN'
            }
        )
    )

    #   Exporting to a .pkl file if desired
    if ToPickle == True:
        final_df.to_pickle(PickleFileLocation)
    
    #   Else just returning it locally as a dataframe
    else:
        return(final_df)