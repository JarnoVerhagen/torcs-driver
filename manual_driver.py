from pytocl.driver import Driver
from pytocl.car import State, Command
import keyboard

class ManualDriver(Driver):
    accelerator = 0
    brake = 0
    steering = 0

    def drive(self, carstate: State) -> Command:
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
        inverseSpeed = carstate.speed_x**-1 # Used to compensate for speed
        minSteering = 0.5*inverseSpeed # Minimum steering speed
        deltaSteering = 0.05*inverseSpeed # Change in steering speed while holding
        if keyboard.is_pressed('a'):
            # Steer left
            self.steering = self.steering + deltaSteering
            self.steering = max([self.steering, minSteering])
        elif keyboard.is_pressed('d'):
            # Steer right
            self.steering = self.steering - deltaSteering
            self.steering = min([self.steering, -minSteering])
        else:
            # Stop all steering
            self.steering = 0
	
	# Gear, done using automatic transmission
        gear = max([carstate.gear, 1]) # At least in gear 1
        if self.accelerator > 0 and carstate.rpm > 8000 and gear < 6:
            gear = gear + 1
        if carstate.rpm < 2500 and gear > 1:
            gear = gear - 1
        
        # Create command
        command = Command()
        command.accelerator = self.accelerator
        command.brake = self.brake
        command.gear = gear
        command.steering = self.steering
        command.focus = 0.0
        
        # Logging, right now done using provided logger which uses pickle
        if self.data_logger:
            self.data_logger.log(carstate, command)

        return command
         
