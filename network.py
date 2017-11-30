from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization, Activation
from keras.regularizers import l2
import numpy as np
import csv


n_features = 26
n_labels = 4
batch_size = 100
epochs = 200
dropout = 0.2
l2_v = 0.0001
np.random.seed(7)


model = Sequential()

model.add(Dense(100, kernel_regularizer=l2(l2_v), input_dim=n_features))
model.add(BatchNormalization())
model.add(Activation('linear'))
model.add(Dropout(dropout))

model.add(Dense(100, kernel_regularizer=l2(l2_v)))
model.add(BatchNormalization())
model.add(Activation('linear'))
model.add(Dropout(dropout))

model.add(Dense(100, kernel_regularizer=l2(l2_v)))
model.add(BatchNormalization())
model.add(Activation('linear'))
model.add(Dropout(dropout))

model.add(Dense(100, kernel_regularizer=l2(l2_v)))
model.add(BatchNormalization())
model.add(Activation('linear'))
model.add(Dropout(dropout))

model.add(Dense(4))
model.add(BatchNormalization())
model.add(Activation('linear'))

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
        labels = data[:, 0:4]
        features = data[:, 4:]
        return features, labels



class Modeller:

    def __init__(self):
        self.reader = Reader('Modeller_Reader')


    def train(self, path):

        for link in path:

            #read
            features, labels = self.reader.read(link)

            #train
            model.fit(features, labels, epochs=epochs, batch_size=batch_size)

            if link == path[-1]:
                model.save(filepath='/home/oem/CI/model.h5')





MyModeller = Modeller()
MyModeller.train(['/home/oem/CI/generated_forza.csv',
                '/home/oem/CI/generated_cg_speedway1.csv',
                '/home/oem/CI/generated_cg_track2.csv',
                '/home/oem/CI/generated_cg_track3.csv'
                  ])



