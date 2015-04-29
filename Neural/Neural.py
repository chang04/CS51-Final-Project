import numpy as np

class neuralNetwork:
    layers = 0
    shape = None
    weights = []

    def __init__(self, network):
        self.layers = len(network)
        self.shape = network
        self.input = []
        self.outputs = []

        for i in range(0, self.layers - 1):
            n = self.shape[i]
            m = self.shape[i+1]
            self.weights.append(np.random.normal(0, 0.1, size = (m,n)))
            self.input.append(np.zeros((0,n)))
            self.outputs.append(np.zeros((0,n)))

    def sgm(self, x):
        return 1/(1+np.exp(-x))

    def dersgm(self, x):
        y = sgm(x)
        return y*(y-1)

    def run(self, inputs):
        input = np.array(inputs)
        input = input.T
        self.input[0] = inputs
        self.outputs[0] = inputs
        for i in range(1, self.layers-1):
            self.input[i] = np.dot(self.weights[i-1], self.outputs[i-1])
            self.outputs[i] = self.sgm(self.input[i])
        return self.outputs[-1]



bpn = neuralNetwork([2,2,1])
print(bpn.weights)
print(bpn.run([2,1]))