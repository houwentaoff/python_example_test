import mss
from pyzbar.pyzbar import decode
from PIL import Image
import struct
import base64
import cv2
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
# 创建mss屏幕截图对象
with mss.mss() as sct:
    # 列出所有显示器的截图
    monitor = sct.monitors[0]
    # 截图单个显示器
    while True:
        screenshot = sct.grab(monitor)
        # mss返回的是一个名为sct_PIL的Image对象，可以直接显示或保存
        from PIL import Image
        img = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
        # 使用pyzbar解码图像中的二维码
        decoded_objects = decode(img)
        # 遍历解码对象
        for obj in decoded_objects:
            # 打印解码内容
            #print("Type:", obj.type)
            #print(obj.data.hex(),type(b'asa'))
            binary_data = base64.b64decode(obj.data)
            offset, le = struct.unpack('<II', binary_data[0:0+8])
            print ('offset:', hex(offset), ' size:', le,' ', len(binary_data))
            data =  binary_data[8:]
            cv2.waitKey(800) 
            #print ('offset:', offset, ' le:', le, 'data:', data.hex())

