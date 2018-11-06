import sys
import JsonParser
import json

class Player:
  def __init__(self):
    self.command_list = { 'keepCard': self.__keepCard__, 'pickCard': self.__pickCard__ }
  
  def __pickCard__(self):
    return 5

  def __keepCard__(self):
    return True

  def read_comands(self):
    parser = JsonParser.JsonParser()
    commands = parser.parse_stream(sys.stdin)
    for command in commands:
      op_name = command['operation-name']
      func = self.command_list[op_name]
      output = func()
      print json.dumps(output)
