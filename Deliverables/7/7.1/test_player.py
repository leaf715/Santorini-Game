import unittest
from JsonParser import JsonParser
from player import Player
from board import Board, Position
from RuleChecker import RuleChecker, Play

class TestRuleChecker(unittest.TestCase):
    INIT_BOARD1 = [[0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0]]
    INIT_BOARD2 = [[[0,'red1'],0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,[0,'blue2']]]
    INIT_BOARD3 = [[[0,'red1'],0,0,0,'a'],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,[0,'blue2']]]
    GAME_BOARD1 = [[[0,'blue1'],0,0,0,[0,'white1']],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [[0,'white2'],0,0,0,[0,'blue2']]]
    GAME_BOARD2 = [[[0,'blue1'],0,0,0,[0,'white1']],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [[0,'white2'],0,0,0,[0,'blue2']]]



    def setUp(self):
        self.player = Player()

    def test_check_input(self):
        self.assertFalse(self.player.check_input([]))
        self.assertFalse(self.player.check_input(1))
        self.assertFalse(self.player.check_input({'key':1}))
        self.assertFalse(self.player.check_input('sdsa'))
        self.assertTrue(self.player.check_input(['Register']))
        self.assertFalse(self.player.check_input(['Fake']))
        self.assertFalse(self.player.check_input(['Place']))
        self.assertFalse(self.player.check_input(['Place','white']))
        self.assertFalse(self.player.check_input(['Place',2,self.INIT_BOARD1]))
        self.assertTrue(self.player.check_input(['Place','white',self.INIT_BOARD1]))
        self.assertTrue(self.player.check_input(['Place','white',self.INIT_BOARD2]))
        self.assertFalse(self.player.check_input(['Place','white',self.INIT_BOARD3]))
        self.assertFalse(self.player.check_input(['Place','white',self.INIT_BOARD1,['e']]))
        self.assertFalse(self.player.check_input(['Place','white','sm']))
        self.assertFalse(self.player.check_input(['Place','white',[0,0,0,0,0]]))
        self.assertFalse(self.player.check_input(['Place','white',[[0,0,0,0,0],
                                                                    [0,0,0,0,0],
                                                                    [0,0,0,0,0],
                                                                    [0,0,0,0,0]]]))
        self.assertFalse(self.player.check_input(['Place','white',[[0],[0],[0],[0],[0]]]))
        self.assertFalse(self.player.check_input(['Play']))
        self.assertFalse(self.player.check_input(['Play',1]))
        self.assertFalse(self.player.check_input(['Play',[]]))
        self.assertTrue(self.player.check_input(['Play',self.GAME_BOARD1]))
        self.assertTrue(self.player.check_input(['Play',self.INIT_BOARD2]))
        self.assertFalse(self.player.check_input(['Play',self.INIT_BOARD3]))
        self.assertFalse(self.player.check_input(['Play',self.GAME_BOARD1,[]]))
        self.assertFalse(self.player.check_input(['Play',[0,0,0,0,0]]))
        self.assertFalse(self.player.check_input(['Play',[[0],[0],[0],[0],[0]]]))
        self.assertFalse(self.player.check_input(['Play',1]))
        self.assertFalse(self.player.check_input(['Play',[[0,0,0,0,0],
                                                        [0,0,0,0,0],
                                                        [0,0,0,0,0],
                                                        [0,0,0,0,0]]]))
        self.assertFalse(self.player.check_input(['Play',[[0],[0],[0],[0],[0]]]))
        self.assertFalse(self.player.check_input(['Game Over']))
        self.assertFalse(self.player.check_input(['Game Over',1]))
        self.assertFalse(self.player.check_input(['Game Over','shu',1]))
        self.assertTrue(self.player.check_input(['Game Over','shu']))

    def test_execute(self):
        self.assertEqual(self.player.execute(['Register']),'Kanye')


unittest.main()
