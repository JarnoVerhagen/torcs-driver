import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import adam
import csv
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class Model:
    # Parameters
    n_features = 20
    n_labels = 4
    batch_size = 128
    lr = 0.0005
    epochs = 150

    def __init__(self):
        np.random.seed(7)
        model = Sequential()

        model.add(Dense(self.n_features, activation='linear', input_dim=self.n_features, bias_initializer='uniform')) # Input layer
        model.add(Dense(10, activation='sigmoid', kernel_initializer='uniform')) # Hidden layers
        model.add(Dense(self.n_labels, activation='linear', kernel_initializer='uniform')) # Output layer

        model.compile(loss='mean_squared_error', optimizer=adam(lr=self.lr))

        self.model = model

    def read(self, path):
        data = open(path, 'rt')
        reader = csv.reader(data, delimiter=",", quoting=csv.QUOTE_NONE)
        data = np.array(list(reader)).astype('float')

        output = data[:, :4]
        input = data[:, 4:]
        # Remove 1: speed_y, 2: speed_z and 5: rpm, others: odd edge distances
        input = np.delete(input, [1, 2, 5, 8, 10, 12, 14, 16, 18, 20, 22, 24], axis=1)
        # Add 6 distances to opponents, initially at max vallue 200
        opponents = np.full((len(input), 6), 200)
        input = np.append(input, opponents, 1)

        return input, output

    def train(self, path):
        input, output = self.read(path)
        print("Start fitting", path)
        self.model.fit(input, output, epochs=self.epochs, batch_size=self.batch_size)

    def train_multiple(self, paths):
        for path in paths:
            self.train(path)

    def save(self, path):
        self.model.save(filepath=path)

model = Model()
model.read('data/drivelog-2017-11-30-23-58-30.csv')