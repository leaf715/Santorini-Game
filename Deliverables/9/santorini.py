import sys
import json
from JsonParser import JsonParser
from board import Board
from player import Player
from RuleChecker import RuleChecker, Play
from playerproxy import ProxyPlayer
import socket
import select

class PlayerTestHarness:
  def __init__(self):
    self.parser = JsonParser()

  def main(self):
    commands = self.parser.parse_stream(sys.stdin)
    admin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    admin.bind(('',8000))
    admin.listen(5)
    client, ip = admin.accept()
    player = ProxyPlayer(client)
    outputs = []
    outputs = [player.execute(['Register'])]
    for command in commands:
        output = player.execute(command)
        if output:
            outputs.append(output)
    admin.close()
    for output in outputs:
      print output

harness = PlayerTestHarness()
harness.main()
