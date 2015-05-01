import csv
import numpy as np
import randomforest

gross = []
gross1 = []

csv_filename = 'parse/500movies_with_gross.csv'
csv_filename1 = 'Prediction/predictions_500.csv'

with open(csv_filename, 'r') as csv_fh:
    reader = csv.reader(csv_fh)

    # Skip the header line
    next(reader, None)

    # Loop over the file by rows and fill in arrays for features
    for row in reader:
        gross.append(float(row[5]))

gross = np.array(gross)

with open(csv_filename1, 'r') as csv_fh1:
    reader1 = csv.reader(csv_fh1)

    # Skip the header line
    next(reader1, None)

    # Loop over the file by rows and fill in arrays for features
    for row in reader1:
        gross1.append(float(row[0]))

# Store the data as one dimensional numpy array
gross1 = np.array(gross1)


print (gross)
print (gross1)

print (abs(gross - gross1))
print(( abs(gross - gross1).sum() ) / 500)
#def error (test, expected) :
    #(test != expected).sum()/float(expected.size)
    #return error

#def main():
    #print (error(randomforest.gross, gross))

#if __name__ == "__main__":
    #main()

