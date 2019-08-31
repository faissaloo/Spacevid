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

import os
import random
import re

import dataset
import ffmpeg

def convert_and_get_stats(video_name, bitrate, framerate=30):
    source_video_path = 'dataset/videos/'+video_name

    new_video_name = re.sub("\..*$",".webm",video_name)
    #We should probably be using a ramdisk for this stuff or we're gonna destroy this SSD
    new_video_path = '/tmp/'+new_video_name

    new_video_path, size = ffmpeg.convert_to_webm(source_video_path, bitrate, new_video_path)

    os.remove(new_video_path)
    length = ffmpeg.get_video_length(source_video_path)
    h_aspect, v_aspect = ffmpeg.get_video_aspect_ratio(source_video_path)
    return size, length, bitrate, h_aspect, v_aspect

while True:
    dataset.write_data(*convert_and_get_stats(random.choice(os.listdir('dataset/videos')), random.randrange(10000,400000)))
