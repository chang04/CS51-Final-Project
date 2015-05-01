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


    def run(self, input):
        self.layerIn = []
        self.layerOut = []

        dim = input.shape[0]

        for i in range(self.layers):
            if i == 0:
                layer = self.weights[0].dot(np.vstack((input.transpose(), np.ones([1,dim]))))
            else:
                layer = self.weights[i].dot(np.vstack((self.layerOut[-1], np.ones([1,dim]))))
            self.layerIn.append(layer)
            self.layerOut.append(self.sgm(layer))

        return (self.layerOut[-1]).transpose()

    def delta(self, input, y):
        output = []
        y_hat = self.run(input)

        for i in reversed(range(self.layers)):
            if i == self.layers-1:
                error = y_hat - y
                output.append(self.dersgm(y_hat) * error)
            else:
                error = self.weights[i+1][:, :-1].dot(output[-1])
                output.append(self.dersgm(self.layerOut[i]) * error)

        return output

    def weight_delta(self, deltas):
        instance_weight_list = []
        ordered_deltas = list(reversed(deltas))
        output = []

        for i in range(self.layers):
            if i == 0:
                instance_weight_list.append(ordered_deltas[i].T * input)
                print input
            else:
                instance_weight_list.append(ordered_deltas[i].T * self.layerOut[i])


        return instance_weight_list

bpn = NeuralNetwork([2,2,1])
input = np.array([[1,2],[3,4]])
output = np.array([2,5])
deltas = bpn.delta(input, output)
bpn.weight_delta(deltas)
"""print bpn.weight_delta(deltas)"""
