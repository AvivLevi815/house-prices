import numpy as np


# mission specific data engineering.
def prepare_data(df):

    """
    Dealing with missing values - for all the features that I use here, if there is a null value
    it might be meaningful - not just denoting there is nothing to say of the feature.
    i.e. null for pool means "no pool".
    """

    df["PoolQC"] = df["PoolQC"].replace(np.nan, 0, regex=True)
    df["LotFrontage"] = df["LotFrontage"].replace(np.nan, 0, regex=True)
    df["LotArea"] = df["LotFrontage"].replace(np.nan, 0, regex=True)
    df["BsmtExposure"] = df["BsmtExposure"].replace(np.nan, 0, regex=True)

    # most common for all else :
    #df.mode - retunrns the most frequent value.

    df = df.replace(np.nan, df.mode().iloc[0])

    """
    Dictionary mapping - 
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

    Alley_mapping = {'Pave': 2, 'Grvl' : 1, 'NA': 0}
    df["Alley"] = df.replace({'Alley': Alley_mapping})["Alley"]

    Fence_mapping = {'GdPrv': 3, 'Good': 3, 'MnPrv': 2,
                     'GdWo' : 1, 'MnWw': 1,'NA': 0}

    df["Fence"] = df.replace({'Fence': Fence_mapping})["Fence"]

    posOS_mapping = {'Artery': 0, 'Feedr': 0, 'Norm': 0,
                     'RRNn': 0, 'RRAn': 0, 'PosN': 1,
                     'PosA': 2, 'RRNe': 0, 'RRAe': 0}

    df["posOS"] = df.replace({'Condition1': posOS_mapping})["Condition1"]

    nearEWR_mapping = {'Artery': 0, 'Feedr': 0, 'Norm': 0,
                       'RRNn': 0, 'RRAn': 0, 'PosN': 0,
                       'PosA': 0, 'RRNe': 1, 'RRAe': 2}

    df["nearEWR"] = df.replace({'Condition1': nearEWR_mapping})["Condition1"]

    Functional_mapping = {'Typ': 3, 'Min1': 2, 'Min2': 2,
                          'Mod': 2, 'Maj1': 1, 'Maj2': 1,
                          'Sev': 1, 'Sal': 1}

    df["Functional"] = df.replace({'Functional': Functional_mapping})["Functional"]

    df["age"] = df["YrSold"] - df["YearBuilt"]

    BsmtFinType1_mapping = {'GLQ': 3,  'ALQ': 2, 'BLQ': 2,
                            'Rec': 1,  'LwQ': 1, 'Unf': 1,
                            'NA' : 0}

    BsmtFinType2_mapping = BsmtFinType1_mapping

    df["BsmtFinType1"] = df.replace({'BsmtFinType1': BsmtFinType1_mapping})["BsmtFinType1"]
    df["BsmtFinType2"] = df.replace({'BsmtFinType2': BsmtFinType2_mapping})["BsmtFinType2"]

    df["basement_finish_grade"] = df["BsmtFinType1"] * df["BsmtFinSF1"] + \
                                  df["BsmtFinType2"] * df["BsmtFinSF2"] - df["BsmtUnfSF"]


    BsmtCond_mapping = {'Ex': 3, 'Gd': 2, 'TA': 1,
                        'Fa': 1, 'Po': 1, 'NA': 0}

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

    FireplaceQu_mapping = {'Ex': 3, 'Gd': 2, 'TA': 2,
                           'Fa': 1, 'Po': 1, 'NA': 0}

    df["FireplaceQu"] = df.replace({'FireplaceQu': FireplaceQu_mapping})["FireplaceQu"]

    LandContour_mapping = {'Lvl': 3, 'Bnk': 2, 'HLS': 1, 'Low': 1}
    df["LandContour"] = df.replace({'LandContour' : LandContour_mapping})["LandContour"]

    df["fire_places_grade"] = df["Fireplaces"] * df['FireplaceQu']

    PoolQC_mapping = {'Ex': 3, 'Gd': 2, 'TA': 1,
                      'Fa': 1, 'NA': 0}

    df["PoolQC_grade"] = df.replace({'PoolQC': PoolQC_mapping})["PoolQC"] * \
                               df['PoolArea']

    df["Cond_Qual"] = df["OverallQual"] * df["OverallCond"]

    df["Porches_area"] = df["EnclosedPorch"] + df["3SsnPorch"] + \
                               df["ScreenPorch"] + df["OpenPorchSF"]

    Street_mapping = {'Pave': 2, 'Grvl': 1, 'NA': 0}
    df["Street"] = df.replace({'Street': Street_mapping})["Street"]

    PavedDrive_mapping = {'Y': 2, 'P': 1, 'N': 0}
    df["PavedDrive"] = df.replace({'PavedDrive': PavedDrive_mapping})["PavedDrive"]

    HeatingQC_mapping = {'Ex': 3, 'Gd': 2, 'TA': 1,
                         'Fa': 1, 'Po': 1, 'NA': 0}
    df["HeatingQC"] = df.replace({'HeatingQC': HeatingQC_mapping})["HeatingQC"]

    GarageFinish_mapping = {'Fin': 3, 'RFn': 2, 'Unf': 1, 'NA': 0}
    df["GarageFinish"] = df.replace({'GarageFinish': GarageFinish_mapping})["GarageFinish"]

    GarageQual_mapping = {'Ex': 3, 'Gd': 2, 'TA': 1,
                          'Fa': 1, 'Po': 1, 'NA': 0}
    df["GarageQual"] = df.replace({'GarageQual': GarageQual_mapping})["GarageQual"]

    GarageCond_mapping = {'Ex': 3, 'Gd': 2, 'TA': 1,
                          'Fa': 1, 'Po': 1, 'NA': 0}
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
                   'ExterCond', 'BsmtExposure', 'BsmtFinSF1', 'BsmtUnfSF',
                   'YearBuilt', 'MSSubClass', 'LotFrontage', 'LotArea',
                   'LotShape', 'Utilities', 'LotConfig', 'BedroomAbvGr',
                   'CentralAir', 'LowQualFinSF', 'BsmtFullBath', 'BsmtHalfBath',
                   'Exterior1st', 'Exterior2nd', 'Electrical', 'GarageCars',
                   'OpenPorchSF', 'MiscFeature', 'MoSold', 'SaleType', 'SaleCondition',
                   'KitchenQual', 'KitchenAbvGr', 'Fireplaces', 'FireplaceQu',
                   'MasVnrType',
                   'Foundation', 'RoofMatl', 'BldgType', 'RoofStyle',
                   'MSZoning', 'HouseStyle', 'Heating', 'GarageType',
                   'Neighborhood',
                   'WoodDeckSF', 'Condition1', 'Condition2', 'FullBath', 'HalfBath'], axis=1, inplace=True)
    return df
