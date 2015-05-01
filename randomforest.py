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

budget = np.array(budget)
genre = np.array(genre)
mpaa = np.array(mpaa)
runtime = np.array(runtime)
rating = np.array(rating)
gross = np.array(gross)

print(np.argmax(gross))
pl.plot(gross, rating, 'o', color = 'b')
pl.show()

#def decisiontree(data, feature):
    #use CART to create a decisiontree

def randomforest(B, mtry):
    for x in range(1, B):
        for y in range(0, ndat):
            ran = np.random.randint(1, ndat)
            trsubset[y][0] = budget[ran]
            trsubset[y][1] = genre[ran]
            trsubset[y][2] = mpaa[ran]
            trsubset[y][3] = runtime[ran]
            trsubset[y][4] = rating[ran]
            gr.append(gross[ran])
        featsubset = np.random.choice(5, mtry, replace = False)
        #decisiontree(trsubset, )

def main():
    randomforest(2, 3)
    print(trsubset)

if __name__ == "__main__":
    main()
