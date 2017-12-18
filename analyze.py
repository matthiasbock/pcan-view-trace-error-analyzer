#!/usr/bin/python

from sys import argv, exit

if len(argv) < 2:
    print("Not enough arguments.")
    exit()

filename = argv[1]


class ecc_register():
    ERRC_BIT_ERROR   = 0x00
    ERRC_FORM_ERROR  = 0x40
    ERRC_STUFF_ERROR = 0x80
    ERRC_OTHER_ERROR = 0xC0
    
    DIR_RX = 0x20
    DIR_TX = 0x00

    SEGMENTS = \
    {
        0x00: 'error disappeared (decrementing error counter)',
        0x03: 'start of frame',
        0x02: 'ID.28 to ID.21',
        0x06: 'ID.20 to ID.18',
        #...
        0x0A: 'data field',
        0x08: 'CRC sequence',
        0x18: 'CRC delimiter',
        0x19: 'acknowledge slot',
        0x1B: 'acknowledge delimiter',
        0x1A: 'end of frame',
        #...
    }
    
    def __init__(self, ecc):
        self.errc = ecc & 0xC0
        self.dir = ecc & 0x20
        self.segment = ecc & 0x1F
        #print('{}: {} {} {}'.format(hex(ecc), hex(self.errc), hex(self.dir), hex(self.segment)))

    def get_errc(self):
        if self.errc == ecc_register.ERRC_BIT_ERROR:
            return "Bit error"
        if self.errc == ecc_register.ERRC_FORM_ERROR:
            return "Form error"
        if self.errc == ecc_register.ERRC_STUFF_ERROR:
            return "Stuffing error"
        if self.errc == ecc_register.ERRC_OTHER_ERROR:
            return "Other error"
        return "Invalid error code"

    def get_dir(self):
        if self.dir == ecc_register.DIR_RX:
            return "Rx"
        if self.dir == ecc_register.DIR_TX:
            return "Tx"
        return "invalid direction"
    
    def get_segment(self):
        if self.segment in ecc_register.SEGMENTS.keys():
            return ecc_register.SEGMENTS[self.segment]
        return "invalid segment code {}".format(hex(self.segment))

    def __str__(self):
        return self.get_errc()+","+self.get_dir()+","+self.get_segment()


def parse_ecc(value):
    ecc = ecc_register(value)
    return str(ecc)


f = open(filename, 'r')

line = f.readline()
while line:
    if line.find("Error") > -1:
        # Extract the four error code bytes at the end of the line
        error_code = [int('0x'+s, 16) for s in line.strip()[-(4*2+3):].split(' ')]

        # SJA1000 error code capture register
        ecc = error_code[1]
        # SJA1000 RX error counter register
        rxerr = error_code[2]
        # SJA1000 TX error counter register
        txerr = error_code[3]
        
        print(parse_ecc(ecc))
        
    line = f.readline()

f.close()

