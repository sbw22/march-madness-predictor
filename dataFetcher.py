if __name__ == "__main__":     

  
    import time
    import csv
    import json
    import requests
    from bs4 import BeautifulSoup
    import cbbpy.mens_scraper as s


    def get_tourney_info():


        start_year = 2004  # First tournament year we are checking 
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
    

    def main():
        
        tourney_dict = get_tourney_info()

        for year in tourney_dict:   # Prints off all values in tourney_dict
            print(f"\n\n\n\nyear: {year}")
            year_dict = tourney_dict[f"{year}"]
            for team in year_dict:
                print(f"\nteam: {team}")
                print(year_dict[f"{team}"])



main()


