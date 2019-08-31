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
import subprocess

def get_video_aspect_ratio(video_path):
    str_horizontal, str_vertical = subprocess.run([
        'ffprobe',
        '-i',
        video_path,
        '-show_entries',
        'stream=display_aspect_ratio',
        '-print_format',
        'csv'
    ], stdout=subprocess.PIPE).stdout.decode('UTF-8').replace("stream,","").replace("\n","").split(":")
    return float(str_horizontal), float(str_vertical)


def get_video_length(video_path):
    return float(subprocess.run([
        'ffprobe',
        '-i',
        video_path,
        '-show_entries',
        'format=duration',
        '-print_format',
        'csv'
    ], stdout=subprocess.PIPE).stdout.decode('UTF-8').replace("format,","").replace("\n",""))

def convert_to_webm(video_path, bitrate, output_video_path=None, framerate=30):
    if output_video_path==None:
        new_video_path = re.sub("\..*$",".webm",video_path)
    else:
        new_video_path = output_video_path

    print("Bitrate: {}".format(bitrate))
    subprocess.run([
        'ffmpeg',
        '-y',
        '-i',
        video_path,
        '-preset',
        'ultrafast',
        '-vcodec',
        'libvpx',
        '-vf',
        'scale=480:-1',
        '-r',
        str(framerate),
        '-b:v',
        str(bitrate),
        new_video_path
    ], stdout=subprocess.PIPE)
    return (new_video_path, os.path.getsize(new_video_path))
