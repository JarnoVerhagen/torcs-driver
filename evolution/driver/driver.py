from driver.car import State, Command, MPS_PER_KMH

import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class Driver():
    def __init__(self, model, n_features):
        self.model = model
        self.n_features = n_features

    def drive(self, carstate: State) -> Command:
        back_opponent = np.average(np.append(carstate.opponents[0:2], carstate.opponents[35]))
        left_opponent = np.average(carstate.opponents[8:11])
        front_left_opponent = np.average(carstate.opponents[15:18])
        front_opponent = np.average(carstate.opponents[17:20])
        front_right_opponent = np.average(carstate.opponents[19:22])
        right_opponent = np.average(carstate.opponents[26:29])
        opponent_distances = np.array([back_opponent, left_opponent, front_left_opponent, front_opponent, front_right_opponent, right_opponent])
        # Feed carstate to model
        data = np.append(
            [carstate.speed_x, carstate.distance_from_center, carstate.angle, carstate.gear],
            list(carstate.distances_from_edge[::2]))
        data = np.append(data, opponent_distances).reshape((1, 20))
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