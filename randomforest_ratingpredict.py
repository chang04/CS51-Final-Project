# Implementation of Random Forest Algorithm:
# Referenced "Programming Collective Intelligence" by Toby Segaran for
# general direction

import csv
import numpy as np
import scipy as sp
import pylab as pl

csv_filename = 'parse/1500movies(train).csv'

budget = []
genre = []
mpaa = []
runtime = []
rating = []
gross = []
ndat = 1500
odat = 500
ncol = 6
trsubset = np.zeros((ndat, ncol))

# Loop over the data set
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
total = [budget, genre, mpaa, runtime, gross, rating]
budget = np.array(budget)
genre = np.array(genre)
mpaa = np.array(mpaa)
runtime = np.array(runtime)
rating = np.array(rating)
gross = np.array(gross)

# Create individual decision tree with the maximum depth md
#and the given subset of data and features
def decisiontree(md, dat, feature):
    # md : maximum depth of the tree
    # dat : data to put through the tree
    # feature : feature to split the data by in the nodes

    # Recursive function for constructing a decision tree
    def build(data, i):

        print("ITERATION: " + str(i))
        # optimal values to keep track of
        opt_infogain = 0.
        opt_cond = None
        opt_split = None
        var = variance(data)

        if len(data) == 0:
            return treenode()

        debugint = 0

        for x in feature:
            print("loop = " + str(debugint))
            debugint += 1
            tempdat = {}

            for film in data:
                tempdat[film[x]] = 0

            print("number of unique vals in col: " + str(len(tempdat)))

            for val in tempdat:
                (d1, d2) = binsplit(data, x, val)
                p = float(len(d1)) / len(data)
                infogain = var - (p*variance(d1) + (1-p)*variance(d2))

                if infogain > opt_infogain and len(d1) > 0 and len(d2) > 0:
                    opt_infogain = infogain
                    opt_cond = (x, val)
                    opt_split = (d1, d2)

        if opt_infogain > 0 and i < md:
            return treenode(col = opt_cond[0], val = opt_cond[1], tnode = build(opt_split[0], i + 1), fnode = build(opt_split[1], i + 1))
        else:
            return treenode(res = count(data))

    # Train the tree
    tree = build(dat, 0)
    printtree(tree)

    # Use the trained tree to predict movie ratings
    prediction = []
    obudget = []
    ogenre = []
    ompaa = []
    oruntime = []
    ogross = []

    test_filename = 'parse/500movies(testvalidation).csv'
    with open(test_filename, 'r') as csv_fh:

        reader = csv.reader(csv_fh)

        # Skip the header line
        next(reader, None)

        # Loop over the file by rows and fill in arrays for features
        for row in reader:
            obudget.append(float(row[1]))
            ogenre.append(float(row[2]))
            ompaa.append(float(row[3]))
            oruntime.append(float(row[4]))
            ogross.append(float(row[6]))

    for x in range(0, odat):
        prediction.append(predict([obudget[x], ogenre[x], ompaa[x], oruntime[x], ogross[x]], tree))
    prediction = np.array(prediction)
    return prediction

# Construct a random forest by aggregating B decision trees with
# Boostrapped data subset and random selection without replacement
# of the features
def randomforest(B, mtry, mdepth):
    # B : number of trees
    # mtry : number of subset of features used for individual decision trees
    # mdepth : maximum depth of decision trees

    summ = 0

    # Aggregate and average the inidividual tree's regression prediction
    for x in range(1, B + 1):
        for y in range(0, ndat):
            ran = np.random.randint(1, ndat)
            for z in range(0, 6):
                trsubset[y][z] = total[z][ran]

        featsubset = np.random.choice(5, mtry, replace = False)
        summ += decisiontree(mdepth, trsubset, featsubset)

    prediction = summ / B
    return prediction

# Main function
def main():

    ntree = input("Enter the number of trees of the random forest: ")
    mtry = input("Enter the number of features (less than or equal to 5): ")
    mdepth = input("Enter the maximum depth of the decision tree: ")

    prediction = randomforest(ntree, mtry, mdepth)
    output = 'Prediction/predictions_500.csv'

    # Write the prediction as a csv file
    with open(output, "w+") as f:
        f.write("Prediction\n")

        for i in prediction:
            f.write("%.2f\n" % i)


# Representation of tree as a decisionnode class;
class treenode:
    def __init__(self, col=-1, val=None, res=None, tnode=None, fnode=None):
        self.col = col
        self.val = val
        self.res = res
        self.tnode = tnode
        self.fnode = fnode

# A binary split of the data based on the value of val
def binsplit(data, col, val):
    # data : data to split
    # col : the column (feature) of the data to split by the value of
    # val : the value that determines the binary split

    splitfn = lambda row:row[col] >= val
    d1 = [row for row in data if splitfn(row)]
    d2 = [row for row in data if not splitfn(row)]
    return (d1, d2)

# Variance of the data
def variance(data):
    gross = []
    if len(data) == 0:
        return 0
    for row in data:
        gross.append(float(row[len(row) - 1]))
    variance = sum([(i - (sum(gross)/len(gross)))**2 for i in gross])/len(gross)
    return variance

# Count (unique) number of data
def count(data):
    count = {}
    for row in data:
        last = row[len(row) - 1]
        if last not in count:
            count[last] = 0
        count[last] += 1
    return count

# Print a rough structure of the tree
def printtree(tree, indent=''):
    # If the terminal node, print res
    if tree.res!=None:
        print str(tree.res)
    else:
        print str(tree.col)+':'+str(tree.val)+'? '
        print indent+'T->',
        printtree(tree.tnode,indent+'  ')
        print indent+'F->',
        printtree(tree.fnode,indent+'  ')

# Given an input, follow the tree and average the values of resulting res
def predict(inp, tree):
    # inp : input features of a film to predict the ratings of
    # the decision tree to base the decision (prediction) on

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
