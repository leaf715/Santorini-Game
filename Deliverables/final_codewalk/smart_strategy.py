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

    def get_color(self, color):
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
        # fix this if necessary
        if not original_plays:
            original_plays = plays
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
        color = self.get_color(color)
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

    def getAlphaBetaMove(self, color, board):
        ply = 2
        beta = float('inf')
        moves = self.get_viable_plays(color, board)
        color = str(color)
        print color
        boards = self.generate_boards(color, board)
        best_board = boards[0]
        alpha = float('-inf')

        for board in boards:
            # checks if their is a winning move
            if self.game_over(board, color):
                return moves[boards.index(board)]
            score = self.min_alpha_beta(board, ply, alpha, beta, self._opponent_color(color))

            if score > alpha:
                best_board = board
                alpha = score

        index = boards.index(best_board)
        return moves[index]

    def min_alpha_beta(self, board, ply, alpha, beta, color):
        moves = self.get_viable_plays(color, board)
        ply += 1
        best_score = float('inf')
        if len(moves) == 0 or ply >= self.depth:
            heur = self.heuristic(board, color)
            return heur
        else:
            boards = self.generate_boards(color, board)
            for board in boards:
                if self.game_over(board, color):
                    return float('-inf')
                score = self.max_alpha_beta(board, ply, alpha, beta, self._opponent_color(color))
                if score <= alpha:
                    return score
                beta = min(beta, score)
                if score < best_score:
                    best_score = score

            return best_score

    def max_alpha_beta(self, board, ply, alpha, beta, color):
        moves = self.get_viable_plays(color, board)
        ply += 1
        best_score = float('-inf')

        # add an or for if game is over? or add is game over once boards have been generated, and return +/-inf if so
        if len(moves) == 0 or ply >= self.depth:
            heur = self.heuristic(board, color)
            return heur
        else:
            boards = self.generate_boards(self, color, board)
            for board in boards:
                if self.game_over(board, color):
                    return float('inf')
                score = self.min_alpha_beta(board, ply, alpha, beta, self._opponent_color(color))
                if score > best_score:
                    best_score = score
                if best_score >= beta:
                    return score
                alpha = max(alpha, score)

            return best_score

    def heuristic(self, board, color):

        # height of surrounding squares, - for 4's near by
        score = 0
        workers = [color + '1', color + '2']
        enemy_workers = [self._opponent_color(color) + '1', self._opponent_color(color) + '2']

        for worker in workers:
            if board.get_worker_height(worker) == 3:
                score = float('inf')
                return score
            else:
                score = score + board.get_worker_height(worker) ** 10

        for worker in enemy_workers:
            if board.get_worker_height(worker) == 3:
                score = float('-inf')
            if self._worker_will_win(worker, board):
                score = float('-inf')
            else:
                score = score - (board.get_worker_height(worker) ** 10) / 2

        board
        return score

# add in checks for when a board is finished, to not continue down that branch
# consider checking in each section of their is a winning move to return
