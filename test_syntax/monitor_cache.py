#!/usr/bin/env python
# coding=utf-8
# 监测cached 大小异常情况下 ipc和tmpfs的使用情况
import sys
import psutil
import time
import os
# dd if=/dev/zero of=/run bs=1G count=1
# nohup python -u test.py > out.log 2>&1 &
class Tool(object):
    #def __init__(self):
        #self.mem = psutil.virtual_memory()

    @staticmethod
    def GetCached():
        mem = psutil.virtual_memory()
        if mem == None:
            return None
        return mem.cached
    @staticmethod
    def GetTmpfs():
        disks=psutil.disk_partitions(True)
        tmpfsl=[]
        for v in disks:
            if v.fstype == 'tmpfs':
                tmpfsl.append(v)
        return tmpfsl 
    @staticmethod
    def GetIPCS():
        process = os.popen('ipcs') 
        output = process.read()
        process.close()
        return output

if __name__ == "__main__":
    time_str =  time.strftime( "%Y-%m-%d-monitor-cached-joy", time.localtime( ) )
    file_name = "./" + time_str + ".log"
    if os.path.exists ( file_name ) == False :
        os.mknod( file_name )
        handle = open (file_name , "w" )
    else :
        handle = open (file_name , "a" )
    while True:
        time.sleep(3)
        # >= 400M
        cached_size = Tool.GetCached()/1024/1024
        if cached_size >= 400:
            debug_str = '当前cached为' + str(cached_size) + 'MB' + ' 超过设定值 400MB\n'
            tmpfsl = Tool.GetTmpfs()
            t_str =  time.strftime( "%Y-%m-%d-%H:%M:%S", time.localtime( ) )
            debug_str += "---------------------" + t_str + "-----------------------\n" 
            debug_str += "------------------------disk info------------------------------\n" 
            print debug_str
            handle.write(debug_str)
            for v in tmpfsl:
                info = psutil.disk_usage(v.mountpoint)
                debug_str = "";
                debug_str += "路径:" + str(v.mountpoint)
                debug_str += " 总大小:" + str(info.total/1024) + " KB"
                debug_str += " 已使用:" + str(info.used/1024) + " KB"
                debug_str += " 使用百分比:%" + str(info.percent) + "\n"
                print debug_str
                handle.write(debug_str)
            debug_str = "---------------------------------------------------------------\n" 
            debug_str += "------------------------ipc info-------------------------------\n" 
            info = Tool.GetIPCS()
            debug_str += info
            print debug_str
            handle.write(debug_str)
        else:
            print '.' 
    handle.close()

