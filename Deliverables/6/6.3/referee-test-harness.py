#!/usr/bin/env python

import sys
import json
from JsonParser import JsonParser
from player import Player
from board import Board
from referee import Referee


class PlayerTestHarness:
    def __init__(self):
        self.parser = JsonParser()

    def main(self):
        referee = Referee()
        commands = self.parser.parse_stream(sys.stdin)
        for i, command in enumerate(commands):
            if i < 2:
                rsp = referee.create_player(command)
                print json.dumps(rsp)
                continue
            elif i < 4:
                rsp = referee.placement(command[0], command[1])
            else:
                rsp = referee.check_play(command[0], command[1])
            if isinstance(rsp, unicode):
                print json.dumps(rsp)
                break
            else:
                print json.dumps(rsp._format_board())


harness = PlayerTestHarness()
harness.main()
