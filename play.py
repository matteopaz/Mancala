from game import Game, Player, manual
from tree import Minimax_Player, TreeWrapper
from helpers import load

def simple_heuristic(board):
    return board[6] - board[13]

m1 = load("./models/trained.pkl")
m2 = simple_heuristic

initpos = [4]*6 + [0] + [4]*6 + [0]

wins = [0, 0]
tree = TreeWrapper()
# p1 = Minimax_Player(tree, m1, 6, 1, True)
p1 = Player(manual, 1)
p2 = Minimax_Player(tree, m2, 6, 2, True)
game = Game(p1, p2, log=True, initpos=initpos)
game.run()