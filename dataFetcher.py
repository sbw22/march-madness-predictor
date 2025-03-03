if __name__ == "__main__":     

  
    import time
    import csv
    import json
    import requests
    from bs4 import BeautifulSoup
    import cbbpy.mens_scraper as s



    



    def get_tourney_info():


        start_year = 2007  # First tournament year we are checking 
        year = start_year   # year variable that increments through the for loop
        end_year = 2023      # Last tournament year we are checking
        year_len = end_year - start_year   # length of time we are checking

        tourney_dict = dict() # dictionary that holds all the data from the ncaa tourney

        # year_dict[f"{team}"] = dict()
        


        for i in range(year_len):  # for loop that looks through the ncaa tourneys

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
                    
                    try:
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

                    

                    if round == "First Round": 
                        year_dict[team1] = dict()
                        year_dict[team2] = dict()

                    team1_dict = year_dict[team1]
                    team2_dict = year_dict[team2]

                    team1_dict[f"{round}"] = team1_stats
                    team2_dict[f"{round}"] = team2_stats
                    

                    # year_dict[f"{team1}"][f"{round}"] = game_stats

                    

                    '''

                    team_dict[f"{round}"] = []

                    round_list = team_dict[f"{round}"]

                    round_list.extend(game_stats)

                    print(f"team_dict length  = {len(team_dict)}")

                    '''

                    # print(round_list)







                   

                    # tourney_year[""]


                    

            year += 1

        return tourney_dict
    

    def main():
        
        tourney_dict = get_tourney_info()

        for year in tourney_dict:
            print(f"year: {year}")
            year_dict = tourney_dict[f"{year}"]
            for team in year_dict:
                print(f"team: {team}")
                print(year_dict[f"{team}"])

        # print(f"tourney_dict = {tourney_dict}")





    


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