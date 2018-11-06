import unittest

from player import Player, Strategy
from RuleChecker import Play
from board import Board, Position

class TestPlayer(unittest.TestCase):
  GAME_BOARD = [
    [0,0,0,0,[1,"white2"]],
    [0,0,0,0,0],
    [0,0,[0, "white1"],3,0],
    [0,4,0,[2, "blue2"],0],
    [0,0,[2, "blue1"],0,0]
  ]

  INITIAL_BOARD = [
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
  ]

  INITIAL_BOARD2 = [
    [[0,'blue1'],0,0,0,[0,'blue2']],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
  ]

  def setUp(self):
    self.board = Board(self.GAME_BOARD)
    self.initial_board = Board(self.INITIAL_BOARD)
    self.player = Player()

  def test_place_workers(self):
    positions = self.player.place_workers(self.initial_board)
    self.assertEqual(positions, [Position(0,0), Position(0,4)])

    initial_board2 = Board(self.INITIAL_BOARD2)
    positions2 = self.player.place_workers(initial_board2)
    self.assertEqual(positions2, [Position(4,4), Position(4,0)])


class TestStrategy(unittest.TestCase):
  GAME_BOARD = [
    [0,0,0,0,[1,"white2"]],
    [0,0,0,0,0],
    [0,0,[0, "white1"],3,0],
    [0,4,0,[2, "blue2"],0],
    [0,0,[2, "blue1"],0,0]
  ]

  GAME_BOARD2 = [
    [0,0,0,0,[1,"white2"]],
    [0,0,0,0,0],
    [0,0,[3, "white1"],2,0],
    [0,4,0,[2, "blue2"],0],
    [0,0,[2, "blue1"],0,0]
  ]

  def setUp(self):
    self.strategy = Strategy()
    self.board = Board(self.GAME_BOARD)
    self.board2 = Board(self.GAME_BOARD2)

  def test_worker_will_win(self):
    white1_wins = self.strategy._worker_will_win('white1', self.board)
    self.assertFalse(white1_wins)
    self.assertTrue(self.strategy._worker_will_win('blue2', self.board))
    self.assertFalse(self.strategy._worker_will_win('blue1', self.board))
    self.assertFalse(self.strategy._worker_will_win('white2', self.board))
    self.assertFalse(self.strategy._worker_will_win('blue2', self.board2))\

  def test_is_losing_play(self):
    play = Play('white1','N', 'N')
    self.assertTrue(self.strategy._is_losing_play('white', play, self.board))
    self.assertFalse(self.strategy._is_losing_play('white', Play('white1', 'N', 'SE'), self.board))

  def test_all_possible_plays(self):
    possible_plays = self.strategy._all_possible_plays('white1', self.board)
    self.assertEqual(len(possible_plays), 8*8+8)

  def test_get_viable_plays(self):
    white_viable_plays = self.strategy.get_viable_plays('white', self.board)
    self.assertEqual(len(white_viable_plays), 5)
    
    blue_viable_plays = self.strategy.get_viable_plays('blue', self.board)
    self.assertEqual(len(blue_viable_plays), 36)

  
unittest.main()