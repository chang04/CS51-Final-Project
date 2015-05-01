import csv
import numpy as np
import randomforest

actualrating = []
prediction = []

csv_filename = 'parse/500movies_with_gross.csv'
csv_filename1 = 'predictions_500.csv'

with open(csv_filename, 'r') as csv_fh:
    reader = csv.reader(csv_fh)

    # Skip the header line
    next(reader, None)

    # Loop over the file by rows and fill in arrays for features
    for row in reader:
        actualrating.append(float(row[5]))

actualrating = np.array(actualrating)

with open(csv_filename1, 'r') as csv_fh1:
    reader1 = csv.reader(csv_fh1)

    # Skip the header line
    next(reader1, None)

    # Loop over the file by rows and fill in arrays for features
    for row in reader1:
        prediction.append(float(row[0]))

# Store the data as one dimensional numpy array
prediction = np.array(prediction)

print (actualrating)
print (prediction)

# prints the percentage error of our prediction
print (abs(actualrating - prediction))
print(( abs(actualrating - prediction).sum() ) / 500)

