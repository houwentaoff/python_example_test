import serial
import time
import os
con = serial.Serial("/dev/ttyUSB1", 115200)
#con.open()
#s = con.readline()
#s = con.read(3)

#s = con.read_until(b'>')
addr=0x34400000
if True:#s == b'xxx>':
    print('parse header')
    while True:
        #devmem 0x34400000 32
        
        cmd = 'devmem ' + str(hex(addr)) + ' 32\n'
        con.write(bytes(cmd, encoding='utf-8'))
        time.sleep(0.1)
        con.read_until(b'\n')
        s = con.read_until(b'\n')
        con.read_until(b'\n')
        ss = str(s, 'utf-8')
        ss = ss.strip('\r\n')
        ss = ss[2:]
        if ss == '0':
           ss = '00000000'
        if len(ss) < 8:
            ss = (8-len(ss))*'0' + ss
        print(ss, " ", hex(addr))
        addr += 4
        if addr > 0x3440ffff:
            break;
con.close()
