#!/usr/bin/env python

import sys
import json
from JsonParser import JsonParser
from board import Board
from player import Player
from RuleChecker import RuleChecker, Play
from playerproxy import ProxyPlayer

class PlayerTestHarness:
  def __init__(self):
    self.parser = JsonParser()

  def main(self):
      player = ProxyPlayer()
      player.connect('localhost',8000)



harness = PlayerTestHarness()
harness.main()
