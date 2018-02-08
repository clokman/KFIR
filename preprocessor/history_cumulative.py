def history_cumulative(target_column_name, n_back, dataset, row_grouping_criteria_header=None,
                       zero_floored_summation=0):
    """
    Calculates the cumulative sums of past x days for each value in the inputted column. Optionally,
    also takes a row grouping criteria (for instance, to calculate cumulative history of each participant id
    within themselves).

    :param target_column_name: (str) The name of the header that needs to be targeted.
    :param n_back: (int) Number of days to go back when calculating cumulative sums.
    :param dataset: (var) A variable that contains a dataset with headers.
    :param row_grouping_criteria_header: (str) The header of the column that will be used for grouping the multi-row variable in
        the target column. When a grouping criteria header is provided, this simply divides the column into multiple lists
        within a list.
    :param zero_floored_summation: (0,1) Performs the cumulative summation in a sequential manner, and sets a floor value for
        calculation. Useful in cases where negative values are not possible (e.g., sleep deficit calculations).
    :return: A list containing integers or floats

    :example - Cumulative two-day histories for a value (per id):
        >>> from preprocessor.print_columns import print_columns
        >>> my_data = [["id",  "value"], ["john", 1], ["JOHN", 2], ["John", 3], ["john", 4],   ["michael", -1], ["michael", -2], ["michael", -3], ["michael", -4], ["james", 10], ["james", 11], ["james", 12], ["james", 13]]
        >>> # Note the capitalization differences above (they are no problem)

        >>> print_columns("value",my_data) # print the original data
        <BLANKLINE>
        value is: [1, 2, 3, 4, -1, -2, -3, -4, 10, 11, 12, 13]

        >>> history_cumulative("value", 3, my_data, "id") # Cumulative two-day histories for 'value' (per id)
        [nan, nan, 6, 9, nan, nan, -6, -9, nan, nan, 33, 36]

    :example:
        >>> sleep_debt_changes = [["id",  "value"], ["john",   -8], ["JOHN",    3], ["John",   -12], ["john",    1], ["michael", 2], ["michael", 10], ["michael",-16], ["michael", 3], ["james",   1], ["james",   1], ["james",   1], ["james",   1]]
        >>> # Note the capitalization differences above (they are no problem)

        >>> print_columns("value",sleep_debt_changes) # print original column
        <BLANKLINE>
        value is: [-8, 3, -12, 1, 2, 10, -16, 3, 1, 1, 1, 1]

        >>> sleep_debts = history_cumulative("value", 4, sleep_debt_changes, "id", zero_floored_summation=1)
        >>> print(sleep_debts)
        [nan, nan, nan, 1, nan, nan, nan, 3, nan, nan, nan, 4]
    """

    #############################################################################################################

    from preprocessor.history_nback import history_nback
    from preprocessor.divide_column_by_criteria import divide_column_by_criteria

    # Make an iterative summation function for calculating variables that cannot go below a certain value (e.g., sleep debt)
    def sum_iterative(vector_to_iterate, floor_value=None):
        vector = vector_to_iterate

        vector_summed_so_far = 0
        current_sum = 0
        for i in range(1, len(vector)):
            if i == 1:
                current_sum = vector[i - 1] + vector[i]
            elif i > 1:
                current_sum = vector_summed_so_far + vector[i]
            if floor_value != None:
                if current_sum < floor_value:
                    current_sum = 0

            vector_summed_so_far = current_sum

        return (vector_summed_so_far)

    # Will give an error if row_grouping_criteria_header is None. Needs to be fixed.
    # Divide the given column with multi-row subjects to groups based on grouping criteria (e.g., id)
    grouped_rows_list = divide_column_by_criteria(row_grouping_criteria_header, target_column_name, dataset)

    cumulative_history_values_for_all_groups = []
    # For each group of values/rows in the current vector/column (rows are grouped by row_grouping_criteria_header)
    for each_group in grouped_rows_list:

        # Create a dictionary that holds historical versions of the current group of rows/values in the current column
        historical_versions_of_current_group_init = {}  # This dictionary has no proper key names yet, so its named _init
        for i in range(0, n_back):
            historical_versions_of_current_group_init[i] = history_nback(each_group, i)

        # If the value is NaN, replace it with 0. This is necessary for cumulative calculations up to n'th day,
        # or first n values would be NaN (desirable for values n days ago, but not for cumulative history)
        # for each_key, each_list in historical_versions_of_current_group_init.items():
        #    for i, each_item in enumerate(each_list):
        #        if each_item != each_item:
        #            historical_versions_of_current_group_init[each_key][i] = 0

        # Update the dictionary so that it holds historical versions of the current group of rows/values in the column.
        historical_versions_of_current_group = {}
        for key, value in historical_versions_of_current_group_init.items():
            historical_versions_of_current_group[str(key) + " days ago"] = historical_versions_of_current_group_init[
                key]
        # print(historical_versions_of_current_group["2 days ago"])

        # Sum all values in last x days to get the cumulative history
        previous_n_values_of_each_value = []
        n_day_cumulative_sums_of_each_value = []
        for i, item in enumerate(historical_versions_of_current_group[
                                     "0 days ago"]):  # for each column stored in the dictionary with representative length
            for key, value in historical_versions_of_current_group.items():  # and for each value in these columns
                previous_n_values_of_each_value.append(
                    historical_versions_of_current_group[key][i])  # add this value to a list
                # For some reason, the items in this previous_n_values_of_each_value vector is reversed. This must be corrected.
                reversed_previous_n_values_of_each_value = list(reversed(previous_n_values_of_each_value))
            if zero_floored_summation == 0:
                n_day_cumulative_sums_of_each_value.append(sum_iterative(
                    reversed_previous_n_values_of_each_value))  # sum this list (which now consists of all values of column)
            elif zero_floored_summation == 1:
                n_day_cumulative_sums_of_each_value.append(
                    sum_iterative(reversed_previous_n_values_of_each_value, floor_value=0))
            previous_n_values_of_each_value = []  # reset list for next aggregation and summation operation

        cumulative_history_values_for_all_groups.append(n_day_cumulative_sums_of_each_value)

    cumulative_history_values_for_all_groups_as_one_list = []
    for each_group_history in cumulative_history_values_for_all_groups:
        cumulative_history_values_for_all_groups_as_one_list.extend(each_group_history)

    return (cumulative_history_values_for_all_groups_as_one_list)  # return all of these sums