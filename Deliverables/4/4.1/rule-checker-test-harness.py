#!/usr/bin/env python
import sys
import json
from JsonParser import JsonParser
from RuleChecker import RuleChecker, Play
from board import Board

class RuleCheckerTestHarness:
  def __init__(self):
    self.parser = JsonParser()
    self.rule_checker = RuleChecker()

  def main(self):
    inputs = self.parser.parse_stream(sys.stdin)
    is_valid_play_list = map(self._check_play, inputs)
    responses = map(lambda is_valid_play: 'yes' if is_valid_play else 'no', is_valid_play_list)
    for response in responses:
      print(json.dumps(response))

  def _check_play(self, test_play):
    game_board = test_play[0]
    worker = test_play[1]
    directions = test_play[2]
    move_direction = directions[0]
    build_direction = directions[1] if len(directions) == 2 else None
    board = Board(game_board)
    play = Play(worker, move_direction, build_direction)
    return self.rule_checker.is_valid_play(board, play)

harness = RuleCheckerTestHarness()
harness.main()
