#! /usr/bin/env python3

from pytocl.main import main
from pytocl.driver import Driver
from pytocl.car import State, Command
import numpy as np

import keyboard
import datetime
import csv

class ManualDriver(Driver):
    accelerator = 0
    brake = 0
    steering = 0

    def __init__(self, logdata=False):
        date = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        file = open('logs/log' + date + '.csv', 'a')
        self.csvWriter = csv.writer(file, delimiter=',')
        super(ManualDriver, self).__init__()

    def drive(self, carstate: State) -> Command:
        if keyboard.is_pressed('o'):
            print([int(x) for x in carstate.opponents])

            back_opponent = np.average(np.append(carstate.opponents[0:2], carstate.opponents[35]))
            left_opponent = np.average(carstate.opponents[8:11])
            front_left_opponent = np.average(carstate.opponents[15:18])
            front_opponent = np.average(carstate.opponents[17:20])
            front_right_opponent = np.average(carstate.opponents[19:22])
            right_opponent = np.average(carstate.opponents[26:29])
            opponent_distances = [back_opponent, left_opponent, front_left_opponent, front_opponent, front_right_opponent, right_opponent]
            print([int(x) for x in opponent_distances])


        # Accelerator
        if keyboard.is_pressed('w'):
            self.accelerator = 1
        else:
            self.accelerator = 0

        # Brake
        if keyboard.is_pressed('s'):
            self.brake = 1
        else:
            self.brake = 0

        # Steering
        inverseSpeed = (carstate.speed_x+0.00001)**-1 # Used to compensate for speed
        deltaSteering = 0.5*inverseSpeed # Minimum steering speed
        if keyboard.is_pressed('a'):
            # Steer left
            self.steering = self.steering + deltaSteering
            self.steering = max([self.steering, deltaSteering])
        elif keyboard.is_pressed('d'):
            # Steer right
            self.steering = self.steering - deltaSteering
            self.steering = min([self.steering, -deltaSteering])
        else:
            # Stop all steering
            self.steering = 0

	# Gear, done using automatic transmission
        gear = max([carstate.gear, 1]) # At least in gear 1
        if self.accelerator > 0 and carstate.rpm > 8000 and gear < 6:
            gear = gear + 1
        if carstate.rpm < 5000 and gear > 1:
            gear = gear - 1
        if keyboard.is_pressed('shift'):
            gear = -1

        # Create command
        command = Command()
        command.accelerator = self.accelerator
        command.brake = self.brake
        command.gear = gear
        command.steering = self.steering
        command.focus = 0.0

        self.csvWriter.writerow([command.accelerator, command.brake, command.steering, command.gear, carstate.speed_x, carstate.speed_y, carstate.speed_z, carstate.distance_from_center, carstate.angle, carstate.rpm, carstate.gear] + list(carstate.distances_from_edge))

        return command

if __name__ == '__main__':
    main(ManualDriver(logdata=False))
