from datetime import datetime
this_yr = datetime.now().strftime("%Y")

def NFL_YearStats(YearBegin, YearEnd = this_yr):
    from sportsipy.nfl.teams import Teams
    from sportsipy.nfl.schedule import Schedule
    import numpy as np
    import pandas as pd

    if int(YearBegin) > int(YearEnd):
        raise ValueError('YearBegin must be less than YearEnd')

    else:
        years = range(int(YearBegin), int(YearEnd) + 1)

        all_years = pd.DataFrame()

        for yr in years:
            curr_year = Teams(year = str(yr)).dataframes

            curr_year['Season'] = [datetime.strptime(str(yr), '%Y').year] * len(curr_year)

            all_years = pd.concat([all_years, curr_year])
    
    all_years = (
        all_years
            .rename(
                columns = {
                    'abbreviation':                     'TeamID',
                    'name':                             'TeamName',
                    'rank':                             'Rank',
                    'post_season_result':               'PostSeasonResult',
                    'games_played':                     'GamesPlayed',
                    'wins':                             'Wins',
                    'losses':                           'Losses',
                    'win_percentage':                   'WinPercentage',
                    'strength_of_schedule':             'StrengthOfSchedule',
                    'points_for':                       'PointsFor',
                    'points_against':                   'PointsAgainst',
                    'points_difference':                'PointsMargin',
                    'points_contributed_by_offense':    'PointsContributedByOffense',
                    'simple_rating_system':             'SimpleRatingSystem',
                    'defensive_simple_rating_system':   'SimpleRatingSystemDefense',
                    'offensive_simple_rating_system':   'SimpleRatingSystemOffense',
                    'plays':                            'Plays',
                    'yards':                            'Yards',
                    'yards_per_play':                   'YardsPerPlay',
                    'first_downs':                      'FirstDowns',
                    'penalties':                        'Penalties',
                    'turnovers':                        'Turnovers',
                    'yards_from_penalties':             'YardsFromPenalties',
                    'first_downs_from_penalties':       'FirstDownsFromPenalties',
                    'percent_drives_with_points':       'PercentOfDrivesWithPoints',
                    'percent_drives_with_turnovers':    'PercentOfDrivesWithTurnover',
                    'pass_completions':                 'PassingCompletions',
                    'pass_attempts':                    'PassingAttempts',
                    'pass_yards':                       'PassingYards',
                    'pass_net_yards_per_attempt':       'PassingYardsPerAttempt',
                    'pass_touchdowns':                  'PassingTouchdowns',
                    'pass_first_downs':                 'PassingFirstDowns',
                    'interceptions':                    'Interceptions',
                    'rush_attempts':                    'RushingAttempts',
                    'rush_yards':                       'RushingYards',
                    'rush_yards_per_attempt':           'RushingYardsPerAttempt',
                    'rush_touchdowns':                  'RushingTouchdowns',
                    'rush_first_downs':                 'RushingFirstDowns',
                    'fumbles':                          'Fumbles'
                }
            )
    )

    return(
        all_years[
            [
                'TeamID',
                'TeamName',
                'Season',
                'Rank',
                'PostSeasonResult',
                'GamesPlayed',
                'Wins',
                'Losses',
                'WinPercentage',
                'StrengthOfSchedule',
                'PointsFor',
                'PointsAgainst',
                'PointsMargin',
                'PointsContributedByOffense',
                'SimpleRatingSystem',
                'SimpleRatingSystemDefense',
                'SimpleRatingSystemOffense',
                'Plays',
                'Yards',
                'YardsPerPlay',
                'FirstDowns',
                'Penalties',
                'Turnovers',
                'YardsFromPenalties',
                'FirstDownsFromPenalties',
                'PercentOfDrivesWithPoints',
                'PercentOfDrivesWithTurnover',
                'PassingCompletions',
                'PassingAttempts',
                'PassingYards',
                'PassingYardsPerAttempt',
                'PassingTouchdowns',
                'PassingFirstDowns',
                'Interceptions',
                'RushingAttempts',
                'RushingYards',
                'RushingYardsPerAttempt',
                'RushingTouchdowns',
                'RushingFirstDowns',
                'Fumbles'
            ]
        ].sort_values(
            by = [
                'Season',
                'TeamName'
                ]
            )
    )