import re
import os
import sys,struct
def usage():
    print(sys.argv[0], 'a.c', '')
def do_replace_inc(oldstr, newstr, text):
    pattern = re.compile(r''+oldstr, re.DOTALL)
    s = pattern.sub(newstr, text)
    return s
def replace_inc(text):
    
    text = do_replace_inc("./../../../../abcd",
        "abcd", text)
    text = do_replace_inc("../../../../xxx/aaa",
        "aaa", text)        
    return text

text = ''
dump_c = sys.argv[1] 
x = sys.argv[2] 
print(x)    
with open(dump_c, 'r', encoding='utf-8') as file:
    text = file.read()

s = replace_inc(text)
if s == text:
   print("no process")
print(s)
