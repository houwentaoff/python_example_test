from PIL import Image
import struct
import os
import re

def str_to_hex(s, sep, bitw=32):
    s = re.split(sep, s)
    #print(s[0])
    send_buf = b''
    #print(len(s), s[0], type(s[0]))
    for i in range(len(s)-1):
        if len(s[i]) == 0:
            continue
        if s[i].find('0x') == -1:
            argb = '0x' + s[i]
        else:
            argb = s[i]
            
        bb=int(argb, 16).to_bytes(4, byteorder='little', signed=False)
        (b,g,r,a) = struct.unpack('<4B', bb)
        if a == 0x0:
            a = 0xff;
        #print((b,g,r,a))
        send_buf  += struct.pack('<4B', r, g, b, a)
    return(send_buf)
bb = str_to_hex('0x123456 0x123457 ', "[ ]")
for c in bb:
    print(hex(c), end=' ')
    
#exit()
''' src.data
12345
112233
44556677
112233
'''
f = open('src.data', 'r')
text=f.read();
f.close();
bdata = str_to_hex(text, '\n')

im = Image.new('RGBA', (480,800), 'Red');
data=bdata;
disp = Image.frombytes('RGBA', (480,7), data, decoder_name='raw')
disp.show()

''' log file
  Pixel Data =
  0x112233 0x223344 ...
  0x334455 ...
  
  Pixel Data = 
  0x113344 ...
  ...

'''
f = open('DSI_video.dump', 'r')
text=f.read();
f.close();
pattern = re.compile(r' Pixel Data =(.*?)\n\n', re.S)
lines=re.findall(pattern, text)
print("total:%d lines" % len(lines))
i = 0;
bdata=b'';

for line in lines:
    bdata += str_to_hex(line, '[\n ]')
data=bdata;
disp = Image.frombytes('RGBA', (480,576), data, decoder_name='raw')
disp.show()
