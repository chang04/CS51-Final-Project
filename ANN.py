import csv
import numpy as np

class NeuralNetwork:
    layers = 0
    shape = None
    weights = []

    layerIn = []
    layerOut = []

    def __init__(self, shape):
        self.shape = shape
        self.layers = len(shape) - 1

        for i in range(0,self.layers):
            n = shape[i]
            m = shape[i+1]
            self.weights.append(np.random.normal(0, 1, size = (m,n+1)))

    def sgm(self, x):
        return 1/(1+np.exp(-x))

    def dersgm(self, x):
        y = self.sgm(x)
        return y*(y-1)


    def Run_one(self, input):
        self.layerIn = []
        self.layerOut = []

        dim = input.shape[0]

        for i in range(self.layers):
            if i == 0:
                layer = self.weights[0].dot(np.vstack((input.transpose(), np.ones([1,dim]))))
            else:
                layer = self.weights[i].dot(np.vstack((self.layerOut[-1], np.ones(1))))
            self.layerIn.append(layer)
            self.layerOut.append(self.sgm(layer))

        return (self.layerOut[-1]).transpose()

    def Run_multiple(self, input):



bpn = NeuralNetwork([2,2,1])
input = np.array([[1,2]])
print bpn.Run_Bitch(input)



