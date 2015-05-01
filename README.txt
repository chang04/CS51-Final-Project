# CS51-Final-Project
CS51 Final Project - Movie Ratings Predictor using Random Forests and Support Vector Regression Algorithm by Peter Chang, Zachry Bai, Dor Baruch, Ann Hwang

All of our code was written and executed with Python 2.7.9, and can be executed as such.
To run the programs, the numpy library must be installed, as well as the IMDbPY library.

To run the randomforest_ratingpredict.py, just execute "python randomforest_ratingpredict.py" in the terminal.
Then follow the instruction to input the number of trees, number of features (<6), and maximum depth of trees.
It will create the predictions_500.csv in the Prediction folder.
The accuracy (percentage) can be calculated by running percentageerror.py.

Our Neural Networks implementation works when trained on smaller sets with smaller inputs, but has difficulty converging when operating on larger inputs and data sets.
Because of this, we did not implement a command line interface; the code can still be executed in an IDE or python shell.

