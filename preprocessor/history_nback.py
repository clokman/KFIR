def history_nback(target_column_name_or_target_var, n_back, input="list", dataset=None,
                  row_grouping_criteria_header=None):
    """
    Displays a vector's n-back element. Vector can be a column specified by its name in the parameters, or it can be a vector that holds a vector.

    :param target_column_name_or_target_var: (str or var) A column specified by its name in the parameters, or a vector that holds a target vector.
    :param n_back: (int) Number of elements to go back when selecting the previous value.
    :param input --> "list": (arg, default) Processes input as a vector that holds a list
    :param input --> "column": (arg) Processes input as a vector that holds a dataset
    :param dataset: (var) Vector that holds that a dataset with headers. Must be provided if target is a column name.
    :param row_grouping_criteria_header: (str) If a dataset is given, a row grouping criteria can also be defined. Can also be left blank.
    :return: A list containing previous values of elements

    :example - using nback for a list:
        >>> my_list = [1, 2, 3, 4, 7]
        >>> my_list_one_back = history_nback(my_list, 1)
        <BLANKLINE>
        >>> my_list_two_back = history_nback(my_list, 2)
        >>> my_list_three_back = history_nback(my_list, 3)
        >>> print(my_list_one_back)
        [nan, 1, 2, 3, 4]
        >>> print(my_list_two_back)
        [nan, nan, 1, 2, 3]
        >>> print(my_list_three_back)
        [nan, nan, nan, 1, 2]

    :example - using nback for a dataset
        >>> my_data = [["id", "value"], ["john", 1], ["JOHN", 2], ["John", 3], ["john", 4],  ["michael", -1], ["michael", -2], ["michael", -3], ["michael", -4], ["james", 10], ["james", 11], ["james", 12], ["james", 13]]
        >>> # Note the capitazliation deifferences in the dataset (they are no problem)

        >>> nback_all    = history_nback("value", 2, "column", dataset=my_data)
        >>> nback_per_id = history_nback("value", 2, "column", dataset=my_data, row_grouping_criteria_header="id")

        >>> print(nback_all)    # this is possibly the wrong usage if a dataset consists of multi-row cases. It is perfectly OK to use if the column does not contain multi-row cases.
        [nan, nan, 1, 2, 3, 4, -1, -2, -3, -4, 10, 11]
        >>> print(nback_per_id) # note that the n-back behavior is reset each time a row with a different id starts to be processed.
        [nan, nan, 1, 2, nan, nan, -1, -2, nan, nan, 10, 11]

    :example - :
        >>> from preprocessor.print_columns import print_columns
        >>> from preprocessor.demo_daily_data import demo_daily_data
        >>> one_days_before   = history_nback("sun_hours", 1, input="column", dataset=demo_daily_data)
        >>> two_days_before   = history_nback("sun_hours", 2, "column"      , demo_daily_data)
        >>> three_days_before = history_nback("sun_hours", 3, "column"      , demo_daily_data)

        >>> print_columns("sun_hours", demo_daily_data)
        <BLANKLINE>
        sun_hours is: [12.3, 8.8, 10.7, 1.3, 7.2, 4.4, 5.8, 5.3, 9.4, 9.0, 6.3, 12.5, 0.7, 6.3, 12.3, 5.3, 8.6, 0.9, 7.7, 2.4, 4.7, 3.4, 7.4, 9.2, 7.1, 12.3, 0.4, 7.8, 5.5, 12.3, 5.3, 8.6, 0.9, 7.7, 2.4, 4.7, 3.4, 7.4, 9.2, 7.1, 12.3, 0.4, 7.8, 12.3, 8.8, 10.7, 1.3, 7.2, 4.4, 5.8, 5.3, 9.4, 9.0, 6.3, 12.5, 0.7, 6.3, 12.3, 6.2, 10.3, 0.9, 6.6, 4.8, 4.5, 2.9, 9.9, 10.2, 7.9, 11.5, 0.3, 6.8, 6.8, 1.9, 7.6, 8.0, 7.5, 7.9, 6.7, 12.5, 1.9, 1.6, 0.1, 6.6, 0.6, 6.8, 8.6, 7.6, 6.3, 5.1, 9.8, 1.1, 6.9, 9.7, 2.4, 10.4, 8.1, 8.1, 12.5, 1.9, 1.6, 0.1, 6.6, 0.6, 6.8, 8.6, 7.6, 6.3, 5.1, 9.8, 1.1, 6.9, 9.7, 2.4, 12.3, 6.2, 10.3, 0.9, 6.6, 4.8, 4.5, 2.9, 9.9, 10.2, 7.9, 11.5, 0.3, 6.8, 6.8, 1.9, 7.6, 8.0, 7.5, 12.3, 6.2, 10.3, 0.9, 6.6, 4.8, 4.5, 2.9, 9.9, 10.2, 7.9, 11.5, 0.3, 6.8, 6.8, 1.9, 7.6, 8.0, 12.5, 1.9, 1.6, 0.1, 6.6, 0.6, 6.8, 8.6, 7.6, 6.3, 5.1, 9.8, 1.1, 6.9, 9.7, 2.4, 10.4, 8.1, 8.1]

        >>> print(one_days_before)
        [nan, 12.3, 8.8, 10.7, 1.3, 7.2, 4.4, 5.8, 5.3, 9.4, 9.0, 6.3, 12.5, 0.7, 6.3, 12.3, 5.3, 8.6, 0.9, 7.7, 2.4, 4.7, 3.4, 7.4, 9.2, 7.1, 12.3, 0.4, 7.8, 5.5, 12.3, 5.3, 8.6, 0.9, 7.7, 2.4, 4.7, 3.4, 7.4, 9.2, 7.1, 12.3, 0.4, 7.8, 12.3, 8.8, 10.7, 1.3, 7.2, 4.4, 5.8, 5.3, 9.4, 9.0, 6.3, 12.5, 0.7, 6.3, 12.3, 6.2, 10.3, 0.9, 6.6, 4.8, 4.5, 2.9, 9.9, 10.2, 7.9, 11.5, 0.3, 6.8, 6.8, 1.9, 7.6, 8.0, 7.5, 7.9, 6.7, 12.5, 1.9, 1.6, 0.1, 6.6, 0.6, 6.8, 8.6, 7.6, 6.3, 5.1, 9.8, 1.1, 6.9, 9.7, 2.4, 10.4, 8.1, 8.1, 12.5, 1.9, 1.6, 0.1, 6.6, 0.6, 6.8, 8.6, 7.6, 6.3, 5.1, 9.8, 1.1, 6.9, 9.7, 2.4, 12.3, 6.2, 10.3, 0.9, 6.6, 4.8, 4.5, 2.9, 9.9, 10.2, 7.9, 11.5, 0.3, 6.8, 6.8, 1.9, 7.6, 8.0, 7.5, 12.3, 6.2, 10.3, 0.9, 6.6, 4.8, 4.5, 2.9, 9.9, 10.2, 7.9, 11.5, 0.3, 6.8, 6.8, 1.9, 7.6, 8.0, 12.5, 1.9, 1.6, 0.1, 6.6, 0.6, 6.8, 8.6, 7.6, 6.3, 5.1, 9.8, 1.1, 6.9, 9.7, 2.4, 10.4, 8.1]
        >>> print(two_days_before)
        [nan, nan, 12.3, 8.8, 10.7, 1.3, 7.2, 4.4, 5.8, 5.3, 9.4, 9.0, 6.3, 12.5, 0.7, 6.3, 12.3, 5.3, 8.6, 0.9, 7.7, 2.4, 4.7, 3.4, 7.4, 9.2, 7.1, 12.3, 0.4, 7.8, 5.5, 12.3, 5.3, 8.6, 0.9, 7.7, 2.4, 4.7, 3.4, 7.4, 9.2, 7.1, 12.3, 0.4, 7.8, 12.3, 8.8, 10.7, 1.3, 7.2, 4.4, 5.8, 5.3, 9.4, 9.0, 6.3, 12.5, 0.7, 6.3, 12.3, 6.2, 10.3, 0.9, 6.6, 4.8, 4.5, 2.9, 9.9, 10.2, 7.9, 11.5, 0.3, 6.8, 6.8, 1.9, 7.6, 8.0, 7.5, 7.9, 6.7, 12.5, 1.9, 1.6, 0.1, 6.6, 0.6, 6.8, 8.6, 7.6, 6.3, 5.1, 9.8, 1.1, 6.9, 9.7, 2.4, 10.4, 8.1, 8.1, 12.5, 1.9, 1.6, 0.1, 6.6, 0.6, 6.8, 8.6, 7.6, 6.3, 5.1, 9.8, 1.1, 6.9, 9.7, 2.4, 12.3, 6.2, 10.3, 0.9, 6.6, 4.8, 4.5, 2.9, 9.9, 10.2, 7.9, 11.5, 0.3, 6.8, 6.8, 1.9, 7.6, 8.0, 7.5, 12.3, 6.2, 10.3, 0.9, 6.6, 4.8, 4.5, 2.9, 9.9, 10.2, 7.9, 11.5, 0.3, 6.8, 6.8, 1.9, 7.6, 8.0, 12.5, 1.9, 1.6, 0.1, 6.6, 0.6, 6.8, 8.6, 7.6, 6.3, 5.1, 9.8, 1.1, 6.9, 9.7, 2.4, 10.4]
        >>> print(three_days_before)
        [nan, nan, nan, 12.3, 8.8, 10.7, 1.3, 7.2, 4.4, 5.8, 5.3, 9.4, 9.0, 6.3, 12.5, 0.7, 6.3, 12.3, 5.3, 8.6, 0.9, 7.7, 2.4, 4.7, 3.4, 7.4, 9.2, 7.1, 12.3, 0.4, 7.8, 5.5, 12.3, 5.3, 8.6, 0.9, 7.7, 2.4, 4.7, 3.4, 7.4, 9.2, 7.1, 12.3, 0.4, 7.8, 12.3, 8.8, 10.7, 1.3, 7.2, 4.4, 5.8, 5.3, 9.4, 9.0, 6.3, 12.5, 0.7, 6.3, 12.3, 6.2, 10.3, 0.9, 6.6, 4.8, 4.5, 2.9, 9.9, 10.2, 7.9, 11.5, 0.3, 6.8, 6.8, 1.9, 7.6, 8.0, 7.5, 7.9, 6.7, 12.5, 1.9, 1.6, 0.1, 6.6, 0.6, 6.8, 8.6, 7.6, 6.3, 5.1, 9.8, 1.1, 6.9, 9.7, 2.4, 10.4, 8.1, 8.1, 12.5, 1.9, 1.6, 0.1, 6.6, 0.6, 6.8, 8.6, 7.6, 6.3, 5.1, 9.8, 1.1, 6.9, 9.7, 2.4, 12.3, 6.2, 10.3, 0.9, 6.6, 4.8, 4.5, 2.9, 9.9, 10.2, 7.9, 11.5, 0.3, 6.8, 6.8, 1.9, 7.6, 8.0, 7.5, 12.3, 6.2, 10.3, 0.9, 6.6, 4.8, 4.5, 2.9, 9.9, 10.2, 7.9, 11.5, 0.3, 6.8, 6.8, 1.9, 7.6, 8.0, 12.5, 1.9, 1.6, 0.1, 6.6, 0.6, 6.8, 8.6, 7.6, 6.3, 5.1, 9.8, 1.1, 6.9, 9.7, 2.4]
    """

    #############################################################################################################

    from preprocessor.divide_column_by_criteria import divide_column_by_criteria

    # If input is not a vector, select the specified column from the dataset.
    if input is "column":
        vectors_list = divide_column_by_criteria(row_grouping_criteria_header, target_column_name_or_target_var,
                                                 dataset)

    # If input is a vector, initialize internal vectors accordingly.
    elif input is "list":
        vectors_list = [target_column_name_or_target_var]

    vectors_list_with_nbacks = []
    for each_vector in vectors_list:
        # Assign a x-back previous values of a column or vector to a new vector.
        current_nbacks = []
        for i, each_element in enumerate(each_vector):
            current_nbacks.append(each_vector[i - n_back])
        current_nbacks[0:n_back] = [float("NaN")] * n_back  # replace meaningless values with 0
        vectors_list_with_nbacks.append(current_nbacks)

    unified_vector_with_nbacks = []
    for each_vector in vectors_list_with_nbacks:
        unified_vector_with_nbacks.extend(each_vector)

    return (unified_vector_with_nbacks)