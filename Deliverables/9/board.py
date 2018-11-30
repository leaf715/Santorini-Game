import copy


class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return 'row: ' + str(self.row) + ' col: ' + str(self.col)

    def __eq__(self, other):
        return isinstance(other, Position) and other.row == self.row and other.col == self.col

    def near(self, other):
        if abs(self.row - other.row) > 1:
            return False
        if abs(self.col - other.col) > 1:
            return False
        return True


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

    # calls parse board to load list representation of board into class structure
    def __init__(self, game_board):
        self._parse_board(game_board)

    # allows board to be printed as a string
    def __str__(self):
        return reduce(lambda x, y: x + str(y) + '\n', self._format_board(), '')

    def __eq__(self, other):
        return self.worker_locations == other.worker_locations and self.height_grid == other.height_grid

    def move_worker(self, worker, direction):
        pos = self._get_new_pos(worker, direction)
        self.worker_locations[worker] = pos

    # given worker and direction, return a bool of if a cell exists in that direction
    def neighboring_cell_exists(self, worker, direction):
        new_pos = self._get_new_pos(worker, direction)
        return self._is_in_bounds(new_pos)

    # given worker and direction, build in that direction
    def build(self, worker, direction):
        new_pos = self._get_new_pos(worker, direction)
        self.height_grid[new_pos.row][new_pos.col] += 1

    # given worker and direction, get the height of the cell in that direction
    def get_height(self, worker, direction):
        new_pos = self._get_new_pos(worker, direction)
        return self.height_grid[new_pos.row][new_pos.col]

    # given worker, get the height of the cell that worker is on
    def get_worker_height(self, worker):
        pos = self.worker_locations[worker]
        return self.height_grid[pos.row][pos.col]

    # given worker and direction, return a bool of if that cell is occupied
    def is_occupied(self, worker, direction):
        new_pos = self._get_new_pos(worker, direction)
        if not self._is_in_bounds(new_pos):
            return False
        return self.is_cell_occupied(new_pos)

    # given position, return if that cell is occupied by a worker or dome
    def is_cell_occupied(self, position):
        return position in self.worker_locations.values() or self._get_cell_height(position) >= self.DOME_HEIGHT

    # given position, return the height of that cell
    def _get_cell_height(self, position):
        return self.height_grid[position.row][position.col]

    # given position, return if that position is within the board
    def _is_in_bounds(self, pos):
        is_valid_row = (pos.row < len(self.height_grid)) and (pos.row >= 0)
        is_valid_col = (pos.col < len(self.height_grid)) and (pos.col >= 0)
        return (is_valid_col and is_valid_row)

    # given worker and direction, returns a new position object that is the cell in that direction
    def _get_new_pos(self, worker, direction):
        dir_coords = self.DIRECTION_MAP[direction]
        curr_pos = self.worker_locations[worker]
        new_pos = Position(curr_pos.row + dir_coords.row, curr_pos.col + dir_coords.col)
        return new_pos

    # given list representation of board, load the data into the class representation
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

    # returns list representation of current board
    def _format_board(self):
        board_copy = copy.deepcopy(self.height_grid)
        for name, pos in self.worker_locations.items():
            height = board_copy[pos.row][pos.col]
            board_copy[pos.row][pos.col] = [height, name]
        return board_copy
