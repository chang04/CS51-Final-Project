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
            self.weights.append(np.random.normal(scale=1 , size = (m,n+1)))

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

    def backpropogate(self, input, y, learning_rate):
        deltas = []
        y_hat = self.run(input)


        #Calculate deltas
        for i in reversed(range(self.layers)):

            #for last layer
            if i == self.layers-1:
                error = y_hat - y
                msq_error = sum(.5 * ((error) ** 2))
                #returns delta, k rows for k inputs, m columns for m nodes
                deltas.append(error * self.dersgm(y_hat))
            else:
                error = deltas[-1].dot(self.weights[i+1][:,:-1])
                deltas.append(self.dersgm(self.layerOut[i]).T * error)

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
                wdelta.append(ordered_deltas[i].T.dot(input_with_bias.T))
            else:
                with_bias = np.vstack((self.layerOut[i-1], np.ones(input.shape[0])))
                wdelta.append(ordered_deltas[i].T.dot(with_bias.T))



        #update_weights
        def update_weights(self, weight_deltas, learning_rate):
            for i in range(self.layers):
                self.weights[i] = self.weights[i] +\
                                  (learning_rate * weight_deltas[i])


        update_weights(self, wdelta, learning_rate)

        return msq_error

        #end backpropogate

    def train(self, input, target, lr, run_iter):
        for i in range(run_iter):
            if i % 100 == 0:
                print self.backpropogate(input, target, lr)







