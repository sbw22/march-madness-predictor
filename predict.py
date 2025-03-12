#  SOMETHING IS WRONG WITH TEAMSCORE IN THE PRINTING OF THE PREDICTIONS, IT IS 1 OFF (OR SOMETHING LIKE THAT)
if __name__ == "__main__":
    
    import numpy as np
    import random
    from random import randint
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.model_selection import train_test_split
    import keras
    from keras import backend as K
    from keras.models import Sequential, Model
    from keras.layers import Activation
    from tensorflow.keras.layers import Input, Dense, Flatten, Dropout, Conv2D, MaxPool2D, GlobalAveragePooling2D, BatchNormalization, Concatenate
    from keras.optimizers import Adam
    from keras.metrics import categorical_crossentropy
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras.layers import BatchNormalization
    from tensorflow.keras.layers import *
    from keras.models import Model
    from keras.applications import imagenet_utils
    from keras.preprocessing import image
    import matplotlib.pyplot as plt 
    from sklearn.metrics import confusion_matrix
    import itertools
    from joblib import load
    import pickle
    import csv
    # from keras.utils.vis_utils import plot_model
    # %matplotlib inline
    import os
    import json
    import joblib
    # import nbimporter
    
    
    
    def makeModel(team_stats, opp_stats, team_scores, opp_scores):

     # Define two inputs
        input_1 = Input(shape=(61,))
        input_2 = Input(shape=(61,))

        # Concatenate them
        merged = Concatenate()([input_1, input_2])

        # Define layers
        x = Dense(16, activation='relu')(merged)
        x = Dropout(0.1)(x)
        x = BatchNormalization()(x)

        x = Dense(32, activation='relu')(x)
        x = Dropout(0.1)(x)
        x = BatchNormalization()(x)

        x = Dense(64, activation='relu')(x)
        x = Dropout(0.1)(x)
        x = BatchNormalization()(x)

        x = Dense(128, activation='relu')(x)
        x = Dropout(0.1)(x)
        x = BatchNormalization()(x)


        x = Dense(64, activation='relu')(x)
        x = Dropout(0.1)(x)
        x = BatchNormalization()(x)

        x = Dense(32, activation='relu')(x)
        x = Dropout(0.1)(x)
        x = BatchNormalization()(x)

        x = Dense(16, activation='relu')(x)

        # Output layer
        output = Dense(2, activation='linear')(x)

        # Define model
        model = Model(inputs=[input_1, input_2], outputs=output)


        model.compile(Adam(learning_rate=0.0002), loss='mean_squared_error', metrics=['mae'])


        # Reshaping here for some reason, even though I thought these scores were already reshaped. will have to look at this later
        # team_scores = team_scores.reshape(-1, 1)  # Reshape to (num_samples, 1)
        # opp_scores = opp_scores.reshape(-1, 1)    # Reshape to (num_samples, 1)

        
        labels = np.concatenate([team_scores, opp_scores], axis=1)


        model.fit([team_stats, opp_stats], labels, validation_split=0.1, batch_size=10, epochs=400, shuffle=True, verbose=2)

        return model
    




    
    def predict(point_scaler, model, test_team_stats, test_opp_stats, test_team_names, test_opp_names, test_years=[], test_team_scores=[], test_opp_scores=[]):
        
        scores_len = -1
        if type(test_team_scores) != int:
            scores_len = len(test_team_scores)

        predictions_1 = model.predict([test_team_stats, test_opp_stats], batch_size=1, verbose=0)
        predictions_2 = model.predict([test_opp_stats, test_team_stats], batch_size=1, verbose=0)
        # Add a predictions 2 here that switches the sports of test_team_stats and team_opp_stats to make sure the model isn't biasing the first team

        total_guesses = len(test_opp_names)
        true_guesses = 0

        team_right_scores = []
        team_left_scores = []
        opp_right_scores = []
        opp_left_scores = []


        for i, guess in enumerate(predictions_1):  # Rescales predicted scores to a readable value

            # print(f"pre-guess guess = {guess}")
            guess_1 = guess[0]
            guess_2 = guess[1]
            # print(f"pre_guess 1 = {guess[0]}, pre_guess 2 = {guess[1]}")
 
            guess_1_reshaped = guess_1.reshape(-1,1)  # Reshape to (1, 1) for inverse_transform
            guess_2_reshaped = guess_2.reshape(-1,1)  # Reshape to (1, 1) for inverse_transform


            # Inverse transform the prediction
            guess_1 = point_scaler.inverse_transform(guess_1_reshaped)
            guess_2 = point_scaler.inverse_transform(guess_2_reshaped)


            # getting integer value from numpy arrays

            guess_1 = int(np.round(guess_1.item()))
            guess_2 = int(np.round(guess_2.item()))


            team_left_scores.append(guess_1)
            opp_right_scores.append(guess_2)

        for i, guess in enumerate(predictions_2):   # Predicts the same games as the previous for loop, but with the teams on different sides of the predict function

            # print(f"pre-guess guess = {guess}")
            guess_1 = guess[0]
            guess_2 = guess[1]
            # print(f"pre_guess 1 = {guess[0]}, pre_guess 2 = {guess[1]}")
 
            guess_1_reshaped = guess_1.reshape(-1,1)  # Reshape to (1, 1) for inverse_transform
            guess_2_reshaped = guess_2.reshape(-1,1)  # Reshape to (1, 1) for inverse_transform


            # Inverse transform the prediction
            guess_1 = point_scaler.inverse_transform(guess_1_reshaped)
            guess_2 = point_scaler.inverse_transform(guess_2_reshaped)


            # getting integer value from numpy arrays

            guess_1 = int(np.round(guess_1.item()))
            guess_2 = int(np.round(guess_2.item()))


            team_right_scores.append(guess_2)
            opp_left_scores.append(guess_1)








        
        for i in range(len(team_right_scores)):

            year = test_years[i]   # Block of code gets year of the game and both teams' names
            team_name = test_team_names[i]
            opp_name = test_opp_names[i]

            if scores_len > 0: # only getting real scores if real scores were provided to us
            
                # Reshaping test scores to 2D for inverse_transform
                score1_reshaped = test_team_scores[i].reshape(1, -1)  # Reshape to (1, 1)
                score2_reshaped = test_opp_scores[i].reshape(1, -1)   # Reshape to (1, 1)

                # guess_1 = point_scaler.inverse_transform(guess_reshaped)
                score1 = point_scaler.inverse_transform(score1_reshaped)
                score2 = point_scaler.inverse_transform(score2_reshaped)
            else: 
                score1 = 0



            guess_1 = round((team_right_scores[i] + team_left_scores[i])/2)
            guess_2 = round((opp_right_scores[i] + opp_left_scores[i])/2)


            if guess_1 == guess_2:
                guess_1 += 1

            
            if scores_len > 0:
                score1 = int(np.round(score1.item()))
                score2 = int(np.round(score2.item()))

            guess_win = True
            true_win = False

            if score1 > 0: # Only keep track of wins and losses if a real score is provided
                guess_win = True if guess_1 > guess_2 else False
                true_win = True if score1 > score2 else False

            
                true_guesses = true_guesses+1 if true_win == guess_win else true_guesses
            


            

            print(f"{team_name} vs {opp_name} in {year}\n")

            
            
            print(f"guess: ({team_name}) {guess_1} to {guess_2} ({opp_name})\n")
            if score1 > 0: # Only print score if real score to game was provided
                print(f"actual score: ({team_name}) {score1} to {score2} ({opp_name})\n\n")

        if scores_len > 0:   # Only calculate correct pick percentage if real scores are provided to us
            print(f"total_guesses = {total_guesses}")
            correct_pick_perc = (true_guesses/total_guesses)*100
            print(f"correct pick percentage: {correct_pick_perc}%")




    
    def single_game(point_scaler, scaler_dict, model):

        # point_scaler, model, test_team_stats, test_opp_stats, test_team_scores, test_opp_scores, test_years, test_team_names, test_opp_names
        
        file_path = f"data/regular_season_data/regular_season_(4-3-25).csv"

        while(True):
            print(f"Teams may have a different spelling than how you spell it. You may have to pick a different name for the team you are referring to.")
            print(f"To exit, enter 'q'.")
            team_name = input("\nEnter team 1: ").strip()

            if team_name == 'q':
                return
            
            opp_name = input("\nEnter team 2: ").strip()

            if opp_name == 'q':
                return
            
            game_year = input("\nEnter year of the game: ").strip()

            if game_year == 'q':
                return
            
            print("")

            team_info_list = []
            opp_info_list = []

            scaled_team_stats = dict()
            scaled_opp_stats = dict()

            with open(file_path, 'r') as season_file:
                
                    season_data = csv.reader(season_file, delimiter=',')    # assigns csv to a variable
                    next(season_data)  # Skips the headers
                    next(season_data)


                    for _team in season_data:
                        if (_team[136] == team_name and _team[0] == game_year) or ("Connecticut" == team_name and _team[136] == "UConn" and _team[0] == game_year):  # if team in dictionary == team in table on same year, get table info to dictionary
                            # print(f"full team name: {_team[137]} in year {year}")

                            team_info_list = [_team[4], _team[6], _team[8], _team[10], _team[12], _team[18], _team[20], _team[22], _team[24], _team[26], _team[28], _team[30], _team[32], _team[34], _team[36], _team[38], _team[40], _team[42], _team[44], _team[46], _team[48], _team[50], _team[52], _team[54], _team[56], _team[58], _team[60],  _team[62], _team[64], _team[66], _team[68], _team[70], _team[72], _team[74], _team[76], _team[78], _team[85], _team[87], _team[89], _team[91], _team[93], _team[95],  _team[97], _team[99], _team[101], _team[103], _team[105], _team[107], _team[109], _team[111], _team[113], _team[115], _team[117], _team[119], _team[121], _team[123], _team[125],  _team[127], _team[129], _team[131], _team[133]]
                            # above list cotains all data points from regular season

                        
                        if (_team[136] == opp_name and _team[0] == game_year) or ("Connecticut" == opp_name and _team[136] == "UConn" and _team[0] == game_year):  # if team in dictionary == team in table on same year, get table info to dictionary
                            # print(f"full team name: {_team[137]} in year {year}")

                            opp_info_list = [_team[4], _team[6], _team[8], _team[10], _team[12], _team[18], _team[20], _team[22], _team[24], _team[26], _team[28], _team[30], _team[32], _team[34], _team[36], _team[38], _team[40], _team[42], _team[44], _team[46], _team[48], _team[50], _team[52], _team[54], _team[56], _team[58], _team[60],  _team[62], _team[64], _team[66], _team[68], _team[70], _team[72], _team[74], _team[76], _team[78], _team[85], _team[87], _team[89], _team[91], _team[93], _team[95],  _team[97], _team[99], _team[101], _team[103], _team[105], _team[107], _team[109], _team[111], _team[113], _team[115], _team[117], _team[119], _team[121], _team[123], _team[125],  _team[127], _team[129], _team[131], _team[133]]
                            # above list cotains all data points from regular season

            
            def tourney_func():

                # Get all teams in the tournament
                # Get all the correct matchups
                # Format the games in a way that winners play winners


                print(f"hello")
                        
                            
            if team_info_list == []:
                print(f"team 1 has not been found. Year might be wrong, or team name might need to be spelled a different way.")

                exit = input(f"\nExit single game prediction? (y/n) ")

                if exit == "y":
                    return
                
                continue
            if opp_info_list == []:
                print(f"team 2 has not been found. Year might be wrong, or team name might need to be spelled a different way.")

                exit = input(f"\nExit single game prediction? (y/n) ")

                if exit == "y":
                    return

                continue



            for i in range(len(team_info_list)):  # does the same thing (relatively) as scale_games() in dataFetcher.py: code below scales stats to pass into predict()

                stat_counter = f"stat{i}"

                new_scaler = scaler_dict[stat_counter]

                scaled_team_stat = np.array(team_info_list[i]).reshape(-1, 1)  # Converts all numbers in training set to numpy. 
                scaled_opp_stat = np.array(opp_info_list[i]).reshape(-1, 1)  # Converts all numbers in training set to numpy. 

                scaled_team_stat = new_scaler.transform((scaled_team_stat))
                scaled_opp_stat = new_scaler.transform((scaled_opp_stat))

                scaled_team_stats[stat_counter] = scaled_team_stat
                scaled_opp_stats[stat_counter] = scaled_opp_stat



            stacked_team_stats = np.hstack([scaled_team_stats[f"stat{i}"] for i in range(61)])    # Rearanges the data to have each column contain 1 type of stat
            stacked_opp_stats = np.hstack([scaled_opp_stats[f"stat{i}"] for i in range(61)])

            stacked_team_stats = stacked_team_stats[:, :, np.newaxis]  # Adds a third dimension (to the vector)
            stacked_opp_stats = stacked_opp_stats[:, :, np.newaxis]   # Adds a third dimension


            predict(point_scaler, model, stacked_team_stats, stacked_opp_stats, [team_name], [opp_name], [game_year], test_team_scores=0, test_opp_scores=0)

            # need to get all the stats in the right format
            

            
      


            

            # Find stats for team and opp


            

    
    
    
    
    
    def main():


        data1 = np.load('team_stats.npz')
        team_stats = data1['stacked_team_stats']

        data2 = np.load('opp_stats.npz')
        opp_stats = data2['stacked_opp_stats']

        data3 = np.load('team_scores.npz')
        team_scores = data3['scaled_team_scores']

        data4 = np.load('opp_scores.npz')
        opp_scores = data4['scaled_opp_scores']

        point_scaler = load('point_scaler.pkl')

        scaler_dict = joblib.load('scalers.joblib')

        data5 = np.load('_opp_names.npz')
        opp_names = data5['opp_names']

        data6 = np.load('_team_names.npz')
        team_names = data6['team_names']

        data7 = np.load('_years.npz')
        years = data7['years']



 

        print(f"team_stats len = {len(team_stats)}")


        test_size = 0.01  # Adjust as needed

        team_stats_train, team_stats_test, opp_stats_train, opp_stats_test, \
        team_scores_train, team_scores_test, opp_scores_train, opp_scores_test, \
        years_train, years_test, team_names_train, team_names_test, \
        opp_names_train, opp_names_test = train_test_split(
            team_stats, opp_stats, team_scores, opp_scores, years, team_names, opp_names,
            test_size=test_size, random_state=42
        )



        model = makeModel(team_stats_train, opp_stats_train, team_scores_train, opp_scores_train)

        #       point_scaler, model, test_team_stats, test_opp_stats, test_team_names, test_opp_names, test_years=[], test_team_scores=[], test_opp_scores=[]
        
        
        while True:
            
            print(f"\n********************* COLLEGE BASKETBALL AI PREDICTOR *********************\n") 
            print(f"(1) Predict An Individual Game")
            print(f"(2) Find Prediction Percentage of Random Games")
            print(f"(3) Quit")
            user_input = int(input(f"\nEnter a NUMBER choice: ").strip())

            if user_input == 1:
                print(f"\n********************** Single Game Predictor *******************************\n")
                single_game(point_scaler, scaler_dict, model)
            elif user_input == 2:
                print(f"\n********************** Random Game Predictor *******************************\n")
                predict(point_scaler, model, team_stats_test, opp_stats_test, team_names_test, opp_names_test, years_test, team_scores_test, opp_scores_test)
            elif user_input == 3:
                print(f"GOODBYE!")
                return
            else:
                print(f"\nDid not recognize the input. Make sure the input is a single number.")

        
            # i += 1


            # ORGANIZE CODE (SEPERATE INTO FUNCTIONS)
            # CREATE FUNCTIONS THAT . . . 
            # 1) . . .  COMPILES/FITS MODEL
            # 2) PREDICTS INDIVIDUAL GAMES
            # 3) PREDICTS ENTIRE TOURNAMENTS (FUNCTION WILL NEED TO ORGANIZE GAMES BASED ON TYPE OF TOURNAMENT (CONFERENCE, NCAA, ETC.))


    main()


