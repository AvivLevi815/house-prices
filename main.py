import pandas as pd
import feature_engineering
from sklearn.linear_model import LinearRegression
import numpy as np
import csv

train_path = 'C:/Users/Owner/Desktop/house_pricing_regression/train.csv'
test_path = 'C:/Users/Owner/Desktop/house_pricing_regression/test.csv'
prediction_path =  'C:/Users/Owner/Desktop/house_pricing_regression/submission.csv'

# get train and test data sets
train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)

# get test ID's
test_id = test_df["Id"]

# data preparation
train_df = feature_engineering.prepare_data(train_df)
test_df = feature_engineering.prepare_data(test_df)

# removing extreme records.
train_df = train_df.drop(train_df[train_df.total_area > 8000].index)
train_df = train_df.drop(train_df[train_df.externy_grade > 9000].index)
train_df = train_df.drop(train_df[train_df.total_area > 8000].index)
train_df = train_df.drop(train_df[train_df.MiscVal > 8000].index)
train_df = train_df.drop(train_df[train_df.basement_finish_grade > 30000].index)
train_df = train_df.drop(train_df[train_df.BsmtGrade > 80000].index)
train_df = train_df.drop(train_df[train_df.fire_places_grade >= 12].index)
train_df = train_df.drop(train_df[train_df.Garage_Grade > 10000].index)

# Create correlation matrix
corr_matrix = train_df.corr().SalePrice.abs()

#drop low correlated features
to_drop = [feature for feature, val in corr_matrix.items() if corr_matrix[feature] < 0.5]

# Drop low correlated features
train_df.drop(to_drop, axis=1, inplace=True)
test_df.drop(to_drop, axis=1, inplace=True)

# get target column
target = np.log1p(train_df["SalePrice"])

# removing target column from train DataFrame.
train_df.drop(['SalePrice'], axis=1, inplace=True)

# train model
linereg = LinearRegression()
linereg.fit(train_df, target)

#predict
prediction = np.expm1(linereg.predict(test_df))

#output to excel csv
with open(prediction_path, 'w', newline='') as test:
    fieldnames = ['Id', 'SalePrice']
    writer = csv.DictWriter(test, fieldnames=fieldnames)

    writer.writeheader()

    i = 0
    for price in prediction:
        writer.writerow({'Id': test_id[i], 'SalePrice' : prediction[i]})
        i = i + 1
