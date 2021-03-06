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
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('', 8000))
    while True:
        read, write, error = select.select([client],[],[])
        json_msg = read[0].recv(4096)
        if not json_msg:
            break
        msg = json.loads(json_msg)
        # print(msg)
        # print("sup")
        rsp = player.execute(msg)
        # print(rsp)
        read, write, error = select.select([],[client],[])
        write[0].sendall(bytes(json.dumps(rsp)))
        if rsp == player.error_message():
            break

    client.close()

main()
