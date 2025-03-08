if __name__ == "__main__":
    
    import numpy as np
    import random
    from random import randint
    from sklearn.preprocessing import MinMaxScaler
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

        # print(f"team_scores = {team_scores}")
        # print(f"point_scaler = {point_scaler}")

        print(f"team_stats len = {len(team_stats)}")

        rand_point = random.randint(0, 55)
        test_team_stats = team_stats.copy()      # These following 12 lines of code create test samples and labels, as well as moving some games from training samples/labels to training samples/tests
        test_team_stats = test_team_stats[rand_point:rand_point+5]
        team_stats = np.concatenate([team_stats[:rand_point], team_stats[rand_point+5:]])

        test_opp_stats = opp_stats.copy()
        test_opp_stats = test_opp_stats[rand_point:rand_point+5]
        opp_stats = np.concatenate([opp_stats[:rand_point], opp_stats[rand_point+5:]])

        test_team_scores = team_scores.copy()
        test_team_scores = test_team_scores[rand_point:rand_point+5]
        team_scores = np.concatenate([team_scores[:rand_point], team_scores[rand_point+5:]])

        test_opp_scores = opp_scores.copy()
        test_opp_scores = test_opp_scores[rand_point:rand_point+5]
        opp_scores = np.concatenate([opp_scores[:rand_point], opp_scores[rand_point+5:]])



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

        predictions = model.predict([test_team_stats, test_opp_stats], batch_size=1, verbose=0)

        print("\n")

        for guess in predictions:
            i = 0

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

            score1 = int(np.round(score1.item()))
            score2 = int(np.round(score2.item()))

            print(f"guess = {guess_1} to {guess_2}, actual score = {score1} to {score2}\n")
            i += 1


    main()


