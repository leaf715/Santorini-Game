#!/usr/bin/env python
import sys
import JsonParser
import json
import copy

class Board:
    def __init__(self):
        self.board_size = 5
        self.direction_map = {
            'N': {'row':-1, 'col':0},
            'E': {'row':0, 'col':1},
            'S': {'row':1, 'col':0},
            'W': {'row':0, 'col':-1},
            'NE': {'row':-1, 'col':1},
            'NW': {'row':-1, 'col':-1},
            'SE': {'row':1, 'col':1},
            'SW': {'row':1, 'col':-1}
        }
        self.order_map = {
            'neighboring-cell-exists?': self.__is_valid_destination__,
            'get-height': self.__get_height__,
            'occupied?': self.__is_occupied__,
            'build': self.__build__,
            'move': self.__move_worker__,
        }

    def __move_worker__(self, worker, direction):
        pos = self.__get_new_pos__(worker, direction)
        self.workers[worker] = pos
        return self.__format_board__()

    def __is_valid_destination__(self, worker, direction):
        new_pos = self.__get_new_pos__(worker, direction)
        is_valid = self.__is_in_bounds__(new_pos)
        return is_valid

    def __build__(self, worker, direction):
        new_pos = self.__get_new_pos__(worker, direction)
        self.height_grid[new_pos['row']][new_pos['col']] += 1
        return self.__format_board__()

    def __get_new_pos__(self, worker, direction):
        dir_coords = self.direction_map[direction]
        curr_pos = self.workers[worker]
        new_pos = {
            'row': curr_pos['row']+dir_coords['row'],
            'col': curr_pos['col']+dir_coords['col']
        }
        return new_pos

    def __is_in_bounds__(self, pos):
        is_valid_row = pos['row']<self.board_size and pos['row']>=0
        is_valid_col = pos['col']<self.board_size and pos['col']>=0
        return is_valid_col and is_valid_row

    def __get_height__(self, worker, direction):
        new_pos = self.__get_new_pos__(worker, direction)
        return self.height_grid[new_pos['row']][new_pos['col']]

    def __is_occupied__(self, worker, direction):
        new_pos = self.__get_new_pos__(worker, direction)
        return new_pos in self.workers.values()

    def __parse_board__(self, board):
        workers = {}
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if isinstance(cell, list):
                    worker_name = cell[1]
                    workers[worker_name] = { 'row': i, 'col': j }

        height_grid = map(lambda row:
            map(lambda cell: cell[0] if isinstance(cell, list) else cell, row), board)
        game_board = { 'height_grid': height_grid, 'workers': workers }
        return game_board

    def __format_board__(self):
        board_copy = copy.deepcopy(self.height_grid)
        for name, pos in self.workers.items():
            height = board_copy[pos['row']][pos['col']]
            board_copy[pos['row']][pos['col']] = [height, name]
        return board_copy

    def __parse_action__(self, action):
        new_board = self.__parse_board__(action[0])
        self.height_grid = new_board['height_grid']
        self.workers = new_board['workers']
        statement = action[1]
        order = statement[0]
        worker = statement[1]
        direction = statement[2]
        if not self.__is_valid_destination__(worker, direction): 
            return json.dumps(False)
        output = self.order_map[order](worker, direction)
        return output

    def exec_action(self):
        parser = JsonParser.JsonParser()
        actions = parser.parse_stream(sys.stdin)
        for action in actions:
            output = self.__parse_action__(action)
            encoded_output = json.dumps(output)
            print(encoded_output)

test_board = Board()
test_board.exec_action()
