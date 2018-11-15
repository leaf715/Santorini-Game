from board import Board, Position
from RuleChecker import RuleChecker, Play
from strategy import Strategy


class Player:

    def __init__(self):
        self.color = ''
        self.strategy = Strategy()
        self.starting_positions = [Position(0, 0), Position(0, 4), Position(4, 4), Position(4, 0)]
        self.RuleChecker = RuleChecker()
        self.game_state = 0
        self.last_board = Board([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

    def execute(self, input):
        command = input[0]
        if not self.check_input(input):
            return self.error_message()
        print "here"
        if command == 'Register' and self.game_state == 0:
            self.game_state = 1
            return 'Kanye'
        if command == 'Place' and self.game_state == 1:
            self.color = input[1]
            b = Board(input[2])
            self.last_board = b
            if not self.RuleChecker.validate_initial_board(b, self.color):
                return self.error_message()
            self.game_state = 2
            return self.place_workers(b)
        if command == 'Play' and self.game_state == 2:
            b = Board(input[1])
            if not self.is_possible_board(b):
                return self.error_message()
            self.last_board = b
            if not self.RuleChecker.validate_board(b):
                return self.error_message()
            play_options = self.get_plays(b)
            if play_options:
                return play_options[0]
            play_options = self.strategy.get_legal_plays(self.color, b)
            return play_options[0]
        if command == 'Game Over' and self.game_state == 2:
            self.game_state = 3
            return 'OK'
        return self.error_message()

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
                if isinstance(input[1], (basestring,)):
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
                if isinstance(input[1], (basestring,)):
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
        l_board = Board(self.last_board)
        opponent_color = self.strategy._opponent_color(self.color)
        my_possible_boards = self.strategy.generate_boards(l_board, self.color)
        for board in my_possible_boards:
            opponent_possible_boards.append(self.strategy.generate_boards(board, opponent_color))
        # print opponent_possible_boards
        # print " kajsflkjaslfkdj"
        # print b
        print len(opponent_possible_boards)
        for check in opponent_possible_boards:
            for check2 in check:
                print check2
                if check2 is b:
                    return True
        return False


BOARD2 = [[[0, 'blue1'], 0, 0, 0, [0, 'white1']],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [[0, 'white2'], 0, 0, 0, [0, 'blue2']]]
BOARD3 = [[1, [0, 'blue1'], 0, 0, [0, 'white1']],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0],
          [1, [0, 'white2'], 0, 0, [0, 'blue2']]]

INIT_BOARD1 = [[0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]]
p = Player()
p.execute(['Register'])

p.execute(['Place', 'white', INIT_BOARD1])
p.last_board = BOARD2
print "play"
# print p.check_input(['Play', BOARD3])
print p.is_possible_board(BOARD3)
# print p.execute(['Play', BOARD3])
# check_input(['Play', self.BOARD2])
