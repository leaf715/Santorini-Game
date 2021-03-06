import json

class JsonParser:
  def __init__(self):
    pass

  def _isValidJSON(self, value):
    try:
      json.loads(value)
      return True
    except:
      return False

  def parse_stream(self, stream):
    lines = stream.readlines()
    stripped_lines = map(lambda line: line.strip(), lines)
    
    block = ""
    json_values = []
    for line in stripped_lines:
      block += line
      if self._isValidJSON(block):
        decoded_json = json.loads(block)
        json_values.append(decoded_json)
        block = ""

    return json_values

  def parse_value(self, stream):
    json_string = stream.readline().strip()

    while not self._isValidJSON(json_string) and not json_string == "":
      json_string += stream.readline().strip()
    
    return json.loads(json_string)
     
    