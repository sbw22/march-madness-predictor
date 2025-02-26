if __name__ == "__main__":     
    from bs4 import BeautifulSoup
    import requests
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    import time
    import csv
    import json
    import requests
    from bs4 import BeautifulSoup
    import cbbpy.mens_scraper as s



    



    def get_tourney_info():


        start_year = 2003
        year = start_year
        year_str = f"{year}"
        end_year = 2024
        year_len = end_year - start_year

        tourney_dict = dict()

        for i in range(year_len):
            tourney_dict[year_str] = dict()

            
            website = f'https://www.sports-reference.com/cbb/postseason/men/{year}-ncaa.html'

            '''
            path = "/usr/local/bin/chromedriver"
            service = Service(executable_path=path)
            driver = webdriver.Chrome(service=service)
            driver.get(website)


            east_b = driver.find_element(By.CLASS_NAME, 'team16')
            round = east_b.find_element(By.CLASS_NAME, 'round')
            games = round.find_elements(By.TAG_NAME, 'div')

            '''
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(website, headers=headers)

            soup = BeautifulSoup(response.text, "html.parser")

            print("******************************************************************")

            overall_div = soup.find('div', id='east')
            #current_tab = overall_div.find('div', class_='current')
            #east_b = current_tab.find('div', class_="team16")
            # games = east_b.find('div')

            print(overall_div)

            '''
            for game in games:
                print('######################################################################')
                # print(game)
                teams = game.find('div')
                # if teams[0].get('class') == "winner":
                _type = type(teams)
                print(f"teams type = {_type}")
                if _type == type(1):
                    print(f"teams text = {teams}")
                else:
                    print(f"teams text = {teams.text}")

            '''
            # print(east_b)


            '''
            for game in games:
                for team in teams:
                    print(team.text)

                print(f"end of game")

            '''

            # print(east_b.text)

            return

            start += 1

            driver.quit()

        return tourney_dict
    
    get_tourney_info()




    













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