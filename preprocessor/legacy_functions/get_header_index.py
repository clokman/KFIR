from preprocessor.legacy_functions.get_headers import get_headers


def get_header_index(header_query, dataset):
    """
    Finds index number of given keyword header_name in demo_data headers

    :param header_query: The header name to search for
    :param dataset:  The variable that contains a dataset with headers
    :return: Integer corresponding to header index
    :example:
        >>> from preprocessor.test_data.demo_data import demo_data
        >>> get_header_index("edu", demo_data)
        5
    """

    #############################################################################################################

    headers = get_headers(dataset)
    # find index number of given keyword header_name in demo_data headers
    current_index = 0
    if header_query in headers:     # if the keyword is in headers list
        for header in headers:      # iterate over headers list
            if header != header_query:   # until the query is matched
                current_index += 1       # keep incrementing index counter
            else:
                return current_index
