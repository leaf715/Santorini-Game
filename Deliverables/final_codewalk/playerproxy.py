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
            msg = 'Santorini is broken! Too many tourists in such a small place...'
        # read, write, error = select.select([self.client],[],[])
        try:
            msg = self.client.recv(4096)
        except:
            msg = 'Santorini is broken! Too many tourists in such a small place...'
        try:
            return json.loads(msg)
        except:
            return msg
