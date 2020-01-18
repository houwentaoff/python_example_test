#使用opencv 对视频文件进行处理并显示在framebuffer里面，如果写
# 入framebuffer的数据大于当前分辨率会提示No space left on device
# for中的计算量达到30多万次 在640*480的情况下,每帧刷新速度太慢
# 解决方法为全部放在矩阵中进行运算然后再每帧写入,所以说为啥图
# 片处理特别耗时
import cv2
import struct
import time
#from PIL import Image

cap=cv2.VideoCapture("/home/joy/Videos/1.mp4")
w = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
h = (int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print("w:", w, "h:", h)


ret, frame = cap.read()
while ret:
    with open('/dev/fb0', 'wb') as f:
        bts = frame.tobytes()
        time.sleep(0)
        f.write(bts)
        cv2.imshow('aaaa', frame)
        cv2.waitKey(100)
        ret, frame = cap.read()
cv2.destroyWindow('aaaa')        
