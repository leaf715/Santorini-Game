import unittest
from board import Board, Position

class TestBoard(unittest.TestCase):
    GAME_BOARD = [
        [0,0,0,0,[1,"white2"]],
        [0,0,0,0,0],
        [0,0,[0, "white1"],0,0],
        [0,4,0,[2, "blue2"],0],
        [0,0,[2, "blue1"],0,0]
    ]

    def setUp(self):
        self.board = Board(self.GAME_BOARD)

    def test_get_new_pos(self):
        new_pos = self.board._get_new_pos('white1', 'N')
        self.assertEqual(new_pos.row, 1)
        self.assertEqual(new_pos.col, 2)

    def test_is_in_bounds(self):
        self.assertFalse(self.board._is_in_bounds(Position(0,5)))
        self.assertFalse(self.board._is_in_bounds(Position(5,3)))
        self.assertFalse(self.board._is_in_bounds(Position(0,-1)))
        self.assertTrue(self.board._is_in_bounds(Position(3,2)))

    def test_is_occupied(self):
        self.assertFalse(self.board.is_occupied('white2', 'S'))
        self.assertTrue(self.board.is_occupied('white1', 'SE'))
        self.assertTrue(self.board.is_occupied('blue1', 'NW'))

    def test_get_height(self):
        self.assertEqual(self.board.get_height('white1', 'S'),0)
        self.assertEqual(self.board.get_height('blue1','NE'), 2)
        self.assertEqual(self.board.get_height('blue1', 'NW'), 4)

    def test_neighboring_cell_exists(self):
        self.assertTrue(self.board.neighboring_cell_exists('white1', 'E'))
        self.assertTrue(self.board.neighboring_cell_exists('white1','SE'))
        self.assertFalse(self.board.neighboring_cell_exists('white2','N'))

    def test_build(self):
        board = Board(self.GAME_BOARD)
        initial_height = board.get_height('white1', 'S')
        board.build('white1','S')
        height_after = board.get_height('white1', 'S')
        self.assertEqual(initial_height+1, height_after)

    def test_move_worker(self):
        board = Board(self.GAME_BOARD)
        new_pos = board._get_new_pos('white1', 'S')
        board.move_worker('white1', 'S')
        self.assertEqual(new_pos, board.worker_locations['white1'])

unittest.main()
