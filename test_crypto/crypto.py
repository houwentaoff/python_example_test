#!/usr/bin/python2.7 
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes 
# nonce --> number once 
data= b'this is a bug!'
key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)
ciphertext, tag = cipher.encrypt_and_digest(data)

print("encrypt data:", ciphertext, "tag:", tag)
cipher = AES.new(key, AES.MODE_EAX, nonce=cipher.nonce)
plaintext = cipher.decrypt(ciphertext)
try:
    cipher.verify(tag)
    print("The message is authentic:", plaintext)
except ValueError:
    print("Key incorrect or message corrupted")
