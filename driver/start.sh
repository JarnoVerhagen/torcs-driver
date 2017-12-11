#! /usr/bin/env python3

from main import main
from driver import Driver
import tensorflow as tf

if __name__ == '__main__':
    model = tf.keras.models.load_model('models/base')
    main(Driver(model))
