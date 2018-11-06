import copy

class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return 'row: '+ str(self.row) + ' col: ' + str(self.col)

    def __eq__(self, other):
        return isinstance(other, Position) and other.row == self.row and other.col == self.col

class Board:
    DOME_HEIGHT = 4
    DIRECTION_MAP = {
        'N': Position(-1, 0),
        'E': Position(0, 1),
        'S': Position(1, 0),
        'W': Position(0, -1),
        'NE': Position(-1, 1),
        'NW': Position(-1, -1),
        'SE': Position(1, 1),
        'SW': Position(1, -1),
    }

    def __init__(self, game_board):
        self._parse_board(game_board)

    def __str__(self):
        return reduce(lambda x, y: x+str(y)+'\n', self._format_board(), '')

    def move_worker(self, worker, direction):
        pos = self._get_new_pos(worker, direction)
        self.worker_locations[worker] = pos

    def neighboring_cell_exists(self, worker, direction):
        new_pos = self._get_new_pos(worker, direction)
        return self._is_in_bounds(new_pos)

    def build(self, worker, direction):
        new_pos = self._get_new_pos(worker, direction)
        self.height_grid[new_pos.row][new_pos.col] += 1

    def get_height(self, worker, direction):
        new_pos = self._get_new_pos(worker, direction)
        return self.height_grid[new_pos.row][new_pos.col]

    def get_worker_height(self, worker):
        pos = self.worker_locations[worker]
        return self.height_grid[pos.row][pos.col]

    def is_occupied(self, worker, direction):
        new_pos = self._get_new_pos(worker, direction)
        if not self._is_in_bounds(new_pos):
            return False
        worker_present = new_pos in self.worker_locations.values()
        dome_present = self.get_height(worker, direction) >= self.DOME_HEIGHT
        return worker_present or dome_present

    def _is_in_bounds(self, pos):
        is_valid_row = (pos.row < len(self.height_grid)) and (pos.row >= 0)
        is_valid_col = (pos.col < len(self.height_grid)) and (pos.col >= 0)
        return (is_valid_col and is_valid_row)

    def _get_new_pos(self, worker, direction):
        dir_coords = self.DIRECTION_MAP[direction]
        curr_pos = self.worker_locations[worker]
        new_pos = Position(curr_pos.row+dir_coords.row, curr_pos.col+dir_coords.col)
        return new_pos

    def _parse_board(self, board):
        worker_locations = {}
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                if isinstance(cell, list):
                    worker_name = cell[1]
                    worker_locations[worker_name] = Position(i, j)

        height_grid = map(lambda row:
            map(lambda cell: cell[0] if isinstance(cell, list) else cell, row), board)
        self.worker_locations = worker_locations
        self.height_grid = height_grid

    def _format_board(self):
        board_copy = copy.deepcopy(self.height_grid)
        for name, pos in self.worker_locations.items():
            height = board_copy[pos.row][pos.col]
            board_copy[pos.row][pos.col] = [height, name]
        return board_copy
