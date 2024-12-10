import numpy as np
import random

class MancalaBoard:
    #   ----- 13 -----
    #     0   |   12
    #     1   |   11
    #     2   |   10
    #     3   |   9
    #     4   |   8
    #     5   |    7
    #   -----  6 -----
 
    def __init__(self, initpos=None):
        slots = [4] * 6 + [0] + [4] * 6 + [0]
        if initpos != None:
            slots = list(initpos).copy()
        
        self.slots = slots

    def possible_moves(self, player):
        if self.checkwin() != -1:
            return []
        
        if player == 1:
            return [i for i in range(6) if self.slots[i] != 0]
        elif player == 2:
            return [i for i in range(7, 13) if self.slots[i] != 0]
    
    def getboard(self):
        return tuple(self.slots)

    def choose(self, player, slot): # modifies board, returns if turn is continued
        if player == 1 and slot >= 6:
            print("Invalid move: P1")
            return False
        elif player == 2 and slot < 7:
            print("Invalid move: P2")
            return False
        elif player == 2 and slot == 13:
            print("Invalid move: P2")
            return False
        
        if self.slots[slot] == 0:
            print("Invalid move: Empty")
            return False
        
        stones = self.slots[slot]
        self.slots[slot] = 0
        for i in range(stones): # Move
            slot = (slot + 1) % 14
            if player == 1 and slot == 13:
                slot = (slot + 1) % 14
            elif player == 2 and slot == 6:
                slot = (slot + 1) % 14
            
            self.slots[slot] += 1

            if player == 1 and slot == 6 and i == stones - 1: # Extra turn
                return True
            elif player == 2 and slot == 13 and i == stones - 1:
                return True
            
            if self.slots[slot] == 1 and i == stones - 1 and self.slots[12 - slot] != 0: # Capturing
                if player == 1 and slot < 6:
                    self.slots[6] += 1 + self.slots[12 - slot]
                    self.slots[slot] = 0
                    self.slots[12 - slot] = 0
                elif player == 2 and slot > 6 and slot != 13:
                    self.slots[13] += 1 + self.slots[12 - slot]
                    self.slots[slot] = 0
                    self.slots[12 - slot] = 0
        return False
        
    def checkwin(self):
        if sum(self.slots[:6]) == 0:
            self.slots[13] += sum(self.slots[7:13])
            self.slots[7:13] = [0] * 6
        elif sum(self.slots[7:13]) == 0:
            self.slots[6] += sum(self.slots[:6])
            self.slots[:6] = [0] * 6
        else:
            return -1
            
        if self.slots[6] > self.slots[13]:
            return 1 # P1 wins
        elif self.slots[6] < self.slots[13]:
            return 2 # P2 wins
        else:
            return 0 # Draw


class Game:
    def __init__(self, player1, player2, log=False, initpos=None):
        self.p1 = player1
        self.p2 = player2
        self.board = MancalaBoard(initpos)
        self.log = log
    
    def getstate(self):
        return self.board.getboard()

    def printguide(self):
        print("""
        Welcome to Mancala!
        If you are not familiar with the game, please refer to the following guide: https://www.scholastic.com/content/dam/teachers/blogs/alycia-zimmerman/migrated-files/mancala_rules.pdf
        
        You will be playing against an AI in turns. To make a move, simply input the slot number you want to move from. The corresponding slot numbers are as follows:
        """)
        demo = MancalaBoard(list(range(14)))
        display(demo.getboard())

        print("""
        If you make an invalid move (e.g. moving from an empty slot, moving from the opponent's slots, etc.), the game will prompt you to make a valid move again.
        """)

        print("""Good luck! No one has beat the AI yet...""")

        return input("Press Enter to start the game")
    
    def run(self):
        self.printguide()
        state = -1
        turn = 1
        while state == -1:

            if turn == 1:
                isturn = True
                while isturn:
                    if self.log:
                        print("Turn: {}".format(turn))
                        display(self.board.getboard())
                    slot = self.p1.play(self.board.getboard())
                    isturn = self.board.choose(1, slot)
                    state = self.board.checkwin()
                    if state != -1:
                        break
                turn = 2
            else:
                isturn = True
                while isturn:
                    if self.log:
                        print("Turn: {}".format(turn))
                        display(self.board.getboard())
                    slot = self.p2.play(self.board.getboard())
                    isturn = self.board.choose(2, slot)
                    state = self.board.checkwin()
                    if state != -1:
                        break
                turn = 1
        
        if self.log:
            display(self.board.getboard())
            print("Player {} wins!".format(state))

        return state

def flip(board):
    return board[7:] + board[:7]

class Player:
    def __init__(self, strategy, player):
        self.player = player
        self.strategy = strategy

    def play(self, board):

        if self.player == 1:
            return self.strategy(board)
        else:
            return 7 + self.strategy(flip(board))
    
def display(board):
    print("  ----- {} -----".format(board[13]))
    print("    {}   |   {}".format(board[0], board[12]))
    print("    {}   |   {}".format(board[1], board[11]))
    print("    {}   |   {}".format(board[2], board[10]))
    print("    {}   |   {}".format(board[3], board[9]))
    print("    {}   |   {}".format(board[4], board[8]))
    print("    {}   |    {}".format(board[5], board[7]))
    print("  -----  {} -----".format(board[6]))
    print()
    print()

def manual(board):
    while True:
        slot = int(input("Slot: "))
        if slot >= 0 and slot < 14:
            return slot
        else:
            print("Invalid slot")


def randomstrategy(board):
    return random.choice([i for i in range(6) if board[i] != 0])