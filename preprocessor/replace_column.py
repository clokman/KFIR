from preprocessor.get_data import get_data
from preprocessor.get_header_index import get_header_index


def replace_column(replacement_column, target_column_header, dataset):
    """
    Function to replace values in a column in a dataset. Useful when re-writing a column after converting it to
    something else. (For instance, after converting likert scale responses from strings to integers).

    :example:
    >>> sample_data = [['day', 'month'], ['1', 'June'], ['3', 'May'], ['4', 'Jun']]
    >>> replacement_column = [10,20,30]

    >>> new_data = replace_column(replacement_column, "day", sample_data)
    >>> print(new_data)
    [[10, 'June'], [20, 'May'], [30, 'Jun']]
    """

    #############################################################################################################

    data = get_data(dataset)

    target_index = get_header_index(target_column_header, dataset)
    for i, row in enumerate(data):
        row[target_index] = replacement_column[i]
    return data
