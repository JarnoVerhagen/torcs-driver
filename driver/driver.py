from car import State, Command, MPS_PER_KMH

import numpy as np
import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class Driver():
    def __init__(self, model):
        self.model = model

    def drive(self, carstate: State) -> Command:
        # Feed carstate to model
        data = np.append(
            [carstate.speed_x, carstate.distance_from_center, carstate.angle, carstate.gear],
            list(carstate.distances_from_edge[::2])).reshape((1, 14))
        predictions = self.model.predict(data)

        # Create command based on predictions
        command = Command()
        command.accelerator = predictions[0, 0]
        command.brake = round(abs(predictions[0, 1]))
        command.steering = predictions[0, 2]
        command.gear = max(predictions[0, 3], 1) # Put the gear to at least 1

        return command

    @property
    def range_finder_angles(self):
        return -90, -75, -60, -45, -30, -20, -15, -10, -5, 0, 5, 10, 15, 20, \
            30, 45, 60, 75, 90