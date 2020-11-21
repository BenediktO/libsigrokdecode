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

import sigrokdecode as srd
from common.srdhelper import bitpack

from .display_simulator import DisplaySimulator, Dir, Shift


class ChannelError(Exception):
    pass


class Pin:
    D4, D5, D6, D7, RS, E, D0, D1, D2, D3, RW = range(11)


class Ann:
    DATACHUNK, READ_WORD, WRITE_WORD, DISP_CLEAR, DISP_HOME, \
    DISP_SET_MODE, DISP_POWER, DISP_SHIFT, DISP_SHIFT_FUNC_SET, \
    DISP_SET_CGRAM, DISP_SET_DDRAM, PIXEL_DATA = range(12)
    LINE = range(12, 12 + 4)


def extract_bit(value, bitpos, val0='Off', val1='On'):
    if value & (1 << bitpos):
        return 1, val1
    return 0, val0


class Decoder(srd.Decoder):
    api_version = 3
    id = 'hd44780'
    name = 'HD44780'
    longname = 'HD44780 display controller bus'
    desc = 'HD44780 display controller bus'
    license = 'gplv2+'
    inputs = ['logic']
    outputs = []
    tags = ['Display']

    # choose which display layout is expected, 2x16 is the default value
    # choose the ROM Code of the display
    options = (
        {'id': 'display_type', 'desc': 'Configuration of the Display',
        'default': '2x16', 'values': ('1x8', '1x16', '1x20', '1x40', '2x8', '2x12', '2x16', '2x20', '2x24', '2x40', '4x16', '4x20')},
        {'id': 'rom_code', 'desc': 'ROM Code of the Display', 'default': 'A00', 'values': ('A00', 'A02')},
        {'id': 'style', 'desc': 'Style of the display', 'default': 'blue', 'values': ('blue', 'green')},
    )

    # channel 4-7 represent the upper 4 bit of the databus and are used in 4 and 8 bit mode
    # rs marks the data as either command or character data
    channels = (
        {'id': 'd4', 'name': 'D4', 'desc': 'Data Bus 4'},
        {'id': 'd5', 'name': 'D5', 'desc': 'Data Bus 5'},
        {'id': 'd6', 'name': 'D6', 'desc': 'Data Bus 6'},
        {'id': 'd7', 'name': 'D7', 'desc': 'Data Bus 7'},
        {'id': 'rs', 'name': 'RS', 'desc': 'Register Select'},
        {'id': 'e', 'name': 'E', 'desc': 'Enable (clock)'},
    )

    # channels 0-3 are optional and only used in 8 bit mode
    # channel rw is only used if read operations are executed
    optional_channels = (
        {'id': 'd0', 'name': 'D0', 'desc': 'Data Bus 0'},
        {'id': 'd1', 'name': 'D1', 'desc': 'Data Bus 1'},
        {'id': 'd2', 'name': 'D2', 'desc': 'Data Bus 2'},
        {'id': 'd3', 'name': 'D3', 'desc': 'Data Bus 3'},
        {'id': 'rw', 'name': 'RW', 'desc': 'Read/Write'},
    )

    # chunks represents one set of data of 4 bits
    # data is used when the display is in 8 bit mode and to combine two 4 bit chunks, seperated into read and write operations
    # command decodes the sent commands
    # sim1-4 represent up to 4 rows of a simulated display
    annotations = (
        ('datachunk', 'Data Chunk'),
        ('read', 'Read'),
        ('write', 'Write'),
        ('clear display', 'Clear Display'),
        ('cursor home', 'Cursor Home'),
        ('entry mode set', 'Entry Mode Set'),
        ('display on/off', 'Display On/Off'),
        ('cursor/display shift', 'Cursor/Display Shift'),
        ('function set', 'Function Set'),
        ('set cgram address', 'Set CGRAM Address'),
        ('set ddram address', 'Set DDRAM Address'),
        ('pixel_definition_data', 'Pixel Definition Data'),
        ('sim1', 'Simulated 1. line'),
        ('sim2', 'Simulated 2. line'),
        ('sim3', 'Simulated 3. line'),
        ('sim4', 'Simulated 4. line'),
    )

    annotation_rows = (
        ('datachunks', 'Data Chunk', (Ann.DATACHUNK,)),
        ('word', 'Word', (Ann.READ_WORD, Ann.WRITE_WORD,)),
        ('command', 'Command',
            (Ann.DISP_CLEAR, Ann.DISP_HOME, Ann.DISP_SET_MODE, Ann.DISP_POWER, Ann.DISP_SHIFT,
            Ann.DISP_SHIFT_FUNC_SET, Ann.DISP_SET_CGRAM, Ann.DISP_SET_DDRAM)),
        ('pixel_data', 'Pixel Data', (Ann.PIXEL_DATA,)),
        ('row1', 'Simulated 1. line', (Ann.LINE[0],)),
        ('row2', 'Simulated 2. line', (Ann.LINE[1],)),
        ('row3', 'Simulated 3. line', (Ann.LINE[2],)),
        ('row4', 'Simulated 4. line', (Ann.LINE[3],)),
    )

    def __init__(self):
        ''' Initialize the object '''
        self.reset()

    def reset(self):
        ''' Reset the object '''
        self.data = None
        self.startData = 0
        self.data_ready = False
        self.writeTo = 'DDRAM'

    def start(self):
        ''' Register output methods, simulated Display '''
        self.out_python = self.register(srd.OUTPUT_PYTHON)
        self.out_ann = self.register(srd.OUTPUT_ANN)
        self.out_binary = self.register(srd.OUTPUT_BINARY)

        self.displaySimulator = DisplaySimulator(self.options['display_type'])

        self.displaySimulator.set_rom_code(self.options['rom_code'])

        self.displaySimulator.set_style(self.options['style'])

        self.writeTo = 'DDRAM'

    def putx(self, data):
        # Helper for annotations which span exactly one sample.
        self.put(self.ss, self.es, self.out_ann, data)

    def putp(self, data):
        # Helper for annotations which span exactly one data packet.
        self.put(self.startData, self.es, self.out_ann, data)

    def putbin(self, data):
        self.put(self.startData, self.es, self.out_binary, data)

    def handle4bits(self, pins):
        ''' combine 4 bit chunks to complete packet '''
        self.chunkData = bitpack(pins[:4])

        if self.data is None:
            self.data = self.chunkData
            self.data_ready = False
        else:
            self.data = (self.data << 4) + self.chunkData
            self.data_ready = True

    def handle8bits(self, pins):
        ''' extract 8 bit packet '''
        self.chunkData = bitpack(pins[:4] + pins[6:10])
        self.data = self.chunkData
        self.data_ready = True

    def handle_command(self, data):
        ''' decode command '''

        if data == 0x01:                # cmd: 0b00000001
            self.handle_clear_display(data)

        elif (data & 0xfe) == 0x02:     # cmd: 0b0000001X
            self.handle_cursor_home(data)

        elif (data & 0xfc) == 0x04:     # cmd: 0b000001XX
            self.handle_entry_mode_set(data)

        elif (data & 0xf8) == 0x08:     # cmd: 0b00001XXX
            self.handle_display_on_off(data)

        elif (data & 0xf0) == 0x10:     # cmd: 0b0001XXXX
            self.handle_cursor_display_shift(data)

        elif (data & 0xe0) == 0x20:     # cmd: 0b001XXXXX
            self.handle_function_set(data)

        elif (data & 0xc0) == 0x40:     # cmd: 0b001XXXXX
            self.handle_set_cgram_address(data)

        elif (data & 0x80) == 0x80:     # cmd: 0b1XXXXXXX
            self.handle_set_ddram_address(data)

    def handle_clear_display(self, data):
        ''' clears simulated Diplay '''
        self.putp([Ann.DISP_CLEAR, ['Clear Display', 'Clr', 'C']])
        self.displaySimulator.clear()

        self.writeTo = 'DDRAM'

    def handle_cursor_home(self, data):
        ''' resets cursor of the simulated Display '''
        self.putp([Ann.DISP_HOME, ['Cursor Home', 'Home', 'H']])
        self.displaySimulator.reset_cursor()

        self.writeTo = 'DDRAM'

    def handle_entry_mode_set(self, data):
        ''' set Entry Mode of the simulated Display '''
        shift, shift_labels = extract_bit(data, 0)
        direction, direction_labels = extract_bit(data, 1, val0='decrease', val1='increase')
        self.putp([Ann.DISP_SET_MODE, ['Entry Mode Set: Shift: %s, Dir: %s' % (shift_labels, direction_labels),
                                      'Mode S: %d, D: %d' % (shift, direction)]])
        self.displaySimulator.set_entry_mode(direction, shift)

    def handle_display_on_off(self, data):
        ''' switch power and cursor of the simulated Display '''
        display, display_label = extract_bit(data, 2)
        cursor, cursor_label = extract_bit(data, 1)
        blinking, blinking_label = extract_bit(data, 0)
        self.putp([Ann.DISP_POWER, ['Display Power: %s, Cursor: %s, Blink: %s' % (display_label, cursor_label, blinking_label),
            'D: %d, C: %d, B: %d' % (display, cursor, blinking)]])
        self.displaySimulator.set_display_on_off_control(display, cursor, blinking)

    def handle_cursor_display_shift(self, data):
        ''' shift the simulated Display '''
        shift_mode, shift_mode_label = extract_bit(data, 3, val0='Cursor', val1='Display')
        shift_dir, shift_dir_label = extract_bit(data, 2, val0='L', val1='R')
        self.putp([Ann.DISP_SHIFT, ['Shift: %s, Dir: %s' % (shift_mode_label, shift_dir_label),
                                    'S: %s%s' % (shift_mode, shift_dir)]])
        self.displaySimulator.shift_cursor_display(shift_mode, shift_dir)
        if shift_mode == Shift.DISPLAY:
            self.simulate_display()

    def handle_function_set(self, data):
        ''' set bit mode, number of lines and fonttype of the simulated Display '''
        dl = 8 if (data & (1 << 4)) else 4								# 0 -> 4bit, 1 -> 8bit
        lines = 2 if (data & (1 << 3)) else 1							# 0 -> 1 line, 1 -> 2 lines
        font = '5x10' if (data & (1 << 2)) else '5x8'					# 0 -> 5x8, 1 -> 5x10
        _, font_label = extract_bit(data, 2, val0='5x8', val1='5x10')
        self.putp([Ann.DISP_SHIFT_FUNC_SET, ['Function Set: Bus: %dbits, Lines: %d, Font: %s' % (dl, lines, font_label),
                                             'B: %d, L: %d, F: %s' % (dl, lines, font_label)]])
        self.displaySimulator.set_function_set(dl, lines, font)

    def handle_set_cgram_address(self, data):
        ''' Move to specified CGRAM address '''
        addr = data & 0x3f
        addr_str = '%0.2X' % addr
        self.putp([Ann.DISP_SET_CGRAM, ['Set CGRAM Address: %s' % addr_str, 'CGRAM: %s' % addr_str, 'CG%s' % addr_str]])
        self.displaySimulator.set_cgram_address(addr)
        self.writeTo = 'CGRAM'

    def handle_set_ddram_address(self, data):
        ''' Move to specified DDRAM address '''
        addr = data & 0x7f
        addr_str = '%0.2X' % addr
        self.putp([Ann.DISP_SET_DDRAM, ['Set DDRAM Address: %s' % addr_str, 'DDRAM: %s' % addr_str, 'DD%s' % addr_str]])
        self.displaySimulator.set_ddram_address(addr)
        self.writeTo = 'DDRAM'

    def simulate_display(self):
        ''' output the simulated Display '''
        self.putp([Ann.LINE[0], [self.displaySimulator.get_line(0)]])

        if self.displaySimulator.rows in [2, 4]:
            self.putp([Ann.LINE[1], [self.displaySimulator.get_line(1)]])

        if self.displaySimulator.rows == 4:
            self.putp([Ann.LINE[2], [self.displaySimulator.get_line(2)]])
            self.putp([Ann.LINE[3], [self.displaySimulator.get_line(3)]])

        self.putbin(self.displaySimulator.generate_png())

    def handle_write_data(self, data):
        ''' write data to display '''
        if self.writeTo == 'DDRAM':
            # write a character
            self.displaySimulator.write_data(data)
            self.simulate_display()

        if self.writeTo == 'CGRAM':
            # write pixel data
            self.putp([Ann.PIXEL_DATA, [format(data, '05b')]])

    def handle_write_operation(self, data, rs):
        ''' handle all write operations '''
        # command register
        if rs == 0:
            self.handle_command(data)

        # data register
        elif rs == 1:
            self.handle_write_data(data)

    def handle_read_operation(self, data, rs):
        ''' handle all read operations '''
        # not implemented yet
        pass

    def decode(self):
        ''' main decoding function '''
        pins = [Pin.D4, Pin.D5, Pin.D6, Pin.D7, Pin.D0, Pin.D1, Pin.D2, Pin.D3]

        self.have_rw = self.has_channel(Pin.RW)

        # upper 4 bits present
        self.have_4bits = all([self.has_channel(i) for i in pins[:4]]) and not any([self.has_channel(i) for i in pins[4:]])

        # all 8 bits are present
        self.have_8bits = all([self.has_channel(i) for i in pins])

        # wait for any change but a maximum of 100 samples
        conditions = [{Pin.D4: 'e'}, {Pin.D5: 'e'}, {Pin.D6: 'e'}, {Pin.D7: 'e'}, {Pin.E: 'e'}, {'skip': 100}]

        if self.have_8bits:
            conditions += [{Pin.D0: 'e'}, {Pin.D1: 'e'}, {Pin.D2: 'e'}, {Pin.D3: 'e'}]
        if self.have_rw:
            conditions.append({Pin.RW: 'e'})
        if not (self.have_4bits or self.have_8bits):
            raise ChannelError('Either use 4 or 8 data bits')

        # wait for a data chunk of 3 used for the init sequence
        pins = self.wait({Pin.D4: 'h', Pin.D5: 'h', Pin.D6: 'l', Pin.D7: 'l'})

        while True:
            # wait for falling enable (E) signal
            pins = self.wait({Pin.E: 'f'})

            # save begin of packet
            self.ss = self.samplenum
            self.cmdpins = pins[:]

            (b4, b5, b6, b7, rs, e, b0, b1, b2, b3, rw) = pins

            if self.have_4bits:
                self.handle4bits(pins)

            elif self.have_8bits:
                self.handle8bits(pins)

            self.ss = self.samplenum

            # find end of command
            self.wait(conditions)

            self.es = self.samplenum

            if self.have_4bits:
                # the correct 4 data lines are present
                val = '%0.1X' % self.chunkData
                self.putx([Ann.DATACHUNK, [val]])

            elif self.have_8bits:
                # all 8 data lines are present
                val = '%0.2X' % self.chunkData
                self.putx([Ann.READ_WORD, [val]])

            # 8 bit data present (either from one 8 bit operation or two 4 bit operations)
            if self.data_ready:
                # handle write Data to Display
                if (self.have_rw and rw == 0) or not self.have_rw:
                    self.handle_write_operation(self.data, rs)
                    val = '%0.2X' % self.data
                    self.putp([Ann.WRITE_WORD, ['Write: %s' % val, 'W: %s' % val, val]])

                # handle read Data from Display
                elif (self.have_rw and rw == 1):
                    self.handle_read_operation(self.data, rs)
                    self.putp([Ann.READ_WORD, ['Read: %s' % val, 'R: %s' % val, val]])

                self.data = None
            else:
                self.startData = self.ss
