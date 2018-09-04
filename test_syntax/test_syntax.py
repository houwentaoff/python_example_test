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
    #2018-2-3 下面的classmethod很重要否则编译不过
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
        pattern = re.compile(r'(\d+)-(\d+)-(\d+)')
        m = pattern.match(string)
        if m != None:
            year = m.group(1)
            month = m.group(2)
            day = m.group(3)
            if (int(month) > 0 and int(month) < 13) and (int(day) > 0 and int(day) < 32):
                date = Date(day, month, year)
                return date
        return None
    #类似于c#中的属性,访问时不带括号 但是只要get没有set就失去了 c#属性的优势
    @property
    def Day(self):
        return self.__day



def test_class():
    d = Date.Parse("2018-4-20")
    if d != None:
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

def test_struct():
    a = 1
    b = 2
    s = struct.pack('!ii', a, b)
    data = s + bytes('12345', encoding='utf-8')
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

