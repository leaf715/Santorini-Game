import unittest
from RuleChecker import RuleChecker, Play
from board import Board, Position

class TestRuleChecker(unittest.TestCase):
    GAME_BOARD1 = Board([
        [0,0,0,4,[1,"white2"]],
        [0,0,0,4,4],
        [0,0,[0, "white1"],0,0],
        [0,1,0,[3, "blue2"],4],
        [0,0,3,[2, "blue1"],0]
    ])

    def setUp(self):
        self.rule_checker = RuleChecker()

    def test_is_winner(self):
        self.assertFalse(self.rule_checker._is_winner(self.GAME_BOARD1, 'white1'))
        self.assertFalse(self.rule_checker._is_winner(self.GAME_BOARD1, 'white2'))
        self.assertTrue(self.rule_checker._is_winner(self.GAME_BOARD1, 'blue2'))
    
    def test_is_valid_target(self):
        self.assertFalse(self.rule_checker._is_valid_target(self.GAME_BOARD1, 'white2', 'N'))
        self.assertFalse(self.rule_checker._is_valid_target(self.GAME_BOARD1, 'white2', 'W'))
        self.assertFalse(self.rule_checker._is_valid_target(self.GAME_BOARD1, 'blue1', 'N'))
        self.assertTrue(self.rule_checker._is_valid_target(self.GAME_BOARD1, 'white1', 'W'))
        self.assertTrue(self.rule_checker._is_valid_target(self.GAME_BOARD1, 'white1', 'NW'))

    def test_is_valid_build(self):
        self.assertFalse(self.rule_checker._is_valid_build(self.GAME_BOARD1, 'white2', 'N'))
        self.assertFalse(self.rule_checker._is_valid_build(self.GAME_BOARD1, 'white2', 'W'))
        self.assertFalse(self.rule_checker._is_valid_build(self.GAME_BOARD1, 'blue1', 'N'))
        self.assertTrue(self.rule_checker._is_valid_build(self.GAME_BOARD1, 'white1', 'W'))
        self.assertTrue(self.rule_checker._is_valid_build(self.GAME_BOARD1, 'white1', 'NW'))

    def test_is_valid_move(self):
        self.assertFalse(self.rule_checker._is_valid_move(self.GAME_BOARD1, 'white2', 'N'))
        self.assertFalse(self.rule_checker._is_valid_move(self.GAME_BOARD1, 'white2', 'W'))
        self.assertFalse(self.rule_checker._is_valid_move(self.GAME_BOARD1, 'blue1', 'N'))
        self.assertFalse(self.rule_checker._is_valid_move(self.GAME_BOARD1, 'blue2', 'E'))
        self.assertTrue(self.rule_checker._is_valid_move(self.GAME_BOARD1, 'white1', 'SW'))
        self.assertTrue(self.rule_checker._is_valid_move(self.GAME_BOARD1, 'blue1', 'W'))
        self.assertTrue(self.rule_checker._is_valid_move(self.GAME_BOARD1, 'blue1', 'E'))

    def test_is_loser(self):
        self.assertFalse(self.rule_checker._is_loser(self.GAME_BOARD1, 'white1'))
        self.assertFalse(self.rule_checker._is_loser(self.GAME_BOARD1, 'blue1'))
        self.assertTrue(self.rule_checker._is_loser(self.GAME_BOARD1, 'white2'))

    def test_is_valid_no_build(self):
        self.assertFalse(self.rule_checker._is_valid_no_build(self.GAME_BOARD1, 'white1'))
        self.assertFalse(self.rule_checker._is_valid_no_build(self.GAME_BOARD1, 'blue1'))
        self.assertTrue(self.rule_checker._is_valid_no_build(self.GAME_BOARD1, 'blue2'))

    def test_is_valid_play(self):
        self.assertTrue(self.rule_checker.is_valid_play(self.GAME_BOARD1, Play('blue1','W')))
        self.assertTrue(self.rule_checker.is_valid_play(self.GAME_BOARD1, Play('blue2','SW')))
        self.assertFalse(self.rule_checker.is_valid_play(self.GAME_BOARD1, Play('blue1','E','N')))
        self.assertFalse(self.rule_checker.is_valid_play(self.GAME_BOARD1, Play('blue1','E','E')))
        self.assertFalse(self.rule_checker.is_valid_play(self.GAME_BOARD1, Play('white1','W')))
        self.assertFalse(self.rule_checker.is_valid_play(self.GAME_BOARD1, Play('white1','N','NE')))
        self.assertTrue(self.rule_checker.is_valid_play(self.GAME_BOARD1, Play('white1','S','W')))
        self.assertFalse(self.rule_checker.is_valid_play(self.GAME_BOARD1, Play('white1','S','E')))
        self.assertFalse(self.rule_checker.is_valid_play(self.GAME_BOARD1, Play('white2','W','SW')))


unittest.main()
