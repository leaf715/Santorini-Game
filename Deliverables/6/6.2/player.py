from board import Board, Position
from RuleChecker import RuleChecker, Play

class Player:

    def __init__(self, color):
        self.color = color
        self.strategy = Strategy()
        self.starting_positions = [Position(0,0),Position(0,4), Position(4,4), Position(4,0)]

    def place_workers(self, board):
        count = 0
        lst = []
        for pos in self.starting_positions:
            if not board.is_cell_occupied(pos) and count < 2:
                lst.append(pos)
                count += 1
        return lst

    def get_plays (self, board):
        return self.strategy.get_viable_plays(self.color, board)

    def who_won(self, winner_color):
        if winner_color == self.color:
            self.winner = 'yes'
