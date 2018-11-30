from board import Board, Position
from RuleChecker import RuleChecker, Play
from strategy import Strategy
from player import Player
from JsonParser import JsonParser
import socket
import select
import json

class ProxyPlayer:

    def __init__(self, socket):
        self.client = socket

    def execute(self,response):
        rsp = json.dumps(response)
        read, write, error = select.select([],[self.client],[])
        write[0].send(bytes(rsp))
        read, write, error = select.select([self.client],[],[])
        msg = read[0].recv(4096)
        if not msg:
            msg = ''
        return msg
