#!/usr/bin/python2
import os
import json
import sys
import time

from Crypto.Cipher import AES

cookiefile = open("cookie", "r").read().strip()
flag = open("flag", "r").read().strip()
key = open("key", "rb").read().strip().encode('hex')

welcome = """
Welcome to Secure Encryption Service version 1.51
"""
def pad(s):
  return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

def isvalidpad(s):
  return ord(s[-1])*s[-1:]==s[-ord(s[-1]):]

def unpad(s):
  return s[:-ord(s[len(s)-1:])]

def encrypt(m):
  IV="This is an IV456"
  cipher = AES.new(key.decode('hex'), AES.MODE_CBC, IV)
  return IV.encode("hex")+cipher.encrypt(pad(m)).encode("hex")

def decrypt(m):
  cipher = AES.new(key.decode('hex'), AES.MODE_CBC, m[0:32].decode("hex"))
  return cipher.decrypt(m[32:].decode("hex"))

example_cookie = json.dumps({'username': 'guest', 'is_admin': 'false',\
                     'expires': '2000-01-01'})

with open('cookie', 'w') as cock:
  cock.write(example_cookie)

print("Here is a sample cookie: " + encrypt(cookiefile))