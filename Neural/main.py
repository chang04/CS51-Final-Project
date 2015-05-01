__author__ = 'zachbai'

import csv
import numpy as np
import ANN

reader=csv.reader(open("1500movie_data.csv","rb"),delimiter=',')
x = list(reader)
x = np.array(x)
x = x[1:,[1,2,3,4,5,6]]
x.astype(float)
target = []

NeuralNetwork = ANN.NeuralNetwork([6,6,6,6,1])
NeuralNetwork.train(x, target, .5, 10000)

