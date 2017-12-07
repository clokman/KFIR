def replace_headers(header_replacements, dataset):
    '''
    Replaces headers with those in the header_replacements list

    :param header_replacements: A list containing the new headers
    :param dataset: A variable that holds a dataset with headers
    :return: Returns no output. Replaces the dataset.
    :example:
        >>> from preprocessor.demo_data import demo_data #import demo_data variable from preprocessor.demo_data module
        >>> print(demo_data[0][0])
        date
        >>> # This is a list taken from 'survey features.xlsx'
        >>> replacements = ["date_x", "consent", "id", "sex", "age", "edu", "timezone_change", "sleep_disorder", "nightshift", "psy_disorder", "wake", "young_kids", "partn", "btptr_1", "btptr_2", "btptr_3", "btptr_4", "btptr_5", "btptr_6", "btptr_7", "btptr_8", "btptr_9", "ats_1", "atbr_1", "sq_1", "sq_2", "sq_3", "sq_4", "sq_5", "sq_6", "atbr_2", "atbr_3", "ats_2", "ats_3", "chron_1", "chron_2", "chron_3", "chron_4", "chron_5", "chron_6", "chron_7", "chron_8", "sc_1", "sc_2", "sc_3", "sc_4", "sc_5", "sc_6", "sc_7", "sc_8", "sc_9", "sc_10", "sc_11", "sc_12", "sc_13"]
        >>> replace_headers(header_replacements=replacements, dataset=demo_data)
        >>> print(demo_data[0][0])
        date_x
    '''

    #############################################################################################################

    for i, header in enumerate(header_replacements):
            dataset[0][i] = header


