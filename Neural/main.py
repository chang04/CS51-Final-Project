__author__ = 'zachbai'

import csv
import numpy as np
import ANN

reader=csv.reader(open("1500movies_with_gross.csv","rb"),delimiter=',')
input = list(reader)
input = np.array(input)
outputs = input[1:,[5]]
outputs = np.array(outputs, np.float)
input = input[1:,[1,2,3,4,6]]
input = np.array(input, np.float)

"""
#Sample Network
bpn = ANN.NeuralNetwork([2,2,1])
y = np.array([[1,2],[3,4],[9,1]])
x = np.array([[1,2]])
zeros = np.array([0])
z = np.array([[0,0],[1,1],[0,1],[1,0]])
target = np.array([[0.05],[0.05],[0.7]])
output = np.array([[6]])


bpn.train(y, target,0.2, 10000)
"""

NeuralNetwork = ANN.NeuralNetwork([5,4,3,1])
NeuralNetwork.train(input, outputs, 0.2, 50000)
print NeuralNetwork.run(np.array([[50000000, 20, 4, 112, 191719337]]))


