from graph import Node, WeightedGraph
from game import MancalaBoard, display
from time import perf_counter
import numpy as np


class GameState(Node, MancalaBoard):
    def __init__(self, rootpos=None, turn=1):
        MancalaBoard.__init__(self, rootpos)
        Node.__init__(self, tuple(self.slots))
        self.turn = turn
        self.heuristic = None
        
    
    def duplicate(self):
        new_gamestate = GameState()
        new_gamestate.children = self.children.copy()
        new_gamestate.parents = self.parents.copy()
        new_gamestate.previous = self.previous
        new_gamestate.distance = self.distance
        new_gamestate.slots = (self.slots.copy())
        new_gamestate.turn = self.turn
        new_gamestate.heuristic = None # 0!!!
        return new_gamestate

    def getchildleaves(self):
        possible_moves = self.possible_moves(self.turn)
        new_states = []
        for move in possible_moves:

            # new_gamestate = copy.deepcopy(self) # deep copy waay too slow but might be a problem
            new_gamestate = self.duplicate()

            new_gamestate.slots = (self.slots.copy()) # Detatches slots from self, either this or deepcopy too slow
            extraturn = new_gamestate.choose(self.turn, move)

            new_gamestate.id = tuple(new_gamestate.slots)
            if extraturn:
                new_gamestate.turn = self.turn 
            else:
                new_gamestate.turn = self.turn % 2 + 1
            
            new_states.append((new_gamestate, move))
        return new_states
    
    def getstate(self):
        return self.slots

class TreeWrapper():
    def __init__(self, root=None):
        self.tree = Tree(GameState(root))
    
    def new(self,root, move):
        self.tree = Tree(GameState(root, move))

    
class Tree(WeightedGraph):
    def __init__(self, root):
        self.nodes = {root.id: root}
        self.edges = {}
        self.current_outer = {root.id: True}
        self.root = root.id

    def next_layers(self, layers=1):
        for i in range(layers):
            parents_to_delete = np.array([])
            children_to_append = np.array([])
            currentouter_immutable = self.current_outer.copy()
            for nodeid in currentouter_immutable:
                node = self.nodes[nodeid]
                leaves = node.getchildleaves() # State-Move tuples
                for leaf in leaves:
                    gamestate = leaf[0]
                    movemade = leaf[1]
                    if gamestate.id in self.nodes:
                        node.addchild(self.nodes[gamestate.id])
                        self.nodes[gamestate.id].addparent(node)
                    else:
                        self.nodes[gamestate.id] = gamestate
                        node.addchild(self.nodes[gamestate.id])
                        self.nodes[gamestate.id].addparent(node)
                    self.current_outer[gamestate.id] = True
                    self.edges[(node.id, gamestate.id)] = movemade
                
                if len(leaves) != 0:
                    del self.current_outer[node.id] # set to false for debuggiung
                

            
            
            for parent in parents_to_delete:
                del self.current_outer[parent]
            for child in children_to_append:
                self.current_outer[child] = True


    def runheuristic(self, heuristic):
        for nodeid in self.current_outer:
            node = self.nodes[nodeid]
            node.heuristic = heuristic(node.getstate())
        return
    
    def propagate_minimax(self, nodeids=None):
        if nodeids == None:
            nodeids = self.current_outer
        parentlayer = []
        for nodeid in nodeids:
            node = self.nodes[nodeid]
            parents = node.getparents()
            for parent in parents:
                parentlayer.append(parent.id)
                if parent.turn == 1:
                    if parent.heuristic != None:
                        parent.heuristic = max(parent.heuristic, node.heuristic)
                    else:
                        parent.heuristic = node.heuristic
                else:
                    if parent.heuristic != None:
                        parent.heuristic = min(parent.heuristic, node.heuristic)
                    else:
                        parent.heuristic = node.heuristic
        if len(nodeids) == 0:
            return
        else:
            return self.propagate_minimax(parentlayer)
        

def heur1(board):
    your_resovoir = board[6]
    opp_resovoir = board[13]
    your_side = sum(board[0:6])
    opp_side = sum(board[7:13])
    return your_resovoir - opp_resovoir + your_side - opp_side


root = None
class Minimax_Player:
    def __init__(self, TREE, heuristic_function, ply, player, log=False):
        self.outer = TREE
        self.outer.tree.next_layers(ply)

        self.heuristic = heuristic_function
        self.ply = ply
        self.log = log
        self.player = player
    
    
    def minimax(self, board):

        if board not in self.outer.tree.nodes:
            if self.log:
                print("Failure: Boardstate not in gametree -- Trying reinitialization")
            #if its outside of the known gametree, then it is being asked of us
            # since its being asked of us, it must be our turn, so the board turn is self.player
            self.outer.new(board, self.player)
            if board not in self.outer.tree.nodes:
                raise Exception("Failure: Boardstate not compatible with gametree")
        
        if self.log:
            print("Minimax: Thinking...")
            t1 = perf_counter()
        
        currentstate = self.outer.tree.nodes[board]

        self.outer.new(currentstate.getstate(), currentstate.turn)
        self.outer.tree.next_layers(self.ply)   

        self.outer.tree.runheuristic(self.heuristic) #HEURISTIC

        self.outer.tree.propagate_minimax() #PROPAGATE

        currentstate = self.outer.tree.nodes[board]
        nextstates = currentstate.getchildren() 
        minimax_values = [x.heuristic for x in nextstates] 
        # This part will be random if there are multiple moves with the same heuristic value, nextstates is randomly shuffled by default
        if self.player == 1: # if theres nones in here, check the propagate function / initialization of heuristic
            best = nextstates[minimax_values.index(max(minimax_values))]
        else:
            best = nextstates[minimax_values.index(min(minimax_values))]
        
        bestmove = self.outer.tree.edges[(currentstate.id, best.id)]


        if self.log:
            t2 = perf_counter()
            print("Minimax: Thinking took {} seconds".format(t2 - t1))
            print("Done: Best move is slot {}".format(bestmove))
    
        return bestmove
    
    def play(self, board):
        move = self.minimax(board)
        return move


    
# root = GameState()
# tree = Tree(root)
# tree.next_layers(2)
# tree.runheuristic(heur1)
# # tree.propagate_minimax()
# print([tree.nodes[i].heuristic for i in tree.nodes])
# tree.propagate_minimax()
# print([tree.nodes[i].heuristic for i in tree.nodes])

