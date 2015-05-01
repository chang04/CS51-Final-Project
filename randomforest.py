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

    reader = csv.reader(csv_fh)

    # Skip the header line
    next(reader, None)

    # Loop over the file by rows and fill in arrays for features
    for row in reader:
        budget.append(float(row[1]))
        genre.append(float(row[2]))
        mpaa.append(float(row[3]))
        runtime.append(float(row[4]))
        rating.append(float(row[5]))
        gross.append(float(row[6]))

# Store the data as numpy array
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

# Create individual decision tree with the maximum depth md
#and the given subset of data and features
def decisiontree(md, dat, feature):
    #treefeat = np.zeros((ndat, 3))
    #for x in range(0, ndat):
    #    for y in range(0, 3):
    #        treefeat[x][y] = dat[x][feature[y]]
    #print(treefeat)

    # Recursive function for constructing a decision tree
    def build(data, i):
        print("ininininininininiinininininininininininininininini")
        # optimal values to keep track of
        opt_infogain = 0.
        opt_cond = None
        opt_split = None
        var = variance(data)
        inn = 0
        if len(data) == 0:
            return treenode()

        for x in feature:
            print(feature)
            print(x)
            print("int = " + str(inn))
            inn+=1
            tempdat = {}
            for film in data:
                tempdat[film[x]] = 0
            print(len(tempdat))
            for val in tempdat:
                (d1, d2) = binsplit(data, x, val)
                p = float(len(d1)) / len(data)
                #print(p)
                gain = var - p*variance(d1) - (1-p)*variance(d2)
                if gain > opt_infogain and len(d1) > 0 and len(d2) > 0:
                    opt_infogain = gain
                    opt_cond = (x, val)
                    opt_split = (d1, d2)
        if opt_infogain > 0 and i < md:
            print("aaaaaaaaaaaaaaannnnnnnnnnnnnnnnnddddddddddd innnnnnnnnnt is: " + str(i))
            return treenode(col = opt_cond[0], val = opt_cond[1], tnode = build(opt_split[0], i+1), fnode = build(opt_split[1], i+1))
        else:
            return treenode(res = count(data))
    tree = build(dat, 0)
    #printtree(tree)
    return predict([25000000,2,3,104,6.8], tree)

# Construct a random forest by aggregating B decision trees with
# Boostrapped data subset and random selection without replacement
# of the features
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
    randomforest(1, 2, 5)

# Representation of tree as a decisionnode class;
# referenced "Programming Collective Intelligence" by Toby Segaran
class treenode:
    def __init__(self, col=-1, val=None, res=None, tnode=None, fnode=None):
        self.col = col
        self.val = val
        self.res = res
        self.tnode = tnode
        self.fnode = fnode

def binsplit(data, col, val):
    splitfn = lambda row:row[col] >= val
    d1 = [row for row in data if splitfn(row)]
    d2 = [row for row in data if not splitfn(row)]
    return (d1, d2)

def variance(data):
    gross = []
    if len(data) == 0:
        return 0
    for row in data:
        gross.append(float(row[len(row) - 1]))
    variance = sum([(i - (sum(gross)/len(gross)))**2 for i in gross])/len(gross)
    return variance

def count(data):
    count = {}
    for row in data:
        last = row[len(row) - 1]
        if last not in count:
            count[last] = 0
        count[last] += 1
    return count

def printtree(tree,indent=''):
    # Is this a leaf node?
    if tree.res!=None:
        print str(tree.res)
    else:
        # Print the criteria
        print str(tree.col)+':'+str(tree.val)+'? '

        # Print the branches
        print indent+'T->',
        printtree(tree.tnode,indent+'  ')
        print indent+'F->',
        printtree(tree.fnode,indent+'  ')

def predict(inp, tree):
    if tree.res != None:
        summ = 0
        num = 0
        for key in tree.res:
            summ += key * tree.res[key]
            num += tree.res[key]
        return summ / num
    else:
        v = inp[tree.col]
        branch = None
        if v >= tree.val:
            branch = tree.tnode
        else:
            branch = tree.fnode
        return predict(inp, branch)

if __name__ == "__main__":
    main()

