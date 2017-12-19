from preprocessor.select_column import select_column


def print_columns(column_names, dataset):
    """
     Prints columns with specified column names in a dataset.

    :param column_names: A list of strings or string of header name(s) in a column.
    :param dataset: The dataset variable. It must be already read, and must contain headers.
    :returns: Prints strings to console line by line:
        __column_name1__ is: __column1_values__
        __column_name2__ is: __column2_values__
    :example:
        >>> example_data = [['day', 'month'], ['1', 'June'], ['3', 'May'], ['4', 'Jun']]
        >>> #print_columns(["day", "month"], example_data)  # print multiple column names
        <BLANKLINE>
        day is: ['1', '3', '4']
        <BLANKLINE>
        month is: ['June', 'May', 'Jun']
        >>> print_columns("day", example_data)             # print a single column name
        <BLANKLINE>
        day is: ['1', '3', '4']
    """
    if type(column_names) is list:  # if the query is a list...
        for i, column_name in enumerate(column_names):
            print("\n" + column_name + " is: " + str(select_column(column_name, dataset)))

    elif type(column_names) is str:  # if the query is a string (i.e., if a single column name is entered)...
        column_name = column_names
        print("\n" + column_name + " is: " + str(select_column(column_name, dataset)))

    else:  # if the query is not a list or single string, return error
        raise ValueError('1: column_names must be a list of strings or a single string.')
