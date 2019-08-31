#!/usr/bin/env python3.6
# This file is part of Spacevid.
#
# Spacevid is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Spacevid is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Spacevid.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import pandas as pd
import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.layers as layers
import numpy as np
import os

import dataset
import ffmpeg

def normalize_dataframe(dataframe, stats):
    return pd.DataFrame(
        data={
        key: (values - stats[key]['mean']) / stats[key]['std'] for key, values in dataframe.items()
        },
        columns=dataframe.keys()
    )

# Assuming frame rate of 24 and output format of VP8/OGG WEBM at 480p
class Spacevid():
    def __init__(self):
        self.load_data()
        self.build_model()

    def build_model(self):
        self.model = keras.Sequential([
            layers.Dense(64, activation=tf.nn.relu, input_shape = self.input_shape),
            layers.Dense(32, activation=tf.nn.relu),
            layers.Dense(16, activation=tf.nn.relu),
            layers.Dense(8, activation=tf.nn.relu),
            layers.Dense(4, activation=tf.nn.relu),
            layers.Dense(2, activation=tf.nn.relu),
            layers.Dense(1)
        ])
        optimizer = tf.keras.optimizers.RMSprop(0.001)

        self.model.compile(loss=tf.losses.mean_squared_error, optimizer=optimizer, metrics=[tf.losses.mean_squared_error, 'mean_absolute_error'])

    def load_data(self):
        ds = pd.read_csv('dataset/dataset.csv')

        if ds['bitrate'].count() < 16:
            raise dataset.InadequateDataError('Not enough data, please run ./generate_data.py')

        test_dataset = ds.sample(16)
        self.test_bitrate = test_dataset.pop('bitrate')

        train_dataset = ds.drop(test_dataset.index)
        self.train_bitrate = train_dataset.pop('bitrate')
        self.train_stats = train_dataset.describe()
        self.input_shape = (len(train_dataset.keys()),)

        self.normalized_train_dataset = normalize_dataframe(train_dataset, self.train_stats)
        self.normalized_test_dataset = normalize_dataframe(test_dataset, self.train_stats)

    def train(self, epochs=2000):
        return self.model.fit(self.normalized_train_dataset, self.train_bitrate, epochs=epochs)

    def test(self):
        result = self.model.evaluate(self.normalized_test_dataset, self.test_bitrate)
        print(self.model.metrics_names)
        print(result)

    def save(self):
        raise MethodError
    def estimate(self, target_size, video_length, h_aspect, v_aspect):
        input_data = pd.DataFrame(
            data={
                'output size in bytes': np.array([target_size]),
                'length in seconds': np.array([video_length]),
                'horizontal aspect': np.array([h_aspect]),
                'vertical aspect': np.array([v_aspect])
            },
            columns=['output size in bytes', 'length in seconds', 'horizontal aspect', 'vertical aspect']
        )
        normalized_input_data = normalize_dataframe(input_data, self.train_stats)
        return int(round(self.model.predict(normalized_input_data)[0][0]))

description = ('Make a video fit a specified file size restriction')
parser = argparse.ArgumentParser(description=description)
parser.add_argument('filename', help='path to input video file', type=str)
parser.add_argument('size', help='target file size in bytes', type=int)
parser.add_argument('-o','--output', help='target file size in bytes', type=str, default=None, required=False)
parser.add_argument('-e','--epochs', help='training cycles', type=int, default=5000, required=False)
parser.add_argument('-d','--dont-remember', help="don't remember the results of this transcode", type=bool, default=False, required=False)
arguments = parser.parse_args()

model=Spacevid()
model.train(arguments.epochs)
model.test()
output_size = float(arguments.size)
video_length = ffmpeg.get_video_length(arguments.filename)
h_aspect, v_aspect = ffmpeg.get_video_aspect_ratio(arguments.filename)
estimated_bitrate = model.estimate(output_size, video_length, h_aspect, v_aspect)
print("ESTIMATED BITRATE: {}".format(estimated_bitrate))
new_path, actual_size = ffmpeg.convert_to_webm(arguments.filename, estimated_bitrate, arguments.output)
if actual_size > arguments.size:
    print("Actual size is larger than specified size!")

if not arguments.dont_remember:
    print("I'll remember this to improve future results, run me with -d if you would like to prevent this")
    dataset.write_data(float(actual_size), video_length, estimated_bitrate, h_aspect, v_aspect)
