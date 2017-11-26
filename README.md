# ci-project

## Executing drivers
Executing "sudo python manual_driver.py" will likely result in errors, since sudo does not use the conda python environment by default. So to execute manual_driver.py in a conda environment using sudo, the easiest is to execute:

"sudo >>python env location<< manual_driver.py"

Where >>python env location<< can be retrieved by activating your conda environment and executing "which python" which will return the location.
