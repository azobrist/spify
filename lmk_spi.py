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

def spi_read(addr,num):
    b=bytearray()
    rw = 0x80
    out = []
    if addr > 255:
        rw ^= addr>>8
    for i in range(num):
        b=[rw,addr+i,0x00]
        print(b)
        out.append(spi.xfer(b)[2])
    print(out)

def spi_write(addr,val):
    b=bytearray()
    rw = 0x00
    out = []
    if add > 255:
        rw ^= addr>>8
    b=[rw,addr,val]
    print(b)
    out.append(spi.xfer(b)[2])
    print(out)

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

def check_is_hex(string):
    if '0x' or 'h' in string:
        s = re.sub("0x|h","",string)
    else:
        s = string
    try:
        return int(s,16)
    except:
        msg = "%r: Enter hex value (0-ff)" % string
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
    
    p.add_argument("-r","--read", action="store", dest='READ_REG_ADD', type=check_is_reg,
                    help="select register to read")
    p.add_argument("-n","--number", default=1,action="store", dest='BYTE_NUM', type=int,
                    help="select number of bytes to read")
    p.add_argument("-b","--read_brd_info", action='store_true', default=False, dest='READ_BRD_INFO',
                    help="read board specific informatin")
    p.add_argument("-w","--write", action="store",dest='WRITE_REG_ADD', type=check_is_reg, 
                    help="select register to write")
    p.add_argument("-v","--value", action="store",dest='WRITE_VAL', type=check_is_hex,
                    help="write hex value to selected reg address")

    return(p.parse_args())

if __name__ == '__main__':
    
    if sys.version_info<(3,0,0):
        sys.stderr.write("You need python 3.0 or later to run this script\n")
        sys.exit(1)
        
    try:
        args = cmdline_args()
        if args.READ_BRD_INFO == True:
            spi_read(3,4)
        if args.WRITE_REG_ADD != None:
            spi_write(args.WRITE_REG_ADD,args.WRITE_VAL)
        if args.READ_REG_ADD != None:
            spi_read(args.READ_REG_ADD,args.BYTE_NUM)
    except:
        print('Try $sudo ./lmk_spi.py -r {reg address} -n {bytes to read}')
        print(args)
