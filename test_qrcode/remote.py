import qrcode
import struct
import os,sys
import numpy as np
import base64
import time
import cv2
import hashlib
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
'id':0,#frame num
'file':'aaa.tar.gz', #20B
'size': 0, #文件总大小
} 
data_frame = {
'id':0,#frame num
'offset': 0,# 文件中的偏移
'len': 0, #该包数据帧的长度
'data': 0,  #二进制数据
}
end_frame = {
'magic': 0, # 0x87654321
'id':0,#frame num
'md5': 0,  #md5 16B
'total': 0, #总发送长度
}
def calculate_file_md5(file_path):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            md5.update(chunk)
    return md5.hexdigest()
def display_frame(img):
    img = img.convert('RGB')
    img_np = np.array(img)
    cv2.imshow('bigbang', img_np)
    cv2.waitKey(1000)
    
def gen_beginfame(frame_id, filename, size):
    data = struct.pack("<II", 0x12345678, frame_id)
    data += filename.encode()[0:20]
    data += struct.pack("<I", size)
    base64_encoded = base64.b64encode(data)
    qr = qrcode.QRCode(
        version=15,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(base64_encoded)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    print(frame_id, ' file:', filename, ',size:', size)
    return img
def gen_endfame(frame_id, md5, total):
    data = struct.pack("<II", 0x87654321, frame_id)
    data += md5.encode()[0:16]
    base64_encoded = base64.b64encode(data)
    qr = qrcode.QRCode(
        version=15,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(base64_encoded)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    print(frame_id, 'md5:', md5, ',total:', total)
    return img
def gen_datafame(frame_id, offset, data, size):
    msg = struct.pack("<III", frame_id, offset, size)
    msg += data
    base64_encoded = base64.b64encode(msg)
    qr = qrcode.QRCode(
        version=15,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(base64_encoded)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    print(frame_id, ' img show offset:', offset, ',len:', size)
    return img
buf=b''
offset=0
infd = os.open(sys.argv[1], os.O_RDONLY| os.O_BINARY);
file_size = os.path.getsize(sys.argv[1])
md5 = calculate_file_md5(sys.argv[1])
print('file size:', file_size, ' md5:', md5)

frame_id = 0
img = gen_beginfame(frame_id, sys.argv[1], file_size)
display_frame(img)
over = False
offset = 0
block=1024   
 
while True:
    buf = os.read(infd, block)
    #print(len(buf))
    size = len(buf)
    if size != block:
        over=True
    frame_id += 1
    img = gen_datafame(frame_id, offset, buf, size)
    display_frame(img)

    offset = offset + size
    if over:
        break;
frame_id += 1        
img = gen_endfame(frame_id, md5, offset)
display_frame(img)        
os.close(infd)
