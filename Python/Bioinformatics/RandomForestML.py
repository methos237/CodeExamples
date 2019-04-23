# ##################
# Assignment 4 - Machine Learning in Python
# Random Forest Prediction on the Need for Biopsy Based
# on Mammogram Data
#
# CSC 571 - Bioinformatics - Dr. Pranshanti Manda - Spring 2019 - UNCG
# @author James Knox Polk <jkpolk@uncg.edu>
# @author William Downs <wmdowns@uncg.edu>
#
# ###################


# Numpy is used for array manipulation
import numpy as np
# Matplot is used for graphs
import matplotlib.pyplot as plt
# Pandas is used for data manipulation
import pandas as pd
# Train_test_split is used to split dataset into Training and Testing
from sklearn.model_selection import train_test_split
# RandomForestClassifier is used to implement Random Forest Model
from sklearn.ensemble import RandomForestClassifier
import sklearn.metrics as skmt

plt.rcParams["figure.figsize"] = 20, 15


# Function to clean up the datafile and get rid of rows containing incomplete
# or out of range data.  This function is unique to the mammographic_masses data file.
def clean_data(file):
    df = pd.read_csv(file)

    # Clean out rows that are missing data
    df = df.replace('?', np.nan)
    df = df.dropna()

    # Convert all columns to int
    df = df.astype('int64')

    # Get rid of rows with bad data
    df = df.loc[
        (df.BIRADS > 0) & (df.BIRADS < 6) & (df.Age > 0) & (df.Shape > 0) & (df.Shape < 5)
        & (df.Margin > 0) & (df.Margin < 6) & (df.Density > 0)
        & (df.Density < 5)].reset_index(drop=True)

    # We will use the BI-RADS column as our baseline predictor.  Since the current values currently range
    # from 1 to 5, we will need to decide a demarcation between benin and cancerous.  Based on the criteria
    # for BI-RAD scores found at:
    # https://www.cancer.org/cancer/breast-cancer/screening-tests-and-early-detection/mammograms/understanding-your-mammogram-report.html)
    # scores above 3 should have a biopsy follow-up.
    # We will set scores between 1 and 3 as 0(benign) and >3 as 1(malignant)
    df['BIRADS'] = np.where(df['BIRADS'].between(1, 3), 0, df['BIRADS'])
    df['BIRADS'] = np.where(df['BIRADS'] > 3, 1, df['BIRADS'])

    # Descriptive statistics for each column
    print('\n\n\nDescriptive Statistics by Column:\n\n')
    print(df.describe())
    print('___________________________________________________________\n')
    # print(features.head(200))
    return df


# Function to split the data set into training and testing and run
# predictive model (Random Forest).  This function is reusable.
def data_convert(file, baseline, target, testsize, trees, rand_seed):
    # Get the cleaned data file
    ds = clean_data(file)

    # Chose the target attribute and move it outside of the data set
    target_label = np.array(ds[target])
    ds = ds.drop(target, axis=1)
    ds_list = list(ds.columns)
    ds = np.array(ds)

    # Split the data into training and testing sets
    train_ds, test_ds, train_target_labels, test_target_labels = train_test_split(ds, target_label,
                                                                                  test_size=testsize,
                                                                                  random_state=rand_seed)

    # Instantiate model with 2500 decision trees
    rf = RandomForestClassifier(n_estimators=trees, random_state=rand_seed)

    # Extract important features, leaving out the baseline measurement
    important_indices = [ds_list.index('Age'), ds_list.index('Shape'), ds_list.index('Margin'),
                         ds_list.index('Density')]
    train_important = train_ds[:, important_indices]
    test_important = test_ds[:, important_indices]

    # Show the way the data set has been split
    train_cases = train_important.shape
    testing_cases = test_important.shape
    print('Training Data Set Cases:', train_cases[0])
    print('Training Data Set Attributes:', train_cases[1])
    print('Testing Data Set Cases:', testing_cases[0])
    print('Testing Data Set Attributes:', testing_cases[1])
    print('___________________________________________________________\n')

    # Train the model on training data
    print('Running Model...')

    rf.fit(train_important, train_target_labels)
    print('___________________________________________________________\n')

    # Use the forest's predict method on the test data
    predictions = rf.predict(test_important)

    # Calculate and display the Testing and Baseline Mean Absolute Errors
    # The baseline predictions are based on the chosen baseline column
    baseline_preds = test_ds[:, ds_list.index(baseline)]

    baseline_mae = skmt.mean_absolute_error(test_target_labels, baseline_preds)
    testing_mae = skmt.mean_absolute_error(test_target_labels, predictions)
    print('Baseline Mean Absolute Error:\t', baseline_mae)
    print('Testing Mean Absolute Error:\t', testing_mae)
    print('Percent Change in Error:\t\t', round(((testing_mae / baseline_mae) * 100) - 100, 3), '%')
    print('___________________________________________________________\n')

    # Calculate and display accuracy of baseline and testing model
    baseline_acc = round(skmt.accuracy_score(test_target_labels, baseline_preds) * 100, 3)
    testing_acc = round(skmt.accuracy_score(test_target_labels, predictions) * 100, 3)
    print('Baseline Accuracy:\t\t\t\t', baseline_acc, '%')
    print('Testing Model Accuracy:\t\t\t', testing_acc, '%')
    print('Percent Change in Accuracy:\t\t', round(((testing_acc / baseline_acc) * 100) - 100, 3), '%')
    print('___________________________________________________________\n')

    # Calculate and display Confusion Matrix
    c_matrix = skmt.confusion_matrix(test_target_labels, predictions)
    print('Confusion Matrix Values')
    print('Total Testing Cases:', testing_cases[0])
    print('True Negatives:', c_matrix[0][0])
    print('False Positives (Type I Errors):', c_matrix[0][1])
    print('False Negatives (Type II Errors):', c_matrix[1][0])
    print('True Positives:', c_matrix[1][1])

    # #################ACCURACY###########################

    n = 1

    ind = np.arange(n)  # the x locations for the groups
    width = .35  # the width of the bars: can also be len(x) sequence

    p1 = plt.bar(ind, testing_acc, width)
    p2 = plt.bar(ind + width, baseline_acc, width)

    plt.ylabel('%')
    plt.title('increased accuracy over baseline')
    plt.xlabel('Accuracy')
    plt.yticks(np.arange(0, 100, 10))
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False,  # ticks along the top edge are off
        labelbottom=False)
    plt.legend((p1[0], p2[0]), ('Testing', 'BaseLine'))

    plt.show()

    # ####################confusion pie chart############################
    # help from examples in matplotlib api
    labels = 'True Negatives', 'True Positive', 'False Negatives', 'False positives'
    sizes = [c_matrix[0][0], c_matrix[1][1], c_matrix[1][0], c_matrix[0][1]]

    fig1, ax1 = plt.subplots()

    # plot the pie chart
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False)
    plt.title('Confusion Matrix Results')
    plt.show()


# Data file from https://archive.ics.uci.edu/ml/datasets/Mammographic+Mass
# File modified to provide headers only
data = 'mammographic_masses.csv'
data_convert(data, 'BIRADS', 'Severity', 0.33, 2500, 54)
