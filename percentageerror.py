import csv
import numpy as np
import randomforest

gross = []

csv_filename = 'parse/1500movies_with_gross.csv'


with open(csv_filename, 'r') as csv_fh:
    reader = csv.reader(csv_fh)

    # Skip the header line
    next(reader, None)

    # Loop over the file by rows and fill in arrays for features
    for row in reader:
        gross.append(float(row[6]))
 
# Store the data as one dimensional numpy array    
gross = np.array(gross)

#print(np.argmax(gross))
def error (test, expected) :
    (test != expected).sum()/float(expected.size)
    return error 
    
def main():
    print (error(randomforest.gross, gross))
    
if __name__ == "__main__":
    main()
    
