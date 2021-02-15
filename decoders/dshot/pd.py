##
## This file is part of the libsigrokdecode project.
##
## Copyright (C) 2021 Benedikt Otto <benedikt_o@web.de>
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

class Pin:
    DATA = 0

class Field:
    BIT, DATA, REQ_TEL, CRC, WARNING = range(5)

# structure: string: (ontime, offtime, bittime) in microseconds
TIMINGS = {
    150: (5.0, 2.5, 6.667),
    300: (2.5, 1.25, 3.333),
    600: (1.25, 0.625, 1.667),
    1200: (0.625, 0.313, 0.833),
}
BAUDRATES = tuple(TIMINGS.keys())

# format is only used for throttle value
FORMAT_STRINGS = {
    'decimal': '%d',
    'hex': '0x%x',
}
FORMATS = tuple(FORMAT_STRINGS.keys())

class SamplerateError(Exception):
    pass

class Decoder(srd.Decoder):
    api_version = 3
    id = 'dshot'
    name = 'DShot'
    longname = 'DShot protocol'
    desc = 'Digital protocol for ESCs'
    license = 'gplv2+'
    inputs = ['logic']
    outputs = []
    tags = ['RC']
    channels = (
        {'id': 'data', 'name': 'DATA', 'desc': 'DATA line'},
    )
    options = (
        {'id': 'polarity', 'desc': 'Expected polarity',
            'default': 'active-high', 'values': ('active-high', 'active-low')},
        {'id': 'baudrate', 'desc': 'Baudrate (kBaud)',
            'default': BAUDRATES[0], 'values': BAUDRATES},
        {'id': 'tolerance', 'desc': 'Tolerance (%)',
            'default': 10},
        {'id': 'format', 'desc': 'Number format (throttle only)',
            'default': FORMATS[0], 'values': FORMATS},
    )
    annotations = (
        ('bit', 'Bit'),
        ('data', 'Data'),
        ('tel_request', 'Telemetry request'),
        ('checksum', 'Checksum'),
        ('warning', 'Warning'),
    )
    annotation_rows = (
        ('bits', 'Bits', (Field.BIT,)),
        ('fields', 'Fields', (Field.DATA, Field.REQ_TEL, Field.CRC)),
        ('warnings', 'Warnings', (Field.WARNING,)),
    )

    def __init__(self):
        self.reset()

    def reset(self):
        self.samplerate = None
        self.on_sample = None
        self.off_sample = None
        self.field_start = 0
        self.bits = []

    def start(self):
        self.out_ann = self.register(srd.OUTPUT_ANN)

    def metadata(self, key, value):
        if key == srd.SRD_CONF_SAMPLERATE:
            self.samplerate = value

    def putb(self, data):
        # Annotation for a single bit.
        self.put(self.on_sample, self.samplenum, self.out_ann, data)

    def putf(self, data):
        # Annotation for a single bit.
        self.put(self.field_start, self.samplenum, self.out_ann, data)

    def puto(self, data):
        # Annotation for a single off period.
        self.put(self.off_sample, self.samplenum, self.out_ann, data)

    def match_tolerance(self, value, compare):
        return (1 - self.tolerance) < (value / compare) < (1 + self.tolerance)

    def handle_bit(self, bit, last=False):
        # handles one bit
        self.putb([Field.BIT, ['01'[bit]]])
        num_bits = len(self.bits)
        if num_bits in (0, 11, 12):
            self.field_start = self.on_sample
        self.bits.append(bit)
        num_bits += 1
        # data
        if num_bits == 11:
            data = bitpack(self.bits[10::-1])
            formatted = self.formatter % data
            explanation = ''
            if data == 0:
                explanation = '(disarm) '
            elif data < 48:
                explanation = '(reserved) '
            self.putf([Field.DATA, ['throttle: %s%s' % (explanation, formatted),
                       'throttle: %s' % formatted, formatted]])
        # telemetry request
        elif num_bits == 12:
            telemetry = self.bits[11]
            self.putf([Field.REQ_TEL, ['telemetry: %d' % telemetry, str(telemetry)]])
        # crc
        elif num_bits == 16:
            data = bitpack(self.bits[:12])
            crc = (data ^ (data >> 4) ^ (data >> 8)) & 0xf
            checksum = bitpack(self.bits[12:])
            self.putf([Field.CRC, ['crc: 0x%x' % checksum, '0x%x' % checksum]])
            if crc != checksum:
                self.putf([Field.WARNING, ['Invalid checksum: 0x%x, 0x%x' % (crc, checksum)]])
        if last:
            self.bits = []

    def to_samplenum(self, time):
        return time * self.samplerate / 1e6

    def to_time(self, samples):
        return samples / self.samplerate * 1e6

    def decode(self):
        if not self.samplerate:
            raise SamplerateError('Cannot decode without samplerate.')

        pos_edge, neg_edge = 'r', 'f'
        if self.options['polarity'] == 'active-low':
            pos_edge, neg_edge = 'f', 'r'

        self.formatter = FORMAT_STRINGS[self.options['format']]
        self.tolerance = self.options['tolerance'] / 100

        # times
        t1h, t0h, period = TIMINGS[self.options['baudrate']]
        t1l, t0l = period - t1h, period - t0h

        # samples
        samples_t1l, samples_t1h = self.to_samplenum(t1l), self.to_samplenum(t1h)
        samples_t0l, samples_t0h = self.to_samplenum(t0l), self.to_samplenum(t0h)

        safety_factor = (1 + 0.1 + 2 * self.tolerance)
        skip_0_samples = int(self.to_samplenum(t0l * safety_factor) + 0.5)
        skip_1_samples = int(self.to_samplenum(t1l * safety_factor) + 0.5)

        # at least 21 zero-bits are recommended
        min_reset_samples = int(self.to_samplenum(21 * period) + 0.5)

        guessed_bit = None
        bit = None

        wait_statements = [
            {Pin.DATA: pos_edge},
            [{Pin.DATA: pos_edge}, {'skip': skip_0_samples}],
            [{Pin.DATA: pos_edge}, {'skip': skip_1_samples}],
            {Pin.DATA: neg_edge},
        ]

        while True:
            # Guess bit
            if self.on_sample is not None:
                on_samples = self.off_sample - self.on_sample
                guessed_bit = None
                if self.match_tolerance(on_samples, samples_t1h):
                    guessed_bit = 1
                elif self.match_tolerance(on_samples, samples_t0h):
                    guessed_bit = 0

            if guessed_bit is None:
                self.wait(wait_statements[0])
            else:
                self.wait(wait_statements[1 + guessed_bit])

            if self.matched[0]:
                # Complete bit
                if self.on_sample is not None:
                    off_samples = (self.samplenum - self.off_sample)
                    bit = None
                    if guessed_bit == 1 and self.match_tolerance(off_samples, samples_t1l):
                        bit = 1
                    elif guessed_bit == 0 and self.match_tolerance(off_samples, samples_t0l):
                        bit = 0

                    if bit is not None:
                        self.handle_bit(bit)
                    else:
                        self.putb([Field.WARNING, ['Invalid timing: %0.2fµs, %0.2fµs' % (
                            self.to_time(on_samples), self.to_time(off_samples))]])
            else:
                # Last half bit
                if guessed_bit is not None:
                    self.handle_bit(guessed_bit, last=True)
                    bit = None
                self.wait(wait_statements[0])
                if (self.samplenum - self.off_sample) < min_reset_samples:
                    self.puto([Field.WARNING, ['Reset time too short: %0.2fµs' % \
                        self.to_time(self.samplenum - self.off_sample)]])

            self.on_sample = self.samplenum
            self.wait(wait_statements[3])
            self.off_sample = self.samplenum
