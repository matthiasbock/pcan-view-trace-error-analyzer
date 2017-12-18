#!/usr/bin/python

from sys import argv, exit

if len(argv) < 2:
    print("Not enough arguments.")
    exit()

filename = argv[1]

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
        
        print(hex(ecc))
        
    line = f.readline()

f.close()

