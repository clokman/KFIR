def transform_column_substring(target_substring, replacement_substring, target_headers_list, dataset):
    """
    Replaces substring for all values in a column and returns the transformed dataset.
    Accepts regex as target_substring.

    :param target_substring: (str, regex) The old substring
    :param replacement_substring: (str) The new substring
    :param target_headers_list: (str, list) A list of he headers of the target columns. A single string value can also be inputted.
    :param dataset: The variable that holds the dataset. Headers must be included in the dataset.
    :return: The transformed dataset (Variable assignment is unnecessary, the original dataset is changed once the function is run)

    :example - Replace irregular AM values:
        >>> my_data = [ ["id", "time"], ["1", "10 a.m."], ["2", "8 a.m."], ["3", "4 A.M."] ]
        >>> transform_column_substring("a.m.", "AM", "time", my_data)
        [['id', 'time'], ['1', '10 AM'], ['2', '8 AM'], ['3', '4 A.M.']]
        >>> transform_column_substring("[Aa].[Mm].", "AM", "time", my_data)
        [['id', 'time'], ['1', '10 AM'], ['2', '8 AM'], ['3', '4 AM']]

    :example - Remove the dots from all values in the specified columns:
        >>> my_data = [ ["id", "time"], ["1", "10 a.m."], ["2", "8 a.m."], ["3", "4 A.M."] ]
        >>> transform_column_substring("\.", "", ["time"], my_data)
        [['id', 'time'], ['1', '10 am'], ['2', '8 am'], ['3', '4 AM']]
    """

    #############################################################################################################

    import re

    from preprocessor.select_column import select_column
    from preprocessor.replace_column import replace_column

    if type(target_headers_list) is str:  # If a single value is inputted as target column header (and not a list)
        target_headers_list = [
            target_headers_list]  # Convert this to a list with one item so the rest of the function can work correctly.

    for target_column_name in target_headers_list:  # For each column in the inputted list
        selected_column = select_column(target_column_name, dataset)  # Select the column
        for i, string in enumerate(selected_column):  # And change the substring
            selected_column[i] = re.sub(target_substring, replacement_substring, string)

        replace_column(selected_column, target_column_name, dataset)  # Rewrite the column with its new version

    return dataset