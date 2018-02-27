def parse_hour_minute(target_columns_list, ymd_column_name, dataset):
    """
    Transforms string object in hh:mm format to a datetime.datetime object.

    :param target_columns_list: (lst) A list of strings containing the headers of target columns.
    :param ymd_column_name: (str) The column that holds the year, month, and date information as a 'datetime' object.
    :param dataset: The variable that the dataset is stored in. Headers of the dataset must be included in the dataset variable.
    :return:  Rewrites the inputted dataset (variable assignment is not necessary.)
    :exception Error 1: Because this function transforms it input variable ("i.e., dataset") into an object it cannot process (i.e., string --> datetime format), it cannot be run twice consequently.

    :usage:
        parse_hour_minute([time1, time2], my_dataset)
    :example - parse 3 columns at the same time to datetime format:
        parse_hour_minute(["wake_time", "bed_time", "bed_time_plan_aligned"], "date", daily_data)
    """

    #############################################################################################################

    for column_name in target_columns_list:
        if type(column_name) is not str:
            raise ValueError(
                "[Error 1] Non-string header name is found in target headers list. Please check your headers.")

    import datetime
    import pandas  # Necessary for creating NaT (Not a time) values.

    for column_name in target_columns_list:  # for each column

        selected_column = select_column(column_name, dataset)

        for i, time in enumerate(selected_column):  # and for each value in each of these columns
            try:
                dates = select_column(ymd_column_name, dataset)
                time_full = (str(dates[i].year) + "." + str(dates[i].month) + "." + str(dates[i].day) + " " + str(time))

                selected_column[i] = datetime.datetime.strptime(time_full, "%Y.%m.%d %H:%M")
            except:  # If time cannot be converted (e.g., because it's a "NA" value)...
                selected_column[
                    i] = pandas.NaT  # Just copy-paste the problematic value (e.g., a NA value) in the new column
        replace_column(selected_column, column_name, dataset)