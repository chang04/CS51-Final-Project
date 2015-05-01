__author__ = 'zachbai'

import csv
import numpy as np
import ANN

reader=csv.reader(open("1500movie_data.csv","rb"),delimiter=',')
input = list(reader)
input = np.array(input)
outputs = input[1:,[6]]
outputs = np.array(outputs, np.float)
input = input[1:,[1,2,3,4,5]]
input = np.array(input, np.float)


NeuralNetwork = ANN.NeuralNetwork([5,5,1])
NeuralNetwork.train(input, outputs, .5, 100000)

