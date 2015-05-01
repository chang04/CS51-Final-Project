import csv
import numpy as np

actualrating = []
prediction = []

csv_filename = '../data/500movies(testvalidation).csv'
csv_filename1 = 'Prediction/predictions_500.csv'

with open(csv_filename, 'r') as csv_fh:
    reader = csv.reader(csv_fh)

    # Skip the header line
    next(reader, None)

    # Use row 5 in order to put in array of ratings
    for row in reader:
        actualrating.append(float(row[5]))

# Store the data as one dimensional numpy array
actualrating = np.array(actualrating)

with open(csv_filename1, 'r') as csv_fh1:
    reader1 = csv.reader(csv_fh1)

    # Skip the header line
    next(reader1, None)

    # The "rating" is already stored in the csv file
    for row in reader1:
        prediction.append(float(row[0]))

# Store the data as one dimensional numpy array
prediction = np.array(prediction)

# prints the percentage error of our prediction
print (abs(actualrating - prediction))
print(( abs(actualrating - prediction).sum() ) / 500)

