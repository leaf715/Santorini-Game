#The player depends on the board module to extract information about the current
# state of the game and make plays
#The strategy module needs board to check the potential plays it can make
import board
#The player depends on the strategy module to tell it what move to make next
import strategy
#The player needs the rule_checker for the play class
#The strategy module needs the rule_checker to check if the plays it considers
# are valid according to the rules of the game
import Rule_Checker

class Player:
    #The player module keeps track of player id, age in years, color of pieces
    @contract(age='int')
    def __init__(self, id, age):
        self.id = id
        self.age = age
        self.color = ''
        self.strategy = strategy.Strategy(self.color)

    #The player registers with the game engine and recieves its color and
    # gives the game engine the player's unique id and age so the game engine
    # can determine who goes first
    @contract(color='string')
    def register(self, color: string):
        self.color = color
        #Initialize strategy module for this player
        self.strategy = strategy.Strategy(color)

    #The player recieves the game board and calls strategy to decide where to put
    # its initial workers. It then places those workers and sends the board back
    # to the game engine
    @contract(board='Board', returns='Board')
    def place_pieces(self, board: board):
        #gets dictionary of worker(key) and where it is being placed(value)
        worker_psns = self.strategy.place_init_workers(board)
        for worker, psn in worker_psns:
            board.place(worker, psn)
        return board

    #The player recieves the current game board from the game engine and decides
    # its next play from the strategy module. It then makes the play and returns
    # the new board
    @contract(board='Board', returns='Board')
    def get_next_play(self, board: board):
        #play is a class within the rule_checker
        play = strategy.next_move(board)
        worker = play.worker
        move_direction = play.move_direction
        build_direction = play.move_direction
        board = board.move(worker, move_direction)
        if build_direction:
            board = board.build(worker, build_direction)
        return board

    #The game module notifies the player who won
    @contract(winner_color='string')
    def who_won(self, winner_color: string):
        if winner_color == self.color:
            self.winner = 'yes'

class Strategy:
    #The strategy class needs to know the color of the player using it and the
    # rules of the game to determine the best play to recommend
    @contract(color='string')
    def __init__(self, color):
        self.color = color
        self.rules = Rule_Checker.Rule_Checker()
        self.workers = [color+'1', color+'2']

    #This function recieves a board with no workers or two workers depending on
    # which player went first and returns a dictionary of the workers and their
    # best placement
    @contract(board='Board', returns='dict')
    def place_init_workers(self, board):
        return {self.workers[0]:psn1, self.workers[1]:psn2}

    #This function considers all possible play combos of a move and a build and
    # returns the best play to the player
    @contract(board='Board', returns='Play')
    def next_move(self, board):
        play_options = self._get_plays(board)
        return best_play

    #Given a board, uses the rule_checker to generate a list of all legal plays
    @contract(board='Board', returns='list(Play)')
    def _get_plays(board):
        return play_options
