import sys
import json
from playerproxy import ProxyPlayer
from referee import Referee
import socket
import math
import imp


class Santorini:
    def __init__(self):
        cfg_file = open('santorini.config', 'r')
        cfg = json.loads(cfg_file.read())
        self.ip = cfg['IP']
        self.port = cfg['port']
        self.default = cfg['default-player']
        self.default_player = imp.load_source('Player', self.default)
        self.bot_num = 1

    def main(self):
        if len(sys.argv) != 3:
            return
        mode = sys.argv[1]
        n = int(sys.argv[2])
        # check to see if power of 2
        n_next = pow(2, math.ceil(math.log(n) / math.log(2)))
        if n_next < 2:
            n_next = 2
        admin = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        admin.bind((self.ip, self.port))
        admin.listen(5)
        players = []
        while len(players) != n:
            admin.listen(5)
            client, ip = admin.accept()
            player = ProxyPlayer(client)
            players.append(player)
            print 'connected a player'
        while len(players) != n_next:
            new_default_player = self.default_player.Player()
            new_default_player.name = "bot" + str(self.bot_num)
            self.bot_num = self.bot_num + 1
            players.append(new_default_player)
        if mode == '-league':
            self.league(players)
        elif mode == '-cup':
            self.cup(players)
        admin.close()

    def league(self, players):
        games = []
        scoreboard = {}
        player_victories = {}
        for i in range(len(players)):
            for j in range(i + 1, len(players)):
                games.append([i, j])
        for game in games:
            p1 = players[game[0]]
            p2 = players[game[1]]
            ref = Referee(p1, p2)
            winner = ref.run_game()

            cheated = len(winner) == 2
            winner = winner[0]
            loser = ref.get_loser(winner)

            if cheated:
                cheater = loser
                scoreboard[loser] = float("-inf")
                if winner not in scoreboard.keys():
                    scoreboard[winner] = 1
                else:
                    scoreboard[winner] = scoreboard[winner] + 1
                if cheater in player_victories.keys():
                    for loser in player_victories[cheater]:
                        scoreboard[loser] = scoreboard[loser] + 2
                new_default_player = self.default_player.Player()
                new_default_player.name = "bot" + str(self.bot_num)
                self.bot_num = self.bot_num + 1

                if ref.p1name == loser:
                    players[players.index(p1)] = new_default_player
                else:
                    players[players.index(p2)] = new_default_player

            else:
                if loser not in scoreboard.keys():
                    scoreboard[loser] = - 1
                else:
                    scoreboard[loser] = scoreboard[loser] - 1
                if winner not in scoreboard.keys():
                    scoreboard[winner] = 1
                else:
                    scoreboard[winner] = scoreboard[winner] + 1
                # to keep track of victories
                if winner not in player_victories.keys():
                    player_victories[winner] = [loser]
                else:
                    player_victories[winner].append(loser)
        scoreboard_list = [(v, k) for k, v in scoreboard.iteritems()]
        # natively sort tuples by first element
        scoreboard_list.sort(reverse=True)
        rank = 0
        buffer = 1
        last_v = 0
        print "Rank Player Score"
        for v, k in scoreboard_list:
            if v != last_v:
                rank = rank + buffer
                buffer = 1
            else:
                buffer = buffer + 1

            last_v = v
            print rank, k, ":", v

    def cup(self, players):
        rounds = math.log(len(players), 2)
        scoreboard = []
        for r in range(int(rounds)):
            winners = []
            for i in range(len(players) / 2):
                p1 = players[i * 2]
                p2 = players[i * 2 + 1]
                ref = Referee(p1, p2)
                winner = ref.run_game()
                cheated = len(winner) == 2
                winner = winner[0]
                if ref.color_to_name['blue'] == winner:
                    winners.append(p1)
                    if cheated:

                        scoreboard.append((float("inf"), ref.color_to_name['white']))
                    else:
                        scoreboard.append((rounds - r + 1, ref.color_to_name['white']))
                else:
                    winners.append(p2)
                    if cheated:
                        scoreboard.append((float("inf"), ref.color_to_name['blue']))
                    else:
                        scoreboard.append((rounds - r + 1, ref.color_to_name['blue']))
                if r == int(rounds) - 1:
                    scoreboard.append((1.0, winner))
            players = winners
        list.sort(scoreboard)
        rank = 0
        buffer = 1
        last_v = 0
        print "Rank Player"
        for v, k in scoreboard:
            if v != last_v:
                rank = rank + buffer
                buffer = 1
            else:
                buffer = buffer + 1

            last_v = v
            print rank, k

if __name__ == "__main__":
    santorini = Santorini()
    santorini.main()
