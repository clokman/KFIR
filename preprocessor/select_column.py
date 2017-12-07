from preprocessor.get_headers import get_headers
from preprocessor.get_data import get_data
from preprocessor.get_header_index import get_header_index


def select_column(header_query, dataset):
    '''
    Allows columns to be selected (i.e., returned) by entering their header names.

    :param header_query: The header name to be searched
    :param dataset: The variable that contains a dataset with headers
    :return: A list vector that contains values from the queried column
    :example:
        >>> from preprocessor.demo_data import demo_data
        >>> select_column("edu", demo_data)
        ['HBO', 'WO', 'WO', 'WO', 'WO', 'HBO', 'HBO', 'WO', 'WO', 'MBO', 'WO']
    '''

    #############################################################################################################

    headers = get_headers(dataset)
    data = get_data(dataset)

    if header_query not in headers:  # if the queried keyword is not in the headers list, return error
        print("ERROR: Header not found in dataset.\nError occured while processing header_query: " + header_query)
        raise ValueError(
            'String not found in headers. Please enter a different column name. (See console output for last '
            'processed input string.)')

    header_index = get_header_index(header_query, dataset)
    column = [row[header_index] for row in
              data]  # assign the column matching the current_index from headers list to a variable
    return column  # return the column sans header
