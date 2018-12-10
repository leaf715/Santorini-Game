from board import Board, Position
from RuleChecker import RuleChecker, Play
import json


class Strategy:

    def __init__(self):
        self.rules = RuleChecker()
        cfg_file = open('strategy.config', 'r')
        cfg = json.loads(cfg_file.read())
        self.rounds = cfg['look-ahead']

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

    def get_any_play(self, color, board):
        worker1 = color + '1'
        worker2 = color + '2'
        plays = self._all_possible_plays(worker1, board) + self._all_possible_plays(worker2, board)
        return plays

    def get_legal_plays(self, color, board):
        worker1 = color + '1'
        worker2 = color + '2'
        plays = self._all_possible_plays(worker1, board) + self._all_possible_plays(worker2, board)

        original_plays = filter(lambda p: self.rules.is_valid_play(board, p), plays)
        return original_plays

    def get_viable_plays(self, color, board):
        worker1 = color + '1'
        worker2 = color + '2'
        plays = self._all_possible_plays(worker1, board) + self._all_possible_plays(worker2, board)

        original_plays = filter(lambda p: self.rules.is_valid_play(board, p), plays)
        bad_plays = []
        for og_play in original_plays:
            new_board = og_play.resulting_board(board)
            if self.check_future_loss(color, new_board, 1):
                bad_plays.append(og_play)
        good_plays = filter(lambda p: p not in bad_plays, original_plays)
        return good_plays

    def check_future_loss(self, color, board, round):
        if self.game_over(board, color):
            return False
        enemy_worker1 = self._opponent_color(color) + '1'
        enemy_worker2 = self._opponent_color(color) + '2'
        opponent_wins = self._worker_will_win(
            enemy_worker1, board) or self._worker_will_win(enemy_worker2, board)
        if opponent_wins:
            return True

        round = round + 1
        if round <= self.rounds:
            new_boards = self.generate_boards(board, self._opponent_color(color))
            for b in new_boards:
                plays = self._all_possible_plays(color + '1', b) + \
                    self._all_possible_plays(color + '2', b)
                new_plays = filter(lambda p: self.rules.is_valid_play(b, p), plays)
                all_winning_plays = True
                for play in new_plays:
                    next_board = play.resulting_board(b)
                    if not self.game_over(next_board, color):
                        # print round
                        # print next_board
                        all_winning_plays = False
                        break
                if all_winning_plays:
                    return False
                for play in new_plays:
                    next_board = play.resulting_board(b)
                    if self.check_future_loss(color, next_board, round):
                        return True
        return False

    def generate_boards(self, board, color):
        worker1 = color + '1'
        worker2 = color + '2'
        plays = self._all_possible_plays(worker1, board) + self._all_possible_plays(worker2, board)
        new_plays = filter(lambda p: self.rules.is_valid_play(board, p), plays)
        boards = []
        for play in new_plays:
            boards.append(play.resulting_board(board))
        return boards

    def game_over(self, board, color):
        workers = [color + '1', color + '2']
        for worker in workers:
            if board.get_worker_height(worker) == 3:
                return True
        return False


# pytest
