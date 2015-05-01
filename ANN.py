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

        for i in range(self.layers):
            if i == 0:
                layer = self.weights[0].dot(np.vstack((input.transpose(), np.ones([1,input.shape[0]]))))
            else:
                layer = self.weights[i].dot(np.vstack((self.layerOut[-1], np.ones([1,input.shape[0]]))))
            self.layerIn.append(layer)
            self.layerOut.append(self.sgm(layer))

        return self.layerOut[-1].T

    def delta(self, input, y):
        output = []
        y_hat = self.run(input)

        for i in reversed(range(self.layers)):
            if i == self.layers-1:
                error = y_hat - y
                output.append(error * self.dersgm(y_hat))
            else:
                output_with_bias = np.hstack((output[-1], [[1]]))
             fshlk    error = self.weights[i+1][:,:-1].T.dot(output_with_bias)
                output.append(self.dersgm(self.layerIn[i]) * error)

        return output

    def weight_delta(self, deltas):
        instance_weight_list = []

        ordered_deltas = list(reversed(deltas))
        output = []

        for i in range(self.layers):
            if i == 0:
                """with_bias = np.vstack((input.T, np.ones(self.shape[0])))"""
                instance_weight_list.append(input.T.dot(ordered_deltas[i]))
            else:
                """with_bias = np.vstack((self.layerOut[i], np.ones(self.shape[0])))"""
                instance_weight_list.append(self.layerOut[i].dot(ordered_deltas))

            output.append(sum(instance_weight_list))
            instance_weight_list = []

        return output

    def update_weights(self, weight_deltas, learning_rate):
        for i in range(self.layers):

            self.weights[i] = self.weights[i]-\
                              (learning_rate * weight_deltas[i]).T
        return self.weights

bpn = NeuralNetwork([2,2,1])
input = np.array([[1,2],[3,4]])
input2 = np.array([[1,2]])
output = np.array([[5]])

bpn.run(input2)

print bpn.delta(input2, output)

