from pytocl.driver import Driver
from pytocl.car import State, Command, MPS_PER_KMH
import numpy as np
import math
import csv
from keras.models import load_model

class MyDriver(Driver):
    # Override the `drive` method to create your own driver
    
    MODEL = load_model('/home/oem/CI/model.h5')
    #OUTPUT = open('/home/oem/CI/train_data.csv', 'w')

    def drive(self, carstate: State) -> Command:

        command = Command()

        speed_total = np.sqrt(np.power(carstate.speed_x, 2) + np.power(carstate.speed_y, 2) + np.power(carstate.speed_z, 2))

        #track_position = carstate.distance_from_center
        #angle = carstate.angle
        #track = carstate.distances_from_edge
    
        data = np.append([speed_total, carstate.distance_from_center, carstate.angle, carstate.rpm, carstate.gear], list(carstate.distances_from_edge)).reshape((1, 24))

        #data = np.array(track).reshape((1, 19))   
        

        predictions = MyDriver.MODEL.predict(data)

        command.accelerator = predictions[0,0]
        #command.brake = predictions[0,1]
        command.steering = predictions[0,1]
        command.gear = round(predictions[0,2])

        #print(predictions)

        #self.steer(carstate, 0.0, command)
        #v_x = 80
        #self.accelerate(carstate, v_x, command)
        print(command.accelerator, command.brake, command.steering, command.gear)

       
  
        #writer = csv.writer(MyDriver.OUTPUT, delimiter=',')
        #writer.writerows([[command.accelerator, command.brake, command.steering, command.gear, np.sqrt(np.power(carstate.speed_x, 2) + np.power(carstate.speed_y, 2) + np.power(carstate.speed_z, 2)), carstate.distance_from_center, cartate.angle, carstate.rpm, carstate.gear] + list(carstate.distances_from_edge)])

        if self.data_logger:
            self.data_logger.log(carstate, command)

        return command

    def accelerate(self, carstate, target_speed, command):
        # compensate engine deceleration, but invisible to controller to
        # prevent braking:
        speed_error = 1.0025 * target_speed * MPS_PER_KMH - carstate.speed_x
        acceleration = self.acceleration_ctrl.control(
            speed_error,
            carstate.current_lap_time
        )

        # stabilize use of gas and brake:
        acceleration = math.pow(acceleration, 3)

        if acceleration > 0:
            if abs(carstate.distance_from_center) >= 1:
                # off track, reduced grip:
                acceleration = min(0.4, acceleration)

            command.accelerator = min(acceleration, 1)

            if carstate.rpm > 8000:
                command.gear = carstate.gear + 1

        # else:
        #     command.brake = min(-acceleration, 1)

        if carstate.rpm < 2500:
            command.gear = carstate.gear - 1

        if not command.gear:
            command.gear = carstate.gear or 1

    def steer(self, carstate, target_track_pos, command):
        steering_error = target_track_pos - carstate.distance_from_center
        command.steering = self.steering_ctrl.control(
            steering_error,
            carstate.current_lap_time
        )
