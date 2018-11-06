#!/usr/bin/env python
import sys
import json
from JsonParser import JsonParser
from player import Player
from board import Board

class PlayerTestHarness:
  def __init__(self):
    self.parser = JsonParser()

  def main(self):
    commands = self.parser.parse_stream(sys.stdin)
    place_command = commands[0]
    play_commands = commands[1:]
    color = place_command[1]

    init_board = place_command[2]
    player = Player(color)
    positions = player.place_workers(Board(init_board))

    place_output = map(self._format_position, positions)
    play_outputs = map(lambda play: self._execute_play_command(play, player),play_commands)
    print(json.dumps(place_output))
    for output in play_outputs:
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
