def calculate_scores(scale_columns_list, dataset, count_values=None, include_values_only=None):
    """
    Calculates the row sums for given columns, which can be used to calculate scale/questionnaire scores.
    It works by taking column names and dataset as input, and returning a list of integers which is the sum of each row of the given column names.

    :param scale_columns_list: This must be a list of strings that hold the header names for target questions.
    :param dataset: The variable that holds the dataset to process. Dataset must also contain headers.
    :param count_values: (List of int or float, int, float) Counts the number of occurences for given values.
    :param include_values_only: (List of int or float, int, float) Values from column to include in the calculation. All other values are be converted to 0.
    :return: A LIST of INTEGERS that holds the calculated scores.
    :exception ValueError [1]: All values in the target rows (except the headers) must be either integers or strings that are convertible to strings.

    :example - simple score summation over columns:
        >>> example_data = [['participant_id', 'question_1', 'question_2', 'question_3'], ['#1', '0', '-2', '1'], ['#2', '2', '-3', '0'], ['#3', '4', '-1', '1'], ['#4', '1', '0', '2']]
        >>> scores = calculate_scores(["question_1", "question_2", "question_3"], example_data)
        >>> print("scores of four participants (row sums of given columns):" + str(scores))
        scores of four participants (row sums of given columns):[-1.0, -1.0, 4.0, 3.0]

    :example - include only certain values in score calculation:
        >>> scores = calculate_scores(["question_1", "question_2", "question_3"], example_data, include_values_only=[1])
        >>> print("filtered scores of four participants (filtered row sums of given columns):" + str(scores))
        filtered scores of four participants (filtered row sums of given columns):[1.0, 0, 1.0, 1.0]

    :example - count number of occurences of a value over columns:
        >>> scores = calculate_scores(["question_1", "question_2", "question_3"], example_data, count_values=[0,1])
        >>> print("counts of scores for four participants:" + str(scores))
        counts of scores for four participants:[2, 1, 1, 2]

    """

    #############################################################################################################

    from preprocessor.select_column import select_column

    #########################
    ###  INITIALIZATION  ###
    #########################
    # Prepare count_values parameter for internal use
    if count_values == None:
        count_values = [None]
    elif type(count_values) != list:
        try:
            count_values = [count_values]
        except:
            raise ValueError("[2] 'count_values' parameter is not convertible to list.")

    # Prepare include_values_only parameter for internal use
    if include_values_only == None:
        include_values_only = [None]
    elif type(include_values_only) != list:
        try:
            include_values_only = [include_values_only]
        except:
            raise ValueError("[3] 'include_values_only' parameter is not convertible to list.")

    ###############################
    ###  DICTIONARY OF COLUMNS  ###
    ###############################
    # Make a dictionary of columns to be included in the score calculation (keys are column headers, values are column rows)
    columns = {}
    for column_name in scale_columns_list:
        current_column = select_column(column_name, dataset)
        for i, element in enumerate(current_column):
            try:
                current_column[i] = float(element)  # For compatibility with NaN values, this must be float
            except:
                raise ValueError(
                    "[1] Scores are not integers or floats (or not strings that are convertible to float). A non-number string exists in the data?")
                break
        columns[column_name] = current_column

    #########################
    ###  TRANSFORMATIONS  ###
    #########################
    # Change all dictionary values that is given in count_values parameter to 1, and all others to 0
    if count_values != [None]:
        for each_key, each_column in columns.items():
            for i, each_value in enumerate(each_column):
                if each_value not in count_values:
                    columns[each_key][i] = 0
                else:
                    columns[each_key][i] = 1

    # Keep all dictionary values that is given in the include_values_only parameter, and make all other values 0
    if include_values_only != [None]:
        for each_key, each_column in columns.items():
            for i, each_value in enumerate(each_column):
                if each_value not in include_values_only:
                    columns[each_key][i] = 0

                    ###################
    ### CALCULATION ###
    ###################
    current_and_previous_column = []  # temporary variable necessary for column additions in the for loop below
    sum_of_each_row_so_far = []  # will ultimately hold scores of each row

    for column_key, column_values in columns.items():  # For each column (which are now in the 'columns' dictionary)
        # To begin, add all values of the first row for all columns to 'sum_of_each_row_so_far'.
        # (At this point, the for loop's index = 0 (i.e., the first column/key in dictionary))

        if len(sum_of_each_row_so_far) == 0:
            for value in column_values:
                sum_of_each_row_so_far.append(value)
        # (By the time the for loop reaches this 'else', index = 1 instead of 0 (i.e., the second key/column in dictionary)).
        else:
            current_and_previous_column = list(zip(sum_of_each_row_so_far,
                                                   column_values))  # Pair values of the first rows of columns (stored in 'sum_of_each_row_so_far') and the values of the next row.
            for i, pair in enumerate(current_and_previous_column):
                sum_of_each_row_so_far[i] = sum(
                    pair)  # Sum the current row (index = 1) and the previous row (index  = 0)
                # After this calculation, let 'sum_of_each_row_so_far' become the result of this sum;
                # And in the next iteration, use this sum as the input (i.e., the previous row) when adding the next row to it.
    return sum_of_each_row_so_far