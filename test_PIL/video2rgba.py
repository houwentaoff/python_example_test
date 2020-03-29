from PIL import Image
import cv2
import struct
import os
import re
import sys
import numpy as np
'''
用法:
python convert_rgb.py  transformers.age.of.extinction.2014.1080p.bluray.x264-sparks.mkv 112550 100 a.rgba
'''
video_name = sys.argv[1]
keys_frame = int(sys.argv[2]) 
cap_frames = int(sys.argv[3])  #250
out_name = sys.argv[4]
# 1. 解析视频
# 2. 设置 提出帧数
# 2. 裁剪成指定分辨率
# 3. 将rgba写入文件.raw
cap=cv2.VideoCapture(video_name)

print('total frame %d %d fps ' % (cap.get(7), cap.get(5)) )
cap.set(cv2.CAP_PROP_POS_FRAMES, keys_frame) 
frame_count = 0
with open(out_name, 'wb') as f:
    while frame_count < cap_frames:
        ret, frame = cap.read()
        im = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        im = im.resize((320, 240))
        im = im.convert('RGBA')
        w, h = im.size
        print('process cur frame ', frame_count)
        for j in range(0,h):
            for i in range(0,w):
                r,g,b,a = im.getpixel((i,j))
                #bgra=struct.pack('BBBB',b,g,r,a)
                rgba=struct.pack('BBBB',r,g,b,a)
                f.write(rgba);
        cv2.imshow('aaaa', frame)
        cv2.waitKey(100)        
        frame_count += 1

print('process over')
