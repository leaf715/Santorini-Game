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
    cfg_file = open('santorini.config', 'r')
    cfg = json.loads(cfg_file.read())
    ip = cfg['IP']
    port = cfg['port']
    client.connect((ip, port))
    while True:
        json_msg = client.recv(4096)
        if not json_msg:
            break
        msg = json.loads(json_msg)
        # print(msg)
        # print("sup")
        rsp = player.execute(msg)
        # print(rsp)
        client.sendall(bytes(json.dumps(rsp)))


if __name__=="__main__":
	main()
