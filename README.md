# ci-project
Description of folder structure.

## driver/
Contains the implementation of the basic driver. It is trained on the files provided in data/ using model.py. The driver can be executed by running start.sh.

## evolution/
Contains everything related to research done related to the evolutionary algorithm for improving the driver. The main interface to everything provided here can be found through util.py, which contains functions for training, driving an eveluating models.

## manual/
Contains an implementaion of driver for generating data by driving manually. The data that is generated using this method can be found in the data/ folder. The data proved itself to be unsuitable for this model and is thus not used in any final solution.
