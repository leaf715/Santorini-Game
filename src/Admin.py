import sys
import json
import JsonParser

class Admin:
  def __init__(self):
    self.parser = JsonParser.JsonParser()
    self.card = 10

  def __issue_command__(self, command, args):
    command_obj = { 'operation-name': command }
    for index, arg in enumerate(args):
      command_obj['operation-argument' + str(index+1)] = arg
    encoded_json = json.dumps(command_obj)
    print encoded_json

  def __read_response__(self):
    response = self.parser.parse_value(sys.stdin)
    return response

  def __did_player_win__(self, did_keep_card, player_card):
    return player_card > self.card if did_keep_card else self.card > player_card

  def start_game(self):
    self.__issue_command__('declareNumber', [])
    player_card = self.__read_response__()

    self.__issue_command__('keepCard', [player_card])
    did_keep_card = self.__read_response__()

    print 'player won' if self.__did_player_win__(did_keep_card, player_card) else 'admin won'
    

  