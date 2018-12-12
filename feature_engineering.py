"""
the goal of this function is to convert a feature that I am interested in and have values that
I cannot sort by myselfe by effect (for example - what is better, Heating of type 1 or 2?)
into a tuple at the size of the feature possible values.

for example for feature "Example" that have the following possible values {red, white, blue}
and the data set { red, red, white }
the feature in the data set will be converted to:
[(1, 0, 0), (1, 0, 0), (0, 0, 1)]
"""
def feature_to_boolean_tuple(df, feature_name, new_name):
    tuple_list = [] #each tuple will represent an option
    feature_options = df[feature_name].unique()
    feature_options_length = len(feature_options)

    # creating a list the size of feature_options_length, all 0's
    list_to_be_tuple = [0 for i in range(feature_options_length)]

    for i in range(feature_options_length):
        list_to_be_tuple[i] = 1 # inserting 1 representing option number i
        tuple_list.append(tuple(list_to_be_tuple))
        list_to_be_tuple[i] = 0

    mapping = dict(zip(feature_options, tuple_list)) # dict from values to vectors
    df[new_name] = df[feature_name].map(mapping)
    df.drop([feature_name], axis=1, inplace=True)

# mission specific data engineering.
def prepare_data(df):
    df.drop(['MSZoning', 'BldgType', 'Foundation'
                , 'Neighborhood' , 'HouseStyle', 'RoofStyle'
                , 'RoofMatl' , 'MasVnrType', 'Fence'
                , 'Heating', 'GarageType' ], axis=1, inplace=True)

    # converting indecisive feature values into option vectors.
    # feature_to_boolean_tuple(df, 'MSZoning', 'MSZoningV')
    # feature_to_boolean_tuple(df, 'BldgType', 'BldgTypeV')
    # feature_to_boolean_tuple(df, 'Foundation', 'FoundationV')
    # feature_to_boolean_tuple(df, 'Neighborhood', 'NeighborhoodV')
    # feature_to_boolean_tuple(df, 'HouseStyle', 'HouseStyleV')
    # feature_to_boolean_tuple(df, 'RoofStyle', 'RoofStyleV')
    # feature_to_boolean_tuple(df, 'RoofMatl', 'RoofMatlV')
    # feature_to_boolean_tuple(df, 'MasVnrType', 'MasVnrTypeV')
    # feature_to_boolean_tuple(df, 'Fence', 'FenceV')
    # feature_to_boolean_tuple(df, 'Heating', 'HeatingV')
    # feature_to_boolean_tuple(df, 'GarageType', 'GarageTypeV')

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
