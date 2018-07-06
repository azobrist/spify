#!/usr/bin/python3
 
import spidev
import time
import sys
import binascii
import re
import argparse
 
spi = spidev.SpiDev()
spi.open(3, 0)
spi.max_speed_hz = 115200 
spi.lsbfirst = False

# Split an integer input into a two byte array to send via SPI
def lmk10_info():
    b = bytearray();
    b = [0x80,0x03,0x00]
    print("TX: {0}".format(b))
    print(type(b))
#    out = bytearray()
    out = spi.xfer(b)
    b = [0x80,4,0x00]
    out.append(spi.xfer(b)[2])
    b = [0x80,0x05,0x00]
    out.append(spi.xfer(b)[2])
    b = [0x80,0x06,0x00]
    out.append(spi.xfer(b)[2])
    b = [0x80,0x0c,0x00]
    out.append(spi.xfer(b)[2])
    b = [0x80,13,0x00]
    out.append(spi.xfer(b)[2])
#    out = spi.readbytes(3)
    print(out, type(out))
 
def spi_interface(addr, val):
    a = int(addr)
    v = int(val)
    print(a,v)
    print(type(a))
    print(type(val))

# Repeatedly switch a MCP4151 digital pot off then on
#while True:
#    addr = input("Enter Reg Addr: ")
#    val = input("Enter byte value in hex: ")
#    spi_interface(addr, val)
#    lmk10_info()
#    time.sleep(0.5)

def check_is_reg(string):
    if 'R' or 'r' in string:
        s = re.sub("r|R","",string)
    else:
        s = string
    if s.isdigit():
        return int(s)
    else:
        msg = "%r: Enter Rxxx or xxx,where x is numeral" % string
        raise argparse.ArgumentTypeError(msg)

def cmdline_args():
    # Make parser object
    p = argparse.ArgumentParser(description=
        """
        ****R/W register 100****
        sudo ./lmk_spi.py -w R100 0x12
        sudo ./lmk_spi.py -r R100 -i 5
        """,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    p.add_argument("-r","--read", action="store", type=check_is_reg,
                    help="select register to read")
    p.add_argument("-i","--iteration", action="store", type=int,
                    help="seltect number of bytes to read")
                   
    return(p.parse_args())

if __name__ == '__main__':
    
    if sys.version_info<(3,0,0):
        sys.stderr.write("You need python 3.0 or later to run this script\n")
        sys.exit(1)
        
    try:
        args = cmdline_args()
        print(args)
    except:
        print('Try $python <script_name> "Hello" 123 --enable')
