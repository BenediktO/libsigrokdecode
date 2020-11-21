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


import zlib
import struct

def I1(value):
    return struct.pack("!B", value & (2**8-1))

def Iline(s, values):
    return struct.pack(s, *[value & (2**8-1) for value in values])

def I4(value):
    return struct.pack("!I", value & (2**32-1))

def generate_palette_png(data, width, height, palette):
    ''' generates a png image using a palette '''
    png = b"\x89" + "PNG\r\n\x1A\n".encode('ascii')

    s = "!" + "B"*width

    #IHDR:
    IHDR = I4(width) + I4(height)
    IHDR += b"\x08\x03\x00\x00\x00"
    block = "IHDR".encode('ascii') + IHDR
    png += I4(len(IHDR)) + block + I4(zlib.crc32(block))

    #PLTE:
    PLTE = b""
    for c in palette:
        PLTE += I1(c[0]) + I1(c[1]) + I1(c[2])
    block = "PLTE".encode('ascii') + PLTE
    png += I4(len(PLTE)) + block + I4(zlib.crc32(block))

    #IDAT:
    raw = b""
    for y in range(height):
        raw += b"\0"
        raw += Iline(s, data[y])

    compressor = zlib.compressobj()
    compressed = compressor.compress(raw)
    compressed += compressor.flush()
    block = "IDAT".encode('ascii') + compressed
    png += I4(len(compressed)) + block + I4(zlib.crc32(block))

    #IEND:
    block = "IEND".encode('ascii')
    png += I4(0) + block + I4(zlib.crc32(block))
    return png
