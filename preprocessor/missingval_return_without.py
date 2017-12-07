def missingval_return_without(missing_value_query, target_column_header, dataset):
    """
    Returns the inputted column with a version of itself that has its missing values removed.
    It should be noted that this new column will be shorter after removal of missing values.

    If the missing value is NaN (and  not 'NaN'), missing_value_query can take any value.

    :param missing_value_query:
    :param target_column_header:
    :param dataset:
    :return:
    """

    #############################################################################################################

    from preprocessor.select_column import select_column

    selected_column = select_column(target_column_header, dataset)

    transformed_column = []
    for i, each_row in enumerate(selected_column):
        # If row is not a missing value or a NaN value (NaN values are never equal to themselves), append it to new column
        if each_row != missing_value_query and each_row == each_row:
            transformed_column.append(selected_column[i])  # append it to the new list
    return transformed_column