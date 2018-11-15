from board import Board, Position
from RuleChecker import RuleChecker, Play
from strategy import Strategy
from player import Player
from JsonParser import JsonParser
import json
import socket
import select


def main():
    player = Player()
    print("driver")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('', 8000))
    print('connected')
    while True:
        read, write, error = select.select([client],[],[])
        json_msg = read[0].recv(4096)
        print(json_msg)
        msg = json.loads(json_msg)
        rsp = player.execute(msg)
        read, write, error = select.select([],[client],[])
        write[0].sendall(bytes(json.dumps(response), 'utf-8'))
        if rsp == player.error_message():
            break

    client.close()

main()
