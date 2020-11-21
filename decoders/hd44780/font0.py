##
## This file is part of the libsigrokdecode project.
##
## Copyright (C) 2019 Benedikt Otto <beneot@web.de>
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

chars = [
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 0: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 1: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 2: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 3: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 4: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 5: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 6: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 7: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 8: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 9: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 10: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 11: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 12: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 13: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 14: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 15: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 16: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 17: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 18: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 19: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 20: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 21: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 22: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 23: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 24: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 25: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 26: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 27: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 28: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 29: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 30: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 31: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 32: " "
    [4, 4, 4, 4, 0, 0, 4, 0],           # char: 33: "!"
    [10, 10, 10, 0, 0, 0, 0, 0],        # char: 34: """
    [10, 10, 31, 10, 31, 10, 10, 0],    # char: 35: "#"
    [4, 30, 5, 14, 20, 15, 4, 0],       # char: 36: "$"
    [3, 19, 8, 4, 2, 25, 24, 0],        # char: 37: "%"
    [6, 9, 5, 2, 21, 9, 22, 0],         # char: 38: "&"
    [6, 4, 2, 0, 0, 0, 0, 0],           # char: 39: "'"
    [8, 4, 2, 2, 2, 4, 8, 0],           # char: 40: "("
    [2, 4, 8, 8, 8, 4, 2, 0],           # char: 41: ")"
    [0, 4, 21, 14, 21, 4, 0, 0],        # char: 42: "*"
    [0, 4, 4, 31, 4, 4, 0, 0],          # char: 43: "+"
    [0, 0, 0, 0, 6, 4, 2, 0],           # char: 44: ","
    [0, 0, 0, 31, 0, 0, 0, 0],          # char: 45: "-"
    [0, 0, 0, 0, 0, 6, 6, 0],           # char: 46: "."
    [0, 16, 8, 4, 2, 1, 0, 0],          # char: 47: "/"
    [14, 17, 25, 21, 19, 17, 14, 0],    # char: 48: "0"
    [4, 6, 4, 4, 4, 4, 14, 0],          # char: 49: "1"
    [14, 17, 16, 8, 4, 2, 31, 0],       # char: 50: "2"
    [31, 8, 4, 8, 16, 17, 14, 0],       # char: 51: "3"
    [8, 12, 10, 9, 31, 8, 8, 0],        # char: 52: "4"
    [31, 1, 15, 16, 16, 17, 14, 0],     # char: 53: "5"
    [12, 2, 1, 15, 17, 17, 14, 0],      # char: 54: "6"
    [31, 17, 16, 8, 4, 4, 4, 0],        # char: 55: "7"
    [14, 17, 17, 14, 17, 17, 14, 0],    # char: 56: "8"
    [14, 17, 17, 30, 16, 8, 6, 0],      # char: 57: "9"
    [0, 6, 6, 0, 6, 6, 0, 0],           # char: 58: ":"
    [0, 6, 6, 0, 6, 4, 2, 0],           # char: 59: ";"
    [8, 4, 2, 1, 2, 4, 8, 0],           # char: 60: "<"
    [0, 0, 31, 0, 31, 0, 0, 0],         # char: 61: "="
    [2, 4, 8, 16, 8, 4, 2, 0],          # char: 62: ">"
    [14, 17, 16, 8, 4, 0, 4, 0],        # char: 63: "?"
    [14, 17, 16, 22, 21, 21, 14, 0],    # char: 64: "@"
    [14, 17, 17, 17, 31, 17, 17, 0],    # char: 65: "A"
    [15, 17, 17, 15, 17, 17, 15, 0],    # char: 66: "B"
    [14, 17, 1, 1, 1, 17, 14, 0],       # char: 67: "C"
    [7, 9, 17, 17, 17, 9, 7, 0],        # char: 68: "D"
    [31, 1, 1, 15, 1, 1, 31, 0],        # char: 69: "E"
    [31, 1, 1, 15, 1, 1, 1, 0],         # char: 70: "F"
    [14, 17, 1, 29, 17, 17, 30, 0],     # char: 71: "G"
    [17, 17, 17, 31, 17, 17, 17, 0],    # char: 72: "H"
    [14, 4, 4, 4, 4, 4, 14, 0],         # char: 73: "I"
    [28, 8, 8, 8, 8, 9, 6, 0],          # char: 74: "J"
    [17, 9, 5, 3, 5, 9, 17, 0],         # char: 75: "K"
    [1, 1, 1, 1, 1, 1, 31, 0],          # char: 76: "L"
    [17, 27, 21, 21, 17, 17, 17, 0],    # char: 77: "M"
    [17, 17, 19, 21, 25, 17, 17, 0],    # char: 78: "N"
    [14, 17, 17, 17, 17, 17, 14, 0],    # char: 79: "O"
    [15, 17, 17, 15, 1, 1, 1, 0],       # char: 80: "P"
    [14, 17, 17, 17, 21, 9, 22, 0],     # char: 81: "Q"
    [15, 17, 17, 15, 5, 9, 17, 0],      # char: 82: "R"
    [30, 1, 1, 14, 16, 16, 15, 0],      # char: 83: "S"
    [31, 4, 4, 4, 4, 4, 4, 0],          # char: 84: "T"
    [17, 17, 17, 17, 17, 17, 14, 0],    # char: 85: "U"
    [17, 17, 17, 17, 17, 10, 4, 0],     # char: 86: "V"
    [17, 17, 17, 21, 21, 21, 10, 0],    # char: 87: "W"
    [17, 17, 10, 4, 10, 17, 17, 0],     # char: 88: "X"
    [17, 17, 17, 10, 4, 4, 4, 0],       # char: 89: "Y"
    [31, 16, 8, 4, 2, 1, 31, 0],        # char: 90: "Z"
    [7, 1, 1, 1, 1, 1, 7, 0],           # char: 91: "["
    [17, 10, 31, 4, 31, 4, 4, 0],       # char: 92: "¥"
    [14, 8, 8, 8, 8, 8, 14, 0],         # char: 93: "]"
    [4, 10, 17, 0, 0, 0, 0, 0],         # char: 94: "^"
    [0, 0, 0, 0, 0, 0, 31, 0],          # char: 95: "_"
    [2, 4, 8, 0, 0, 0, 0, 0],           # char: 96: "`"
    [0, 0, 14, 16, 30, 17, 30, 0],      # char: 97: "a"
    [1, 1, 13, 19, 17, 17, 15, 0],      # char: 98: "b"
    [0, 0, 14, 1, 1, 17, 14, 0],        # char: 99: "c"
    [16, 16, 22, 25, 17, 17, 30, 0],    # char: 100: "d"
    [0, 0, 14, 17, 31, 1, 14, 0],       # char: 101: "e"
    [12, 18, 2, 7, 2, 2, 2, 0],         # char: 102: "f"
    [0, 30, 17, 17, 30, 16, 14, 0],     # char: 103: "g"
    [1, 1, 13, 19, 17, 17, 17, 0],      # char: 104: "h"
    [4, 0, 6, 4, 4, 4, 14, 0],          # char: 105: "i"
    [8, 0, 12, 8, 8, 9, 6, 0],          # char: 106: "j"
    [1, 1, 9, 5, 3, 5, 9, 0],           # char: 107: "k"
    [6, 4, 4, 4, 4, 4, 14, 0],          # char: 108: "l"
    [0, 0, 11, 21, 21, 17, 17, 0],      # char: 109: "m"
    [0, 0, 13, 19, 17, 17, 17, 0],      # char: 110: "n"
    [0, 0, 14, 17, 17, 17, 14, 0],      # char: 111: "o"
    [0, 0, 15, 17, 15, 1, 1, 0],        # char: 112: "p"
    [0, 0, 22, 25, 30, 16, 16, 0],      # char: 113: "q"
    [0, 0, 13, 19, 1, 1, 1, 0],         # char: 114: "r"
    [0, 0, 14, 1, 14, 16, 15, 0],       # char: 115: "s"
    [2, 2, 7, 2, 2, 18, 12, 0],         # char: 116: "t"
    [0, 0, 17, 17, 17, 25, 22, 0],      # char: 117: "u"
    [0, 0, 17, 17, 17, 10, 4, 0],       # char: 118: "v"
    [0, 0, 17, 21, 21, 21, 10, 0],      # char: 119: "w"
    [0, 0, 17, 10, 4, 10, 17, 0],       # char: 120: "x"
    [0, 0, 17, 17, 30, 16, 14, 0],      # char: 121: "y"
    [0, 0, 31, 8, 4, 2, 31, 0],         # char: 122: "z"
    [8, 4, 4, 2, 4, 4, 8, 0],           # char: 123: "{"
    [4, 4, 4, 4, 4, 4, 4, 0],           # char: 124: "|"
    [2, 4, 4, 8, 4, 4, 2, 0],           # char: 125: "}"
    [0, 4, 8, 31, 8, 4, 0, 0],          # char: 126: "→"
    [0, 4, 2, 31, 2, 4, 0, 0],          # char: 127: "←"
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 128: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 129: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 130: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 131: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 132: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 133: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 134: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 135: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 136: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 137: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 138: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 139: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 140: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 141: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 142: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 143: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 144: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 145: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 146: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 147: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 148: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 149: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 150: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 151: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 152: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 153: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 154: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 155: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 156: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 157: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 158: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 159: " "
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 160: " "
    [0, 0, 0, 0, 7, 5, 7, 0],           # char: 161: " "
    [28, 4, 4, 4, 0, 0, 0, 0],          # char: 162: "⌜"
    [0, 0, 0, 4, 4, 4, 7, 0],           # char: 163: "⌟"
    [0, 0, 0, 0, 1, 2, 4, 0],           # char: 164: "╲"
    [0, 0, 0, 6, 6, 0, 0, 0],           # char: 165: "・"
    [0, 31, 16, 31, 16, 8, 4, 0],       # char: 166: "ヲ"
    [0, 0, 31, 16, 12, 4, 2, 0],        # char: 167: " "
    [0, 0, 8, 4, 6, 5, 4, 0],           # char: 168: "イ"
    [0, 0, 4, 31, 17, 16, 12, 0],       # char: 169: "ゥ"
    [0, 0, 31, 4, 4, 4, 31, 0],         # char: 170: "ェ"
    [0, 0, 8, 31, 12, 10, 9, 0],        # char: 171: "ォ"
    [0, 0, 2, 31, 18, 10, 2, 0],        # char: 172: "ャ"
    [0, 0, 0, 14, 8, 8, 31, 0],         # char: 173: "ュ"
    [0, 0, 15, 8, 15, 8, 15, 0],        # char: 174: "ョ"
    [0, 0, 0, 21, 21, 16, 12, 0],       # char: 175: "ツ"
    [0, 0, 0, 31, 0, 0, 0, 0],          # char: 176: "ー"
    [31, 16, 20, 12, 4, 4, 2, 0],       # char: 177: " "
    [16, 8, 4, 6, 5, 4, 4, 0],          # char: 178: "イ"
    [4, 31, 17, 17, 16, 8, 4, 0],       # char: 179: "ウ"
    [0, 31, 4, 4, 4, 4, 31, 0],         # char: 180: "エ"
    [8, 31, 8, 12, 10, 9, 8, 0],        # char: 181: "オ"
    [2, 31, 18, 18, 18, 18, 9, 0],      # char: 182: "カ"
    [4, 31, 4, 31, 4, 4, 4, 0],         # char: 183: "キ"
    [0, 30, 18, 17, 16, 8, 6, 0],       # char: 184: "ク"
    [2, 30, 9, 8, 8, 8, 4, 0],          # char: 185: "ケ"
    [0, 31, 16, 16, 16, 16, 31, 0],     # char: 186: "コ"
    [10, 31, 10, 10, 8, 4, 2, 0],       # char: 187: "サ"
    [0, 3, 16, 19, 16, 8, 7, 0],        # char: 188: "シ"
    [0, 31, 16, 8, 4, 10, 17, 0],       # char: 189: "ス"
    [2, 31, 18, 10, 2, 2, 28, 0],       # char: 190: "セ"
    [0, 17, 17, 18, 16, 8, 6, 0],       # char: 191: "ソ"
    [0, 30, 18, 21, 24, 8, 6, 0],       # char: 192: "タ"
    [8, 7, 4, 31, 4, 4, 2, 0],          # char: 193: "チ"
    [0, 21, 21, 21, 16, 8, 4, 0],       # char: 194: "ツ"
    [14, 0, 31, 4, 4, 4, 2, 0],         # char: 195: "テ"
    [2, 2, 2, 6, 10, 2, 2, 0],          # char: 196: "ト"
    [4, 4, 31, 4, 4, 2, 1, 0],          # char: 197: "ナ"
    [0, 14, 0, 0, 0, 0, 31, 0],         # char: 198: "ニ"
    [0, 31, 16, 10, 4, 10, 1, 0],       # char: 199: "ヌ"
    [4, 31, 8, 4, 14, 21, 4, 0],        # char: 200: "ネ"
    [8, 8, 8, 8, 8, 4, 2, 0],           # char: 201: "ノ"
    [0, 4, 8, 17, 17, 17, 17, 0],       # char: 202: " "
    [1, 1, 31, 1, 1, 1, 30, 0],         # char: 203: "ヒ"
    [0, 31, 16, 16, 16, 8, 6, 0],       # char: 204: "フ"
    [0, 2, 5, 8, 16, 16, 0, 0],         # char: 205: "ヘ"
    [4, 31, 4, 4, 21, 21, 4, 0],        # char: 206: "ホ"
    [0, 31, 16, 16, 10, 4, 8, 0],       # char: 207: "マ"
    [0, 14, 0, 14, 0, 14, 16, 0],       # char: 208: " "
    [0, 4, 2, 1, 17, 31, 16, 0],        # char: 209: "ム"
    [0, 16, 16, 10, 4, 10, 1, 0],       # char: 210: "メ"
    [0, 31, 2, 31, 2, 2, 28, 0],        # char: 211: "モ"
    [2, 2, 31, 18, 10, 2, 2, 0],        # char: 212: "ヤ"
    [0, 14, 8, 8, 8, 8, 31, 0],         # char: 213: "ユ"
    [0, 31, 16, 31, 16, 16, 31, 0],     # char: 214: "ヨ"
    [14, 0, 31, 16, 16, 8, 4, 0],       # char: 215: "ラ"
    [9, 9, 9, 9, 8, 4, 2, 0],           # char: 216: "リ"
    [0, 4, 5, 5, 21, 21, 13, 0],        # char: 217: "ル"
    [0, 1, 1, 17, 9, 5, 3, 0],          # char: 218: "レ"
    [0, 31, 17, 17, 17, 17, 31, 0],     # char: 219: "ロ"
    [0, 31, 17, 17, 16, 8, 4, 0],       # char: 220: "ワ"
    [0, 3, 0, 16, 16, 8, 7, 0],         # char: 221: "ン"
    [4, 9, 2, 0, 0, 0, 0, 0],           # char: 222: " "
    [7, 5, 7, 0, 0, 0, 0, 0],           # char: 223: "°"
    [0, 0, 18, 21, 9, 9, 22, 0],        # char: 224: "α"
    [10, 0, 14, 16, 30, 17, 30, 0],     # char: 225: "ä"
    [0, 0, 14, 17, 15, 17, 15, 1],      # char: 226: "ß"
    [0, 0, 14, 1, 6, 17, 14, 0],        # char: 227: "ε"
    [0, 0, 17, 17, 17, 25, 23, 1],      # char: 228: "µ"
    [0, 0, 30, 5, 9, 17, 14, 0],        # char: 229: "σ"
    [0, 0, 12, 18, 17, 17, 15, 1],      # char: 230: "ρ"
    [0, 0, 30, 17, 17, 17, 30, 16],     # char: 231: "g"
    [0, 0, 28, 4, 4, 5, 2, 0],          # char: 232: " "
    [0, 8, 11, 8, 0, 0, 0, 0],          # char: 233: " "
    [8, 0, 12, 8, 8, 8, 8, 8],          # char: 234: "j"
    [0, 5, 2, 5, 0, 0, 0, 0],           # char: 235: " "
    [0, 4, 14, 5, 21, 14, 4, 0],        # char: 236: "¢"
    [2, 2, 7, 2, 7, 2, 30, 0],          # char: 237: "Ⱡ"
    [14, 0, 13, 19, 17, 17, 17, 0],     # char: 238: " "
    [10, 0, 14, 17, 17, 17, 14, 0],     # char: 239: "ö"
    [0, 0, 13, 19, 17, 17, 15, 1],      # char: 240: "p"
    [0, 0, 22, 25, 17, 17, 30, 16],     # char: 241: "q"
    [0, 14, 17, 31, 17, 17, 14, 0],     # char: 242: "θ"
    [0, 0, 0, 26, 21, 11, 0, 0],        # char: 243: "∞"
    [0, 0, 14, 17, 17, 10, 27, 0],      # char: 244: "Ω"
    [10, 0, 17, 17, 17, 17, 25, 22],    # char: 245: "ü"
    [31, 1, 2, 4, 2, 1, 31, 0],         # char: 246: "Σ"
    [0, 0, 31, 10, 10, 10, 25, 0],      # char: 247: "π"
    [31, 0, 17, 10, 4, 10, 17, 0],      # char: 248: " "
    [0, 0, 17, 17, 17, 17, 30, 16],     # char: 249: "<"
    [0, 16, 15, 4, 31, 4, 4, 0],        # char: 250: "ŧ"
    [0, 0, 31, 2, 30, 18, 17, 0],       # char: 251: "Ћ"
    [0, 0, 31, 21, 31, 17, 17, 0],      # char: 252: " "
    [12, 12, 0, 31, 0, 4, 0, 0],        # char: 253: "÷"
    [0, 0, 0, 0, 0, 0, 0, 0],           # char: 254: " "
    [31, 31, 31, 31, 31, 31, 31, 31],   # char: 255: "█"
]
