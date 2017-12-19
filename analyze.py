#!/usr/bin/python

from sys import argv, exit


#
# Parser for ECC information from PCAN-View Trace log "Error" line/frame
#
class ECC_Info():
    # Acceptable error codes as stored in ID field (PCAN-specific)
    ERRC_UPDATED     = 0
    ERRC_BIT_ERROR   = 1
    ERRC_FORM_ERROR  = 2
    ERRC_STUFF_ERROR = 4
    ERRC_OTHER_ERROR = 8
    
    # Acceptable directions
    DIR_RX = 1
    DIR_TX = 0

    # SJA1000 frame bit position codes (aka segments)
    FRAME_BIT_POSITION_CODES = \
    {
        0: 'no error',
        2: 'ID.28 to ID.21',
        3: 'start of frame',
        4: 'bit SRTR',
        5: 'bit IDE',
        6: 'ID.20 to ID.18',
        7: 'ID.17 to ID.13',
        8: 'CRC sequence',
        9: 'reserved bit 0',
        10: 'data field',
        11: 'data length code',
        12: 'bit RTR',
        13: 'reserved bit 1',
        14: "ID.4 to ID.0",
        15: "ID.12 to ID.5",
        17: "active error flag",
        18: "intermission",
        19: "tolerate dominant bits",
        23: "error delimiter",
        24: 'CRC delimiter',
        25: 'acknowledge slot',
        26: 'end of frame',
        27: 'acknowledge delimiter',
        28: "overload flag",
    }

    def __init__(self, id, dir, seg):
        self.errc = id #ecc & 0xC0
        self.dir = dir #ecc & 0x20
        self.segment = seg #ecc & 0x1F
        #print('{}: {} {} {}'.format(hex(ecc), hex(self.errc), hex(self.dir), hex(self.segment)))

    def get_errc(self):
        if self.errc == ECC_Info.ERRC_UPDATED:
            return "Updated error counter"
        if self.errc == ECC_Info.ERRC_BIT_ERROR:
            return "Bit error"
        if self.errc == ECC_Info.ERRC_FORM_ERROR:
            return "Form error"
        if self.errc == ECC_Info.ERRC_STUFF_ERROR:
            return "Stuffing error"
        if self.errc == ECC_Info.ERRC_OTHER_ERROR:
            return "Other error"
        return "Invalid error code"

    def get_dir(self):
        if self.dir == ECC_Info.DIR_RX:
            return "Rx"
        if self.dir == ECC_Info.DIR_TX:
            return "Tx"
        return "invalid direction"

    def get_segment(self):
        if self.segment in ECC_Info.FRAME_BIT_POSITION_CODES.keys():
            return ECC_Info.FRAME_BIT_POSITION_CODES[self.segment]
        return "invalid frame bit position code {}".format(hex(self.segment))

    def __str__(self):
        return self.get_errc()+","+self.get_dir()+","+self.get_segment()


#
# Parser for PCAN-View Trace log "Error" line/frame
#
class Line:
    def __init__(self, line):
                # Remove duplicate spaces to allow for splitting
        line = line.strip()
        while line.find("  ") > -1:
            line = line.replace("  ", " ")

        s = line.split(" ")

        # Extract error ID
        ID = int(s[3])

        # Extract the four error code bytes at the end of the line
        error_code = [int('0x'+s[i], 16) for i in range(len(s)-4, len(s))]

        # SJA1000 error code capture register
        dir = error_code[0]
        seg = error_code[1]
        # SJA1000 RX error counter register
        rxerr = error_code[2]
        # SJA1000 TX error counter register
        txerr = error_code[3]

        self.ECC_Info = ECC_Info(ID, dir, seg)


if len(argv) < 2:
    print("Not enough arguments.")
    exit()

filename = argv[1]

f = open(filename, 'r')

line = f.readline()
while line:
    if line.find("Error") > -1:
        parsed_line = Line(line)
        print(str(parsed_line.ECC_Info))

    line = f.readline()

f.close()

