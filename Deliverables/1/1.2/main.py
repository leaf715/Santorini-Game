import json
import sys

curly_count = 0
square_count = 0

def main():
  lines = sys.stdin.readlines()
  stripped_lines = map(lambda line: line.strip(), lines)
  parsed_json_values = reduce(lambda prev, curr: process_line(prev, curr), stripped_lines, [])
  
  json_values = map(lambda value: json.loads(value), parsed_json_values)
  
  formatted_json_values = [{ 'index': i+1,'value': x } for i,x in enumerate(json_values)]
  reversed_list = reversed(formatted_json_values)
  for value in reversed_list: print(json.dumps(value))

def process_line(list, line):
  global curly_count
  global square_count

  isInObject = (curly_count > 0) | (square_count > 0)
  if isInObject:
    newItem = list.pop() + line
    list.append(newItem)
  else:
    list.append(line)

  curly_count += line.count("{")
  curly_count -= line.count("}")
  square_count += line.count("[")
  square_count -= line.count("]")
  return list

if __name__=="__main__":
	main()
