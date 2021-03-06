# The referee needs to have access to the board to determine move validity
from board import Board, Position
# The referee recieves two instances of players
from player import Player
# The referee determines the validity of moves using the Rule_Checker
from RuleChecker import Play, RuleChecker


class Referee:
    # The referee stores references to the players and contains a rule_checker
    # object so it knows what plays are valid and what are not
    def __init__(self):
        self.rule_checker = RuleChecker()
        self.turn = 'blue'
        self.name_to_color = {}
        self.board = Board([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

    def create_player(self, name):
        if self.turn == 'blue':
            self.p1 = Player(self.turn, name)
            self.name_to_color['blue'] = name
            self.turn = 'white'
            return 'blue'
        else:
            self.p2 = Player(self.turn, name)
            self.name_to_color['white'] = name
            self.turn = 'blue'
            return 'white'

    def placement(self, coord1, coord2):
        worker1 = self.turn + '1'
        worker2 = self.turn + '2'
        worker1_Pos = Position(coord1[0], coord1[1])
        worker2_Pos = Position(coord2[0], coord2[1])
        if not self.board._is_in_bounds(worker1_Pos) or not self.board._is_in_bounds(worker2_Pos):
            return self._opponent_wins(self.turn)
        if self.board.is_cell_occupied(worker1_Pos) or self.board.is_cell_occupied(worker2_Pos):
            return self._opponent_wins(self.turn)

        self.board.worker_locations[worker1] = worker1_Pos
        self.board.worker_locations[worker2] = worker2_Pos
        self.turn = self._opponent_color(self.turn)
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
            return self._opponent_wins(self.turn)

        self.board.move_worker(play.worker, play.move_direction)
        if play.build_direction:
            self.board.build(play.worker, play.build_direction)
            self.turn = self._opponent_color(self.turn)
            return self.board
        else:
            return self.name_to_color[self.turn]

    def get_player_color(self, play):
        return play.worker[: -1]

    def _opponent_color(self, color):
        if color == 'blue':
            return 'white'
        return 'blue'

    def _opponent_wins(self, color):
        winner_color = self._opponent_color(color)
        return self.name_to_color[winner_color]
