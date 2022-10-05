from datetime import datetime
this_yr = datetime.now().strftime("%Y")

def NFL_GameStats(Year = this_yr, Team = 'ALL'):
    from sportsipy.nfl.teams import Teams
    from sportsipy.nfl.schedule import Schedule
    import numpy as np
    import pandas as pd

    if Team == 'ALL':
        # Getting a list of all teams to cycle through
        team_abbr = Teams(year = Year).dataframes['abbreviation']

        # Create an empty dateframe to act as our master table that stores all the schedule rows
        all_games = pd.DataFrame()

        # Loop through every team to pull each team's schedule
        for team in team_abbr:

            # Use SportsReference's Schedule function to pull the current team's games
            curr_team = Schedule(
                abbreviation = team,
                year = Year
            ).dataframe.dropna()

            # Creating a column with the current team's abbreviation
            curr_team['TeamID'] = [Team] * len(curr_team)

            # Creating a column with the season that was queried
            curr_team['Season'] = [datetime.strptime(Year, '%Y').year] * len(curr_team)

            # Append this team's schedule to our master data table
            all_games = pd.concat([all_games, curr_team])


    else:
        # Use SportsReference's Schedule function to pull the current team's games
        all_games = Schedule(abbreviation = Team, year = Year).dataframe.dropna()

        # Creating a column with the current team's abbreviation
        all_games['TeamID'] = [Team] * len(all_games)

        # Creating a column with the season that was queried
        all_games['Season'] = [datetime.strptime(Year, '%Y').year] * len(all_games)

    # Creating a crosswalk to join each team abbreviation to their full name
    TeamNameXwalk = Teams(year = Year).dataframes[['name']]

    # Use the crosswalk to bring in the team names for both the away and home teams
    all_games = all_games.merge( 
            # Joining the team's names from the crosswalk
            TeamNameXwalk, 
            how = 'left', 
            left_on = 'TeamID', 
            right_index = True
        ).rename( 
            # Renaming the columns to something prettier
            columns = {
                'datetime':                 'DateTime',
                'week':                     'Week',
                'type':                     'GameType',
                'name':                     'TeamName',
                'location':                 'HomeOrAway',
                'opponent_abbr':            'OpponentID',
                'opponent_name':            'OpponentName',
                'result':                   'Result',
                'overtime':                 'OvertimeFlag',
                'points_scored':            'PointsScored',
                'points_allowed':           'PointsAllowed',
                'time_of_possession':       'TimeOfPossession',
                'pass_completions':         'PassingCompletions',
                'pass_attempts':            'PassingAttempts',
                'pass_completion_rate':     'PassingCompletionRate',
                'pass_yards':               'PassingYards',
                'pass_yards_per_attempt':   'PassingYardsPerAttempt',
                'pass_touchdowns':          'PassingTouchdowns',
                'interceptions':            'PassingInterceptions',
                'quarterback_rating':       'PassingRating',
                'rush_attempts':            'RushingAttempts',
                'rush_yards':               'RushingYards',
                'rush_yards_per_attempt':   'RushingYardsPerAttempt',
                'third_down_conversions':   'ThirdDownConversions',
                'third_down_attempts':      'ThirdDownAttempts',
                'fourth_down_conversions':  'FourthDownConversions',
                'fourth_down_attempts':     'FourthDownAttempts',
                'field_goals_made':         'FieldGoalsMade',
                'field_goals_attempted':    'FieldGoalsAttempted',
                'extra_points_made':        'ExtraPointsMade',
                'extra_points_attempted':   'ExtraPointsAttempted',
                'punts':                    'Punts',
                'punt_yards':               'PuntYards',
                'times_sacked':             'TimesSacked',
                'yards_lost_from_sacks':    'YardsLostFromSacks'
                }
        )
        
    # Returning the final table sorted by date and getting rid of the duplicated game rows 
    return(
        all_games[
            ['DateTime',
            'Season',
            'Week',
            'GameType',
            'TeamID',
            'TeamName',
            'HomeOrAway',
            'OpponentID',
            'OpponentName',
            'Result',
            'OvertimeFlag',
            'PointsScored',
            'PointsAllowed',
            'TimeOfPossession',
            'PassingCompletions',
            'PassingAttempts',
            'PassingCompletionRate',
            'PassingYards',
            'PassingYardsPerAttempt',
            'PassingTouchdowns',
            'PassingInterceptions',
            'PassingRating',
            'RushingAttempts',
            'RushingYards',
            'RushingYardsPerAttempt',
            'ThirdDownConversions',
            'ThirdDownAttempts',
            'FourthDownConversions',
            'FourthDownAttempts',
            'FieldGoalsMade',
            'FieldGoalsAttempted',
            'ExtraPointsMade',
            'ExtraPointsAttempted',
            'Punts',
            'PuntYards',
            'TimesSacked',
            'YardsLostFromSacks']
        ].sort_values(
            by = 'DateTime'
        )
    )