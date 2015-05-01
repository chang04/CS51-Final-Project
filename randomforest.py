import csv
import numpy as np
import scipy as sp
import pylab as pl

csv_filename = 'parse/1500movie_data.csv'

budget = []
genre = []
mpaa = []
runtime = []
rating = []
gross = []
ndat = 1500
gr = []
trsubset = np.zeros((1500, 5))

with open(csv_filename, 'r') as csv_fh:

    #Parse as a CSV file
    reader = csv.reader(csv_fh)

    #Skip header line
    next(reader, None)

    #Loop over the file
    for row in reader:

        budget.append(float(row[1]))
        genre.append(float(row[2]))
        mpaa.append(float(row[3]))
        runtime.append(float(row[4]))
        rating.append(float(row[5]))
        gross.append(float(row[6]))

total = [budget, genre, mpaa, runtime, rating]
budget = np.array(budget)
genre = np.array(genre)
mpaa = np.array(mpaa)
runtime = np.array(runtime)
rating = np.array(rating)
gross = np.array(gross)

#print(np.argmax(gross))
#pl.plot(gross, rating, 'o', color = 'b')
#pl.show()

def decisiontree(data, feature, mtry):
    treefeat = np.zeros((ndat, mtry))
    for y in range(0, ndat):
        treefeat

def randomforest(B, mtry):
    for x in range(1, B + 1):
        for y in range(0, ndat):
            ran = np.random.randint(1, ndat)
            for z in range(0, 5):
                trsubset[y][z] = total[z][ran]
                gr.append(gross[ran])
        featsubset = np.random.choice(5, mtry, replace = False)
        decisiontree(trsubset, featsubset, mtry)

def main():
    randomforest(1, 3)

class decisionnode:
    def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
        self.col=col
        self.value=value
        self.results=results
        self.tb=tb
        self.fb=fb

# Gini impurity tells us the probability of a mistake in categorizing that item.
def giniimpurity(lst):
    total = len(lst)
    counts = {}
    for i in lst:
        counts.setdefault(i,0)
        counts[i]+=1

    impurity = 0
    for j in lst:
        f1 = float(counts[j]) / total
        for k in lst:
            if j == k : continue
            f2 = float(counts[k]) / total
            impurity += (f1 * f2)
    return imp

if __name__ == "__main__":
    main()

