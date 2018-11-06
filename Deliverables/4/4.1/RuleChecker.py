#!/usr/bin/env python
from board import Board
from contracts import contract, new_contract
import copy

@new_contract
def direction(d):
  if d not in Board.DIRECTION_MAP.keys():
    msg = 'The string %s is not a valid Direction.' % d
    raise ValueError(msg)

@new_contract
def worker_name(name):
  names = ['white1', 'white2', 'blue1', 'blue2']
  if name not in names:
    msg = 'The string name is not a valid worker name.' % name
    raise ValueError(msg)

class Play:
  @contract(worker='(str|unicode),worker_name', move_direction='(str|unicode),direction', build_direction='((str|unicode),direction)|None')
  def __init__(self, worker, move_direction, build_direction = None):
    self.worker = worker
    self.move_direction = move_direction
    self.build_direction = build_direction

class RuleChecker:

  def _is_valid_move(self, board, worker, direction):
    if not self._is_valid_target(board, worker, direction): return False
    worker_height = board.get_worker_height(worker)
    target_height = board.get_height(worker, direction)
    is_too_high = target_height - worker_height > 1
    return not is_too_high

  def _is_valid_target(self, board, worker, direction):
    return board.neighboring_cell_exists(worker, direction) and not board.is_occupied(worker, direction)

  def _is_valid_build(self, board, worker, direction):
    return self._is_valid_target(board, worker, direction)

  def _is_winner(self, board, worker):
    return board.get_worker_height(worker) == 3

  def _is_loser(self, board, worker):
    valid_build_directions = map(lambda direction: self._is_valid_build(board, worker, direction), board.DIRECTION_MAP.keys())
    return not any(valid_build_directions)

  def _is_valid_no_build(self, board, worker):
    return self._is_winner(board, worker) or self._is_loser(board, worker)

  @contract(board=Board, play=Play, returns=bool)
  def is_valid_play(self, board, play):
    board_copy = copy.deepcopy(board)
    if self._is_valid_move(board_copy, play.worker, play.move_direction):
      board_copy.move_worker(play.worker, play.move_direction)
      if play.build_direction:
        return self._is_valid_build(board_copy, play.worker, play.build_direction)
      else:
        return self._is_valid_no_build(board_copy, play.worker)
    else:
      return False

rule_checker = RuleChecker()
# rule_checker._is_winner(None, 'whie1')
# rule_checker._basic_necessities(None,None,'NM')
# Play('white1', 'N')
