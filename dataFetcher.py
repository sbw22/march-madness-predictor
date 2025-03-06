if __name__ == "__main__":     

  
    import time
    import csv
    import json
    import requests
    from bs4 import BeautifulSoup
    import cbbpy.mens_scraper as s


    def get_tourney_info():


        start_year = 2023  # First tournament year we are checking  (tourneys before 2007 didn't track advanced metrics) 
        year = start_year   # year variable that increments through the for loop
        end_year = 2024      # First tournament year we are not checking
        year_len = end_year - start_year   # length of time we are checking

        tourney_dict = dict() # dictionary that holds all the data from the ncaa tourney

        # year_dict[f"{team}"] = dict()
        


        for i in range(year_len):  # for loop that looks through the ncaa tourneys

            if year == 2020 or year == 2021 or year == 2005:  # Skips 2020 year, becuase it was canceled because of covid. Skips 2021 year (for now) because a game was not played. Idk why 2005 is messed up (something with UNC).
                year += 1
                continue 

            year_str = f"{year}"    # string version of the year variable

            file_path = f'data/revised_tourney_results/corrected_{year_str}_tourney.csv'  # file path to the tourney results tables csv
            
            tourney_dict[year_str] = dict() # creates a new key and value pair in the ncaa tourney results dictionary



            year_dict = tourney_dict[year_str]




            with open(file_path, 'r') as tourney_stats:   # Opens csv file


                tourney_data = csv.reader(tourney_stats, delimiter=',')    # assigns csv to a variable
                next(tourney_data) # Skips the headers
                next(tourney_data)

                for game in tourney_data:   # iterates through every row in the ncaa tourney table for that year to find teams 

                    # print(f"{year_str} row = {game}, data type = {type(game)}")  # prints every row in the table

                    game_string = game[2]   # assigns game_string variable to the string describing the two teams ()
                    game_list = game_string.split(" ")  # Converts the game_string to a list

                    round = game[1]  # round the current game is in

                    vs_index = game_list.index("vs.")

                    team1_seed = game_list[0][1]   # seed of team 
                    team1 = " ".join(game_list[1:vs_index])   # team name
                    team2_seed = game_list[vs_index+1][1]    # seed of opponent
                    team2 = " ".join(game_list[vs_index+2:])    # oppenents team name
                    score = game[3] # score of the game

                    if score == "0-0":
                        continue
                    
                    try:   # finds scores of each team in the game
                        subt = len(score)-3
                        score1 = int(score[0:subt])
                        score2 = int(score[subt+1:])
                    except:
                        subt = len(score)-4
                        score1 = int(score[0:subt])
                        score2 = int(score[subt+1:])



                    team1_result = True if score1 > score2 else False  # win or loss stat for teams
                    team2_result = False if score1 > score2 else True


                    teams = [team1, team2]

                    team1_stats = [team1_result, team1, team2, score] # list that (for now, might add seeds and win variables) holds teams and score of the game
                    team2_stats = [team2_result, team1, team2, score]

                    
                    
                    if round == "First Round":   # creates a dictionary for the team if they havent been found aleady
                        year_dict[team1] = dict()
                        year_dict[team2] = dict()

                    # print(f"year = {year}")

                    team1_dict = year_dict[team1] # Assigns the team dictionary to team1_dict variable
                    team2_dict = year_dict[team2]

                    team1_dict[f"{round}"] = team1_stats  # assigns game info to the team dictionary
                    team2_dict[f"{round}"] = team2_stats
                    

            year += 1  # Increments the year by 1

        return tourney_dict

    def getRegSeasonInfo(tourney_dict):

        empty_teams = []

        ## Loop through tourney info
        ## For every year: 
            ## Find team in tourney
            ## Find team's regular season stats
            ## Append list of team's regular season stats to teams dictionary
            ## Repeat for every team in tourney

        for year in tourney_dict: # loops through every year in the tourney dictionary
            print(f"year = {year}")
            year_dict = tourney_dict[f"{year}"]
            # print(f"year_dict = {year_dict}")

            for team in year_dict:
                # print(f"team = {team}")
                team_dict = year_dict[f"{team}"]
                #print(f"team_dict = {team_dict}")

        
                file_path = f"data/regular_season_data/regular_season_(4-3-25).csv"

                with open(file_path, 'r') as season_file:
                
                    season_data = csv.reader(season_file, delimiter=',')    # assigns csv to a variable
                    next(season_data)  # Skips the headers
                    next(season_data)

                    pre_len = len(team_dict)

                    for _team in season_data:
                        if (_team[136] == f"{team}" and _team[0] == f"{year}") or ("Connecticut" == f"{team}" and _team[136] == "UConn" and _team[0] == f"{year}"):  # if team in dictionary == team in table on same year, get table info to dictionary
                            # print(f"full team name: {_team[137]} in year {year}")

                            team_info_list = [_team[4], _team[6], _team[8], _team[10], _team[12], _team[18], _team[20], _team[22], _team[24], _team[26], _team[28], _team[30], _team[32], _team[34], _team[36], _team[38], _team[40], _team[42], _team[44], _team[46], _team[48], _team[50], _team[52], _team[54], _team[56], _team[58], _team[60],  _team[62], _team[64], _team[66], _team[68], _team[70], _team[72], _team[74], _team[76], _team[78], _team[85], _team[87], _team[89], _team[91], _team[93], _team[95],  _team[97], _team[99], _team[101], _team[103], _team[105], _team[107], _team[109], _team[111], _team[113], _team[115], _team[117], _team[119], _team[121], _team[123], _team[125],  _team[127], _team[129], _team[131], _team[133]]
                            # above list cotains all data points from regular season

                            team_dict["regSeason"] = team_info_list   # Puts the regular season info in the same dictionary as the tourney round info
                            # print(f"team dict regSeason info = {team_dict["regSeason"]}")
                            
                            
                            continue

                    if len(team_dict) == pre_len: # If we can't find the team in the regular season database, assign regSeason data to False (might try to find a way to access the data later).
                        # print(f" team = {team_dict}")
                        empty_teams.append(f"{team}")
                        team_dict["regSeason"] = False 


        return empty_teams   # returns teams with no regular season data
    
    
    def verifyGames(empty_teams, tourney_dict):   # Makes sure both teams in a game have regular season stats
        print("empty teams:")
        for team in empty_teams:
            print(team)
        
        for year in tourney_dict: # loops through every year in the tourney dictionary
            print(f"year = {year}")
            year_dict = tourney_dict[f"{year}"]
            # print(f"year_dict = {year_dict}")

            for team in year_dict:

                team_dict = year_dict[f"{team}"]

                for game in team_dict:   # Loops through each game a team played in the tourney to verify they played a team with regular season stats (that we can access)
                    if game == "regSeason":  # prints all rounds for a team and skips the regSeason array in team_dict
                        continue

                    team1 = team_dict[game][1]
                    team2 = team_dict[game][2]
                    teams = [team1, team2]
                    opp = team1 if team1 != team else team2  # Finds the opponent in a game
                    
                    if opp in empty_teams or team in empty_teams:    # If the team or team's opponent does not have regular season stats, do NOT verify the game
                        is_verified = False   
                        team_dict[game].append(is_verified) 
                    else:                                           # If both teams in the game have regular season stats, verify the game
                        is_verified = True
                        team_dict[game].append(is_verified)
                    
                    

    
    def sortGames(tourney_dict):
        i = 0
        counter = f"game{i}"

        verified_dict = dict()

        for year in tourney_dict: # loops through every year in the tourney dictionary
            print(f"year = {year}")
            year_dict = tourney_dict[f"{year}"]
            # print(f"year_dict = {year_dict}")

            for team in year_dict:

                team_dict = year_dict[f"{team}"]

                for game in team_dict:

                    if team_dict["regSeason"] == False or game == "regSeason":
                        continue

                    score = team_dict[game][3]

                    # print(f"score = {score}")

                    try:   # finds scores of each team in the game
                        subt = len(score)-3
                        score1 = int(score[0:subt])
                        score2 = int(score[subt+1:])
                    except:
                        subt = len(score)-4
                        score1 = int(score[0:subt])
                        score2 = int(score[subt+1:])

                    scores = [score1, score2]  # Keeps both the scores in a list

                    print(f"scores = {scores}")

                    # Maybe add [ [regSeason_of_team1, regSeasonOfTeam2], [team1_score, team2_score] ] list to verified_dict()?

                      


                        
                
                    

        
        
        
                


    

    def main():
        
        tourney_dict = get_tourney_info()

        empty_teams = getRegSeasonInfo(tourney_dict)

        verifyGames(empty_teams, tourney_dict)  # Makes sure both teams in a game have regular season stats

        # maybe make a function that makes a dictionary containing games and teams in those games, to make it easier to put games into the model?
        # Make sure teams are from the same tourney/year. 

        sortGames(tourney_dict)

        '''
        for year in tourney_dict:   # Prints off all values in tourney_dict
            print(f"\n\n\n\nyear: {year}")
            year_dict = tourney_dict[f"{year}"]
            for team in year_dict:
                print(f"\nteam: {team}")
                print(year_dict[f"{team}"])
        '''



main()


