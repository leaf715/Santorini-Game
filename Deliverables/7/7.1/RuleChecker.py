#!/usr/bin/env python
from board import Board
import copy


class Play:
    def __init__(self, worker, move_direction, build_direction=None):
        self.worker = worker
        self.move_direction = move_direction
        self.build_direction = build_direction

    def __str__(self):
        return 'Play worker: ' + self.worker + ' move: ' + self.move_direction + ' build: ' + str(self.build_direction)

    def __eq__(self, other):
        return self.build_direction == other.build_direction and self.worker == other.worker and self.move_direction == other.move_direction

    def resulting_board(self, board):
        new_board = copy.deepcopy(board)
        new_board.move_worker(self.worker, self.move_direction)
        if(self.build_direction):
            new_board.build(self.worker, self.build_direction)
        return new_board


class RuleChecker:

    WINNING_HEIGHT = 3

    def validate_initial_board(self, board, player_color):

        if len(board.worker_locations) != 0 and len(board.worker_locations) != 2:
            return False
        grid = board.height_grid
        sum = 0
        for row in grid:
            for cell in row:
                sum = sum + cell
        if sum > 0:
            return False
        if len(board.worker_locations) == 2:
            opponent_worker_names = []
            for key in board.worker_locations:
                opponent_worker_names.append(key)
            opponent_color = opponent_worker_names[0][:-1]
            # checks that opponent has same colors as each other
            for opp_name in opponent_worker_names:
                if opp_name[:-1] != opponent_color:
                    return False
            # checks to make sure that opponent has two different named players
            if opponent_worker_names[0] == opponent_worker_names[1]:
                return False
            # checks that opponent color is not your players color
            if opponent_color == player_color:
                return False
            # checks to makes sure that workers are not on the same spot
            if board.worker_locations[opponent_worker_names[0]] == board.worker_locations[opponent_worker_names[1]]:
                return False

        return True

    def validate_board(self, board):
        for row in board.height_grid:
            for cell in row:
                if cell < 0 or cell > 4:
                    return False
                if not isinstance(cell, (int,)):
                    return False
        for worker in board.worker_locations.keys():
            if board._get_cell_height(board.worker_locations[worker]) >= 3:
                return False
        if len(board.worker_locations) != 4:
            return False
        return True

    def _is_valid_move(self, board, worker, direction):
        if not self._is_valid_target(board, worker, direction):
            return False
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
        valid_build_directions = map(lambda direction: self._is_valid_build(
            board, worker, direction), board.DIRECTION_MAP.keys())
        return not any(valid_build_directions)

    def _is_valid_no_build(self, board, worker):
        return self._is_winner(board, worker) or self._is_loser(board, worker)

    def is_valid_play(self, board, play):
        board_copy = copy.deepcopy(board)
        if self._is_valid_move(board_copy, play.worker, play.move_direction):
            board_copy.move_worker(play.worker, play.move_direction)
            if play.build_direction:
                return self._is_valid_build(board_copy, play.worker, play.build_direction) and not self._is_winner(board_copy, play.worker)
            else:
                return self._is_valid_no_build(board_copy, play.worker)
        else:
            return False


rule_checker = RuleChecker()
