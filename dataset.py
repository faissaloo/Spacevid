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

def write_data(output, length, bitrate, horizontal_aspect, vertical_aspect):
    with open('dataset/dataset.csv', 'a+') as f:
        if f.tell() == 0:
            f.write("output size in bytes,length in seconds,bitrate,horizontal aspect,vertical aspect\n")
        f.write("{},{},{},{},{}".format(output, length, bitrate, horizontal_aspect, vertical_aspect)+"\n")

class InadequateDataError(Exception):
    pass
