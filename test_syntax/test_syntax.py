#!/usr/bin/python3.5
import sys

#测试基本语法

def aaa(myl):
    myl += [6,7,8];
    # 添加一个对象
    #myl.append([6,7,8]);
    return

def test_other():
    if 1:
        print("1 is true");
    elif 0:
        print("0 is true");
    else:
        print("1 is false");
    
    i = 5;
    while i:
        i -= 1;
        print(i);

    while i > 0:
        print ("i>0 i:", i);
    else:
        print ("i<=0 i:", i)

    for i in range(6, 9):#6 7 8 ,range(5) , range(10, 1, -1)
        print (i)
    else:
        print("no cell in range??");

    for v in ["aabbcc", 6,2,3,4,5,6,"ccc"]:
        print (v);

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
    aaa(mylist);
    print(mylist);

    test_other();

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

