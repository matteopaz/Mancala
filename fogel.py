import numpy as np
from nn import NeuralHeuristic
from game import Game, randomstrategy, Player
from tree import Minimax_Player, TreeWrapper
import random
from time import perf_counter
from helpers import save, load
import matplotlib.pyplot as plt

def simple_heuristic(board):
    return board[6] - board[13]

def play_models(model1, model2, ply):
    tree = TreeWrapper()
    p1 = Minimax_Player(tree,model1, ply, 1)
    p2 = Minimax_Player(tree,model2, ply, 2)
    game = Game(p1, p2, False)
    return game.run()

def play_model_and_strategy(model, strategy, ply, modelplayer):
    if modelplayer == 1:
        p1 = Minimax_Player(TreeWrapper(), model, ply, 1)
        p2 = Player(strategy, 2)
        return Game(p1, p2, False).run()
    else:
        p1 = Player(strategy, 1)
        p2 = Minimax_Player(TreeWrapper(), model, ply, 2)
        return Game(p1, p2, False).run()

def play_model_and_mixed(model, strategy, model2, ply, modelplayer, chance_of_strategy=0.5):
    # if
    if np.random.randint(0, 100) < 100*chance_of_strategy:
        return play_model_and_strategy(model, strategy, ply, modelplayer)
    else:
        if modelplayer == 1:
            return play_models(model, model2, ply)
        else:
            return play_models(model2, model, ply)


def N(var):
    return np.random.normal(0, var)

def mutate_wts(wts, normalvariance=0.05**2, sizechangeodds=2):
    newwts = []
    newb = []
    for mtx in wts[0]:
        newmtx = np.copy(mtx)
        for e in newmtx:
            e += N(normalvariance)
        newwts.append(newmtx)

    for mtx in wts[1]:
        newmtx = np.copy(mtx)
        for e in newmtx:
            e += N(normalvariance)
        newb.append(newmtx)
    
    if not np.random.randint(0, sizechangeodds): # custom odds of changing structure
        if np.random.randint(0, 2): # 50-50 odds of adding or removing a layer
            newwts[1] = newwts[1][:, :-1] # Remove a column aka remove a node from hidden layer
            newwts[0] = newwts[0][:-1, :] # remove a row
            newb[0] = newb[0][:-1, :] # remove a row
        else:
            newwts[1] = np.concatenate((newwts[1], np.random.rand(*(newwts[1].shape[0], 1))), axis=1) # Add a column
            newwts[0] = np.concatenate((newwts[0], np.random.rand(*(1, newwts[0].shape[1]))), axis=0) # Add a row
            newb[0] = np.concatenate((newb[0], np.random.rand(*(1, 1))), axis=0) # Add a row
    return newwts, newb

def get_mutated_child(network, normalvariance=0.05**2, sizechangeodds=2):
    kid = NeuralHeuristic(network.shape, rad=0)
    newwts, newb = mutate_wts((network.w, network.b), normalvariance, sizechangeodds)
    kid.w = newwts
    kid.b = newb
    return kid



# m1 = Classifier([14, 10, 6], rad=0)
# m2 = Classifier([14, 10, 6], rad=0)
# save to pickle in ./models
# save(m1, "./models/m1.pkl")
# save(m2, "./models/m2.pkl")

# load from pickle in ./models
# m1 = pickle.load(open("./models/m1.pkl", "rb"))
# m2 = pickle.load(open("./models/m2.pkl", "rb"))

# print(play(m1, m2))

log5 = lambda x: np.log(x) / np.log(5)


# LOAD = "./models/alt2.pkl"
LOAD = False
LOG = False

loss_strategy = randomstrategy
startpop = 20
kidsper = 1
EPOCHS = 200
PLY = 2
top = 10
OPPONENTS = 50
NORMALVARIANCE = 0.03**2
SIZECHANGEODDS = 3
GAMESPER = 5


papas = [[NeuralHeuristic([14, np.random.randint(4, 12), 1], rad=0.5), 0] for i in range(startpop)] # network, score

if LOAD:
    seed = load(LOAD)
    papas = [[seed, 0, 0]] + [[get_mutated_child(seed, NORMALVARIANCE, SIZECHANGEODDS), 0, 0] for i in range(startpop - 1)]

losses = []

best = None
for epoch in range(EPOCHS):
    print("Epoch", epoch)
    papas = [[papa[0], 0, 0] for papa in papas] # reset scores

    for papa in papas: # play each papa against random opponent
        opp = random.choice(papas)
        t1 = perf_counter()
        # for game in range(GAMESPER):
        #     win = play(papa[0], opp[0], PLY)
        #     if win == 1:
        #         papa[1] += 2
        #         opp[1] -= 3
        #     elif win == 2:
        #         papa[1] -= 3
        #         opp[1] += 2
        # t2 = perf_counter()
        # if LOG:
        #     print("Games took", t2 - t1, "seconds")
        
        # simple_win_pts = abs(papa[1] / (log5(epoch+2) * GAMESPER))
        simple_win_pts = 1
        win = []
        for i in range(GAMESPER):
            win_simple = play_model_and_mixed(papa[0], loss_strategy, simple_heuristic, PLY, 1, 0)
            if win_simple == 1:
                papa[1] += simple_win_pts
                papa[2] += 1
            elif win_simple == 2:
                papa[1] -= simple_win_pts*1.5
                papa[2] -= 1

    # take top 25
    papas.sort(key=lambda x: x[2], reverse=True)
    papas = papas[:top]
    best = papas[0][0]
    avgscore = sum([papa[2] for papa in papas]) / len(papas)
    losses.append(avgscore)


    # mutate
    kids = []
    for papa in papas:
        for i in range(kidsper):
            kids.append([get_mutated_child(papa[0], NORMALVARIANCE, SIZECHANGEODDS), 0])
    papas += kids


# save best model with pickle
save(best, "./models/trained.pkl")
    

plt.plot(losses)
plt.show()
    
