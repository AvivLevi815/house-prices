import pandas as pd
import feature_engineering
from sklearn.linear_model import LinearRegression
import numpy as np
import csv
from scipy.stats import skew
pd.options.display.max_rows = 9999

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
# data_visual.show_all_instances(train_df, "Kitchens")

# removing extreme records.

train_df = train_df.drop(train_df[train_df.total_area > 8000].index)
train_df = train_df.drop(train_df[train_df.externy_grade > 9000].index)
train_df = train_df.drop(train_df[train_df.total_area > 8000].index)
train_df = train_df.drop(train_df[train_df.MiscVal > 8000].index)
train_df = train_df.drop(train_df[train_df.basement_finish_grade > 30000].index)
train_df = train_df.drop(train_df[train_df.BsmtGrade > 80000].index)
train_df = train_df.drop(train_df[train_df.fire_places_grade >= 12].index)
train_df = train_df.drop(train_df[train_df.Garage_Grade > 10000].index)

# get target column
target = np.log1p(train_df["SalePrice"])

# get all numerical (non-object features)
train_numerical_features = train_df.select_dtypes(exclude = ["object"]).columns
train_num = train_df[train_numerical_features]

test_numerical_features = test_df.select_dtypes(exclude = ["object"]).columns
test_num = test_df[test_numerical_features]


# get all categoricall (object features)
train_categorical_features = train_df.select_dtypes(include = ["object"]).columns
train_cat = train_df[train_categorical_features]

test_categorical_features = test_df.select_dtypes(include = ["object"]).columns
test_cat = test_df[test_categorical_features]

# Create correlation matrix
corr_matrix = train_num.corr().SalePrice.abs()

#drop low correlated features
to_drop = [feature for feature, val in corr_matrix.items() if corr_matrix[feature] < 0.5]

# removing target column from train DataFrame.
train_num.drop(['SalePrice'], axis=1, inplace=True)

# Drop features
train_num.drop(to_drop, axis=1, inplace=True)
test_num.drop(to_drop, axis=1, inplace=True)

# re-combine numerical and categorical features
train_df = pd.concat([train_num, train_cat], axis = 1)
test_df = pd.concat([test_num, test_cat], axis = 1)

# one-hot encoding + fixing value dieffrences after one-hot encoding.
train_df = pd.get_dummies(train_df)
test_df = pd.get_dummies(test_df)

feature_engineering.add_missing_dummy_columns(train_df, test_df)

# train model
linereg = LinearRegression()
linereg.fit(train_df, target)

train_L = list(train_df)
test_L = list(test_df)

# print(train_L)
# print(test_L)

prediction = np.expm1(linereg.predict(test_df))


with open(prediction_path, 'w', newline='') as test:
    fieldnames = ['Id', 'SalePrice']
    writer = csv.DictWriter(test, fieldnames=fieldnames)

    writer.writeheader()

    i = 0
    for price in prediction:
        writer.writerow({'Id': test_id[i], 'SalePrice' : prediction[i]})
        i = i + 1
