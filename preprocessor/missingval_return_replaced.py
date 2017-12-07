def missingval_return_replaced(missing_value_query, replacement_value, target_column_header, dataset):
    """
    Returns the inputted column with a version of itself that has its missing values replaced with the given value.
    NaN values will be replaced no matter which missing_value_query is entered, so in such caes, it can also be just
    an empty string (i.e., "").

    :param missing_value_query:
    :param replacement_value:
    :param target_column_header:
    :param dataset:
    :return:
    """

    #############################################################################################################

    from preprocessor.select_column import select_column

    selected_column = select_column(target_column_header, dataset)

    for i, each_row in enumerate(selected_column):
        # If row is a missing value or a NaN value (NaN values are never equal to themselves), replace it.
        if each_row == missing_value_query or each_row != each_row:
            selected_column[i] = replacement_value
    return selected_column