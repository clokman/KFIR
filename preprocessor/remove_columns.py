from preprocessor.get_data import get_data
from preprocessor.get_header_index import get_header_index


def remove_columns(target_column_headers_list, dataset):
    """
    Function to remove a column in a dataset.

    :example:
    >>> sample_data = [['day', 'month', 'hour', 'minute'], ['1', 'June', '12', '39'], ['3', 'May', '11', '50'], ['4', 'Jun', '15', '20']]
    >>> print(sample_data)
    [['day', 'month', 'hour', 'minute'], ['1', 'June', '12', '39'], ['3', 'May', '11', '50'], ['4', 'Jun', '15', '20']]
    >>> remove_columns(["month", "day"], sample_data)
    >>> print(sample_data)
    [['hour', 'minute'], ['12', '39'], ['11', '50'], ['15', '20']]
    >>> remove_columns("minute", sample_data)
    >>> print(sample_data)
    [['hour'], ['12'], ['11'], ['15']]
    """

    #############################################################################################################

    if type(target_column_headers_list) is str:
        target_column_headers_list = [target_column_headers_list]

    for each_column_name in target_column_headers_list:
        #data = get_data(dataset) is not used here unlike in most other functions of prerpocess library. This is because the column header also needs to be included in removal process.
        target_index = get_header_index(each_column_name, dataset)
        for i, row in enumerate(dataset):
            del(row[target_index])
