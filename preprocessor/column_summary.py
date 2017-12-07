from preprocessor.select_column import select_column


def column_summary(column_name, dataset, print_values=False):
    """
    Return (or print) the number of occurences for each value in the specified column in a dataset.

    :param column_name: (str) Target column name from the dateset headers.
    :param dataset: (var) Variable that holds the dataset. Headers must be included.
    :param print_values: (bool) Specifies whether to return or print variables

    :returns:
        - If print_values == False (default) --> A dictionary object
        - If print_values == True            --> *Line by line* output to console (and no dictionary object returns)

    :examples:
        >>> my_data = [["id", "number"],["John", 0], ["John", 12], ["Someone else", 7]]
        >>> column_summary(column_name="id", dataset=my_data, print_values=True)
        John
        Someone else
    """

    #############################################################################################################

    column_summaries = {}
    selected_column = select_column(column_name, dataset)

    for value in selected_column:
        if value not in column_summaries:
            column_summaries[value] = 1
        else:
            column_summaries[value] += 1

    if print_values:
        for value in column_summaries:
            print(value)
    else:
        return column_summaries
