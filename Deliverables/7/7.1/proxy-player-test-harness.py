#!/usr/bin/env python

import sys
import json
from JsonParser import JsonParser
from player import Player
from board import Board
from RuleChecker import RuleChecker, Play

class PlayerTestHarness:
  def __init__(self):
    self.parser = JsonParser()

  def main(self):
    commands = self.parser.parse_stream(sys.stdin)
    print commands
    player = Player()
    play_outputs = map(lambda command: player.execute(command),commands)
    for output in play_outputs:
        if isinstance(output, (Play,)):
            output = self._format_play(output)
        print(json.dumps(output))

  def _format_position(self, position):
    return [position.row, position.col]

  def _execute_play_command(self, play_command, player):
    board = Board(play_command[1])
    viable_plays = player.get_plays(board)
    return map(self._format_play,viable_plays)

  def _format_play(self, play):
    directions = [play.move_direction]
    if (play.build_direction): directions.append(play.build_direction)
    return [play.worker, directions]


harness = PlayerTestHarness()
harness.main()
