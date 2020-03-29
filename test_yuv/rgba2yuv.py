from PIL import Image
import cv2
import struct
import os
import re
import sys
import numpy as np
import threading
'''
用法:
    修改下列的5个变量，out_format的格式参考代码if中的匹配项,运行后会输出
    '(str(w)+'x'+str(h)+'.'+ out_format +'.yuv'后缀名的文件
    frames = 3
    out_format = 'yuv420-nv21'
    filename = 'E:\yuv\\320x240.rgba'
    w = 320
    h = 240
'''
def video2rgba():
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
'''
获取rgba指定位置的像素
'''
def getpixel(arr, frame, x, y):
    (r,g,b,a) = arr[frame][y][x]
    return r,g,b,a

def load_rgba(file_name, frames, w, h, byte_width):
    rgba_file = file_name #"E:\jlq\yuv\\320x240.rgba" #sys.argv[1]
    f = open(rgba_file, 'rb')
    binary=f.read(w*h*byte_width*frames)
    f.close()
    arr = np.array(list(binary), dtype=np.uint8)
    arr = arr.reshape(frames, h, w, byte_width)
    return arr
# 1plane
def rgba_convert_yuv(arr, frame, w, h):
    yuvbytes = b''
    for row in range(h):
        for col in range(w): 
            (R,G,B,A) = getpixel(arr, frame, col, row)
            Y = int(0.257 * R + 0.504 * G + 0.098 * B + 16) 
            U = int(-0.148 * R - 0.291 * G + 0.439 * B + 128)
            V = int(0.439 * R - 0.368 * G - 0.071 * B + 128)
            yuvbytes += struct.pack('<3B', Y, U, V)
    return yuvbytes
# 3 plane
def rgba_convert_yuv444(arr, frame, w, h):
    y_plane =b''
    u_plane=b''
    v_plane=b''
    for row in range(h):
        for col in range(w): 
            (R,G,B,A) = getpixel(arr, frame, col, row)
            Y = int(0.257 * R + 0.504 * G + 0.098 * B + 16) 
            U = int(-0.148*R -0.291*G + 0.439*B + 128)
            V = int(0.439*R - 0.368*G - 0.071*B + 128)
            y_plane += struct.pack('<1B', Y)
            u_plane += struct.pack('<1B', U)
            v_plane += struct.pack('<1B', V)

    return (y_plane, u_plane, v_plane)
# 3plane uv隔一个采样一个
def rgba_convert_yuv422(arr, frame, w, h):
    y_plane =b''
    u_plane=b''
    v_plane=b''
    uv=0
    for row in range(h):
        for col in range(w): 
            (R,G,B,A) = getpixel(arr, frame, col, row)
            Y = int(0.257 * R + 0.504 * G + 0.098 * B + 16)
            y_plane += struct.pack('<1B', Y)
            if uv % 2 == 0:
                U = int(-0.148*R -0.291*G + 0.439*B + 128)
                V = int(0.439*R - 0.368*G - 0.071*B + 128)
                u_plane += struct.pack('<1B', U)
                v_plane += struct.pack('<1B', V)
            uv += 1
    return (y_plane, u_plane, v_plane)
# 1plane uv隔一个采样一个uv分开采样
def rgba_convert_yuv422_yuyv(arr, frame, w, h):
    yuvbytes =b''
    uv=0
    for row in range(h):
        for col in range(w): 
            (R,G,B,A) = getpixel(arr, frame, col, row)
            Y = int(0.257 * R + 0.504 * G + 0.098 * B + 16)
            yuvbytes += struct.pack('<1B', Y)
            if uv % 2 == 0:
                U = int(-0.148*R -0.291*G + 0.439*B + 128)
                yuvbytes += struct.pack('<1B', U)
            else:
                V = int(0.439*R - 0.368*G - 0.071*B + 128)
                yuvbytes += struct.pack('<1B', V)
            uv += 1
    return yuvbytes
# 1plane uv隔一个采样一个uv分开采样
def rgba_convert_yuv422_uyvy(arr, frame, w, h):
    yuvbytes =b''
    uv=0
    for row in range(h):
        for col in range(w): 
            (R,G,B,A) = getpixel(arr, frame, col, row)
            Y = int(0.257 * R + 0.504 * G + 0.098 * B + 16)
            if uv % 2 == 0:
                U = int(-0.148*R -0.291*G + 0.439*B + 128)
                yuvbytes += struct.pack('<1B', U)
            else:
                V = int(0.439*R - 0.368*G - 0.071*B + 128)
                yuvbytes += struct.pack('<1B', V)
            yuvbytes += struct.pack('<1B', Y)
            uv += 1
    return yuvbytes
# 3plane y都进行采样，uv 横着和竖着 4个点采样一个uv （横着和竖着相邻的像素点相同） 
def rgba_convert_yuv420(arr, frame, w, h):
    y_plane =b''
    u_plane=b''
    v_plane=b''
    uv=0
    for row in range(h):
        for col in range(w): 
            (R,G,B,A) = getpixel(arr, frame, col, row)
            Y = int(0.257 * R + 0.504 * G + 0.098 * B + 16)
            y_plane += struct.pack('<1B', Y)
            if uv % 2 and row % 2 == 0:
                U = int(-0.148*R -0.291*G + 0.439*B + 128)
                V = int(0.439*R - 0.368*G - 0.071*B + 128)
                u_plane += struct.pack('<1B', U)
                v_plane += struct.pack('<1B', V)
            uv += 1
    return (y_plane, u_plane, v_plane)
# 2plane y都进行采样，uv 横着和竖着 4个点采样一个uv （横着和竖着相邻的像素点相同） uv 一起放一个plane
def rgba_convert_yuv420_nv12(arr, frame, w, h):
    y_plane =b''
    uv_plane=b''
    uv=0
    for row in range(h):
        for col in range(w): 
            (R,G,B,A) = getpixel(arr, frame, col, row)
            Y = int(0.257 * R + 0.504 * G + 0.098 * B + 16)
            y_plane += struct.pack('<1B', Y)
            if uv % 2 and row % 2 == 0:
                U = int(-0.148*R -0.291*G + 0.439*B + 128)
                V = int(0.439*R - 0.368*G - 0.071*B + 128)
                uv_plane += struct.pack('<1B', U)
                uv_plane += struct.pack('<1B', V)
            uv += 1
    return (y_plane, uv_plane)
# 2plane y都进行采样，uv 横着和竖着 4个点采样一个uv （横着和竖着相邻的像素点相同） vu 一起放一个plane
def rgba_convert_yuv420_nv21(arr, frame, w, h):
    y_plane =b''
    uv_plane=b''
    uv=0
    for row in range(h):
        for col in range(w): 
            (R,G,B,A) = getpixel(arr, frame, col, row)
            Y = int(0.257 * R + 0.504 * G + 0.098 * B + 16)
            y_plane += struct.pack('<1B', Y)
            if uv % 2 and row % 2 == 0:
                U = int(-0.148*R -0.291*G + 0.439*B + 128)
                V = int(0.439*R - 0.368*G - 0.071*B + 128)
                uv_plane += struct.pack('<1B', V)
                uv_plane += struct.pack('<1B', U)
            uv += 1
    return (y_plane, uv_plane)
def worker(arr, frame_id, format, w, h):
    global threadLock
    global dic
    yuv4xx=b''
    yuv=b''
    print('process frame id[%d] begin' % frame_id)
    if format == 'yuv444':
        yuv4xx = rgba_convert_yuv444(arr, frame_id, w, h)
    if format == 'yuv422':
        yuv4xx = rgba_convert_yuv422(arr, frame_id, w, h)
    if format == 'yuv422-yuyv':
        yuv = rgba_convert_yuv422_yuyv(arr, frame_id, w, h)
    if format == 'yuv422-uyvy':
        yuv = rgba_convert_yuv422_uyvy(arr, frame_id, w, h)
    if format == 'yuv420':
        yuv4xx = rgba_convert_yuv420(arr, frame_id, w, h)
    if format == 'yuv420-nv12':
        yuv4xx = rgba_convert_yuv420_nv12(arr, frame_id, w, h)
    if format == 'yuv420-nv21':
        yuv4xx = rgba_convert_yuv420_nv21(arr, frame_id, w, h)
    if format == 'yuv':
        yuv = rgba_convert_yuv(arr, frame_id, w, h)
    threadLock.acquire()
    if format == 'yuv444' or format == 'yuv422' or format == 'yuv420' or format == 'yuv420-nv12' or format == 'yuv420-nv21':
        dic[frame_id] = yuv4xx
    if format == 'yuv' or format == 'yuv422-yuyv' or format == 'yuv422-uyvy':
        dic[frame_id] = yuv 
    threadLock.release()
    print('process frame id[%d] over' % frame_id)

threadLock = threading.Lock()
dic = {}

if __name__ == "__main__":
    #video2rgba()
    arr = None
    frames = 3
    out_format = 'yuv420-nv21'
    filename = 'E:\yuv\\320x240.rgba'
    w = 320
    h = 240
    arr = load_rgba(filename, frames, w, h, 4)
    tids = []
    for tid in range(frames):
        t = threading.Thread(target=worker, args=(arr, tid, out_format, w, h), name='worker' + str(tid))
        tids.append(t)
    for t in tids:
        t.start()
    for t in tids:
        t.join()
    l = sorted(dic.items(), key=lambda dic:dic[0])

    outfd = os.open(str(w)+'x'+str(h)+'.'+ out_format +'.yuv', os.O_RDWR|os.O_CREAT|os.O_TRUNC)
    for i in l:
        # packed
        if out_format == 'yuv' or  out_format == 'yuv422-yuyv' or  out_format == 'yuv422-uyvy':
            #packed 1 plane
            os.write(outfd, i[1])
        if out_format == 'yuv422' or out_format == 'yuv444' or out_format == 'yuv420':
            #3 plane
            os.write(outfd, i[1][0]) 
            os.write(outfd, i[1][1]) 
            os.write(outfd, i[1][2]) 
        if out_format == 'yuv420-nv12' or out_format == 'yuv420-nv21':
            # 2 plane
            os.write(outfd, i[1][0]) 
            os.write(outfd, i[1][1]) 
    os.close(outfd)   
