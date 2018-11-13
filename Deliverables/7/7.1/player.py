from board import Board, Position
from RuleChecker import RuleChecker, Play
from strategy import Strategy

class Player:

    def __init__(self):
        self.color = ''
        self.strategy = Strategy()
        self.starting_positions = [Position(0,0),Position(0,4), Position(4,4), Position(4,0)]
        self.game_state = 0

    def execute(self, input):
        command = input[0]
        if not self.check_input(input):
            return self.error_message()
        if command == 'Register' and self.game_state == 0:
            self.game_state = 1
            return 'Kanye'
        if command == 'Place' and self.game_state == 1:
            self.color = input[1]
            b = Board(input[2])
            self.game_state = 2
            return self.place_workers(b)
        if command == 'Play' and self.game_state == 2:
            b = Board(input[1])
            play_options = self.get_plays(b)
            if play_options:
                return play_options[0]
            play_options = self.strategy.get_legal_plays(self.color,b)
            return play_options[0]
        if command == 'Game Over' and self.game_state == 2:
            self.game_state = 3
            return 'OK'
        return self.error_message()

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

    def error_message(self):
        return 'Santorini is broken! Too many tourists in such a small place...'
