##
## This file is part of the libsigrokdecode project.
##
## Copyright (C) 2019 Benedikt Otto <benedikt_o@web.de>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, see <http://www.gnu.org/licenses/>.
##

# source: https://stackoverflow.com/questions/8554282/creating-a-png-file-in-python/25835368#25835368

__copyright__ = "Copyright (C) 2014 Guido Draheim"
__licence__ = "Public Domain"

from .font0 import chars as font0
from .font2 import chars as font2

from common.png_output import generate_palette_png

border = 3
distance = 2


def generateImage(text, height, width, style, font):
    """
    generates a png image based on the content of the simulated display
    expects an array with dimensions width * height
    """

    if style == "green":
        style = [(100, 160, 0), (0, 0, 0)]              # black on green

    elif style == "blue":
        style = [(0, 0, 200), (255, 255, 255)]          # white on blue

    if font == "A00":
        font = font0[:]

    elif font == "A02":
        font = font2[:]

    font = [[[int(bool(line & (1 << i))) for i in range(5)] for line in char] for char in font]

    img_width = width * (5 + distance) + 2 * border - distance
    img_height = height * (8 + distance) + 2 * border - distance

    data = [[0] * img_width for x in range(img_height)]
    for line in range(height):
        for char in range(width):
            for ix in range(8):
                data[line * (8 + distance) + border + ix][char * (5 + distance) + border: char * (5 + distance) + border + 5] = font[text[line][char]][ix]

    return generate_palette_png(data, img_width, img_height, style)
