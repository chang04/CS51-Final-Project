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
ncol = 6
gr = []
trsubset = np.zeros((ndat, ncol))

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

total = [budget, genre, mpaa, runtime, rating, gross]
budget = np.array(budget)
genre = np.array(genre)
mpaa = np.array(mpaa)
runtime = np.array(runtime)
rating = np.array(rating)
gross = np.array(gross)

#print(np.argmax(gross))
#pl.plot(gross, rating, 'o', color = 'b')
#pl.show()

def decisiontree(md, dat, feature):
    treefeat = np.zeros((ndat, 3))
    for x in range(0, ndat):
        for y in range(0, 3):
            treefeat[x][y] = dat[x][feature[y]]
    #print(treefeat)
    def build(data, i):
        if len(data) == 0:
            return treenode()
        curr_gini = giniimpurity(data)

        opt_gain = 0.
        opt_crit = None
        opt_set = None
        print(feature)
        for x in range(0, 5):#feature:
            colval = {}
            for film in data:
                colval[film[x]] = 1
            for val in colval.keys():
                (s1, s2) = divideset(data, x, val)
                p = float(len(s1)) / len(data)
                print(p)
                gain = curr_gini - p*giniimpurity(s1) - (1-p)*giniimpurity(s2)
                if gain > opt_gain and len(s1) > 0 and len(s2) > 0:
                    opt_gain = gain
                    opt_crit = (x, val)
                    opt_set = (s1, s2)
        if opt_gain > 0 and i <= md:
            tBranch = build(opt_set[0], i + 1)
            fBranch = build(opt_set[1], i + 1)
            return treenode(col = opt_crit[0], val = opt_crit[1], tnode = tBranch, fnode = fBranch)
        else:
            return treenode(res = uniquecounts(data))
    tree = build(dat, 0)

def randomforest(B, mtry, mdepth):
    for x in range(1, B + 1):
        for y in range(0, ndat):
            ran = np.random.randint(1, ndat)
            for z in range(0, 6):
                trsubset[y][z] = total[z][ran]
                gr.append(gross[ran])
        featsubset = np.random.choice(5, mtry, replace = False)
        decisiontree(mdepth, trsubset, featsubset)

def main():
    randomforest(1, 3, 2)

#representation of tree as a decisionnode class;
#referenced "Programming Collective Intelligence" by Toby Segaran
class treenode:
    def __init__(self, col=-1, val=None, res=None, tnode=None, fnode=None):
        self.col = col
        self.val = val
        self.res = res
        self.tnode = tnode
        self.fnode = fnode

def divideset(rows, column, value):
    splitfn = lambda row:row[column] >= value
    set1 = [row for row in rows if splitfn(row)]
    set2 = [row for row in rows if not splitfn(row)]
    return (set1, set2)

# Gini impurity tells us the probability of a mistake in categorizing that item.
def giniimpurity(lst):
    total = len(lst)
    counts = {}
    for dat in lst:
        last = dat[len(dat) - 1]
        if last not in counts:
            counts[last] = 0
        counts[last] += 1
    impurity = 0
    for j in counts:
        f1 = float(counts[j]) / total
        for k in counts:
            if j == k : continue
            f2 = float(counts[k]) / total
            impurity += (f1 * f2)
    return impurity

# Create counts of possible results (the last column of
# each row is the result)
def uniquecounts(rows):
    results={}
    for row in rows:
        # The result is the last column
        r=row[len(row)-1]
        if r not in results: results[r]=0
        results[r]+=1
    return results

if __name__ == "__main__":
    main()

