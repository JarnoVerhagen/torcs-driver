#! /usr/bin/env python3

from pytocl.main import main
from pytocl.driver import Driver
from pytocl.car import State, Command, MPS_PER_KMH

import numpy as np
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class ModelDriver(Driver):
    MODEL = tf.keras.models.load_model('../model/model.h5')
    FEATURES = 14

    def drive(self, carstate: State) -> Command:
        # Feed carstate to model
        data = np.append(
            [carstate.speed_x, carstate.distance_from_center, carstate.angle,
             carstate.gear], list(carstate.distances_from_edge[::2])).reshape((1, ModelDriver.FEATURES))
        predictions = ModelDriver.MODEL.predict(data)
        print(predictions)
        # Create command based on predictions
        command = Command()
        command.accelerator = predictions[0, 0]
        command.brake = round(abs(predictions[0, 1]))
        command.steering = predictions[0, 2]
        command.gear = max(predictions[0, 3], 1)

        # Gear, done using automatic transmission
        # gear = max([carstate.gear, 1])  # At least in gear 1
        # if command.accelerator > 0 and carstate.rpm > 8000 and gear < 6:
        #     gear = gear + 1
        # if carstate.rpm < 5000 and gear > 1:
        #     gear = gear - 1
        #
        # command.gear = gear

        return command

if __name__ == '__main__':
    main(ModelDriver(logdata=False))