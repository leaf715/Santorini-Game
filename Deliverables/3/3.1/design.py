class Board:
    def __init__(self):
        # dimensions of board (board_size x board_size)
        self.board_size = 5
        # 2D array representing heights of each cell
        self.height_grid = [[]]
        # Tracks workers locations
        # {'worker': {'row':index, 'col':index}}
        self.workers = {}
        # Maps direction to numerical change in row/col index
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

    # Given worker and direction, moves worker in that direction if possible
    def __move_worker__(self, worker, direction):
        pass

    # Given worker and direction, builds in direction from worker's position if possible
    def __build__(self, worker, direction):
        pass
