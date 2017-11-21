from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import csv


model = Sequential()
model.add(Dense(100, activation='linear', input_dim=24))
model.add(Dense(100, activation='linear'))
model.add(Dense(3, activation='linear'))
model.compile(loss='mean_squared_error',
              optimizer='adam',
              metrics=['accuracy'])


class Reader:

    def __init__(self, name):

        self.name = name

    def read(self, path):

        raw_data = open(path, 'rt')
        reader = csv.reader(raw_data, delimiter=",", quoting=csv.QUOTE_NONE)
        data = np.array(list(reader)).astype('float')
        #labels = data[:,0:4]
        #ignore brake
        labels = np.concatenate((data[:,0:1], data[:,2:4]), axis=1)
        features = data[:,4:]

        return features, labels



class Modeller:

    def __init__(self):
        self.reader = Reader('Modeller_Reader')

    def train(self, path):

        for link in path:

            features, labels = self.reader.read(link)
            model.fit(features, labels, epochs=200, batch_size=32)

            if link == path[-1]:
                model.save(filepath='/home/oem/CI/model.h5')


MyModeller = Modeller()
MyModeller.train(['/home/oem/CI/train_data.csv',
                  ])



