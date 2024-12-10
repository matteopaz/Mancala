import numpy as np
import matplotlib.pyplot as plt
import math
import pickle

sig = np.vectorize(lambda x: 1 / (1+math.exp(-x)))
sigprime = np.vectorize(lambda x: sig(x) * (1 - sig(x)))

def matmul(a, b):
    if a.size == 1:
        return np.multiply(a.item(), b)
    if b.size == 1:
        return np.multiply(a, b.item())
    return np.matmul(a, b)

def nextlayer(weights: np.ndarray, nodes: np.ndarray, bias: np.ndarray):
    # if nodes.size == 1:
    #     return (np.multiply(weights, nodes[0]) + bias)
    return (np.reshape(np.matmul(weights, nodes), (weights.shape[0], 1)) + bias)

def plot(data, nn, res, vis = ""):
    for pt in data:
        plt.plot(pt[0], pt[1], "ro")

    x = [n / res for n in range(0, 1*res)]
    y = [nn(np.array([[xpt]]))[1][-1].item() for xpt in x]
    plt.plot(x,y, vis)

    plt.show()

def copyshape(ndarray: np.ndarray): 
    new = np.ndarray(ndarray.shape)
    new.fill(0)
    return new

def elemwise(a: np.ndarray, b: np.ndarray):
    # if a.shape != b.shape:
    #     raise Exception("invalid elemwise multiply")
    return np.multiply(a,b)


def adjust_list(a, da, learningrate):
    new = []
    for i in range(len(a)):
        new.append(a[i] - learningrate*da[i])
        if new[i].size != a[i].size or new[i].size != da[i].size:

            raise Exception("bad +/- result", new[i], "=", a[i], "-", da[i])

    return new

def copyarr(arr):
    return [a for a in arr]

def save(obj, filename):
    with open(filename, "wb") as f:
        pickle.dump(obj, f)

def load(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)