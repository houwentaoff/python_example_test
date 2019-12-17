import os,sys,struct
'''
转换bin文件中的16进制数据转化为txt中0x12345这种的文件
'''
def usage():
    print (sys.argv[0], 'inputfile', 'outfile')
if len(sys.argv) < 3:
    usage()
    exit(1)

infd = os.open(sys.argv[1], os.O_RDONLY);
outfd = os.open(sys.argv[2], os.O_RDWR|os.O_CREAT);
buf=b''
over=False
while True:
    buf=os.read(infd, 1024)
    if len(buf) != 1024:
        buf += (4-len(buf)%4) * b'\x00' # 补齐否则会unpack 会由于长度不够 i:4会失败
        over=True
    for i in range(0, len(buf), 4):
        tmp = struct.unpack('<I', buf[i:i+4]) #必须要切片，否则提示左边需要4B而右边太长
        os.write(outfd, bytes("%8.8x\n" % tmp, encoding='utf-8')) #必须写上编码，这是必须填的参数
    if over:
        break;

os.close(infd)    
os.close(outfd)    
print ('generate', sys.argv[2] ,'successed')




