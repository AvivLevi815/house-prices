import pandas as pd
import feature_engineering

# get train and test data sets
train_df = pd.read_csv('C:/Users/Owner/Desktop/house_pricing_regression/train.csv')
test_df = pd.read_csv('C:/Users/Owner/Desktop/house_pricing_regression/test.csv')

# data preparation
train_df = feature_engineering.prepare_data(train_df)
test_df = feature_engineering.prepare_data(test_df)

