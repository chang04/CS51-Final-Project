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
            self.weights.append(np.random.normal(scale=0.01, size = (m,n+1)))

    def sgm(self, x):
        return 1/(1+np.exp(-x))

    def dertanh(self, x):
        out = np.tanh(x)
        return 1 - out ** 2


    def dersgm(self, x):
        y = self.sgm(x)
        return y*(1-y)


    def run(self, input):
        self.layerIn = []
        self.layerOut = []

        for i in range(self.layers):
            if i == 0:
                layer = self.weights[0].dot(np.vstack((input.transpose(), np.ones([1,input.shape[0]]))))
            else:
                layer = self.weights[i].dot(np.vstack((self.layerOut[-1], np.ones([1,input.shape[0]]))))
            self.layerIn.append(layer)
            self.layerOut.append(np.tanh(layer))

        return self.layerOut[-1].T

    def backpropogate(self, input, y, learning_rate):
        deltas = []
        y_hat = self.run(input)


        #Calculate deltas
        for i in reversed(range(self.layers)):

            #for last layer
            if i == self.layers-1:
                out_delt = self.layerOut[i] - y.T
                msq_error = np.sum(.5 * ((out_delt) ** 2))
                #returns delta, k columns for k inputs, m rows for m nodes
                deltas.append(out_delt * self.dertanh(self.layerIn[i]))
            else:
                #backprop -- uses subsequents layer delta to calculate next delta
                last_deltas = self.weights[i+1].T.dot(deltas[-1])
                deltas.append(last_deltas[:-1,:] * self.dertanh(self.layerIn[i]))

        #Calculate weight-deltas
        wdelta = []
        ordered_deltas = list(reversed(deltas)) #reverse order because created backwards


        #returns weight deltas, k rows for k nodes, m columns for m next layer nodes
        for i in range(self.layers):
            if i == 0:
                #add bias
                input_with_bias = np.vstack((input.T, np.ones(input.shape[0])))
                #some over n rows of deltas for n training examples to get one delta for all examples
                #for all nodes
                wdelta.append(ordered_deltas[i].dot(input_with_bias.T))
            else:
                with_bias = np.vstack((self.layerOut[i-1], np.ones(input.shape[0])))
                wdelta.append(ordered_deltas[i].dot(with_bias.T))

        #update_weights
        def update_weights(self, weight_deltas, learning_rate):
            for i in range(self.layers):
                self.weights[i] = self.weights[i] -\
                                  (learning_rate * weight_deltas[i])

        update_weights(self, wdelta, learning_rate)

        return msq_error

        #end backpropogate

    def train(self, input, target, lr, run_iter):
        for i in range(run_iter):
            a = self.backpropogate(input, target, lr)
            if i % 5000 == 0:
                print "Training..."
            if run_iter - i == 1: print a









