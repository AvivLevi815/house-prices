import pandas as pd
import feature_engineering


train_df = pd.read_csv('C:/Users/Owner/Desktop/house_pricing_regression/train.csv')
test_df = pd.read_csv('C:/Users/Owner/Desktop/house_pricing_regression/test.csv')

feature_engineering.feature_to_boolean_tuple(train_df, 'MSZoning', 'Zone')

train_df.drop(['Id', 'MSSubClass', 'LotFrontage', 'LotArea', 'Street', 'Alley',
               'LotShape', 'LandContour', 'Utilities', 'LotConfig',
               'Exterior1st', 'Exterior2nd', 'Electrical', 'GarageCars',
               'WoodDeckSF'], axis=1, inplace=True)

test_df.drop(['Id', 'MSSubClass', 'LotFrontage', 'LotArea', 'Street', 'Alley',
              'LotShape', 'LandContour', 'Utilities', 'LotConfig',
              'Exterior1st', 'Exterior2nd', 'Electrical', 'GarageCars',
              'WoodDeckSF'], axis=1, inplace=True)

print(train_df)



