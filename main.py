import pandas as pd
import feature_engineering
from sklearn.linear_model import LinearRegression
import numpy as np
pd.set_option('display.expand_frame_repr', False)

# get train and test data sets
train_df = pd.read_csv('C:/Users/Owner/Desktop/house_pricing_regression/train.csv')
test_df = pd.read_csv('C:/Users/Owner/Desktop/house_pricing_regression/test.csv')

# get target column
target = train_df["SalePrice"]

# removing target column from train DataFrame.
train_df.drop(['SalePrice'], axis=1, inplace=True)

# data preparation

train_df = feature_engineering.prepare_data(train_df)
test_df = feature_engineering.prepare_data(test_df)

# replace NaN values with column mean

train_df = train_df.replace(np.nan, train_df.mean(), regex=True)
test_df = test_df.replace(np.nan, train_df.mean(), regex=True)


# train model

linereg = LinearRegression()
linereg.fit(train_df, target)


