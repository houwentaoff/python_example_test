import mss
from pyzbar.pyzbar import decode, ZBarSymbol
from PIL import Image
import struct
import base64
import cv2
import os
import zlib
from PIL import Image
import hashlib
import sys
def xmd5(fname):
    with open(fname, 'rb') as f:
        md5 = hashlib.md5(f.read()).hexdigest()
    print(fname, ":md5:", md5)
begin_fmt = struct.Struct(
    'I20sI'
)
data_fmt = struct.Struct(
    'I20sI'
)
end_fmt = struct.Struct(
    'I16sI'
)
begin_frame = {
'magic': 0x12345678,
'file':'aaa.tar.gz', #20B
'size': 0, #文件总大小
} 
data_frame = {
'offset': 0,# 文件中的偏移
'len': 0, #该包数据帧的长度
'data': 0,  #二进制数据
}
end_frame = {
'magic': 0, # 0x87654321
'md5': 0,  #md5
'total': 0, #总发送长度
}
file_name = ''
md5=''
frame_id = 0
size = 0
offset = 0
le=0
outfd=0
global_frame = -1
last_frame = -1
xxxmode = 0
if len(sys.argv) == 2:
    xxxmode = int(sys.argv[1], 10)
fillmode=False
if xxxmode == 1:
   fillmode=True 
# 创建mss屏幕截图对象
with mss.mss() as sct:
    # 列出所有显示器的截图
    monitor = sct.monitors[0]
    # 截图单个显示器
    while True:
        screenshot = sct.grab(monitor)
        # mss返回的是一个名为sct_PIL的Image对象，可以直接显示或保存
        
        img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
        # 使用pyzbar解码图像中的二维码
        decoded_objects = decode(img, symbols=[ZBarSymbol.QRCODE])
        if decoded_objects != None:     
            # 遍历解码对象
            for obj in decoded_objects:
                # 打印解码内容
                #print("Type:", obj.type)
                #print(obj.data.hex(),type(b'asa'))
                binary_data = base64.b64decode(obj.data)
                #print(len(binary_data))
                x, y = struct.unpack('<II', binary_data[0:0+8])
                if x == 0x12345678: #begin frame
                    frame_id = y
                    file_name = binary_data[8:28].decode()
                    size,curcrc = struct.unpack('<II', binary_data[28:36])
                    crc = zlib.crc32(binary_data[0:32])
                    if crc != curcrc:
                        print('crc err: crc:', hex(curcrc), ' expect:', hex(crc))
                    else:                        
                        if global_frame == frame_id:
                            continue
                        if fillmode:
                            outfd = os.open(file_name+"back", os.O_RDWR| os.O_BINARY );
                        else:
                            outfd = os.open(file_name+"back", os.O_RDWR| os.O_BINARY | os.O_CREAT);
                        global_frame = frame_id                                               
                    print('begin frame file:', file_name, ' size:', size)
                elif x == 0x87654321: #end frame
                    frame_id = y
                    md5 = binary_data[8:24].decode()
                    total,curcrc = struct.unpack('<II', binary_data[24:32])
                    crc = zlib.crc32(binary_data[0:28])
                    if crc != curcrc:
                        print('crc err: crc:', hex(curcrc), ' expect:', hex(crc))
                    else:                        
                        if global_frame == frame_id:
                            continue
                        os.close(outfd) 
                        global_frame = frame_id                                            
                    print('end frame, id:', frame_id, ' md5:', md5, ' already send:', total)
                    xmd5(file_name+"back")
                    exit()
                else :#data frame
                    frame_id = x
                    offset = y
                    le = struct.unpack('<I', binary_data[8:12])[0]
                    data = binary_data[12:12+le]
                    curcrc = struct.unpack('<I', binary_data[12+le:])[0]
                    if le != len(data):
                        print('frame err len:', le, ' act:', len(data))
                    #write 2 file
                    crc = zlib.crc32(binary_data[0:12+le])
                    if crc != curcrc:
                        print('crc err: crc:', hex(curcrc), ' expect:', hex(crc))
                    else:                        
                        if global_frame == frame_id:
                            continue
                        os.lseek(outfd, offset, 0)
                        os.write(outfd, data)                        
                        last_frame = global_frame
                        global_frame = frame_id
                        if global_frame - last_frame >= 2:
                            if fillmode == False:
                                print('loss frame! last frame:', last_frame, ' cur frame:', frame_id)
                    print('data frame id:', frame_id, ' offset:', offset, 'len:', le)
                    
                print ('offset:', hex(offset), ' size:', le,' ', len(binary_data))
                #cv2.waitKey(0) 
            #print ('offset:', offset, ' le:', le, 'data:', data.hex())

