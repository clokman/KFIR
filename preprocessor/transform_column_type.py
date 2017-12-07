def transform_column_type(target_headers, target_type, dataset):
    """
    Transforms a column of string integers or floats to integers or floats.

    :param target_headers: Header(s) of the columns to transformed to integers. Can be a list of strings (for multiple columns) or a single string (for a single column).
    :param target_type: (str) value:"int" --> Converts all values in the selected columns from strings to integers. value: "float" -->  Converts strings to float values.
    :param dataset: A dataset that is read to a variable. It must contain headers.
    :return: Transformed dataset. NOTE: If function is run without any variable assignment, it still changes the original dataset variable.

    :example - transform single column to integers:
        >>> my_data = [["letters", "numbers"], ["a", "1"], ["b", "2"], ["c","3"]] # <- Notice the number strings
        >>> transform_column_type("numbers", "int", my_data)
        [['letters', 'numbers'], ['a', 1], ['b', 2], ['c', 3]]

    :example - transform multiple columns to integers:
        >>> my_data = [["letters", "small numbers", "large numbers"], ["a", "1", "100"], ["b", "2", "200"], ["c","3", "300"]]
        >>> transform_column_type(["small numbers", "large numbers"], "float", my_data)
        [['letters', 'small numbers', 'large numbers'], ['a', 1.0, 100.0], ['b', 2.0, 200.0], ['c', 3.0, 300.0]]
    """

    #############################################################################################################

    from preprocessor.select_column import select_column
    from preprocessor.replace_column import replace_column

    try:
        if type(target_headers) is str:
            target_headers = [target_headers]

        for header_name in target_headers:
            selected_column = select_column(header_name, dataset)
            if target_type is "int":
                selected_column = [int(value) for value in selected_column]
            elif target_type is "float":
                selected_column = [float(value) for value in selected_column]
            replace_column(selected_column, header_name, dataset)
    except:
        raise ValueError(
            "Unable to transform column values to target type. Column values are not strings that are convertible to target type?")

    return (dataset)