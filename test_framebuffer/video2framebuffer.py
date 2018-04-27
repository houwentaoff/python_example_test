#使用opencv 对视频文件进行处理并显示在framebuffer里面，如果写
# 入framebuffer的数据大于当前分辨率会提示No space left on device
# for中的计算量达到30多万次 在640*480的情况下,每帧刷新速度太慢
# 解决方法为全部放在矩阵中进行运算然后再每帧写入,所以说为啥图
# 片处理特别耗时
import cv2
import struct
#from PIL import Image

cap=cv2.VideoCapture("/work/video.mp4")
w = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
h = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print("w:", w, "h:", h)

bs = bytearray(640*480 * 4)
#bts = bytes()
print(len(bs))

ret, frame = cap.read()
while ret:
    with open('/dev/fb0', 'wb') as f:
        fh, fw, frgb = frame.shape
        ii = 0
        for i in range(0, 480):
            for j in range(0, fw):
                b,g,r = frame[i][j]
                #bgra=struct.pack('BBBB',b,g,r,0x0)
                bs[ii] = b
                bs[ii+1] = g
                bs[ii+2] = r
                bs[ii+3] = 0x0
                ii += 4

#                bs[i*480*4 + j] = b
#                bs[i*480*4 + j+1] = g
#                bs[i*480*4 + j+2] = r
#                bs[i*480*4 + j+3] = 0x0

                #f.write(bgra);
            #补0填充
            ii += 4*(640-fw)
            #for j in range(fw, 640):
                #bs[ii] = 0
                #bs[ii+1] = 0
                #bs[ii+2] = 0
                #bs[ii+3] = 0
             #   ii += 4

                #bgra = struct.pack('BBBB', 0, 0, 0, 0)
 #               bs[i*480*4 + fw*4 + j - fw] = 0
 #               bs[i*480*4 + fw*4 + j+1 -fw ] = 0
 #               bs[i*480*4 + fw*4 + j+2 - fw] = 0
 #               bs[i*480*4 + fw*4 + j+3 - fw] = 0
 #               print("j:", j, "fw:", fw)
                #f.write(bgra);
        #bs.append(bts)
        #bts = frame.tobytes()
        f.write(bs)
        ret, frame = cap.read()
