import os,sys

infd = os.open(sys.argv[1], os.O_RDONLY| os.O_BINARY);
lossfd = os.open(sys.argv[2], os.O_RDONLY| os.O_BINARY);
outfd = os.open(sys.argv[1]+"fill", os.O_RDWR| os.O_BINARY | os.O_CREAT);
block=2048
offset = 0
over = False
while True:
    buf = os.read(infd, block)
    #print(len(buf))
    size = len(buf)
    if size != block:
        over=True
    if offset == 0x6b000:
        #write to file
        loss = os.read(lossfd, block)
        os.write(outfd, loss)
    os.write(outfd, buf) 
    offset = offset + size
    if over:
        break;
os.close(outfd) 
os.close(infd)  
os.close(lossfd)