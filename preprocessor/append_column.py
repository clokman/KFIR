def append_column(new_column_values, new_column_name, dataset):
    """

    :param new_column_values:
    :param new_column_name:
    :param dataset:
    :return: Changes the inputted dataset when ran (no need for assigning the output to a variable).
    :usage: append_column(NEW_COLUMN_VARIABLES_LIST, NEW_COLUMN_NAME_STRING, DATASET)

    :example:
        >>> sample_data  = [['day', 'month'], ['1', 'June'], ['3', 'May'], ['4', 'Jun']]
        >>> years_column = [2149,2150,2151]

        >>> append_column(years_column, "year", sample_data)
        [['day', 'month', 'year'], ['1', 'June', 2149], ['3', 'May', 2150], ['4', 'Jun', 2151]]
        >>> print(sample_data) # changes the original data set without a need to assign the output to a new variable, etc.
        [['day', 'month', 'year'], ['1', 'June', 2149], ['3', 'May', 2150], ['4', 'Jun', 2151]]
    """

    #############################################################################################################

    from preprocessor.get_headers import get_headers

    # Check for duplicate header names
    headers = get_headers(dataset)
    if new_column_name in headers:  # if this duplicate check is not included, things go wrong (the duplicate header gets added to column values—a strange behavior, but it is prevented with not allowing duplicate headers).
        print(
            "ERROR: Header name already in dataset. Re-run all code up to this point or change header name.\nError occured while processing new_column_name: " + str(
                new_column_name))
        raise ValueError(
            "Header name already in dataset. Please choose a different name. If name is correct, try re-running all code up to this point. (See console output for last header name processed.)")

    # Append the inputted column to specified dataset
    new_column = new_column_values  # pass argument to variable
    new_column.insert(0, new_column_name)  # new column = merging of column name and column values
    for i, row in enumerate(dataset):  # for each row in the dataset...
        row.append(new_column[
                       i])  # ...append the new column at the end (original dataset is already changed with this line, and there is no additional action [e.g., variable re-assignment] needed to change the dataset).
    return dataset  # output the changed dataset