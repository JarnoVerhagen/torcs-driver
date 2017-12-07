import tensorflow as tf
import numpy as np

def mutate(input_path, output_path, mean, std):
    sess = tf.InteractiveSession()
    init = tf.global_variables_initializer()

    model = tf.keras.models.load_model(input_path)
    weights = model.weights

    for var in weights:
        sess.run(init)
        matrix = sess.run(var)
        if len(matrix.shape) > 1: # Only change weights in between layers
            for r_i, row in enumerate(matrix):
                for w_i, weight in enumerate(row):
                    add = np.random.normal(loc=mean, scale=std, size=None)
                    matrix[r_i, w_i] = matrix[r_i, w_i] + add
            assign_op = var.assign(matrix)
            sess.run(assign_op)

    tf.keras.models.save_model(model, output_path)