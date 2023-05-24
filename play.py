from game import Game, Player, manual
from tree import Minimax_Player, TreeWrapper
from helpers import load

def simple_heuristic(board):
    return board[6] - board[13]

m1 = load("./models/alt2.pkl")
m2 = simple_heuristic

initpos = [4]*6 + [0] + [4]*6 + [0]

wins = [0, 0]
tree = TreeWrapper()
p1 = Minimax_Player(tree, m1, 6, 1, True)
p2 = Minimax_Player(tree, m2, 6, 2, True)
for i in range(8):
    game = Game(p1, p2, True, initpos)
    wins[game.run() - 1] += 1
    print(i)

print(wins)


