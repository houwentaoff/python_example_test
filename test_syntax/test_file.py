#!/usr/bin/python3
import sys
import keyword
import  fcntl # ioctl 

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

    
if __name__ == "__main__":
    test_argv();
    test_keyword();
    test_file(sys.argv[1])
