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

    def execute(self, response):
        rsp = json.dumps(response)
        # read, write, error = select.select([],[self.client],[])
        try:
            self.client.send(bytes(rsp))
        except:
            msg = ''
        # read, write, error = select.select([self.client],[],[])
        try:
            msg = self.client.recv(4096)
        except:
            msg = ''
        try:
            return json.loads(msg)
        except:
            print msg
            return msg
