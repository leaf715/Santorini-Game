from board import Board, Position
from RuleChecker import RuleChecker, Play
from strategy import Strategy
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
        self.last_board = Board([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                                 [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

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
            self.last_board = b
            if not self.RuleChecker.validate_initial_board(b, self.color):
                return self.error_message()
            self.game_state = 2
            posns = self.place_workers(b)
            return posns
        if command == 'Play' and self.game_state == 2:
            b = Board(input[1])
            if not self.is_possible_board(b):
                return self.error_message()
            self.last_board = b
            if not self.RuleChecker.validate_board(b):
                return self.error_message()
            play_options = self.get_plays(b)
            return self.format_plays(play_options)
        if command == 'Game Over' and self.game_state == 2:
            self.game_state = 3
            return 'OK'
        return self.error_message()

    def format_plays(self, plays):
        listplays = []
        for play in plays:
            listplay = [play.worker,play.move_direction]
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
                if isinstance(input[1], (basestring,str)):
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
                if isinstance(input[1], (basestring,str)):
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
        if len(l_board.worker_locations.keys())<2:
            grid = b.height_grid
            for row in grid:
                for cell in row:
                    if cell > 0:
                        return False
            return True
        if len(l_board.worker_locations.keys())<4:
            grid = b.height_grid
            sum = 0
            for row in grid:
                for cell in row:
                    sum = sum + cell
            if sum == 1:
                return True
            return False
        oldgrid = l_board.height_grid;
        newgrid = b.height_grid;
        oldworkers = l_board.worker_locations;
        newworkers = b.worker_locations;
        heightchange = []
        movedworkers = []
        for i in range(len(oldgrid)):
            for j in range (len(oldgrid[0])):
                if oldgrid[i][j] != newgrid[i][j]:
                    if newgrid[i][j] - oldgrid[i][j] != 1:
                        return False
                    heightchange.append(Position(i,j))
        if len(heightchange) > 2:
            return False
        for worker in oldworkers.keys():
            if oldworkers[worker] != newworkers[worker]:
                if not oldworkers[worker].near(newworkers[worker]):
                    return False
                movedworkers.append(worker)
        found = 0
        if len(movedworkers) > 2:
            return False
        if movedworkers[0][:-1] == movedworkers[1][:-1]:
            return False
        for worker in movedworkers:
            newpos = newworkers[worker]
            if newpos.near(heightchange[0]):
                heightchange[0] = heightchange[1]
                found = found + 1
            elif newpos.near(heightchange[1]):
                heightchange[1] = heightchange[0]
                found = found + 1
        return found == 2
