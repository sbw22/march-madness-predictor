import numpy as np
import random
from random import randint
from sklearn.preprocessing import MinMaxScaler
import keras
from keras import backend as K
from keras.models import Sequential
from keras.layers import Activation
from tensorflow.keras.layers import Input, Dense, Flatten, Dropout, Conv2D, MaxPool2D, GlobalAveragePooling2D, BatchNormalization
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
# from keras.utils.vis_utils import plot_model
# %matplotlib inline

import os
import json
# import nbimporter