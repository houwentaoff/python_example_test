import qrcode
import struct
import os,sys
import numpy as np
import base64
import time
import cv2
import hashlib
import zlib
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
'crc32':0
} 
data_frame = {
'id':0,#frame num
'offset': 0,# 文件中的偏移
'len': 0, #该包数据帧的长度
'data': 0,  #二进制数据
'crc32':0
}
end_frame = {
'magic': 0, # 0x87654321
'id':0,#frame num
'md5': 0,  #md5 16B
'total': 0, #总发送长度
'crc32':0
}

def xor_encrypt(data, key):
    return bytes([byte ^ key for byte in data]) 

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
    cv2.waitKey(200)
    
def gen_beginfame(frame_id, filename, size):
    data = struct.pack("<II", 0x12345678, frame_id)
    if len(filename) < 20:
        filename += 10*'A'
    data += filename.encode()[0:20]
    data += struct.pack("<I", size)
    data += zlib.crc32(data).to_bytes(4, 'little')
    base64_encoded = base64.b64encode(data)
    qr = qrcode.QRCode(
        version=4,
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
    data += total.to_bytes(4, 'little')
    data += zlib.crc32(data).to_bytes(4, 'little')
    base64_encoded = base64.b64encode(data)
    qr = qrcode.QRCode(
        version=4,
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
    data=xor_encrypt(data, frame_id&0xff)
    msg += data
    crc = zlib.crc32(msg).to_bytes(4, 'little')
    a = struct.unpack('<I', crc)[0]
    print(hex(a))
    msg += zlib.crc32(msg).to_bytes(4, 'little')
    base64_encoded = base64.b64encode(msg)
    qr = qrcode.QRCode(
        version=40,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=2,
    )
    qr.add_data(base64_encoded)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    print(frame_id, ' img show offset:', offset, ',len:', size)
    return img
buf=b''
offset=0
xxxmode = 0
infd = os.open(sys.argv[1], os.O_RDONLY| os.O_BINARY);
if len(sys.argv) == 3:
    xxxmode = int(sys.argv[2], 10);
fillmode=False
if xxxmode == 1:
   fillmode=True 
file_size = os.path.getsize(sys.argv[1])
md5 = calculate_file_md5(sys.argv[1])
print('file size:', file_size, ' md5:', md5)

frame_id = 0
img = gen_beginfame(frame_id, sys.argv[1], file_size)
display_frame(img)
cv2.waitKey(1000)
over = False
offset = 0
block=2048   
lossframes=[2,5,568] 
lossid=0
while True:
    buf = os.read(infd, block)
    #print(len(buf))
    size = len(buf)
    if size != block:
        over=True
    frame_id += 1
    #if frame_id != 215:
        #continue
    if fillmode:
        if frame_id in lossframes:            
            img = gen_datafame(frame_id, offset, buf, size)
            display_frame(img)
        if frame_id in lossframes:            
            img = gen_datafame(frame_id, offset, buf, size)
            display_frame(img)
    else:
        img = gen_datafame(frame_id, offset, buf, size)
        display_frame(img)
    offset = offset + size
    if over:
        break;
frame_id += 1  
cv2.waitKey(1000)       
img = gen_endfame(frame_id, md5, offset)
display_frame(img) 
cv2.waitKey(1000)       
os.close(infd)
