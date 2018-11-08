# The player depends on the board module to extract information about the current
# state of the game and make plays
# The strategy module needs board to check the potential plays it can make
import board
# The player depends on the strategy module to tell it what move to make next
import strategy
# The player needs the rule_checker for the play class
# The strategy module needs the rule_checker to check if the plays it considers
# are valid according to the rules of the game
import Rule_Checker


class Player:
    # The player module keeps track of player id, age in years, color of pieces
    def __init__(self, color):
        self.color = color
        self.strategy = Strategy()
        self.starting_positions = [Position(0, 0), Position(0, 4), Position(4, 4), Position(4, 0)]

    # The player recieves the game board. It then places those workers and sends the board back
    # to the game engine
    def place_workers(self, board):
        count = 0
        lst = []
        for pos in self.starting_positions:
            if not board.is_cell_occupied(pos) and count < 2:
                lst.append(pos)
                count += 1
        return lst

    # The player recieves the current game board from the game engine and decides
    # its next plays from the strategy module.
    def get_plays(self, board):
        return self.strategy.get_viable_plays(self.color, board)

    # The game module notifies the player who won
    @contract(winner_color='string')
    def who_won(self, winner_color: string):
        if winner_color == self.color:
            self.winner = 'yes'
