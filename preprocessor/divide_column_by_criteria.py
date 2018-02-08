def divide_column_by_criteria(row_grouping_criteria_header, target_column_name, dataset, output="list"):
    """
    Divides a column to multiple parts based on the division criteria provided (e.g., grouping rows based on participant IDs
    that are spread to multiple rows). Ignores capitalization differences in criteria names.

    :param row_grouping_criteria_header: (str): Header of the column that contains the criteria that will be used when creating groups of rows
    (e.g., Participant ID)
    :param target_column_name: (str) The column that will be divided into groups
    :param dataset: (var) A variable containing a dataset with headers
    :param output --> "list": (default) turns on the list mode, which returns the output as a list that is in the same order with the
                              inputted data (if the rows of the row grouping criteria column has no interruption [i.e., this shouldn't happen in data:
                              participant A's id for 10 rows, and then participant B's id, and then participant A's again.])
    :param output --> "dict" returns a dictionary instead of a list. Does not preserve order.
    :return: A list of lists containing subgroups made out of the inputted column.

    :example - divide column/group rows by id (and output a list):
        >>> from preprocessor.print_columns import print_columns
        >>> from preprocessor.demo_daily_data import demo_daily_data
        >>> print_columns("id", demo_daily_data)
        <BLANKLINE>
        id is: ['AB64', 'AB64', 'AB64', 'AB64', 'AB64', 'AB64', 'AB64', 'AB64', 'AB64', 'AB64', 'AB64', 'AB64', 'AB64', 'AB64', 'EM11', 'EM11', 'EM11', 'EM11', 'EM11', 'EM11', 'EM11', 'EM11', 'EM11', 'EM11', 'EM11', 'EM11', 'EM11', 'EM11', 'EM11', 'FT12', 'FT12', 'FT12', 'FT12', 'FT12', 'FT12', 'FT12', 'FT12', 'FT12', 'FT12', 'FT12', 'FT12', 'FT12', 'FT12', 'gh93', 'gh93', 'gh93', 'gh93', 'gh93', 'gh93', 'gh93', 'Gh93', 'gh93', 'gh93', 'gh93', 'Gh93', 'gh93', 'gh93', 'GW98', 'GW98', 'GW98', 'GW98', 'GW98', 'GW98', 'GW98', 'GW98', 'GW98', 'GW98', 'GW98', 'GW98', 'GW98', 'GW98', 'GW98', 'GW98', 'GW98', 'GW98', 'GW98', 'GW98', 'GW98', 'HA61', 'HA61', 'HA61', 'HA61', 'HA61', 'HA61', 'HA61', 'HA61', 'HA61', 'HA61', 'HA61', 'HA61', 'HA61', 'HA61', 'HA61', 'HA61', 'HA61', 'HA61', 'HA61', 'he46', 'he46', 'he46', 'HE46', 'he46', 'he46', 'he46', 'he46', 'he46', 'he46', 'HE46', 'he46', 'he46', 'he46', 'he46', 'he46', 'MJ87', 'MJ87', 'MJ87', 'MJ87', 'MJ87', 'MJ87', 'MJ87', 'MJ87', 'MJ87', 'MJ87', 'MJ87', 'MJ87', 'MJ87', 'MJ87', 'MJ87', 'MJ87', 'MJ87', 'MJ87', 'MJ87', 'PM61', 'PM61', 'PM61', 'PM61', 'PM61', 'PM61', 'PM61', 'PM61', 'PM61', 'PM61', 'PM61', 'PM61', 'PM61', 'PM61', 'PM61', 'PM61', 'PM61', 'PM61', 'wh18', 'wh18', 'wh18', 'wh18', 'wh18', 'wh18', 'wh18', 'wh18', 'wh18', 'wh18', 'wh18', 'wh18', 'wh18', 'wh18', 'wh18', 'wh18', 'wh18', 'wh18', 'wh18']

        >>> x = divide_column_by_criteria("id", "sun_hours", demo_daily_data)
        >>> print(x)
        [[12.3, 8.8, 10.7, 1.3, 7.2, 4.4, 5.8, 5.3, 9.4, 9.0, 6.3, 12.5, 0.7, 6.3], [12.3, 5.3, 8.6, 0.9, 7.7, 2.4, 4.7, 3.4, 7.4, 9.2, 7.1, 12.3, 0.4, 7.8, 5.5], [12.3, 5.3, 8.6, 0.9, 7.7, 2.4, 4.7, 3.4, 7.4, 9.2, 7.1, 12.3, 0.4, 7.8], [12.3, 8.8, 10.7, 1.3, 7.2, 4.4, 5.8, 5.3, 9.4, 9.0, 6.3, 12.5, 0.7, 6.3], [12.3, 6.2, 10.3, 0.9, 6.6, 4.8, 4.5, 2.9, 9.9, 10.2, 7.9, 11.5, 0.3, 6.8, 6.8, 1.9, 7.6, 8.0, 7.5, 7.9, 6.7], [12.5, 1.9, 1.6, 0.1, 6.6, 0.6, 6.8, 8.6, 7.6, 6.3, 5.1, 9.8, 1.1, 6.9, 9.7, 2.4, 10.4, 8.1, 8.1], [12.5, 1.9, 1.6, 0.1, 6.6, 0.6, 6.8, 8.6, 7.6, 6.3, 5.1, 9.8, 1.1, 6.9, 9.7, 2.4], [12.3, 6.2, 10.3, 0.9, 6.6, 4.8, 4.5, 2.9, 9.9, 10.2, 7.9, 11.5, 0.3, 6.8, 6.8, 1.9, 7.6, 8.0, 7.5], [12.3, 6.2, 10.3, 0.9, 6.6, 4.8, 4.5, 2.9, 9.9, 10.2, 7.9, 11.5, 0.3, 6.8, 6.8, 1.9, 7.6, 8.0], [12.5, 1.9, 1.6, 0.1, 6.6, 0.6, 6.8, 8.6, 7.6, 6.3, 5.1, 9.8, 1.1, 6.9, 9.7, 2.4, 10.4, 8.1, 8.1]]

    :example - divide column/group rows by id and output a dictionary:
        >>> y = divide_column_by_criteria("id", "sun_hours", demo_daily_data, "dict")
        >>> # print(y) # No comparisons in docstring is possible because a dictionary prints its items in a different order each time the function is run.
        >>> # an example output, however, is as following:
        >>> # {'gw98': [12.3, 6.2, 10.3, 0.9, 6.6, 4.8, 4.5, 2.9, 9.9, 10.2, 7.9, 11.5, 0.3, 6.8, 6.8, 1.9, 7.6, 8.0, 7.5, 7.9, 6.7], 'wh18': [12.5, 1.9, 1.6, 0.1, 6.6, 0.6, 6.8, 8.6, 7.6, 6.3, 5.1, 9.8, 1.1, 6.9, 9.7, 2.4, 10.4, 8.1, 8.1], 'em11': [12.3, 5.3, 8.6, 0.9, 7.7, 2.4, 4.7, 3.4, 7.4, 9.2, 7.1, 12.3, 0.4, 7.8, 5.5], 'gh93': [12.3, 8.8, 10.7, 1.3, 7.2, 4.4, 5.8, 5.3, 9.4, 9.0, 6.3, 12.5, 0.7, 6.3], 'he46': [12.5, 1.9, 1.6, 0.1, 6.6, 0.6, 6.8, 8.6, 7.6, 6.3, 5.1, 9.8, 1.1, 6.9, 9.7, 2.4], 'ft12': [12.3, 5.3, 8.6, 0.9, 7.7, 2.4, 4.7, 3.4, 7.4, 9.2, 7.1, 12.3, 0.4, 7.8], 'ab64': [12.3, 8.8, 10.7, 1.3, 7.2, 4.4, 5.8, 5.3, 9.4, 9.0, 6.3, 12.5, 0.7, 6.3], 'ha61': [12.5, 1.9, 1.6, 0.1, 6.6, 0.6, 6.8, 8.6, 7.6, 6.3, 5.1, 9.8, 1.1, 6.9, 9.7, 2.4, 10.4, 8.1, 8.1], 'pm61': [12.3, 6.2, 10.3, 0.9, 6.6, 4.8, 4.5, 2.9, 9.9, 10.2, 7.9, 11.5, 0.3, 6.8, 6.8, 1.9, 7.6, 8.0], 'mj87': [12.3, 6.2, 10.3, 0.9, 6.6, 4.8, 4.5, 2.9, 9.9, 10.2, 7.9, 11.5, 0.3, 6.8, 6.8, 1.9, 7.6, 8.0, 7.5]}
    """

    #############################################################################################################

    from preprocessor.select_column import select_column

    # Compatibilty column for history_nback function. Can be ignored.
    if row_grouping_criteria_header is None:
        return [select_column(target_column_name, dataset)]

    # Initialize criteria that is going to be used to divide the columns, and initialize the target column to be divided
    target_column = select_column(target_column_name, dataset)
    criteria_column = select_column(row_grouping_criteria_header, dataset)

    # Make all elements in the criteria column (e.g., participant ids) lowecase, so instead of creating different groups for
    # ... each capitalization style of the criteria, one group is created.
    for i, row in enumerate(criteria_column):
        criteria_column[i] = row.lower()

    # Reduce all items in the criteria column to their unique ocurences
    criteria = set(criteria_column)

    # Divide the target column based on given criteria
    grouped_rows_dict = {}
    for criterion in criteria:

        grouped_rows_dict[criterion] = []

        counter = range(0, len(criteria_column))
        for i, criterion_value, target_value in zip(counter, criteria_column, target_column):
            if criterion_value == criterion:
                grouped_rows_dict[criterion].append(target_value)

    # Return a version of the inputted column that is divided per the criteria column
    if output == "list":
        # Order dictionary return order based on row order in the column
        divider_column = select_column(row_grouping_criteria_header, dataset)
        groups_order = []
        for criterion in criteria_column:
            if criterion not in groups_order:
                groups_order.append(criterion)

        grouped_rows_ordered_list = []
        # for group_key, group_values in grouped_rows_dict.items():
        #    for group_name in groups_order:
        #        if group_key is group_name:
        #            grouped_rows_ordered_list.append(grouped_rows_dict[group_key])

        for group_name in groups_order:
            for group_key, group_values in grouped_rows_dict.items():
                if group_key is group_name:
                    grouped_rows_ordered_list.append(grouped_rows_dict[group_key])

        return grouped_rows_ordered_list
    elif output == "dict":
        return grouped_rows_dict