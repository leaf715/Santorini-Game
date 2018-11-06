from board import Board, Position
from RuleChecker import RuleChecker, Play
from contracts import contract

class Player:

    def __init__(self, color):
        self.color = color
        self.strategy = Strategy()
        self.starting_positions = [Position(0,0),Position(0,4), Position(4,4), Position(4,0)]

    @contract(board=Board, returns='list[2]($Position)')
    def place_workers(self, board):
        count = 0
        lst = []
        for pos in self.starting_positions:
            if not board.is_cell_occupied(pos) and count < 2:
                lst.append(pos)
                count += 1
        return lst

    @contract(board=Board, returns='list($Play)')
    def get_plays (self, board):
        return self.strategy.get_viable_plays(self.color, board)

    @contract(winner_color='string')
    def who_won(self, winner_color):
        if winner_color == self.color:
            self.winner = 'yes'

class Strategy:

    def __init__(self):
        self.rules = RuleChecker()

    @contract(color='str|unicode')
    def _opponent_color(self, color):
        return 'white' if color == 'blue' else 'blue'

    @contract(board=Board, returns=bool)
    def _worker_will_win(self, worker, board):
        if board.get_worker_height(worker) != 2:
            return False
        for direction in board.DIRECTION_MAP:
            if not board.neighboring_cell_exists(worker, direction) or board.is_occupied(worker, direction):
                continue
            if board.get_height(worker, direction) == RuleChecker.WINNING_HEIGHT:
                return True
        return False

    @contract(color='str|unicode', play=Play, board=Board)
    def _is_losing_play(self, color, play, board):
        enemy_worker1 = self._opponent_color(color) + '1'
        enemy_worker2 = self._opponent_color(color) + '2'

        resulting_board = play.resulting_board(board)

        return self._worker_will_win(enemy_worker1, resulting_board) or self._worker_will_win(enemy_worker2, resulting_board)

    @contract(worker='str|unicode', board=Board, returns='list($Play)')
    def _all_possible_plays(self, worker, board):
        plays = []
        for move_direction in board.DIRECTION_MAP:
            for build_direction in board.DIRECTION_MAP:
                play = Play(worker, move_direction, build_direction)
                plays.append(play)
            no_build_play = Play(worker, move_direction)
            plays.append(no_build_play)
        return plays

    @contract(board=Board, returns='list($Play)')
    def get_viable_plays(self, color, board):
        worker1 = color + '1'
        worker2 = color + '2'
        plays = self._all_possible_plays(worker1, board) + self._all_possible_plays(worker2, board)

        valid_plays = filter(lambda p: self.rules.is_valid_play(board, p), plays)
        viable_plays = filter(lambda p: not self._is_losing_play(color, p, board), valid_plays)
        return viable_plays
