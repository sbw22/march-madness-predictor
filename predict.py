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
    # from keras.utils.vis_utils import plot_model
    # %matplotlib inline
    import os
    import json
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

    
    def predict(point_scaler, model, test_team_stats, test_opp_stats, test_team_scores, test_opp_scores, test_years, test_team_names, test_opp_names):
        
        predictions = model.predict([test_team_stats, test_opp_stats], batch_size=1, verbose=0)

        print("\n")

        total_guesses = 0
        true_guesses = 0

        for i, guess in enumerate(predictions):

            total_guesses = i
            # i = 0

            # print(f"Index {i}, test_scores[i]: {test_team_scores[i]}, test_opp_scores[i]: {test_opp_scores[i]}")


            year = test_years[i]
            team_name = test_team_names[i]
            opp_name = test_opp_names[i]

            # print(f"pre-guess guess = {guess}")
            guess_1 = guess[0]
            guess_2 = guess[1]
            # print(f"pre_guess 1 = {guess[0]}, pre_guess 2 = {guess[1]}")
 
            guess_1_reshaped = guess_1.reshape(-1,1)  # Reshape to (1, 1) for inverse_transform
            guess_2_reshaped = guess_2.reshape(-1,1)  # Reshape to (1, 1) for inverse_transform


            # Inverse transform the prediction
            guess_1 = point_scaler.inverse_transform(guess_1_reshaped)
            guess_2 = point_scaler.inverse_transform(guess_2_reshaped)


            # Reshaping test scores to 2D for inverse_transform
            score1_reshaped = test_team_scores[i].reshape(1, -1)  # Reshape to (1, 1)
            score2_reshaped = test_opp_scores[i].reshape(1, -1)   # Reshape to (1, 1)

            # guess_1 = point_scaler.inverse_transform(guess_reshaped)
            score1 = point_scaler.inverse_transform(score1_reshaped)
            score2 = point_scaler.inverse_transform(score2_reshaped)


            # getting integer value from numpy arrays

            guess_1 = int(np.round(guess_1.item()))
            guess_2 = int(np.round(guess_2.item()))

            if guess_1 == guess_2:
                guess_1 += 1


            score1 = int(np.round(score1.item()))
            score2 = int(np.round(score2.item()))

            guess_win = True
            true_win = False

            
            guess_win = True if guess_1 > guess_2 else False
            true_win = True if score1 > score2 else False

            
            true_guesses = true_guesses+1 if true_win == guess_win else true_guesses
            


            

            print(f"{team_name} vs {opp_name} in {year}")
            print(f"guess = {guess_1} to {guess_2}, actual score = {score1} to {score2}\n")

        
        print(f"total_guesses = {total_guesses}")
        correct_pick_perc = (true_guesses/total_guesses)*100
        print(f"correct pick percentage: {correct_pick_perc}%")

    
    
    
    
    
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

        data5 = np.load('_opp_names.npz')
        opp_names = data5['opp_names']

        data6 = np.load('_team_names.npz')
        team_names = data6['team_names']

        data7 = np.load('_years.npz')
        years = data7['years']



 

        print(f"team_stats len = {len(team_stats)}")


        test_size = 0.07  # Adjust as needed

        team_stats_train, team_stats_test, opp_stats_train, opp_stats_test, \
        team_scores_train, team_scores_test, opp_scores_train, opp_scores_test, \
        years_train, years_test, team_names_train, team_names_test, \
        opp_names_train, opp_names_test = train_test_split(
            team_stats, opp_stats, team_scores, opp_scores, years, team_names, opp_names,
            test_size=test_size, random_state=42
        )




        model = makeModel(team_stats_train, opp_stats_train, team_scores_train, opp_scores_train)
        
       

        predict(point_scaler, model, team_stats_test, opp_stats_test, team_scores_test, opp_scores_test, years_test, team_names_test, opp_names_test)

        
            # i += 1


            # ORGANIZE CODE (SEPERATE INTO FUNCTIONS)
            # CREATE FUNCTIONS THAT . . . 
            # 1) . . .  COMPILES/FITS MODEL
            # 2) PREDICTS INDIVIDUAL GAMES
            # 3) PREDICTS ENTIRE TOURNAMENTS (FUNCTION WILL NEED TO ORGANIZE GAMES BASED ON TYPE OF TOURNAMENT (CONFERENCE, NCAA, ETC.))


    main()


