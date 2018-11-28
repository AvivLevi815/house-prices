import pandas as pd
import scipy as sc


train_df = pd.read_csv('C:/Users/Owner/Desktop/house_pricing_regression/train.csv')
test_df = pd.read_csv('C:/Users/Owner/Desktop/house_pricing_regression/test.csv')

"""
train_df.loc[train_df.SalePrice <= 34900, 1] = 0
train_df.loc[train_df.female == 'female', 'female'] = 1
"""

# dropping unnesesery columns
train_df.drop(['Id', 'LotFrontage', 'LotArea', 'Street', 'Alley',
               'LotShape', 'LandContour', 'Utilities', 'LotConfig',
               'Exterior1st', 'Exterior2nd', 'Electrical', 'GarageCars',
               'WoodDeckSF'], axis=1, inplace=True)

test_df.drop(['Id', 'LotFrontage', 'LotArea', 'Street', 'Alley',
              'LotShape', 'LandContour', 'Utilities', 'LotConfig',
              'Exterior1st', 'Exterior2nd', 'Electrical', 'GarageCars',
              'WoodDeckSF'], axis=1, inplace=True)
print(train_df)