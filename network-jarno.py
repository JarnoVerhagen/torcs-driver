import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, BatchNormalization, Activation
from keras.regularizers import l2
from keras.optimizers import sgd, adam
from keras.models import load_model
from keras.layers.advanced_activations import LeakyReLU
import csv

# Parameters
n_features = 14
n_labels = 4
batch_size = 128
epochs = 50
dropout = 0.2
l2_v = 0.0001
n_layers = 3
activation = 'linear'
lr = 0.001
leak = 0.00005
momentum = 0.9
dropped = [1, 4, 7, 10, 13, 16, 19]

np.random.seed(7)
model = Sequential()

# Input layer
model.add(Dense(14, input_dim=n_features, activation='linear', init='uniform'))
# model.add(BatchNormalization())

# Hidden layers
for i in range(1, n_layers-1):
    model.add(Dense(10, activation='sigmoid', init='uniform'))
    # model.add(BatchNormalization())

# Output layer
model.add(Dense(n_labels, activation='linear', init='uniform'))
# model.add(BatchNormalization())

model.compile(loss='mean_squared_error', optimizer=adam(lr=0.0005))

# print(model.summary())

class Modeller:
    def read(self, path):
        data = open(path, 'rt')
        reader = csv.reader(data, delimiter=",", quoting=csv.QUOTE_NONE)
        data = np.array(list(reader)).astype('float')

        output = data[:, :4]
        input = data[:, 4:]
        input = np.delete(input, [1, 2, 5, 8, 10, 12, 14, 16, 18, 20, 22, 24], axis=1) # 1: remove speed_y, 2: speed_z and 5: rpm
        return input, output

    def train(self, path):
        input, output = self.read(path)
        model.fit(input, output, epochs=epochs, batch_size=batch_size)

    def train_multiple(self, paths):
        for path in paths:
            self.train(path)
        model.save(filepath='model/model.h5')

MyModeller = Modeller()
MyModeller.train_multiple([
# 'driver/logs/Manual/CG Track 3/log2017-11-28-12-19-53.csv',
# 'driver/logs/Manual/CG Track 3/log2017-11-28-12-23-41.csv',
# 'driver/logs/Manual/CG Track 2/log2017-11-28-12-11-53.csv',
# 'driver/logs/Manual/CG Track 2/log2017-11-28-12-13-16.csv',
# 'driver/logs/Manual/CG Track 2/log2017-11-28-12-14-36.csv',
# 'driver/logs/Manual/CG Track 2/log2017-11-28-12-15-56.csv',
# 'driver/logs/Manual/CG Speedway number 1/log2017-11-28-12-04-33.csv',
# 'driver/logs/Manual/CG Speedway number 1/log2017-11-28-12-06-02.csv',
# 'driver/logs/Manual/CG Speedway number 1/log2017-11-28-12-07-10.csv',
# 'driver/logs/Manual/CG Speedway number 1/log2017-11-28-12-08-23.csv',
# 'driver/logs/Manual/Forza/log2017-11-28-11-48-18.csv',
# 'driver/logs/Manual/Forza/log2017-11-28-11-51-52.csv',
# 'driver/logs/Manual/Forza/log2017-11-28-11-54-10.csv',
# 'driver/logs/Manual/Forza/log2017-11-28-11-56-13.csv',
'driver/logs/Generated2/drivelog-2017-11-30-23-56-14.csv',
'driver/logs/Generated2/drivelog-2017-11-30-23-57-12.csv',
'driver/logs/Generated2/drivelog-2017-11-30-23-58-30.csv',
'driver/logs/Generated2/drivelog-2017-11-30-23-58-55.csv',
'driver/logs/Generated2/drivelog-2017-11-30-23-59-27.csv',
'driver/logs/Generated2/drivelog-2017-12-01-00-00-00.csv',
'driver/logs/Generated2/testdrive.csv',
# 'driver/logs/Manual/3 laps center focus/log2017-12-05-12-55-07.csv',
# 'driver/logs/Manual/3 laps center focus/log2017-12-05-12-38-55.csv',
# 'driver/logs/Manual/3 laps center focus/log2017-12-05-12-38-55.csv',
# 'driver/logs/Manual/3 laps center focus/log2017-12-05-12-47-56.csv',
# 'driver/logs/Manual/3 laps center focus/log2017-12-05-12-44-21.csv',
])





