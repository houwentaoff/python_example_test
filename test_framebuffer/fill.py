'''
测试将一幅图片向framebuffer中输出，结果为屏幕显示为指定的图片
'''
import struct
from PIL import Image

im = Image.open('/work/111.png')

im = im.resize((640,480))
w, h = im.size
print( "w:", w ,"h:", h)

with open('logo.fb', 'wb') as f:
    for j in range(0,h):
        for i in range(0,w):
            r,g,b,a = im.getpixel((i,j))
            #print(type(a))
            #print(a)
            bgra=struct.pack('BBBB',b,g,r,a)
            f.write(bgra);
            #补0填充
        for i in range(w, 640):
            bgra = struct.pack('BBBB', 0, 0, 0, 0)
            f.write(bgra);
