from board import Board, Position
from RuleChecker import RuleChecker, Play

class Strategy:

    def __init__(self):
        self.rules = RuleChecker()

    def _opponent_color(self, color):
        return 'white' if color == 'blue' else 'blue'

    def _worker_will_win(self, worker, board):
        if board.get_worker_height(worker) != 2:
            return False
        for direction in board.DIRECTION_MAP:
            if not board.neighboring_cell_exists(worker, direction) or board.is_occupied(worker, direction):
                continue
            if board.get_height(worker, direction) == RuleChecker.WINNING_HEIGHT:
                return True
        return False

    def _is_losing_play(self, color, play, board):
        enemy_worker1 = self._opponent_color(color) + '1'
        enemy_worker2 = self._opponent_color(color) + '2'

        resulting_board = play.resulting_board(board)

        return self._worker_will_win(enemy_worker1, resulting_board) or self._worker_will_win(enemy_worker2, resulting_board)

    def _all_possible_plays(self, worker, board):
        plays = []
        for move_direction in board.DIRECTION_MAP:
            for build_direction in board.DIRECTION_MAP:
                play = Play(worker, move_direction, build_direction)
                plays.append(play)
            no_build_play = Play(worker, move_direction)
            plays.append(no_build_play)
        return plays

    def get_viable_plays(self, color, board):
        worker1 = color + '1'
        worker2 = color + '2'
        plays = self._all_possible_plays(worker1, board) + self._all_possible_plays(worker2, board)

        valid_plays = filter(lambda p: self.rules.is_valid_play(board, p), plays)
        viable_plays = filter(lambda p: not self._is_losing_play(color, p, board), valid_plays)
        return viable_plays
