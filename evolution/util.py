from model import Model
from mutate import mutate
from driver.driver import Driver
from driver.main import main
import tensorflow as tf
import os
import threading

def create_initial_model():
    model = Model()
    model.train_multiple([
        'data/drivelog-2017-11-30-23-56-14.csv',
        'data/drivelog-2017-11-30-23-57-12.csv',
        'data/drivelog-2017-11-30-23-58-30.csv',
        'data/drivelog-2017-11-30-23-58-55.csv',
        'data/drivelog-2017-11-30-23-59-27.csv',
        'data/drivelog-2017-12-01-00-00-00.csv',
        'data/testdrive.csv'])
    model.save('models/init')

def create_initial_generation():
    folder = 'models/gen0/'
    if not os.path.exists(folder):
        os.makedirs(folder)

    mean = 0
    std = 0.01
    print("Starting generation of generation 0")
    for i in range(100):
        model_name = "g0m" + str(i)
        threading.Thread(target=mutate, args=('models/init', folder + model_name, mean, std)).start()
    print("Completed generation of 100 models")

def drive_model(path):
    model = tf.keras.models.load_model(path)
    features = 14
    driver = Driver(model, features)
    main(driver)

# drive_model('models/gen0/g0m1')