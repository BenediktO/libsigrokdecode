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

from .generate_png import generateImage


class Dir:
    LEFT, RIGHT = range(2)


class Shift:
    CURSOR, DISPLAY = range(2)


# charset of the display with ROM Code A00
font0 = '                ' + \
        '                ' + \
        ' !"#$%&\'()*+,-./' + \
        '0123456789:;<=>?' + \
        '@ABCDEFGHIJKLMNO' +  \
        'PQRSTUVWXYZ[¥]^_' + \
        '`abcdefghijklmno' + \
        'pqrstuvwxyz{|}→←' + \
        '                ' + \
        '                ' + \
        '  ⌜⌟╲・ヲ イゥェォャュョツ' + \
        'ー イウエオカキクケコサシスセソ' + \
        'タチツテトナニヌネノ ヒフヘホマ' + \
        ' ムメモヤユヨラリルレロワン °' + \
        'αäßεµσρg  j ¢Ⱡ ö' + \
        'pqθ∞ΩüΣπ <ŧЋ ÷ █'


# charset of the display with ROM Code A02
font2 = '                ' + \
        '▶◀“”  ●↲↑↓→←  ▲▼' + \
        ' !"#$%&\'()*+,-./' + \
        '0123456789:;<=>?' + \
        '@ABCDEFGHIJKLMNO' +  \
        'PQRSTUVWXYZ[\\]^_' + \
        '`abcdefghijklmno' + \
        'pqrstuvwxyz{|}~⌂' + \
        'БДЖЗИЙлЛУЦцШЩЪЫЭ' + \
        'α♪ΓπΣσ♬τ🔔θΩδ∞♥ε ' + \
        '‖¡¢₤¤¥╎$ƒª≪ЮЯ   ' + \
        '°±²³ µ ·ω¹º≫¼½¾¿' + \
        'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏ' + \
        'ÐÑÒÓÔÕÖ×ΦÙÚÛÜÝÞß' + \
        'àáâãäåæçèéêëìíîï' + \
        'ðñòóôõö÷∮ùúûüýþÿ'


displayConfigs = {
    '1x8':  (1, 8,  [0x00]),
    '1x16': (1, 16, [0x00]),
    '1x20': (1, 16, [0x00]),
    '1x40': (1, 16, [0x00]),
    '2x8':  (2, 8,  [0x00, 0x40]),
    '2x12': (2, 12, [0x00, 0x40]),
    '2x16': (2, 16, [0x00, 0x40]),
    '2x20': (2, 20, [0x00, 0x40]),
    '2x24': (2, 24, [0x00, 0x40]),
    '2x40': (2, 40, [0x00, 0x40]),
    '4x16': (4, 16, [0x00, 0x40, 0x10, 0x50]),
    '4x20': (4, 20, [0x00, 0x40, 0x14, 0x54]),
}


class DDRAM:
    """ Holds the character data of the display """
    def __init__(self):
        self.bank0 = [0x20 for _ in range(0x00, 0x27 + 1)]
        self.bank1 = [0x20 for _ in range(0x40, 0x67 + 1)]

        self.length = 0x67 + 1

    def write(self, addr, data):
        # set ddrom at given addr and data
        if addr in range(0x00, 0x27 + 1):
            self.bank0[addr - 0x00] = data

        elif addr in range(0x40, 0x67 + 1):
            self.bank1[addr - 0x40] = data

    def read(self, addr):
        # get ddrom at given addr
        if addr in range(0x00, 0x27 + 1):
            return self.bank0[addr - 0x00]

        elif addr in range(0x40, 0x67 + 1):
            return self.bank1[addr - 0x40]

    def shift_left(self):
        # shift both banks seperatly to the left
        self.bank0 = self.bank0[1:] + [self.bank0[0]]
        self.bank1 = self.bank1[1:] + [self.bank1[0]]

    def shift_right(self):
        # shift both banks seperatly to the right
        self.bank0 = [self.bank0[-1]] + self.bank0[:-1]
        self.bank1 = [self.bank1[-1]] + self.bank1[:-1]


class DisplaySimulator:
    def __init__(self, config):
        # reset display content
        self.clear()
        self.reset_cursor()

        self.power = False
        self.showCursor = False
        self.blinkCursor = False
        self.cgram_address = 0

        self.interfaceLength = 8
        self.numberLines = 1
        self.font = 0

        self.modeDirection = 'I'
        self.shiftCursorWrite = 0

        self.config = config
        self.configTuple = displayConfigs[self.config]

        self.rows = self.configTuple[0]
        self.cols = self.configTuple[1]
        self.startAddresses = self.configTuple[2]

    def clear(self):
        '''
        Clears display
        command: 0b00000001
        '''
        self.ddram = DDRAM()
        self.cgramLength = 100

    def reset_cursor(self):
        '''
        Resets cursor
        command: 0b0000001*
        '''
        self.cursor = 0

    def set_entry_mode(self, modeDirection, shiftCursorWrite):
        '''
        Sets entry Mode
        command: 0b000001**
        '''
        self.modeDirection = modeDirection
        self.shiftCursorWrite = shiftCursorWrite

    def set_display_on_off_control(self, power, cursor, blink):
        '''
        Sets display On Off Control
        command: 0b00001***
        '''
        self.set_display_power(power)
        self.set_show_cursor(cursor)
        self.set_blink_cursor(blink)

    def set_display_power(self, power):
        self.power = power

    def set_show_cursor(self, cursor):
        self.showCursor = cursor

    def set_blink_cursor(self, blink):
        self.blinkCursor = blink

    def shift_cursor_display(self, mode, direction):
        ''' Shifts Cursor or Display content, command: 0b0001**** '''
        if mode == Shift.CURSOR:
            self.shift_cursor(direction)
        elif mode == Shift.DISPLAY:
            self.shift_display(direction)

    def shift_cursor(self, direction):
        ''' Shift Cursor '''
        if direction == Dir.RIGHT:
            self.cursor = (self.cursor + 1) % self.ddram.length
        elif direction == Dir.LEFT:
            self.cursor = (self.cursor - 1) % self.ddram.length

    def shift_display(self, direction):
        ''' Shift content of the display '''
        if direction == Dir.RIGHT:
            self.ddram.shift_right()
        elif direction == Dir.LEFT:
            self.ddram.shift_left()

    def write_data(self, data):
        ''' Write Data, RS = 1 '''
        self.ddram.write(self.cursor, data)
        self.handle_shift_cursor()

    def handle_shift_cursor(self):
        ''' Shift Cursor or Text after writing one character '''
        if not self.shiftCursorWrite:
            if self.modeDirection == Dir.RIGHT:
                self.cursor = (self.cursor + 1) % self.ddram.length
            elif self.modeDirection == Dir.LEFT:
                self.cursor = (self.cursor - 1) % self.ddram.length
        else:
            if self.modeDirection == Dir.RIGHT:
                self.ddram.shift_left()
            elif self.modeDirection == Dir.LEFT:
                self.ddram.shift_right()

    def set_rom_code(self, value):
        ''' Set the ROM Code and therefore the font '''
        self.rom_code = value
        if value == 'A00':
            self.charset = font0

        elif value == 'A02':
            self.charset = font2

    def to_str(self, line, num):
        ''' returns the content of one digit as a string '''
        addr = self.startAddresses[line] + num

        val = self.ddram.read(addr)

        if val in range(0x20, len(self.charset)):
            return self.charset[val]

        elif val < 16:
            # bank for up to 8 special characters
            customCharacter = val % 8
            return 'CC%d' % customCharacter
        else:
            return ' '

    def get_line(self, line):
        ''' returns the content of one line as a string '''
        return ''.join([self.to_str(line, i) for i in range(self.cols)])

    def to_array(self):
        return [[self.ddram.read(startAddress + i) for i in range(self.cols)] for startAddress in self.startAddresses]

    def set_function_set(self, dl, n, f):
        '''
        Sets Function Set
        command: 0b001*****
        '''
        self.interfaceLength = dl
        self.numberLines = n
        self.font = f

    def set_ddram_address(self, address):
        '''
        Sets DDRAM Address
        command: 0b01******
        '''
        if address < self.ddram.length:
            self.cursor = address
        else:
            print('Error: DD Address %d out of range' % address)

    def set_cgram_address(self, address):
        '''
        Sets CGRAM Address
        command: 0b1*******
        '''
        if address in range(self.cgramLength):
            self.cgram_address = address
        else:
            print('Error: CG Address %d out of range' % address)

    def set_style(self, style):
        self.style = style

    def generate_png(self):
        return generateImage(self.to_array(), self.rows, self.cols, self.style, self.rom_code)
