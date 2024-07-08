'''
将busmonitor统计结果放入csv表格中
使用方法：python3 xx.py monitor.log > monitor.csv 
'''
import os,sys,struct,re

def usage():
    print (sys.argv[0], 'traffic.txt', 'traffic_statistics.txt')
    
if len(sys.argv) < 3:
    usage()
    exit(1)

dump_txt = open(sys.argv[1])

traffic_pattern = re.compile(r'\[[0-9]\]\[[0-9\:\.]+\] (\[bus monitor\]):([0-9a-zA-Z_ ]+): (BYTESCAL_[RW]) ([0-9]+)') 
match_num = 0
for line in dump_txt:
    
    line = line.strip()
    m = traffic_pattern.match(line)
    if m != None:
        match_num += 1
        item = m.group(2)
        ty = m.group(3)
        if ty == 'BYTESCAL_R':
            ty = 'R'
        if ty == 'BYTESCAL_W':
            ty = 'W'            
        size = m.group(4)
        m_size = int(size)/1000000
        m_size = round(m_size, 2)
        if match_num <= 32:
            print(item, ", ", ty, ", ", m_size)
#print(match_num)       
     
dump_txt.seek(0, 0)
traf_total_pattern = re.compile(r'\[[0-9]\]\[[0-9\:\.]+\] (\[bus monitor\]):(ALL_BW_BYTE) ([0-9]+)') 
for line in dump_txt:
    line = line.strip()
    m = traf_total_pattern.match(line)
    if m != None:
        item = m.group(2)
        size = m.group(3)
        m_size = int(size)/1000000
        m_size = round(m_size, 2)
        print("TOTAL", ", ,", m_size)
        
dump_txt.seek(0, 0)
latency_pattern = re.compile(r'\[[0-9]\]\[[0-9\:\.]+\] (\[bus monitor\]):([0-9a-zA-Z_ ]+): (LAT_[RW]_MAX) ([0-9]+)') 
for line in dump_txt:
    line = line.strip()
    m = latency_pattern.match(line)
    if m != None:
        item = m.group(2)
        ty = m.group(3)
        size = m.group(4)
        ns_size = int(size)*5
        ns_size = str(ns_size)+'ns'
        print(item, ",",ty, ", ", ns_size)
        
dump_txt.close()

