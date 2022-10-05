from datetime import datetime
this_yr = datetime.now().strftime("%Y")

def NFL_GameSchedule(Year = this_yr, Team = 'ALL'):

    from sportsipy.nfl.teams import Teams
    from sportsipy.nfl.schedule import Schedule
    from datetime import datetime
    import numpy as np
    import pandas as pd

    if Team == 'ALL':

        # Getting a list of all teams to cycle through
        team_abbr = Teams(year = Year).dataframes['abbreviation']

        # Create an empty dateframe to act as our master table that stores all the schedule rows
        all_games = pd.DataFrame()

        # Loop through every team to pull each team's schedule
        for team in team_abbr:

            # Use SportsReference's Schedule function to pull each team's games
            curr_team = Schedule(
                abbreviation = team,
                year = Year
            ).dataframe[
            # Keeping only certain columns
                [
                    'datetime',
                    'week',
                    'location',
                    'opponent_abbr',
                ]
            ]

            # Creating a column with the current team's abbreviation
            curr_team['team_abbr'] = [team] * len(curr_team)

            # Creating a column with the season that was queried
            curr_team['Season'] = [datetime.strptime(Year, '%Y').year] * len(curr_team)
            
            # Figuring out which team is the away team
            curr_team['AwayTeamID'] = np.select(
                [curr_team.location == 'Away'], 
                [curr_team.team_abbr], 
                default = curr_team.opponent_abbr
                )

            # Figuring out which team is the home team
            curr_team['HomeTeamID'] = np.select(
                [curr_team.location == 'Home'], 
                [curr_team.team_abbr], 
                default = curr_team.opponent_abbr
                )

            # Append this team's schedule to our master data table
            all_games = pd.concat([all_games, curr_team])

    else:
        # Use SportsReference's Schedule function to pull the current team's games
        all_games = Schedule(
            abbreviation = Team, 
            year = Year
        ).dataframe[
            # Keeping only certain columns
                [
                    'datetime',
                    'week',
                    'location',
                    'opponent_abbr',
                ]
            ]

        # Creating a column with the current team's abbreviation
        all_games['team_abbr'] = [Team] * len(all_games)

        # Creating a column with the season that was queried
        all_games['Season'] = [datetime.strptime(Year, '%Y').year] * len(all_games)
                        
        # Figuring out which team is the away team
        all_games['AwayTeamID'] = np.select(
            [all_games.location == 'Away'], 
            [all_games.team_abbr], 
            default = all_games.opponent_abbr
            )

        # Figuring out which team is the home team
        all_games['HomeTeamID'] = np.select(
            [all_games.location == 'Home'], 
            [all_games.team_abbr], 
            default = all_games.opponent_abbr
            )

    # Creating a crosswalk to join each team abbreviation to their full name
    TeamNameXwalk = Teams(year = Year).dataframes[['name']]

    # Use the crosswalk to bring in the team names for both the away and home teams
    all_games = all_games.merge( # Joining the away team's names from the crosswalk
            TeamNameXwalk, 
            how = 'left', 
            left_on = 'AwayTeamID', 
            right_index = True
        ).merge( # Joining the home team's names from the crosswalk
            TeamNameXwalk,
            how = 'left',
            left_on = 'HomeTeamID',
            right_index = True
        ).rename( # Renaming the columns to something prettier
            columns = {
                'datetime': 'DateTime',
                'week': 'Week',
                'name_x': 'AwayTeamName',
                'name_y': 'HomeTeamName'
                }
        )

    # Returning the final table sorted by date and getting rid of the duplicated game rows 
    return(
        all_games[
            ['DateTime',
            'Season',
            'Week',
            'AwayTeamID',
            'HomeTeamID',
            'AwayTeamName',
            'HomeTeamName']
        ].sort_values(
            by = 'DateTime'
        ).drop_duplicates()
    )
