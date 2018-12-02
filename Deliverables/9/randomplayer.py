from board import Board, Position
from RuleChecker import RuleChecker, Play
from strategy import Strategy
import random
try:
    basestring
except NameError:
    basestring = str


class Player:

    def __init__(self):
        self.color = ''
        self.strategy = Strategy()
        self.starting_positions = [Position(0, 0), Position(0, 4), Position(4, 4), Position(4, 0)]
        self.RuleChecker = RuleChecker()
        self.game_state = 0
        self.name = 'Kanye'
        self.last_board = Board([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

    def execute(self, input):
        command = input[0]
        if not self.check_input(input):
            return self.error_message()
        if command == 'Register' and self.game_state == 0:
            self.game_state = 1
            return self.name
        if command == 'Place' and self.game_state == 1:
            self.color = str(input[1])
            b = Board(input[2])
            self.last_board = b
            if not self.RuleChecker.validate_initial_board(b, self.color):
                return self.error_message()
            self.game_state = 2
            posns = self.place_workers(b)
            self.last_board.worker_locations[self.color + '1'] = Position(posns[0][0], posns[0][1])
            self.last_board.worker_locations[self.color + '2'] = Position(posns[1][0], posns[1][1])
            return posns
        if command == 'Play' and self.game_state == 2:
            b = Board(input[1])
            if not self.is_possible_board(b):
                return self.error_message()
            self.last_board = b
            if not self.RuleChecker.validate_board(b):
                return self.error_message()
            play_options = self.strategy.get_legal_plays(self.color,b)
            if play_options:
                index = random.randint(0,len(play_options)-1)
                playmade = self.format_plays(play_options)[index]
            else:
                playmade = []
            if playmade:
                if len(playmade) == 3:
                    Playmade = Play(playmade[0],playmade[1],playmade[2])
                else:
                    Playmade = Play(playmade[0],playmade[1])
                self.last_board = Playmade.resulting_board(self.last_board);
            return playmade
        if command == 'Game Over':
            self.game_state = 0
            self.last_board = Board([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
            self.color = ''
            return 'OK'
        return self.error_message()

    def format_plays(self, plays):
        listplays = []
        for play in plays:
            listplay = [play.worker, play.move_direction]
            if play.build_direction:
                listplay.append(play.build_direction)
            listplays.append(listplay)
        return listplays

    def check_input(self, input):
        if not input:
            return False
        if not isinstance(input, (list,)):
            return False
        if input[0] == 'Register':
            if len(input) == 1:
                return True
        if input[0] == 'Place':
            if len(input) == 3:
                if isinstance(input[1], (basestring, str)):
                    if isinstance(input[2], (list,)):
                        if len(input[2]) == 5:
                            for lst in input[2]:
                                if not isinstance(lst, (list,)):
                                    return False
                                if len(lst) != 5:
                                    return False
                                for cell in lst:
                                    if not isinstance(cell, (list, int)):
                                        return False
                            return True
        if input[0] == 'Play':
            if len(input) == 2:
                if isinstance(input[1], (list,)):
                    if len(input[1]) == 5:
                        for lst in input[1]:
                            if not isinstance(lst, (list,)):
                                return False
                            if len(lst) != 5:
                                return False
                            for cell in lst:
                                if not isinstance(cell, (list, int)):
                                    return False
                        return True
        if input[0] == 'Game Over':
            if len(input) == 2:
                if isinstance(input[1], (basestring, str)):
                    return True
        return False

    def place_workers(self, board):
        count = 0
        lst = []
        for pos in self.starting_positions:
            if not board.is_cell_occupied(pos) and count < 2:
                lst.append([pos.row, pos.col])
                count += 1
        return lst

    def get_plays(self, board):
        return self.strategy.get_viable_plays(self.color, board)

    def error_message(self):
        return 'Santorini is broken! Too many tourists in such a small place...'

    def is_possible_board(self, b):
        opponent_possible_boards = []
        l_board = self.last_board
        if len(l_board.worker_locations) < 4:
            return self.RuleChecker.validate_start_board(l_board, b)
        opponent_color = self.strategy._opponent_color(self.color)
        opponent_possible_boards = self.strategy.generate_boards(l_board, opponent_color)
        for check in opponent_possible_boards:
            if isinstance(check, Board):
                if check == b:
                    return True
        return False
