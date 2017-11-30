from pytocl.driver import Driver
from pytocl.car import State, Command, MPS_PER_KMH
import numpy as np
import tensorflow as tf


class MyDriver(Driver):
    # Override the `drive` method to create your own driver
    
    MODEL = tf.keras.models.load_model('/home/oem/CI/model.h5')
    FEATURES = 26
       
    def drive(self, carstate: State) -> Command:

        command = Command()
       
        data = np.append([carstate.speed_x, carstate.speed_y, carstate.speed_z, carstate.distance_from_center, carstate.angle, carstate.rpm, carstate.gear], list(carstate.distances_from_edge)).reshape((1, MyDriver.FEATURES))

        
        predictions = MyDriver.MODEL.predict(data)

        command.accelerator = predictions[0,0]
        command.brake = round(abs(predictions[0,1]))
        command.steering = predictions[0,2]
        command.gear = predictions[0,3]


        print(command.accelerator, command.brake, command.steering, command.gear)

        #if self.data_logger:
        #    self.data_logger.log(carstate, command)

        return command

        
