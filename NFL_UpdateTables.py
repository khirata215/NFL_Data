import os
def NFL_UpdateTables(YearStart, YearEnd = 2022, FolderLocation = os.getcwd(), TableExclude = ['NFL_PlayByPlay']):
    import os
    import sys
    sys.path.append("C:/Users/khira/OneDrive/Documents/GitHub/NFL_Data")
    from NFL_BettingInfo import NFL_BettingInfo
    from NFL_GameInfo import NFL_GameInfo
    from NFL_GameScores import NFL_GameScores
    from NFL_PlayByPlay import NFL_PlayByPlay
    from NFL_SeasonPlayer import NFL_SeasonPlayer
    from NFL_SeasonTeam import NFL_SeasonTeam
    from NFL_WeekTeam import NFL_WeekTeam
    from NFL_WeekPlayer import NFL_WeekPlayer
    
    os.chdir(FolderLocation)
    yrs = range(YearStart, YearEnd + 1)

    if 'NFL_BettingInfo' not in TableExclude:
        NFL_BettingInfo(Years = yrs, ToPickle = True)
    else:
        pass    

    if 'NFL_GameInfo' not in TableExclude:
        NFL_GameInfo(Years = yrs, ToPickle= True)
    else:
        pass

    if 'NFL_GameScores' not in TableExclude:
        NFL_GameScores(Years = yrs, ToPickle=True)
    else:
        pass

    if 'NFL_PlayByPlay' not in TableExclude:
        NFL_PlayByPlay(Years = yrs, ToPickle=True)
    else:
        pass

    if 'NFL_SeasonPlayer' not in TableExclude:
        NFL_SeasonPlayer(Years = yrs, ToPickle=True)
    else:
        pass

    if 'NFL_SeasonTeam' not in TableExclude:
        NFL_SeasonTeam(Years = yrs, ToPickle=True)
    else:
        pass

    if 'NFL_WeekTeam' not in TableExclude:
        NFL_WeekTeam(Years=yrs, ToPickle=True)
    else:
        pass

    if 'NFL_WeekPlayer' not in TableExclude:
        NFL_WeekPlayer(Years=yrs, ToPickle=True)
    else:
        pass

    print('NFL Table Updates Successful!')
