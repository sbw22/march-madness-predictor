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
        end_year = 2023      # Last tournament year we are checking
        year_len = end_year - start_year   # length of time we are checking

        tourney_dict = dict() # dictionary that holds all the data from the ncaa tourney

        for i in range(4, 5):  # for loop that looks through the ncaa tourneys

            if year == 2020:  # Skips 2020 year, becuase it was canceled because of covid
                year += 1
                continue 

            year_str = f"{year}"    # string version of the year variable

            file_path = f'data/chat_tourney_results/{year_str}_March_Madness_Full_Results_With_Final4.csv'  # file path to the tourney results tables csv

            tourney_dict[year_str] = dict() # creates a new key and value pair in the ncaa tourney results dictionary

            year_dict = tourney_dict[year_str]

            with open(file_path, 'r') as tourney_stats:   # Opens csv file
                tourney_data = csv.reader(tourney_stats, delimiter=',')    # assigns csv to a variable
                next(tourney_data) # Skips the header
                for game in tourney_data:   # iterates through every row in the ncaa tourney table for that year

                    # print(f"{year_str} row = {game}, data type = {type(game)}")  # prints every row in the table

                    game_string = game[2]   # assigns game_string variable to the string describing the two teams ()


                    game_list = game_string.split(" ")  # Converts the game_string to a list

                    round = game[1]  # round the current game is in

                    team_seed = game_list[0][1]   # seed of team 
                    team = game_list[1]   # team name
                    opp_seed = game_list[3][1]    # seed of opponent
                    opp_team = " ".join(game_list[4:])    # oppenents team name
                    score = game[3] # score of the game

                    game_stats = [team, opp_team, score] # list that (for now, might add seeds and win variables) holds teams and score of the game

                    year_dict[f"{team}"] = dict()

                    team_dict = year_dict

                    team_dict[f"{round}"] = []
                    round_list = team_dict[f"{round}"]
                    round_list.extend(game_stats)







                   

                    # tourney_year[""]


                    

            year += 1

        return tourney_dict
    

    def main():
        
        tourney_dict = get_tourney_info()

        print(tourney_dict)





    


main()










'''


key = "8nm9CtzeicYltsEkboHv1bGDKGnFBtDku8BdZc8n2C6qDg5l23iPLpO9QwZ2tL9i"
url = "https://www.ncaa.com/scoreboard/basketball-men/d1"

headers = {"Authorization": f"Bearer {key}"}

response = requests.get(url)

data = response.json()
print(response.text)
print(data)



iowa_state_game_info = s.get_game_info('401725710')
iowa_state_game_boxscore = s.get_game_boxscore('401725710')

stretch = s.get_games_range('11-30-2022', '12-10-2022')

# print(iowa_state_game_info)
# print(iowa_state_game_boxscore)

print(stretch)
'''