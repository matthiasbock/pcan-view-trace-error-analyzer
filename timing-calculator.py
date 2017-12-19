#!/usr/bin/python
#
# Script to calculate the timing parameters of the PCAN-USB adapter 
#


#
# Represents all relevant bus timing parameters for the SJA1000
#
class BusTiming:
    def __init__(self, btr0btr1=None, btr0=None, btr1=None):
        if (btr0btr1 is None) and (btr0 is None or btr1 is None):
            return

        if btr0btr1 is None:
            btr0btr1 = (btr0 << 8) | btr1
        else:
            btr0 = btr0btr1 >> 8
            btr1 = btr0btr1 & 0xff
        self.btr0btr1 = btr0btr1

        # Parse
        self.SJW = btr0 >> 6
        self.BRP = btr0 & 0x3f
        self.SAM = btr1 >> 7
        self.tSEG1 = btr1 & 0x0f
        self.tSEG2 = (btr1 & 0x70) >> 4

        # Adapter constants
        self.fXTAL = 16e6 # Hz
        self.tCLK = 1/self.fXTAL # s
        self.tSCL = 2*self.tCLK*(self.BRP+1)

    def __str__(self):
        return "BTR0BTR1=0x{:04x}: ".format(self.btr0btr1) \
            +"SJW=" + str(self.SJW) + "(+1), " \
            +"BRP=" + str(self.BRP) + "(+1), " \
            +"SAM=" + str(self.SAM) + " (" + str(self.SAM*3) + " samples), " \
            +"tSEG1=" + str(self.tSEG1) + "(+1), " \
            +"tSEG2=" + str(self.tSEG2) + "(+1):\n" \
            +"System frequency=" + str(16./(self.BRP+1)) + "MHz, " \
            +"System clock tick=" + str(self.tSCL*1e6) + "us, " \
            +"CAN bitrate=" + str((1/self.tSCL)/(self.SJW+1 + self.tSEG1+1 + self.tSEG2+1)/1e3) + "Kbps, " \
            +"Sample point: {:.1f}".format((1.+self.tSEG1)/(self.tSEG1+1 + self.tSEG2+1)*100) + "%"


t = BusTiming(btr0btr1=0x0016)
print(str(t))
