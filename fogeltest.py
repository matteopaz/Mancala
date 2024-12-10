import numpy as np
from nn import Classifier
from game import Game
from tree import Minimax_Player, TreeWrapper
import random
from time import perf_counter
import concurrent.futures
import pickle
import matplotlib.pyplot as plt 

def play(model1, model2, ply):
    tree = TreeWrapper()
    p1 = Minimax_Player(tree,model1, ply, 1)
    p2 = Minimax_Player(tree,model2, ply, 2)
    game = Game(p1, p2, False)
    return game.run()

def N():
    return np.random.normal(0, 0.05**2)

def mutate(wts):
    newwts = []
    newb = []
    for mtx in wts[0]:
        newmtx = np.copy(mtx)
        for e in newmtx:
            e += N()
        newwts.append(newmtx)

    for mtx in wts[1]:
        newmtx = np.copy(mtx)
        for e in newmtx:
            e += N()
        newb.append(newmtx)
    
    # if np.random.randint(0, 2):
    #     if np.random.randint(0, 2):
    #         newwts[1] = newwts[1][:, :-1] # Remove a column aka remove a node from hidden layer
    #         newwts[0] = newwts[0][:-1, :] # remove a row
    #         newb[0] = newb[0][:-1, :] # remove a row
    #     else:
    #         newwts[1] = np.concatenate((newwts[1], np.random.rand(*(newwts[1].shape[0], 1))), axis=1) # Add a column
    #         newwts[0] = np.concatenate((newwts[0], np.random.rand(*(1, newwts[0].shape[1]))), axis=0) # Add a row
    #         newb[0] = np.concatenate((newb[0], np.random.rand(*(1, 1))), axis=0) # Add a row
    return newwts, newb



# m1 = Classifier([14, 10, 6], rad=0)
# m2 = Classifier([14, 10, 6], rad=0)
# save to pickle in ./models
# save(m1, "./models/m1.pkl")
# save(m2, "./models/m2.pkl")

# load from pickle in ./models
# m1 = pickle.load(open("./models/m1.pkl", "rb"))
# m2 = pickle.load(open("./models/m2.pkl", "rb"))

# print(play(m1, m2))


def play_game(papa, opp):
    # Play the game and return the result
    win = play(papa[0], opp[0], PLY)
    if win == 1:
        return (papa, opp, 3)
    elif win == 2:
        return (papa, opp, -1)
    else:
        return (papa, opp, 0)

startpop = 24
kidsper = 1
EPOCHS = 200
PLY = 5
top = 12

# papas = [[Classifier([14, np.random.randint(1, 20), 14], rad=0.5), 0] for i in range(startpop)] # network, score

losses = []

for epoch in range(EPOCHS):
    print("Epoch", epoch)
    papas = [[papa[0], 0] for papa in papas] # reset scores

    # for papa in papas: # play each papa against random opponent
    #     opp = random.choice(papas)
    #     t1 = perf_counter()
    #     win = play(papa[0], opp[0], PLY)

    t1 = perf_counter()
    # Create a list of opponents for each papa
    opponents = [random.choice(papas) for _ in range(len(papas))]

    # Create a thread pool with a default size of os.cpu_count() threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit each game to the thread pool
        futures = [executor.submit(play_game, papa, opp) for papa, opp in zip(papas, opponents)]

        # Wait for all games to complete and get the results
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    # Update the scores
    for papa, opp, score in results:
        papa[1] += score
        opp[1] -= score
    
    t2 = perf_counter()
    print("Game took", t2 - t1, "seconds")

    # take top 25
    papas.sort(key=lambda x: x[1], reverse=True)
    papas = papas[:top]

    # mutate
    kids = []
    for papa in papas:
        for i in range(kidsper):
            kid = Classifier(papa[0].shape, rad=0)
            newwts, newb = mutate((papa[0].w, papa[0].b))
            kid.w = newwts
            kid.b = newb
            kids.append([kid, 0])
    papas += kids

    
    


plt.plot(losses)
plt.show()
    
