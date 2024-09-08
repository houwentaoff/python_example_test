import qrcode
import struct
import os,sys
import numpy as np
import base64
import time
import cv2
# 定义 uImage 头部结构
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
buf=b''
offset=0
infd = os.open(sys.argv[1], os.O_RDONLY| os.O_BINARY);
file_size = os.path.getsize(sys.argv[1])
print('file size:', file_size)
over = False
first = True
offset = 0
block=1024    
while True:
    buf = os.read(infd, block)
    print(len(buf))
    size = len(buf)
    if size != block:
        over=True
    data= struct.pack("<II", offset, size)
    data += buf
    base64_encoded = base64.b64encode(data)
    #base64_message = #base64_encoded.decode("utf-8")
    qr = qrcode.QRCode(
        version=15,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(base64_encoded)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    print('img show offset:', offset, ',len:', size, over)
    if first:
        first = False

    img = img.convert('RGB')
    img_np = np.array(img)
    '''
    # 获取原始图像的宽度和高度
    old_width, old_height = img.size
    # 设置缩放比例（例如，缩小到原来的一半）
    scale_percent = 100  # 缩小到50%

    # 计算新的宽度和高度
    new_width = int(old_width * scale_percent / 100)
    new_height = int(old_height * scale_percent / 100)
    print('w:',old_width, 'h:', old_height, ' nw:', new_width, ' nh:', new_height)

    # 设置缩放尺寸
    dim = (new_width, new_height)
    img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    resized_img = cv2.resize(img_np, dim, interpolation=cv2.INTER_AREA)
    '''
    cv2.imshow('qrcode', img_np)
    cv2.waitKey(1000) 

    offset = offset + size
    if over:
        break;
        
os.close(infd)
