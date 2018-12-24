import pandas as pd
import feature_engineering
from sklearn.linear_model import LinearRegression
import numpy as np
import csv
import data_visual

pd.set_option('display.expand_frame_repr', False)

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

# print(list(test_df))
data_visual.show_all_instances(train_df, "LandSlope")

# removing extreme records.

print(list(train_df))
train_df = train_df.drop(train_df[train_df.total_area > 8000].index)

#print(train_df)
train_df = train_df.drop(train_df[train_df.BsmtGrade > 45000].index)
train_df = train_df.drop(train_df[train_df.externy_grade > 9000].index)
train_df = train_df.drop(train_df[train_df.total_area > 8000].index)

# get target column
target = train_df["SalePrice"]

# removing target column from train DataFrame.
train_df.drop(['SalePrice'], axis=1, inplace=True)

# fixing value dieffrences after one-hot encoding.
feature_engineering.add_missing_dummy_columns(train_df, test_df)

# train model

linereg = LinearRegression()
linereg.fit(train_df, target)

train_L = list(train_df)
test_L = list(test_df)

prediction = linereg.predict(test_df)


with open(prediction_path, 'w', newline='') as test:
    fieldnames = ['Id', 'SalePrice']
    writer = csv.DictWriter(test, fieldnames=fieldnames)

    writer.writeheader()

    i = 0
    for price in prediction:
        writer.writerow({'Id': test_id[i], 'SalePrice' : prediction[i]})
        i = i + 1
