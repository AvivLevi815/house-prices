import  pandas as pd


def add_missing_dummy_columns(train_df ,test_df):
    missing_cols = set( train_df ) - set( test_df.columns )
    for c in missing_cols:
        test_df[c] = 0


# mission specific data engineering.
def prepare_data(df):

    cols_to_transform = ['MSZoning', 'BldgType', 'Foundation',
                         'Neighborhood', 'HouseStyle', 'RoofStyle',
                         'RoofStyle', 'RoofMatl', 'MasVnrType', 'Fence',
                         'Heating', 'GarageType']
    df = pd.get_dummies(df, columns=cols_to_transform)
    """
    Dictonary mapping - 
    Features for which I know (or hope to know) the better or worse options.
    """
    LandSlope_mapping = {'Gtl': 3, 'Mod': 2, 'Sev': 1}
    df = df.replace({'LandSlope': LandSlope_mapping})

    Nstreet_mapping = {'Artery': 2, 'Feedr': 1, 'Norm': 0,
                       'RRNn': 0, 'RRAn': 0, 'PosN': 0,
                       'PosA': 0, 'RRNe': 0, 'RRAe': 0}

    # add a column "NearStreet" that holds mapping as in Nstreet_mapping,
    # not overriding original Condition1 column
    df["NearStreet"] = df.replace({'Condition1': Nstreet_mapping})["Condition1"]
    df["NearStreet2"] = df.replace({'Condition2': Nstreet_mapping})["Condition2"]

    NormalProx_mapping = {'Artery': 0, 'Feedr': 0, 'Norm': 1,
                          'RRNn': 0, 'RRAn': 0, 'PosN': 0,
                          'PosA': 0, 'RRNe': 0, 'RRAe': 0}

    df["NormalProx"] = df.replace({'Condition1': NormalProx_mapping})["Condition1"]
    df["NormalProx2"] = df.replace({'Condition2': NormalProx_mapping})["Condition2"]

    nearNSR_mapping = {'Artery': 0, 'Feedr': 0, 'Norm': 0,
                       'RRNn': 1, 'RRAn': 2, 'PosN': 0,
                       'PosA': 0, 'RRNe': 0, 'RRAe': 0}

    df["nearNSR"] = df.replace({'Condition1': nearNSR_mapping})["Condition1"]
    df["nearNSR2"] = df.replace({'Condition2': nearNSR_mapping})["Condition2"]

    posOS_mapping = {'Artery': 0, 'Feedr': 0, 'Norm': 0,
                     'RRNn': 0, 'RRAn': 0, 'PosN': 1,
                     'PosA': 2, 'RRNe': 0, 'RRAe': 0}

    df["posOS"] = df.replace({'Condition1': posOS_mapping})["Condition1"]
    df["posOS2"] = df.replace({'Condition2': posOS_mapping})["Condition2"]

    nearEWR_mapping = {'Artery': 0, 'Feedr': 0, 'Norm': 0,
                       'RRNn': 0, 'RRAn': 0, 'PosN': 0,
                       'PosA': 0, 'RRNe': 1, 'RRAe': 2}

    df["nearEWR"] = df.replace({'Condition1': nearEWR_mapping})["Condition1"]
    df["nearEWR2"] = df.replace({'Condition2': nearEWR_mapping})["Condition2"]

    Functional_mapping = {'Typ': 8, 'Min1': 7, 'Min2': 6,
                          'Mod': 5, 'Maj1': 4, 'Maj2': 3,
                          'Sev': 2, 'Sal': 1}

    df["Functional"] = df.replace({'Functional': Functional_mapping})["Functional"]

    df["age"] = df["YrSold"] - df["YearBuilt"]

    # df["roof"] = df["RoofStyle"]

    BsmtCond_mapping = {'Ex': 5, 'Gd': 4, 'TA': 3,
                        'Fa': 2, 'Po': 1, 'NA': 0}

    BsmtQual__mapping = BsmtCond_mapping

    df["BsmtGrade"] = df.replace({'BsmtCond': BsmtCond_mapping})["BsmtCond"] * \
                      df.replace({'BsmtQual': BsmtQual__mapping})["BsmtQual"] * \
                            df['TotalBsmtSF']


    ExterQual_mapping = BsmtCond_mapping
    df["ExterQual"] = df.replace({'ExterQual': ExterQual_mapping})["ExterQual"]

    ExterCond_mapping = ExterQual_mapping
    df["ExterCond"] = df.replace({'ExterCond': ExterCond_mapping})["ExterCond"]

    df["externy_grade"] = df['MasVnrArea'] * (df['ExterQual'] + df['ExterCond'])

    df["total_area"] = df['1stFlrSF'] + df['2ndFlrSF'] + df['GrLivArea']

    df["remod_age"] = df["YearRemodAdd"] - df["YearBuilt"]

    df["baths"] = df['FullBath'] + df['HalfBath']

    FireplaceQu_mapping = {'Ex': 5, 'Gd': 4, 'TA': 3,
                           'Fa': 2, 'Po': 1, 'NA': 0}

    df["FireplaceQu"] = df.replace({'FireplaceQu': FireplaceQu_mapping})["FireplaceQu"]

    df["fire_places_grade"] = df["Fireplaces"] * df['FireplaceQu']

    PoolQC_mapping = {'Ex': 4, 'Gd': 3, 'TA': 2,
                      'Fa': 1, 'NA': 0}

    df["PoolQC_grade"] = df.replace({'PoolQC': PoolQC_mapping})["PoolQC"] * \
                               df['PoolArea']

    df["Cond_Qual"] = df["OverallQual"] * df["OverallCond"]

    df["Porches_area"] = df["EnclosedPorch"] + df["3SsnPorch"] + \
                               df["ScreenPorch"] + df["OpenPorchSF"]

    PavedDrive_mapping = {'Y': 2, 'P': 1, 'N': 0}
    df["PavedDrive"] = df.replace({'PavedDrive': PavedDrive_mapping})["PavedDrive"]

    HeatingQC_mapping = {'Ex': 5, 'Gd': 4, 'TA': 3,
                         'Fa': 2, 'Po': 1, 'NA': 0}
    df["HeatingQC"] = df.replace({'HeatingQC': HeatingQC_mapping})["HeatingQC"]

    GarageFinish_mapping = {'Fin': 3, 'RFn': 2, 'Unf': 1, 'NA': 0}
    df["GarageFinish"] = df.replace({'GarageFinish': GarageFinish_mapping})["GarageFinish"]

    GarageQual_mapping = {'Ex': 5, 'Gd': 4, 'TA': 3,
                          'Fa': 2, 'Po': 1, 'NA': 0}
    df["GarageQual"] = df.replace({'GarageQual': GarageQual_mapping})["GarageQual"]

    GarageCond_mapping = {'Ex': 5, 'Gd': 4, 'TA': 3,
                          'Fa': 2, 'Po': 1, 'NA': 0}
    df["GarageCond"] = df.replace({'GarageCond': GarageCond_mapping})["GarageCond"]



    df["Garage_Grade"] = df["GarageArea"] *  (df["GarageCond"] +
                                              df["GarageQual"] +
                                              df["GarageFinish"])

    df["Garage_age"] = df["YrSold"] - df["GarageYrBlt"]

    KitchenQual_mapping = GarageCond_mapping
    df["KitchenQual"] = df.replace({'KitchenQual': KitchenQual_mapping})["KitchenQual"]

    df["Kitchens"] = df["KitchenQual"] * df["KitchenAbvGr"]

    # removing unwanted features and features I engineered into one.
    df.drop(['Id', 'GarageArea', 'GarageCond', 'GarageQual', 'GarageFinish',
                   'GarageYrBlt', "EnclosedPorch", "3SsnPorch", "ScreenPorch", "OverallCond",
                   'OverallQual', 'PoolArea', 'PoolQC', 'BsmtCond', 'TotalBsmtSF',
                   'BsmtQual', 'YearRemodAdd', 'BsmtFinType2', 'BsmtFinSF2',
                   '1stFlrSF', '2ndFlrSF', 'GrLivArea', 'YrSold','MasVnrArea','ExterQual',
                   'ExterCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinSF1', 'BsmtUnfSF',
                   'YearBuilt', 'MSSubClass', 'LotFrontage', 'LotArea', 'Street', 'Alley',
                   'LotShape', 'LandContour', 'Utilities', 'LotConfig', 'BedroomAbvGr',
                   'CentralAir', 'LowQualFinSF', 'BsmtFullBath', 'BsmtHalfBath',
                   'Exterior1st', 'Exterior2nd', 'Electrical', 'GarageCars',
                   'OpenPorchSF', 'MiscFeature', 'MoSold', 'SaleType', 'SaleCondition',
                   'KitchenQual', 'KitchenAbvGr', 'Fireplaces', 'FireplaceQu',
                   'WoodDeckSF', 'Condition1', 'Condition2', 'FullBath', 'HalfBath'], axis=1, inplace=True)
    return df
