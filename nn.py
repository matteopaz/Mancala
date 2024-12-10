from helpers import nextlayer
import numpy as np

norm = lambda x: x / np.linalg.norm(x)
t = lambda x: np.tanh(x)

def initWB(shape, rad=1.0):
    W = []
    B = []
    for i in range(len(shape) - 1):
        W.append(np.random.rand(shape[i+1], shape[i]) * rad)
        B.append(np.random.rand(shape[i+1], 1) * rad)
    return W, B

class fc: 
    def __init__(self, weights=None, biases=None):
        if weights:
            self.w = weights
        if biases:
            self.b = biases
        self.layers = len(self.w)
    
    def forward(self, inp):
        s = [np.array(inp)]
        h = [t(np.array(inp))]
        for i in range(self.layers):
            s.append(nextlayer(self.w[i], h[i], self.b[i]))
            h.append(t(s[i+1]))
        return h[-1]
    
    
    def __call__(self, inp):
        return self.forward(inp)

class ANN(fc):
    def __init__(self, shape, rad=1.0):

        weights, biases = initWB(shape, rad)
        self.shape = shape
        super().__init__(weights, biases)

class Classifier(ANN):
    def __init__(self, shape, rad=1.0):
        super().__init__(shape, rad)
    
    def __call__(self, inp):
       vals =  self.forward(inp)
       return np.argmax(vals)
    

class NeuralHeuristic(ANN):
    def __init__(self, shape, rad=1.0):
        super().__init__(shape, rad)
        if shape[-1] != 1:
            raise ValueError("Last layer must be of size 1")

    def __call__(self, inp):
        return self.forward(inp).item()

    