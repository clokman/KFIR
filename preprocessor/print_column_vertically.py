def print_column_vertically(target_column_name, dataset):
    """
    Prints each variable of a column to a new line in console.

    :param target_column_name: (str) Header of the column to be printed
    :param dataset: dataset to column is in
    :returns: Strings printed to console
    :example:
        >>> long_data = [["date"], ['2017/03/30 12:20:57 AM UTC+0200'], ['2017/03/31 1:38:41 AM UTC+0200'], ['2017/04/01 12:00:27 AM UTC+0200']]
        >>> print_column_vertically("date", long_data)
        2017/03/30 12:20:57 AM UTC+0200
        2017/03/31 1:38:41 AM UTC+0200
        2017/04/01 12:00:27 AM UTC+0200
    """

    #############################################################################################################

    from preprocessor.select_column import select_column

    selected_column = select_column(target_column_name, dataset)
    for i, value in enumerate(selected_column):
        print(value)
