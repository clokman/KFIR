def transform_column_values(target_replacement_dictionary, target_column_headers_list, dataset):
    """
    Replaces values in columns by using a dictionary of conversions (e.g., in order to quantify likert scales).

    :param target_replacement_dictionary: (dict) A dictionary in which *keys* are old (target) values and
        dictionary *values* are new (replacement) values.
    :param target_column_headers_list: (str) A list of headers as a list of strings, which specifies in which
        columns the transformation will occur.
    :param dataset: (var) A variable that holds the dataset. Headers must be included.
    :returns:
        Transforms the original dataset, and also returns it.
        Assignment of output to a variable is not necessary; inputted dataset will be changed without assignment
        as well.

    :example (single target column as input):
        >>> from preprocessor.demo_data import demo_data
        >>> from preprocessor.print_columns import print_columns
        >>> print_columns("consent", demo_data)
        <BLANKLINE>
        consent is: ['Ja, ik neem deel', 'Ja, ik neem deel', 'Ja, ik neem deel', 'Ja, ik neem deel', 'Ja, ik neem deel', 'Ja, ik neem deel', 'Ja, ik neem deel', 'Ja, ik neem deel', 'Ja, ik neem deel', 'Ja, ik neem deel', 'Ja, ik neem deel']

        >>> transform_column_values({"Ja, ik neem deel":1, "no":2}, "consent", demo_data)
        [['date', 'consent', 'id', 'sex', 'age', 'edu', 'timezone_change', 'sleep_disorder', 'nightshift', 'psy_disorder', 'wake', 'young_kids', 'partn', 'btptr_1', 'btptr_2', 'btptr_3', 'btptr_4', 'btptr_5', 'btptr_6', 'btptr_7', 'btptr_8', 'btptr_9', 'ats_1', 'atbr_1', 'sq_1', 'sq_2', 'sq_3', 'sq_4', 'sq_5', 'sq_6', 'atbr_2', 'atbr_3', 'ats_2', 'ats_3', 'chron_1', 'chron_2', 'chron_3', 'chron_4', 'chron_5', 'chron_6', 'chron_7', 'chron_8', 'sc_1', 'sc_2', 'sc_3', 'sc_4', 'sc_5', 'sc_6', 'sc_7', 'sc_8', 'sc_9', 'sc_10', 'sc_11', 'sc_12', 'sc_13'], ['2017/04/01 8:35:57 p.m. EET', 1, 'EM11', 'Vrouw', '44', 'HBO', 'Nee', 'Nee', 'Nee', 'Nee', 'Ja', 'Nee', 'Soms', 'soms', '(bijna) altijd', '(bijna) altijd', 'soms', '(bijna) nooit', 'soms', '(bijna) altijd', '(bijna) nooit', '(bijna) altijd', '(bijna) nooit', '(bijna) nooit', 'binnen een kwartier', 'nooit', 'nooit', 'nooit', 'een beetje', 'erg goed', '(bijna) nooit', '(bijna) nooit', 'vaak', '(bijna) altijd', 'helemaal eens', 'helemaal oneens', 'helemaal oneens', 'helemaal eens', 'oneens', 'helemaal eens', 'helemaal eens', 'helemaal oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'helemaal oneens', 'helemaal oneens', 'oneens', 'eens', 'even vaak eens als oneens', 'eens', 'oneens', 'eens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'oneens'], ['2017/04/01 8:15:27 p.m. EET', 1, 'gh93', 'Man', '54', 'WO', 'Nee', 'Ja', 'Nee', 'Ja', 'Ja', 'Nee', 'Soms', 'vaak', 'vaak', 'regelmatig', 'soms', 'soms', 'vaak', '(bijna) nooit', 'soms', '(bijna) altijd', 'vaak', '(bijna) nooit', 'binnen een uur', '1 nacht per week', '2-3 keer per nacht', 'nooit', 'heel vaak', 'redelijk goed', '(bijna) nooit', '(bijna) altijd', 'vaak', 'vaak', 'even vaak eens als oneens', 'eens', 'helemaal eens', 'helemaal oneens', 'eens', 'even vaak eens als oneens', 'oneens', 'helemaal eens', 'oneens', 'eens', 'helemaal oneens', 'helemaal oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'oneens', 'even vaak eens als oneens', 'eens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'helemaal oneens'], ['2017/04/01 9:01:28 a.m. EET', 1, 'AB64', 'Vrouw', '49', 'WO', 'Nee', 'Nee', 'Nee', 'Nee', 'Ja', 'Nee', 'Niet van toepassing', 'vaak', 'soms', 'soms', 'soms', 'vaak', 'regelmatig', '(bijna) nooit', 'vaak', 'regelmatig', '(bijna) nooit', '(bijna) nooit', 'binnen een kwartier', 'nooit', '2-3 keer per nacht', 'nooit', 'helemaal niet', 'goed', '(bijna) nooit', 'soms', '(bijna) nooit', '(bijna) altijd', 'even vaak eens als oneens', 'oneens', 'even vaak eens als oneens', 'eens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'helemaal oneens', 'oneens', 'eens', 'eens', 'helemaal oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'eens', 'oneens', 'eens', 'even vaak eens als oneens', 'oneens', 'eens', 'even vaak eens als oneens'], ['2017/04/01 5:17:20 p.m. EET', 1, 'FT12', 'Man', '51', 'WO', 'Nee', 'Nee', 'Nee', 'Nee', 'Nee', 'Nee', 'Niet van toepassing', 'regelmatig', 'vaak', 'vaak', 'soms', 'soms', 'soms', 'regelmatig', 'soms', 'vaak', 'soms', 'soms', 'binnen een kwartier', '1 nacht per week', '4-5 keer per nacht', '1 nacht per week', 'een beetje', 'redelijk goed', 'soms', 'soms', 'soms', 'soms', 'eens', 'oneens', 'even vaak eens als oneens', 'oneens', 'oneens', 'eens', 'even vaak eens als oneens', 'oneens', 'eens', 'eens', 'oneens', 'oneens', 'eens', 'eens', 'oneens', 'even vaak eens als oneens', 'eens', 'oneens', 'eens', 'eens', 'eens'], ['2017/04/01 9:29:43 p.m. EET', 1, 'MJ87', 'Vrouw', '23', 'WO', 'Nee', 'Nee', 'Nee', 'Nee', 'Nee', 'Nee', 'Niet van toepassing', 'regelmatig', 'regelmatig', 'vaak', 'soms', 'soms', 'soms', 'soms', 'soms', 'regelmatig', '(bijna) nooit', 'soms', 'binnen een half uur', '1 nacht per week', 'nooit', '2-3 nachten per week', 'een beetje', 'goed', 'soms', 'soms', 'soms', '(bijna) altijd', 'even vaak eens als oneens', 'helemaal oneens', 'oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'helemaal oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'oneens', 'oneens', 'oneens', 'eens', 'oneens', 'even vaak eens als oneens', 'oneens', 'oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'oneens'], ['2017/04/01 11:08:39 p.m. EET', 1, 'PM61', 'Man', '25', 'HBO', 'Nee', 'Nee', 'Nee', 'Ja', 'Ja', 'Nee', 'Nooit', 'regelmatig', 'regelmatig', 'soms', 'vaak', 'regelmatig', 'regelmatig', 'regelmatig', 'regelmatig', 'soms', 'regelmatig', 'vaak', 'binnen een uur', '2-3 nachten per week', 'nooit', 'nooit', 'enigszins', 'redelijk goed', 'vaak', 'regelmatig', 'vaak', 'vaak', 'eens', 'helemaal eens', 'oneens', 'helemaal oneens', 'oneens', 'oneens', 'eens', 'eens', 'oneens', 'eens', 'eens', 'helemaal oneens', 'eens', 'oneens', 'helemaal eens', 'helemaal oneens', 'oneens', 'eens', 'eens', 'eens', 'eens'], ['2017/04/01 10:53:53 a.m. EET', 1, 'JL25', 'Vrouw', '44', 'HBO', 'Nee', 'Nee', 'Nee', 'Nee', 'Ja', 'Nee', 'Soms', 'vaak', 'regelmatig', 'regelmatig', 'soms', 'regelmatig', 'regelmatig', 'soms', 'soms', 'regelmatig', 'soms', 'soms', 'binnen een half uur', '1 nacht per week', '2-3 keer per nacht', '2-3 nachten per week', 'een beetje', 'redelijk goed', 'soms', 'soms', 'regelmatig', 'regelmatig', 'even vaak eens als oneens', 'even vaak eens als oneens', 'oneens', 'helemaal oneens', 'eens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'oneens', 'eens', 'even vaak eens als oneens', 'oneens', 'eens', 'even vaak eens als oneens', 'helemaal eens', 'oneens', 'even vaak eens als oneens', 'oneens', 'even vaak eens als oneens', 'eens', 'even vaak eens als oneens'], ['2017/04/01 12:22:06 a.m. EET', 1, 'GW98', 'Man', '28', 'WO', 'Nee', 'Nee', 'Ja', 'Nee', 'Nee', 'Nee', 'Nooit', '(bijna) altijd', '(bijna) nooit', 'vaak', '(bijna) altijd', 'soms', '(bijna) altijd', '(bijna) nooit', 'regelmatig', 'soms', 'regelmatig', 'vaak', 'binnen een kwartier', 'nooit', 'nooit', 'nooit', 'een beetje', 'goed', '(bijna) altijd', '(bijna) altijd', '(bijna) nooit', '(bijna) altijd', 'oneens', 'even vaak eens als oneens', 'eens', 'helemaal oneens', 'oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'oneens', 'oneens', 'even vaak eens als oneens', 'eens', 'helemaal oneens', 'helemaal eens', 'oneens', 'helemaal eens', 'helemaal oneens', 'eens', 'eens', 'oneens', 'eens', 'even vaak eens als oneens'], ['2017/04/01 7:35:17 p.m. EET', 1, 'HA61', 'Man', '51', 'WO', 'Nee', 'Nee', 'Nee', 'Nee', 'Ja', 'Nee', 'Niet van toepassing', '(bijna) nooit', 'vaak', 'vaak', 'soms', 'soms', 'soms', 'regelmatig', 'soms', 'regelmatig', '(bijna) nooit', '(bijna) nooit', 'binnen een half uur', 'nooit', '2-3 keer per nacht', '4-5 nachten per week', 'vaak', 'slecht', '(bijna) nooit', 'soms', '(bijna) nooit', 'regelmatig', 'even vaak eens als oneens', 'oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'eens', 'even vaak eens als oneens', 'helemaal oneens', 'even vaak eens als oneens', 'eens', 'oneens', 'helemaal oneens', 'eens', 'even vaak eens als oneens', 'oneens', 'even vaak eens als oneens', 'helemaal oneens', 'oneens', 'eens', 'even vaak eens als oneens', 'oneens'], ['2017/04/01 8:55:08 a.m. EET', 1, 'wh18', 'Vrouw', '70', 'MBO', 'Nee', 'Nee', 'Nee', 'Nee', 'Nee', 'Nee', 'Nooit', 'soms', 'soms', '(bijna) altijd', '(bijna) nooit', '(bijna) nooit', '(bijna) nooit', '(bijna) nooit', '(bijna) nooit', '(bijna) altijd', '(bijna) nooit', '(bijna) nooit', 'binnen een kwartier', 'nooit', '2-3 keer per nacht', '1 nacht per week', 'helemaal niet', 'redelijk goed', '(bijna) nooit', '(bijna) nooit', '(bijna) nooit', 'vaak', 'even vaak eens als oneens', 'oneens', 'even vaak eens als oneens', 'eens', 'oneens', 'eens', 'oneens', 'oneens', 'eens', 'oneens', 'helemaal oneens', 'helemaal oneens', 'even vaak eens als oneens', 'oneens', 'oneens', 'eens', 'oneens', 'oneens', 'eens', 'oneens', 'oneens'], ['2017/04/01 8:14:46 p.m. EET', 1, 'he46', 'Man', '44', 'WO', 'Nee', 'Ja', 'Nee', 'Nee', 'Ja', 'Nee', 'Niet van toepassing', 'vaak', 'regelmatig', 'soms', 'vaak', 'vaak', 'vaak', '(bijna) nooit', 'vaak', 'soms', 'soms', 'soms', 'binnen een half uur', '2-3 nachten per week', '1 keer per nacht', '1 nacht per week', 'een beetje', 'slecht', 'vaak', 'vaak', 'soms', 'vaak', 'even vaak eens als oneens', 'even vaak eens als oneens', 'eens', 'oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'eens', 'even vaak eens als oneens', 'eens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens']]
        >>> print_columns("consent", demo_data)
        <BLANKLINE>
        consent is: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    :example (list of target columns as input):
        >>> replacements_dictionary = {"oneens":1, "eens":2, "even vaak eens als oneens":3, "helemaal oneens":4, "x":5}
        >>> print_columns("sc_9", demo_data)
        <BLANKLINE>
        sc_9 is: ['oneens', 'even vaak eens als oneens', 'eens', 'eens', 'oneens', 'oneens', 'even vaak eens als oneens', 'eens', 'helemaal oneens', 'oneens', 'eens']
        >>> transform_column_values(replacements_dictionary, ["sc_9", "sc_10"], demo_data)
        [['date', 'consent', 'id', 'sex', 'age', 'edu', 'timezone_change', 'sleep_disorder', 'nightshift', 'psy_disorder', 'wake', 'young_kids', 'partn', 'btptr_1', 'btptr_2', 'btptr_3', 'btptr_4', 'btptr_5', 'btptr_6', 'btptr_7', 'btptr_8', 'btptr_9', 'ats_1', 'atbr_1', 'sq_1', 'sq_2', 'sq_3', 'sq_4', 'sq_5', 'sq_6', 'atbr_2', 'atbr_3', 'ats_2', 'ats_3', 'chron_1', 'chron_2', 'chron_3', 'chron_4', 'chron_5', 'chron_6', 'chron_7', 'chron_8', 'sc_1', 'sc_2', 'sc_3', 'sc_4', 'sc_5', 'sc_6', 'sc_7', 'sc_8', 'sc_9', 'sc_10', 'sc_11', 'sc_12', 'sc_13'], ['2017/04/01 8:35:57 p.m. EET', 1, 'EM11', 'Vrouw', '44', 'HBO', 'Nee', 'Nee', 'Nee', 'Nee', 'Ja', 'Nee', 'Soms', 'soms', '(bijna) altijd', '(bijna) altijd', 'soms', '(bijna) nooit', 'soms', '(bijna) altijd', '(bijna) nooit', '(bijna) altijd', '(bijna) nooit', '(bijna) nooit', 'binnen een kwartier', 'nooit', 'nooit', 'nooit', 'een beetje', 'erg goed', '(bijna) nooit', '(bijna) nooit', 'vaak', '(bijna) altijd', 'helemaal eens', 'helemaal oneens', 'helemaal oneens', 'helemaal eens', 'oneens', 'helemaal eens', 'helemaal eens', 'helemaal oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'helemaal oneens', 'helemaal oneens', 'oneens', 'eens', 'even vaak eens als oneens', 'eens', 1, 2, 'even vaak eens als oneens', 'even vaak eens als oneens', 'oneens'], ['2017/04/01 8:15:27 p.m. EET', 1, 'gh93', 'Man', '54', 'WO', 'Nee', 'Ja', 'Nee', 'Ja', 'Ja', 'Nee', 'Soms', 'vaak', 'vaak', 'regelmatig', 'soms', 'soms', 'vaak', '(bijna) nooit', 'soms', '(bijna) altijd', 'vaak', '(bijna) nooit', 'binnen een uur', '1 nacht per week', '2-3 keer per nacht', 'nooit', 'heel vaak', 'redelijk goed', '(bijna) nooit', '(bijna) altijd', 'vaak', 'vaak', 'even vaak eens als oneens', 'eens', 'helemaal eens', 'helemaal oneens', 'eens', 'even vaak eens als oneens', 'oneens', 'helemaal eens', 'oneens', 'eens', 'helemaal oneens', 'helemaal oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'oneens', 3, 2, 'even vaak eens als oneens', 'even vaak eens als oneens', 'helemaal oneens'], ['2017/04/01 9:01:28 a.m. EET', 1, 'AB64', 'Vrouw', '49', 'WO', 'Nee', 'Nee', 'Nee', 'Nee', 'Ja', 'Nee', 'Niet van toepassing', 'vaak', 'soms', 'soms', 'soms', 'vaak', 'regelmatig', '(bijna) nooit', 'vaak', 'regelmatig', '(bijna) nooit', '(bijna) nooit', 'binnen een kwartier', 'nooit', '2-3 keer per nacht', 'nooit', 'helemaal niet', 'goed', '(bijna) nooit', 'soms', '(bijna) nooit', '(bijna) altijd', 'even vaak eens als oneens', 'oneens', 'even vaak eens als oneens', 'eens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'helemaal oneens', 'oneens', 'eens', 'eens', 'helemaal oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'eens', 'oneens', 2, 3, 'oneens', 'eens', 'even vaak eens als oneens'], ['2017/04/01 5:17:20 p.m. EET', 1, 'FT12', 'Man', '51', 'WO', 'Nee', 'Nee', 'Nee', 'Nee', 'Nee', 'Nee', 'Niet van toepassing', 'regelmatig', 'vaak', 'vaak', 'soms', 'soms', 'soms', 'regelmatig', 'soms', 'vaak', 'soms', 'soms', 'binnen een kwartier', '1 nacht per week', '4-5 keer per nacht', '1 nacht per week', 'een beetje', 'redelijk goed', 'soms', 'soms', 'soms', 'soms', 'eens', 'oneens', 'even vaak eens als oneens', 'oneens', 'oneens', 'eens', 'even vaak eens als oneens', 'oneens', 'eens', 'eens', 'oneens', 'oneens', 'eens', 'eens', 'oneens', 'even vaak eens als oneens', 2, 1, 'eens', 'eens', 'eens'], ['2017/04/01 9:29:43 p.m. EET', 1, 'MJ87', 'Vrouw', '23', 'WO', 'Nee', 'Nee', 'Nee', 'Nee', 'Nee', 'Nee', 'Niet van toepassing', 'regelmatig', 'regelmatig', 'vaak', 'soms', 'soms', 'soms', 'soms', 'soms', 'regelmatig', '(bijna) nooit', 'soms', 'binnen een half uur', '1 nacht per week', 'nooit', '2-3 nachten per week', 'een beetje', 'goed', 'soms', 'soms', 'soms', '(bijna) altijd', 'even vaak eens als oneens', 'helemaal oneens', 'oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'helemaal oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'oneens', 'oneens', 'oneens', 'eens', 'oneens', 'even vaak eens als oneens', 1, 1, 'even vaak eens als oneens', 'even vaak eens als oneens', 'oneens'], ['2017/04/01 11:08:39 p.m. EET', 1, 'PM61', 'Man', '25', 'HBO', 'Nee', 'Nee', 'Nee', 'Ja', 'Ja', 'Nee', 'Nooit', 'regelmatig', 'regelmatig', 'soms', 'vaak', 'regelmatig', 'regelmatig', 'regelmatig', 'regelmatig', 'soms', 'regelmatig', 'vaak', 'binnen een uur', '2-3 nachten per week', 'nooit', 'nooit', 'enigszins', 'redelijk goed', 'vaak', 'regelmatig', 'vaak', 'vaak', 'eens', 'helemaal eens', 'oneens', 'helemaal oneens', 'oneens', 'oneens', 'eens', 'eens', 'oneens', 'eens', 'eens', 'helemaal oneens', 'eens', 'oneens', 'helemaal eens', 'helemaal oneens', 1, 2, 'eens', 'eens', 'eens'], ['2017/04/01 10:53:53 a.m. EET', 1, 'JL25', 'Vrouw', '44', 'HBO', 'Nee', 'Nee', 'Nee', 'Nee', 'Ja', 'Nee', 'Soms', 'vaak', 'regelmatig', 'regelmatig', 'soms', 'regelmatig', 'regelmatig', 'soms', 'soms', 'regelmatig', 'soms', 'soms', 'binnen een half uur', '1 nacht per week', '2-3 keer per nacht', '2-3 nachten per week', 'een beetje', 'redelijk goed', 'soms', 'soms', 'regelmatig', 'regelmatig', 'even vaak eens als oneens', 'even vaak eens als oneens', 'oneens', 'helemaal oneens', 'eens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'oneens', 'eens', 'even vaak eens als oneens', 'oneens', 'eens', 'even vaak eens als oneens', 'helemaal eens', 'oneens', 3, 1, 'even vaak eens als oneens', 'eens', 'even vaak eens als oneens'], ['2017/04/01 12:22:06 a.m. EET', 1, 'GW98', 'Man', '28', 'WO', 'Nee', 'Nee', 'Ja', 'Nee', 'Nee', 'Nee', 'Nooit', '(bijna) altijd', '(bijna) nooit', 'vaak', '(bijna) altijd', 'soms', '(bijna) altijd', '(bijna) nooit', 'regelmatig', 'soms', 'regelmatig', 'vaak', 'binnen een kwartier', 'nooit', 'nooit', 'nooit', 'een beetje', 'goed', '(bijna) altijd', '(bijna) altijd', '(bijna) nooit', '(bijna) altijd', 'oneens', 'even vaak eens als oneens', 'eens', 'helemaal oneens', 'oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'oneens', 'oneens', 'even vaak eens als oneens', 'eens', 'helemaal oneens', 'helemaal eens', 'oneens', 'helemaal eens', 'helemaal oneens', 2, 2, 'oneens', 'eens', 'even vaak eens als oneens'], ['2017/04/01 7:35:17 p.m. EET', 1, 'HA61', 'Man', '51', 'WO', 'Nee', 'Nee', 'Nee', 'Nee', 'Ja', 'Nee', 'Niet van toepassing', '(bijna) nooit', 'vaak', 'vaak', 'soms', 'soms', 'soms', 'regelmatig', 'soms', 'regelmatig', '(bijna) nooit', '(bijna) nooit', 'binnen een half uur', 'nooit', '2-3 keer per nacht', '4-5 nachten per week', 'vaak', 'slecht', '(bijna) nooit', 'soms', '(bijna) nooit', 'regelmatig', 'even vaak eens als oneens', 'oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'eens', 'even vaak eens als oneens', 'helemaal oneens', 'even vaak eens als oneens', 'eens', 'oneens', 'helemaal oneens', 'eens', 'even vaak eens als oneens', 'oneens', 'even vaak eens als oneens', 4, 1, 'eens', 'even vaak eens als oneens', 'oneens'], ['2017/04/01 8:55:08 a.m. EET', 1, 'wh18', 'Vrouw', '70', 'MBO', 'Nee', 'Nee', 'Nee', 'Nee', 'Nee', 'Nee', 'Nooit', 'soms', 'soms', '(bijna) altijd', '(bijna) nooit', '(bijna) nooit', '(bijna) nooit', '(bijna) nooit', '(bijna) nooit', '(bijna) altijd', '(bijna) nooit', '(bijna) nooit', 'binnen een kwartier', 'nooit', '2-3 keer per nacht', '1 nacht per week', 'helemaal niet', 'redelijk goed', '(bijna) nooit', '(bijna) nooit', '(bijna) nooit', 'vaak', 'even vaak eens als oneens', 'oneens', 'even vaak eens als oneens', 'eens', 'oneens', 'eens', 'oneens', 'oneens', 'eens', 'oneens', 'helemaal oneens', 'helemaal oneens', 'even vaak eens als oneens', 'oneens', 'oneens', 'eens', 1, 1, 'eens', 'oneens', 'oneens'], ['2017/04/01 8:14:46 p.m. EET', 1, 'he46', 'Man', '44', 'WO', 'Nee', 'Ja', 'Nee', 'Nee', 'Ja', 'Nee', 'Niet van toepassing', 'vaak', 'regelmatig', 'soms', 'vaak', 'vaak', 'vaak', '(bijna) nooit', 'vaak', 'soms', 'soms', 'soms', 'binnen een half uur', '2-3 nachten per week', '1 keer per nacht', '1 nacht per week', 'een beetje', 'slecht', 'vaak', 'vaak', 'soms', 'vaak', 'even vaak eens als oneens', 'even vaak eens als oneens', 'eens', 'oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens', 'eens', 'even vaak eens als oneens', 2, 3, 'even vaak eens als oneens', 'even vaak eens als oneens', 'even vaak eens als oneens']]
        >>> print_columns("sc_9", demo_data)
        <BLANKLINE>
        sc_9 is: [1, 3, 2, 2, 1, 1, 3, 2, 4, 1, 2]

    """

    #############################################################################################################

    from preprocessor.select_column import select_column
    from preprocessor.replace_column import replace_column
    from preprocessor.print_columns import print_columns

    # If target_column_headers_list is not a list but a string (i.e., target is a single column)...
    # Convert this string to a single list item so that the upcoming lines in the function can still take it as input.
    if type(target_column_headers_list) is str:  # If parameter is string
        target_column_headers_list = [target_column_headers_list]  # Convert it to a list

    # Separate headers from data
    # headers_list = get_headers(dataset)
    # data = get_data(dataset)

    # Separate the dictionary to targets and replacements
    targets_list = []
    replacements_list = []
    for i, key in enumerate(target_replacement_dictionary):  # iterate over each item in the input dictionary
        targets_list.append(key)  # add keys to targets list
        replacements_list.append(target_replacement_dictionary[key])  # add values to replacements list

    # Extract values of the specified column in the given dataset by using a separate headers variable
    columns = {}
    for i, target_column_header in enumerate(target_column_headers_list):
        columns[target_column_header] = select_column(target_column_header, dataset)
        # and not 'data'; the headers in 'dataset' is necessary for the select_column() to work.

    # Search targets in each of the extracted columns, and when the target values are found, replace them
    # with their counterparts specific in the dictionary.
    for column in columns:
        for i, target in enumerate(targets_list):
            for j, value in enumerate(columns[column]):
                if value == target:
                    columns[column][j] = replacements_list[i]

    # Replace columns within a copy of the provided dataset and return this dataset
    for col_name, col_values in columns.items():
        replace_column(col_values, col_name, dataset)  # and not 'data' but 'dataset', which includes headers

    return dataset  # and not 'data' but 'dataset', which includes headers
