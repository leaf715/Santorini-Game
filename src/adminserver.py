import sys
import socket
import os
import JsonParser
import json

def main():
    address = ('localhost', 8844)
    directory = os.getcwd()
    parser = JsonParser.JsonParser()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(address)
    s.listen(5)

    while True:
        print 'waiting for connection'
        (client, ip) = s.accept()
        try:
            while True:
                req = client.recv(1024)
                try:
                    parsedreq = json.loads(req)
                    print("sending " + parsedreq)
                    client.send(parsedreq+' gotem\n')
                except:
                    client.send('not json bruh')
                    pass
        finally:
            client.close()


if __name__ == "__main__":
    main()
