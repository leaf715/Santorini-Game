#The referee needs to have access to the board to determine move validity
import board
#The referee recieves two instances of players
import player
#The referee determines the validity of moves using the Rule_Checker
import Rule_Checker

class Referee:
    #The referee stores references to the players and contains a rule_checker
    # object so it knows what plays are valid and what are not
    @contract(p1=Player, p2=Player)
    def __init__(p1, p2):
        self.rule_checker = RuleChecker()
        self.player1 = p1
        self.player2 = p2

    #Takes a play given to it by a player and tells the player they lose if it is
    # not a legal play and tells the other player they won
    @contract(play=Play)
    def check_play(self, play):
        is_legal = self.rule_checker.is_valid_play(play)
        if not is_legal:
            loser = self.get_player_color(play)
            if loser == 'blue':
                winner = 'white'
            else:
                winner = 'blue'
            self.player1.who_won(winner)
            self.player2.who_won(winner)

    #Get the color from the worker string in the Play class
    @contract(play=Play)
    def get_player_color(self, play):
        return play.worker[:-1]
