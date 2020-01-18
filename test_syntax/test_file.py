#!/usr/bin/python3
import sys
import keyword
import  fcntl # ioctl 
import os,sys,struct

def test_argv():
    try:
        argc = len(sys.argv)
        print("argv count:", argc)
        for v in sys.argv:
            print(v);
    except e:
        print(e)
#f = open(, "r+b")

def test_keyword():
    print(dir(keyword));
    print(keyword.__all__);

def test_file(fileName):
    f = open(fileName, "a+")
    print(type(f))
    s = "abcde\n"
    #f.write(s.encode())#str ->  bytes
    f.write(s)
    f.flush()
    #f.write(b"2abcde\n")#写入二进制需要将字符串进行转换
    f.write("2abcde\n")
    f.flush()
    f.seek(0)#这句很重要 不然不能读出数据
    buf = f.read(300)
    #print(type(buf), "buf:", buf.decode())#bytes --> str
    print(type(buf), "buf:\n", buf)
    f.close()
def test_file2():
    infd = os.open(sys.argv[1], os.O_RDONLY);
    outfd = os.open(sys.argv[2], os.O_RDWR|os.O_CREAT);
    buf=b''
    over=False
    while True:
        buf=os.read(infd, 512)
        if len(buf) != 512:
        # 4字节对齐，防止unpack时失败
            buf += (4-len(buf)%4) * b'\x00' 
            over=True
        for i in range(0, len(buf), 4):
            tmp = struct.unpack('<I', buf[i:i+4])
            #写入的是字符串文本形式
            os.write(outfd, bytes("%8.8x\n" % tmp, encoding='utf-8')) 
        if over:
            break;

    os.close(infd)    
    os.close(outfd)    
if __name__ == "__main__":
    '''
    test_argv();
    test_keyword();
    test_file(sys.argv[1])
    '''
    test_file2()
