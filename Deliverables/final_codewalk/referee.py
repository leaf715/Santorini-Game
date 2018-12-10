# The referee needs to have access to the board to determine move validity
from board import Board, Position
# The referee recieves two instances of players
from player import Player
# The referee determines the validity of moves using the Rule_Checker
from RuleChecker import Play, RuleChecker
import json


class Referee:
    # The referee stores references to the players and contains a rule_checker
    # object so it knows what plays are valid and what are not
    def __init__(self, player1, player2):
        self.rule_checker = RuleChecker()
        self.turn = 'blue'
        self.p1 = player1
        self.p2 = player2
        self.color_to_name = {}
        self.p1name = self.p1.execute(['Register'])
        self.p2name = self.p2.execute(['Register'])
        self.color_to_name['blue'] = self.p1name
        self.color_to_name['white'] = self.p2name
        self.board = Board([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

    def run_game(self):
        print self.color_to_name
        result = self.placement(self.p1)
        if isinstance(result, (basestring, str)):
            return [self.otherplayerwins(), 'cheating']
        self.board = result
        result = self.placement(self.p2)
        if isinstance(result, (basestring, str)):
            return [self.otherplayerwins(), 'cheating']
        self.board = result
        while True:
            if self.turn == 'blue':
                rsp = self.p1.execute(['Play', self.board.format_board()])
            if self.turn == 'white':
                rsp = self.p2.execute(['Play', self.board.format_board()])

            if isinstance(rsp, (basestring, str)):
                self.p1.execute(['Game Over', self.otherplayerwins()])
                self.p2.execute(['Game Over', self.otherplayerwins()])
                return [self.otherplayerwins(), 'cheating']
            if rsp == []:
                self.p1.execute(['Game Over', self.otherplayerwins()])
                self.p2.execute(['Game Over', self.otherplayerwins()])
                return [self.otherplayerwins()]
            result = self.check_play(rsp[0], rsp[1])
            if isinstance(result, (list,)):
                self.p1.execute(['Game Over', rsp[0]])
                self.p2.execute(['Game Over', rsp[0]])
                return result
            if isinstance(result, (basestring, str)):
                self.p1.execute(['Game Over', self.otherplayerwins()])
                self.p2.execute(['Game Over', self.otherplayerwins()])
                return [self.otherplayerwins(), 'cheating']
            self.board = result

    def placement(self, p):
        rsp = p.execute(['Place', self.turn, self.board.format_board()])
        coords = rsp
        if isinstance(coords, (basestring, str)):
            return self.otherplayerwins()
        coord1 = coords[0]
        coord2 = coords[1]
        worker1 = self.turn + '1'
        worker2 = self.turn + '2'
        worker1_Pos = Position(coord1[0], coord1[1])
        worker2_Pos = Position(coord2[0], coord2[1])
        if not self.board._is_in_bounds(worker1_Pos) or not self.board._is_in_bounds(worker2_Pos):
            return self.otherplayerwins()
        if self.board.is_cell_occupied(worker1_Pos) or self.board.is_cell_occupied(worker2_Pos):
            return self.otherplayerwins()

        self.board.worker_locations[worker1] = worker1_Pos
        self.board.worker_locations[worker2] = worker2_Pos
        self.turn = self.other_color(self.turn)
        return self.board

    # Takes a play given to it by a player and tells the player they lose if it is
    # not a legal play and tells the other player they won
    def check_play(self, worker, directions):
        # checks if its valid play
        if len(directions) < 2:
            directions.append(None)
        play = Play(worker, directions[0], directions[1])
        is_legal = self.rule_checker.is_valid_play(self.board, play)
        if not is_legal or self.turn != self.get_player_color(play):
            return self.otherplayerwins()

        self.board.move_worker(play.worker, play.move_direction)
        if play.build_direction:
            self.board.build(play.worker, play.build_direction)
            self.turn = self.other_color(self.turn)
            return self.board
        else:
            return [self.color_to_name[self.turn]]

    def get_player_color(self, play):
        return play.worker[: -1]

    def other_color(self, color):
        if color == 'blue':
            return 'white'
        return 'blue'

    def otherplayerwins(self):
        return self.color_to_name[self.other_color(self.turn)]

    def get_loser(self, name):
        if self.color_to_name['white'] == name:
            return self.color_to_name['blue']
        return self.color_to_name['white']
