'''
将ai的资源文件转换为2进制文件
使用方法：python3 ai_txt2bin.py cmd_buffer.h cmd_buffer.bin 
'''
import os,sys,struct,re

def usage():
    print (sys.argv[0], 'command.txt', 'command.bin')
    
if len(sys.argv) < 3:
    usage()
    exit(1)

def mask2x(mask):
    bytesmask = 0
    for i in range(0,4):
        a = mask & (0x1<<i)
        if a != 0:
            bytesmask |= 0xff << (8*i)
    return bytesmask
   
dump_txt = open(sys.argv[1])

outfd = os.open(sys.argv[2], os.O_RDWR|os.O_CREAT|os.O_TRUNC)
pattern = re.compile(r'([0-9a-fA-F]+)[ ]+([0-9a-fA-F]+)[ ]+([0-9a-fA-F]+)') 
line_num = 0
pre_addr = 0
begin_addr = 0
end_addr = 0
for line in dump_txt:
    line_num += 1
    line = line.strip()
    m = pattern.match(line)
    if m != None:
        addr = m.group(1)
        addr = int(addr, 16)
        mask = m.group(2)
        mask = int(mask, 16)
        value = m.group(3)
        value = int(value, 16)
        if pre_addr != 0:
            if addr - pre_addr != 4:
                print('cur add [0x%x] err, pre addr[0x%x] ' %(addr, pre_addr))
        else:
            begin_addr = addr
        pre_addr = addr
        
        mask = mask2x(mask)
        #print('addr:', hex(addr), " mask:", hex(mask), " value:", hex(value), " write val:", hex(value & mask) )
        #hex = int(hex, 16)
        binary  = struct.pack('<I', value & mask)
        os.write(outfd, binary)  
        #print('op:', op, " addr:", addr, " value:",value)
end_addr = pre_addr
os.close(outfd)
newfile = os.path.basename((sys.argv[2]))
newfile = newfile.split('.')[0]
newfile = newfile + "_" + str(hex(begin_addr)) + "_" + str(hex(end_addr)) + ".bin"

os.rename(sys.argv[2], newfile)
dump_txt.close()
print ('covert [%s] to %s  total line [%d] begin [0x%x] end [0x%x] successed' %
 (sys.argv[1] , sys.argv[2], line_num, begin_addr, end_addr))




