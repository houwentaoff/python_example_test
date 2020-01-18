#!/usr/bin/python3.5
import sys
import keyword
import time

import re
import struct
#测试基本语法
#用空方法模拟接口
class File:
    def read(self):
        pass
    def write(self):
        pass

class Date(object):
    def __init__(self, day=0, month=0, year=0):
        self.__day = day
        self.month = month
        self.year = year
    #重载运算符
    def __eq__(self, other):
        return self.year == other.year

    def __le__(self, other):
        return self.year < other.year

    def __gt__(self, other):
        return self.year > other.year        
    #2018-2-3 下面的classmethod很重要否则编译不过,class/static method都是类使用，不要用于对象
    '''
    @classmethod
    def Parse(cls, string):
        pattern = re.compile(r'(\d+)-(\d+)-(\d+)')
        m = pattern.match(string)
        if m != None:
            year = m.group(1)
            month = m.group(2)
            day = m.group(3)
            if (int(month) > 0 and int(month) < 13) and (int(day) > 0 and int(day) < 32):
                date = cls(day, month, year)
                return date
        return None
     '''
    @staticmethod
    def Parse(string):
    ''' 正则表达式分组获取数据，如下为获取1990-02-01这种年月日'''
    '''pattern = re.compile(r'(cmd_mem)_(\d+)_(0[xX][0-9a-fA-F]+)\.txt')这句可以分组获取cmd_mem_123_0xff123.txt
    m.group(1) m.group(2) m.group(3)
       中的cmd_mem 123 0xff123
       
    '''
        pattern = re.compile(r'(\d+)-(\d+)-(\d+)')
        m = pattern.match(string)
        if m != None:
            year = m.group(1)
            month = m.group(2)
            day = m.group(3)
            if (int(month,10) > 0 and int(month) < 13) and (int(day) > 0 and int(day) < 32):
                date = Date(day, month, year)
                return date
        return None
    #类似于c#中的属性,访问时不带括号 但是只要get没有set就失去了 c#属性的优势
    @property
    def Day(self):
        return self.__day



def test_class():
    d = Date.Parse("2018-4-20")
    #用is替换 == ; is比较的是对象引用, == 是比较值，若重载了==号就只能使用is
    if d is not None:
        print("year:", d.year, "mon:", d.month, "day:", d.day)
    else:
        print("format error!")

def aaa(myl):
    myl += [6,7,8];
    # 添加一个对象
    #myl.append([6,7,8]);
    return
def test_with():
#上下文管理协议则是__enter__和__exit__
#
#配合with语句使用的时候，上下文管理器会自动调用__enter__方法，然后进入运行时上下文环境，如果有as 从
#句，返回自身或另一个与运行时上下文相关的对象，值赋值给var。当with_body执行完毕退出with语句块或者
#with_body代码块出现异常，则会自动执行__exit__方法，并且会把对于的异常参数传递进来。如果__exit__函数
#返回True。则with语句代码块不会显示的抛出异常，终止程序，如果返回None或者False，异常会被主动raise，
#并终止程序。
    with open('aaa', 'w') as f:
        f.write('sss');

def test_keyword():
    print("python keyword:")
    print(keyword.kwlist)

def test_other():
    if 1:
        print("1 is true");
    elif 0:
        print("0 is true");
    else:
        print("1 is false");
    

    #while
    #while True:
    #    pass

    i = 5;
    while i:
        i -= 1;
        print(i);

    while i > 0:
        print ("i>0 i:", i);
    else:
        print ("i<=0 i:", i)

    #for range
    for i in range(6, 9):#6 7 8 ,range(5) , range(10, 1, -1)
        print (i)
    else:
        print("no cell in range??");

    for v in ["aabbcc", 6,2,3,4,5,6,"ccc"]:
        print (v);
def test_format():
    print("%s,0x%8.8x, %d" % ('12fdsv', int('1234'), int('0x12345', 16)))
    '''用struct.pack/unpack进行格式化'''
def test_struct():
    a = 1
    b = 2
    '''
    s为bytes对象, bytes对象能直接写入文件,如outfd = os.open(sys.argv[2], os.O_RDWR|os.O_CREAT); 
    os.write(outfd,s)
    bytes是一个不可变的数据类型,如果要修改需使用切片操作
    bytesarray可修改如a=bytesarray(10);a[8] = 0x2
    '''
    s = struct.pack('!ii', a, b)
    # tmp为int
    tmp = struct.unpack('<I', s[0:4])
    data = s + bytes("12345%8.8x\n" % tmp,, encoding='utf-8')
    payload = data
    # send ...
    #struct.calcsize用于计算格式字符串所对应的结果的长度，如：struct.calcsize('ii')，返回8
    #first = struct.unpack("!i", payload[0:4]) #ok first->tuple
    #(first) = struct.unpack("!i", payload[0:4])  #ok
    (first,) = struct.unpack("!i", payload[0:4]) #ok
    sec = struct.unpack("!i", payload[4:8])
    d = payload[8:]
    print ("len %d" % len(payload), "fir:", hex(first), " ","payload[0]:",hex(d[0]))
    for c in d:
        print (hex(c), end='')#输出不换行 chr() :ascii -> string ord: string->ascii
        #print hex(ord(c),)  #python2 中用,表示不换行

if __name__ == "__main__":
    #str
    s ='dsd"vvv"'
    print("hello world!", s);
    #list
    mylist = [1,2,3,4,"aas",];
    #tuple 空元组 tup=()
    tup = ('1233', [1,2,3], 8)
    #dict
    #键必须不可变，所以可以用数字，字符串或元组充当，而用列表就不行
    d = {'name':'joy', 55:[111,222]}
    aaa(mylist)
    print(mylist)
    test_struct()
    test_other()
    test_keyword()
    test_with()
    time.sleep(0.2)
    test_class()
    #从键盘输入 阻塞
    st = input("请输入:")
    print ("st:", st)

    try:
        f = open("aaaaa");
        #Open file and return a stream   --> 不是os.open 
        #the type of f is `TextIOWrapper`
        print (type(f));
        f.read(3);
        f.close();
    except:
        print("joy:Unexpected error:", sys.exc_info()[0]);

