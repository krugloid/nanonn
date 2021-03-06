#!/usr/bin/env python3

import tensorflow as tf
import json
import csv

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(units=36, activation=tf.nn.leaky_relu))
model.add(tf.keras.layers.Dense(units=14, activation=tf.nn.leaky_relu))
model.add(tf.keras.layers.Dense(units=10, activation=tf.nn.softmax))

model.compile(
    optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)
model.fit(x_train, y_train, epochs=20)
model.evaluate(x_test, y_test)

# Save model
model.save("mnist.h5")

# Load model
# model = tf.keras.models.load_model(
    # "mnist.h5", custom_objects={"leaky_relu": tf.nn.leaky_relu}
# )

W = model.get_weights()

# Convert weights from TF format (units as rows + seprate bias vector) to
# NanoNN format (units as cols, with bias as the rightmost column)
L1 = tf.reshape(tf.transpose(tf.concat([W[0], [W[1]]], 0)), [-1]).numpy().tolist()
L2 = tf.reshape(tf.transpose(tf.concat([W[2], [W[3]]], 0)), [-1]).numpy().tolist()
L3 = tf.reshape(tf.transpose(tf.concat([W[4], [W[5]]], 0)), [-1]).numpy().tolist()

# Save weights as JSON
with open("mnist.json", "w") as f:
    weights_json = json.dumps([L1, L2, L3])
    f.write(weights_json)

# Save weights as CSV
with open("mnist.csv", "w") as f:
    w = csv.writer(f)
    w.writerow(L1)
    w.writerow(L2)
    w.writerow(L3)
