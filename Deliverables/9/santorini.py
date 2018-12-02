import sys
import json
from JsonParser import JsonParser
from board import Board
from player import Player
from RuleChecker import RuleChecker, Play
from playerproxy import ProxyPlayer
from referee import Referee
import socket
import select
import defaultdriver
import math

class Santorini:
  def __init__(self):
    self.parser = JsonParser()
    cfg_file = open('santorini.config', 'r')
    cfg = json.loads(cfg_file.read())
    self.ip = cfg['IP']
    self.port = cfg['port']
    self.default = cfg['default-player']

  def main(self):
    if len(sys.argv) != 3:
        return
    mode = sys.argv[1]
    n = int(sys.argv[2])
    # totaln = self.power2(n)
    admin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    admin.bind((self.ip,self.port))
    admin.listen(5)
    players = []
    games = []
    while len(players) != n:
        client, ip = admin.accept()
        player = ProxyPlayer(client)
        players.append(player)
    num_games = len(players)/2
    if mode == '-league':
        games = []
        scoreboard = {}
        for i in range(len(players)):
            for j in range(i+1,len(players)):
                games.append([players[i],players[j]])
        for game in games:
            p1 = game[0]
            p2 = game[1]
            ref = Referee(p1, p2)
            winner = ref.run_game();
            cheated = len(winner) == 2
            winner = winner[0]
            # print ref.board.format_board()
            # print winner
            loser = ref.get_loser(winner)
            if loser not in scoreboard.keys():
                scoreboard[loser] = 0
            if winner in scoreboard.keys():
                scoreboard[winner] = scoreboard[winner] + 1
            else:
                scoreboard[winner] = 1
            print scoreboard
    if mode == '-cup':
        rounds = math.log(len(players),2)
        scoreboard = []
        for r in range(int(rounds)):
            winners = []
            for i in range(len(players)/2):
                p1 = players[i*2]
                p2 = players[i*2+1]
                ref = Referee(p1, p2)
                winner = ref.run_game();
                cheated = len(winner) == 2
                winner = winner[0]
                print ref.board.format_board()
                print winner
                if ref.color_to_name['blue'] == winner:
                    winners.append(p1)
                    if cheated:
                        scoreboard.append((rounds + 1, ref.color_to_name['white']))
                    else:
                        scoreboard.append((rounds-r + 1, ref.color_to_name['white']))
                else:
                    winners.append(p2)
                    if cheated:
                        scoreboard.append((rounds + 1, ref.color_to_name['white']))
                    else:
                        scoreboard.append((rounds-r + 1, ref.color_to_name['blue']))
                if r == int(rounds) - 1:
                    scoreboard.append((1.0, winner))
            players = winners
        list.sort(scoreboard)
        print scoreboard
    admin.close()

if __name__=="__main__":
    santorini = Santorini()
    santorini.main()
