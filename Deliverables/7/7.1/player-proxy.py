from board import Board, Position
from RuleChecker import RuleChecker, Play
from strategy import Strategy
from player import player
from JsonParser import JsonParser
import socket

class ProxyPlayer:

    def __init__(self):
        self.player = Player()
        self.parser = JsonParser()

    def connect(self,ip,port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.send(self.player.execute(['Register']))
        while True:
            json_msg = client.recv(1024)
            if not json_msg:
                break
            msg = json.loads(json_msg)
            rsp = self.player.execute(msg)
            client.send(json.dumps(rsp))
            if rsp == self.player.error_message:
                break

        client.close()
