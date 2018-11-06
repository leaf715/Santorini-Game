import sys
import socket
import os
import JsonParser
import json

def main():
    address = ('localhost', 8844)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    while True:
        try:
            line = raw_input("")
            s.send(line)
        except:
            pass

if __name__=="__main__":
    main()
