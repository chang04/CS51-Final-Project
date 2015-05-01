__author__ = 'zachbai'

import csv
import numpy as np
import ANN

reader=csv.reader(open("1500movies_with_gross.csv","rb"),delimiter=',')
input = list(reader)
input = np.array(input)
outputs = input[1:,[6]]
outputs = np.array(outputs, np.float)
input = input[1:,[1,2,3,4,5]]
input = np.array(input, np.float)


bpn = ANN.NeuralNetwork([2,2,1])
y = np.array([[1,2],[3,4],[9,1]])
x = np.array([[1,2]])
z = np.array([[0,0],[1,1],[0,1],[1,0]])
target = np.array([[0.05],[0.05],[0.95],[0.95]])
output = np.array([[6]])

bpn.train(z,target,.2,1)





NeuralNetwork = ANN.NeuralNetwork([5,5,1])
NeuralNetwork.train(input, outputs, .01, 100000)

