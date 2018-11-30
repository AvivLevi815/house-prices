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

