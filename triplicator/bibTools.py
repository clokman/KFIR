class Bibliography:
    """
    Creates a 'Bibliography' class instance.

    Bibliography classs objects entail a collection of variables and functions that gives control over naming and
    formatting of variables during bibliography to triple (i.e., RDF) conversion.

    Returns:
        A Bibliography class object.

    Examples:
        >>> # import class and instantiate a Bibliography object.
        >>> from triplicator.bibTools import Bibliography
        >>> my_bibliography = Bibliography()

        >>> # add entries to the instance
        >>> my_bibliography.setEntry('01', 'author', 'John Can Lokman')
        >>> my_bibliography.setEntry('01', 'title', 'A title')
        >>> my_bibliography.setEntry('02', 'title', 'Another title')
        >>> my_bibliography.entries
        {'01': {'author': 'John Can Lokman', 'title': 'A title'}, '02': {'title': 'Another title'}}
    """
    _class_instance_registry     = []   # will contain all instances created in this class
    _class_id_registry           = []   # will hold all instance ids created in this class
    _class_field_values_registry = {}   # will hold all field name-value pairs and entry ids associated
                                        # ...with field values.
    # ...this enables fast searching for field values such as author names, etc.
    # ...across bibliographies.

    def __init__(instance):
        """
        Constructor for Bibliography Class Instance.

        It creates an empty Bibliography object, which can later be populated by using e.g., .setEntry or .import
        methods.

        """
        # adds the instance to the list of all instances of the class
        Bibliography._class_instance_registry.append(instance)

        # local equivalent of _class_field_values_registry. Does the same thing for the bibliography instance.
        instance._field_values_registry = {}

        # hold all ids created within the bibliography instance. allows quick checking whether an id exists.
        instance._id_registry = []

        # dictionary for holding all field types and number of their occurrences
        instance._field_type_registry = {}

        # dictionary that holds all entries. this is where the bibliography data is held, including ids & field values.
        instance.entries = {}

        instance.no_of_enrichments_made_in_last_operation = 0
        instance.no_of_additions_made_in_last_operation = 0

        instance.log_file_path = 'log.txt'

    ###################################################################################################################
    ############################################### IMPORT FUNCTIONS ##################################################
    ###################################################################################################################

    def importBib(instance, path_of_file_to_import, conversion_arguments_list='bib_default', verbose_import=False, show_progress_bar=False):
        """
        Parses a Bibliography class object from a .bib file. During parsing, field names in the bib file is converted
        to names (i.e., strings) specified in conversation_conversion_arguments_list.

        Args:
            path_of_file_to_import(str): Location of the .bib file to be parsed
            conversion_arguments_list(str or list):A list of lists that contains arguments to be passed to
                bibliography_intance.setEntry(entry_id, TARGET_FIELD, FORMATTING ALGORITHM, NEW_FIELD_NAME) method.
                because field names in .bib files is fixed, a custom arguments list will often will not be necessary;
                the hardcoded conversion arguments list will likely be sufficient. However, in cases where
                modifications may still be necessary, the format in the example sublist below should be followed:
                ['each_pybtex_entry.fields["title"]', 'pybtex_document_instance_name', 'b_document'],
            verbose_import (bool): Specifies whether to print the imported entries to console

        Returns:
            Nothing; modifies the object it is called from.

        Examples:
            >>> # Import a .bib object as Bibliography object
            >>> my_bib = Bibliography()
            >>> my_bib.importBib('example_data//test.bib')
            Parsing of example_data//test.bib started
            pybtex package is parsing using bibtex.Parser()...
            pybtex package finished parsing
            Calculating file length...
            <BLANKLINE>
            <BLANKLINE>
            ---------------------------------------------------------------------------------------------------
            example_data//test.bib parsed and imported as Bibliography object.
            <BLANKLINE>
            Fields added to the parsed the Bibliography object:
            {'b_abstract': 2,
             'b_author_labels': 4,
             'b_authors': 4,
             'b_document': 4,
             'b_document_label': 4,
             'b_doi': 2,
             'b_issn': 3,
             'b_issue_number': 1,
             'b_journal': 3,
             'b_journal_label': 3,
             'b_pages': 2,
             'b_publication_month': 4,
             'b_publication_year': 4,
             'b_publisher': 4,
             'b_publisher_label': 4,
             'b_topic_labels': 2,
             'b_topics': 2,
             'b_type': 4,
             'b_volume': 3}
            <BLANKLINE>
            <BLANKLINE>
        """
        from builtins import KeyError
        from pprint import pprint
        from triplicator.pybtexImporter import Pybtex_import
        from meta.consoleOutput import ConsoleOutput
        from preprocessor.Text_File import Log_File

        log_file = Log_File(instance.log_file_path)

        console = ConsoleOutput(log_file_path='log.txt')
        console.log_message('Parsing of %s started' % path_of_file_to_import, add_timestamp_in_file=True)


        # import input data into pybtex_data variable
        pybtex_import_instance = Pybtex_import(path_of_file_to_import)
        pybtex_data = pybtex_import_instance.data

        ########################################################################
        #  Transfer items from pybtex parsed dictionary to output dictionary   #
        ########################################################################

        # In order to shorten the code, a list of arguments is given below, and then passed to the .setFormattedEntry method
        # ... through a for loop. In the list, each line is a (sub-)list of three arguments to be passed.

        # # Without the use of this shortening procedure, a function for each field should be written in try-except
        # # blocks
        # # ... as following:
        # for each_pybtex_entry_id, each_pybtex_entry in pybtex_data.entries.items():
        #     # try-except blocks are necessary for use in for loops, as specified field may not always be present in an entry
        #     try:
        #         output_bibliography.setFormattedEntry(each_pybtex_entry_id, each_pybtex_entry.fields['title'],
        #                                             'pybtex_document_instance_name', 'b_document')
        #     except:
        #         pass

        if conversion_arguments_list == 'bib_default':
           conversion_arguments_list = [
                # [target_field_value in existing data,     formatting_algorithm,               desired_field_name in new object]
                ['each_pybtex_entry.type',                  'none',                             'b_type'],
                ['each_pybtex_entry.fields["title"]',       'pybtex_document_instance_name',    'b_document'],
                ['each_pybtex_entry.fields["title"]',       'pybtex_document_label',            'b_document_label'],
                ['each_pybtex_entry.persons["author"]',     'pybtex_author_instance_name',      'b_authors'],
                ['each_pybtex_entry.persons["author"]',     'pybtex_author_label',              'b_author_labels'],
                ['each_pybtex_entry.fields["keywords"]',    'pybtex_topic_instance_name',       'b_topics'],
                ['each_pybtex_entry.fields["keywords"]',    'pybtex_topic_label',               'b_topic_labels'],
                ['each_pybtex_entry.fields["journal"]',     'pybtex_document_instance_name',    'b_journal'],
                ['each_pybtex_entry.fields["journal"]',     'pybtex_document_label',            'b_journal_label'],
                ['each_pybtex_entry.fields["booktitle"]',   'pybtex_document_instance_name',    'b_parent_book'],
                ['each_pybtex_entry.fields["booktitle"]',   'pybtex_document_label',            'b_parent_book_label'],
                ['each_pybtex_entry.fields["publisher"]',   'pybtex_document_instance_name',    'b_publisher'],
                ['each_pybtex_entry.fields["publisher"]',   'pybtex_document_label',            'b_publisher_label'],
                ['each_pybtex_entry.fields["year"]',        'none',                             'b_publication_year'],
                ['each_pybtex_entry.fields["month"]',       'none',                             'b_publication_month'],
                ['each_pybtex_entry.fields["number"]',      'none',                             'b_issue_number'],
                ['each_pybtex_entry.fields["volume"]',      'none',                             'b_volume'],
                ['each_pybtex_entry.fields["pages"]',       'none',                             'b_pages'],
                ['each_pybtex_entry.fields["doi"]',         'none',                             'b_doi'],
                ['each_pybtex_entry.fields["issn"]',        'none',                             'b_issn'],
                ['each_pybtex_entry.fields["isbn"]',        'none',                             'b_isbn'],
                ['each_pybtex_entry.fields["edition"]',     'none',                             'b_edition'],
                ['each_pybtex_entry.fields["abstract"]',    'none',                             'b_abstract'],
                ['each_pybtex_entry.fields["note"]',        'none',                             'b_note']
            ]

        # if conversion_arguments_list is provided, proceed without modifying the provided arguments list
        elif type(conversion_arguments_list) is list:
            pass
        # if conversion_arguments_list is neither hardcoded nor provided, return error.
        else:
            raise ValueError("Conversion_arguments_list parameter should be either 'bib_default' or be a list that "
                              "contains at least one list of arguments.")

        # variables for progress bar
        current_progress = 0
        console.log_message('Calculating file length...', add_timestamp_in_file=True)
        maximum_progress = len(pybtex_data.entries.items())

        # loop through individual reference entries in the parsed pybtex bib file
        for each_pybtex_entry_id, each_pybtex_entry in pybtex_data.entries.items():
            # loop through each line in the conversion_arguments_list
            for each_argument_list in conversion_arguments_list:
                # try using the elements of each sub-list in conversion_arguments_list as arguments of .setFormattedEntry method
                # (try-except block is necessary, as each field may not exist for each entry)
                try:
                    instance.setFormattedEntry(each_pybtex_entry_id, eval(each_argument_list[0]),
                                               each_argument_list[1], each_argument_list[2])
                except KeyError:
                    pass

            if show_progress_bar:  # default is false to prevent very long test outputs
                console.print_current_progress(current_progress, maximum_progress,
                                               'Parsing file "%s"' % path_of_file_to_import)
                current_progress += 1

            # if process should be printed to terminal
            if verbose_import:
                # print each imported entry to console in {entry_id:entry_data} format
                pprint({each_pybtex_entry_id: instance.getEntryById(each_pybtex_entry_id)}, compact=True)
                print(
                    "=============================================================================================="
                    "==================")

        ########################################################################

        # SERIES_TITLE AND ID -- To be implemented if needed
        # This has to be kept out of the main loop, as series is not a field, but a whole bibliography entry
        # themselves.
        # They are not nested within individual entries, and are rather parallel to them.
        # Some older code from previous versions, which extracts and converts series title:
        # try:
        #    # collection refers to a full reference entity, and this is why the title of the collection is nested quite
        #    # ...deeper than other elements parsed before in this script
        #    for series_id in pybtex_data.entries[each_pybtex_entry_id].collection.entries:
        #        print series_id, each_pybtex_entry_id
        #        #bibDictionary[each_pybtex_entry_id].append({"is_part_of_series_with_title":[each_pybtex_entry_id].fields["title"].encode("ascii",errors="ignore")
        #        bibDictionary[each_pybtex_entry_id].append({"is_part_of_series_with_id":series_id})
        #        #[each_pybtex_entry_id].fields["title"].encode("ascii",errors="ignore")
        ## field missing from bibliography
        # except(KeyError):
        #    pass


        ########################
        #  OPERATION SUMMARY   #
        ########################

        # Print and log success message
        import_complete_message = path_of_file_to_import + ' ' + 'parsed and imported as Bibliography object.'
        print('\n\n-----------------------------------------------------------------------------------------------'
              '----')
        console.log_message(import_complete_message, add_timestamp_in_file=True)

        # Print and log statistics about the import operation
        # TODO: print total number of imported entries
        console.log_message("\nFields added to the parsed the Bibliography object:")
        instance.summarize()
        for each_key, each_value in instance._field_type_registry.items():
            log_file.append_line(str(each_key) + ': ' + str(each_value))

        # Print and log a sample from parsed entries
        console.log_message("\n")
        instance.write_preview_to_log(number_of_entries_to_preview=3)


    def importCsv(instance,
                  path_of_file_to_import,
                  csv_delimiter_character,
                  field_value_list_separator,
                  id_column_header,
                  conversion_arguments_list,
                  cleaning_algorithm=None,
                  verbose_import=False
    ):
        """
        Parses a Bibliography class object from a .csv file.

        Args:
            path_of_file_to_import(str): Location of the .csv file to be parsed
            csv_delimiter_character(str): One-character-long string that separates the columns of the CSV file.
            field_value_list_separator:(str): One- or multi-character-long string that separates multiple
                values in a cell.
            id_column_header(str): Header of the id column
            conversion_arguments_list(str or list): A list of lists that contains arguments to be passed to
                bibliography_intance.setEntry(entry_id, TARGET_FIELD, FORMATTING ALGORITHM, NEW_FIELD_NAME) method.
                a custom arguments list will look like this:
                ['each_entry_data["titles"]', 'pybtex_document_label', 'b_document_label']
            cleaning_algorithm(str): CSV cleaning algorithm that will be executed in .cleanAndTokenizeCsv() method of
                CSV_container class in csvImporter module.
            verbose_import(bool): Specifies whether to print the imported entries to console

        Keyword Args:
            "open citations" (conversion_arguments_list): Calls a list of lists that holds arguments for .setEntry
                method. An example sub-list from conversion_arguments_list is:
                ['each_entry_data["titles"]', 'pybtex_document_instance_name', 'b_document']
            "open citations" (cleaning_algorithm): Cleans commas that occur in entry field values using an algorithm
                tuned for CSV files downloaded from Open Citatons.
            "parse only" (cleaning_algorithm): Skips cleaning

        Returns:
            Nothing; modifies the object it is called from.

        Examples:
            # import a csv object
            >>> my_csv_bibliography = Bibliography()
            >>> my_csv_bibliography.importCsv(path_of_file_to_import='example_data//test.csv',
            ...                                conversion_arguments_list='open citations',
            ...                                cleaning_algorithm="open citations",
            ...                                csv_delimiter_character=',',
            ...                                field_value_list_separator=' | ',
            ...                                id_column_header='referenceEntry',
            ...                                verbose_import=False
            ... )
            <BLANKLINE>
            <BLANKLINE>
            ---------------------------------------------------------------------------------------------------
            example_data//test.csv imported.
            <BLANKLINE>
            Fields added to the parsed bibliography:
            {'b_author_labels': 7,
             'b_authors': 7,
             'b_document': 7,
             'b_document_label': 7,
             'b_doi': 7,
             'b_publication': 7,
             'b_publication_label': 7,
             'b_publication_type': 7,
             'b_publication_year': 7,
             'b_publisher': 7,
             'b_publisher_label': 7,
             'b_type': 7}

            >>> # create a Bibliography instance by using custom conversion_arguments_list
            >>> custom_arguments_list = [
            ...     ['each_entry_data["titles"]', 'pybtex_document_instance_name', 'x_document'],
            ...     ['each_entry_data["titles"]', 'pybtex_document_label',         'x_document_label']
            ... ]
            >>> my_custom_bibliography = Bibliography()
            >>> my_custom_bibliography.importCsv(path_of_file_to_import='example_data//test.csv',
            ...                                    conversion_arguments_list=custom_arguments_list,
            ...                                    cleaning_algorithm="open citations",
            ...                                    csv_delimiter_character=',',
            ...                                    field_value_list_separator=' | ',
            ...                                    id_column_header='referenceEntry',
            ...                                    verbose_import=False
            ... )
            <BLANKLINE>
            <BLANKLINE>
            ---------------------------------------------------------------------------------------------------
            example_data//test.csv imported.
            <BLANKLINE>
            Fields added to the parsed bibliography:
            {'x_document': 7, 'x_document_label': 7}
            >>> my_custom_bibliography.preview(1)
            <BLANKLINE>
            ----------------------------------ENTRY 1----------------------------------
            ('https://w3id.org/oc/corpus/br/44493',
             {'x_document': 'Midwife-led_continuity_models_versus_other_models_of_care_for_childbearing_women',
              'x_document_label': 'Midwife-led continuity models versus other models of '
                                  'care for childbearing women'})
            <BLANKLINE>
        """
        from triplicator.csvImporter import CSV_container

        # pass functions to CSV container and create an instance of CSV_container class
        csv_container = CSV_container(csv_file_path=path_of_file_to_import,
                                      id_column_header=id_column_header,
                                      field_value_list_separator=field_value_list_separator,
                                      csv_delimiter_character=csv_delimiter_character,
                                      cleaning_algorithm=cleaning_algorithm
        )

        if conversion_arguments_list == 'open citations':

            conversion_arguments_list = [
                # [target_field_value in existing data,     formatting_algorithm,                   desired_field_name in new object]
                ['each_entry_data["titles"]', 'pybtex_document_instance_name', 'b_document'],
                ['each_entry_data["titles"]', 'pybtex_document_label', 'b_document_label'],
                ['each_entry_data["dois"]', 'open_citations_list_minimizer', 'b_doi'],
                ['each_entry_data["authors"]', 'open_citations_author_instance_name', 'b_authors'],
                ['each_entry_data["authors"]', 'open_citations_author_label', 'b_author_labels'],
                ['each_entry_data["publications"]', 'pybtex_document_instance_name', 'b_publication'],
                ['each_entry_data["publications"]', 'pybtex_document_label', 'b_publication_label'],
                ['each_entry_data["publication_types"]', 'open_citations_list_minimizer_2', 'b_publication_type'],
                ['each_entry_data["types"]', 'open_citations_list_minimizer_2', 'b_type'],
                ['each_entry_data["years"]', 'open_citations_list_minimizer', 'b_publication_year'],
                ['each_entry_data["publishers"]', 'pybtex_document_instance_name', 'b_publisher'],
                ['each_entry_data["publishers"]', 'pybtex_document_label', 'b_publisher_label']
            ]

        elif conversion_arguments_list == 'open citations with citations':
        # "publication_type" , "journal_article" , "journal_issue_number" , "journal_volume_number" , "startEndPages" , "publisher_name" , "cited_by_article"
            conversion_arguments_list = [
                # [target_field_value in existing data,  formatting_algorithm,                   desired_field_name in new object]
                ['each_entry_data["publication_type"]',  'open_citations_list_minimizer_2',     'b_type'],
                ['each_entry_data["title"]',             'pybtex_document_instance_name',       'b_document'],
                ['each_entry_data["title"]',             'pybtex_document_label',               'b_document_label'],
                ['each_entry_data["doi"]',               'open_citations_list_minimizer',       'b_doi'],
                ['each_entry_data["author_name"]',       'open_citations_author_instance_name', 'b_authors'],
                ['each_entry_data["author_name"]',       'open_citations_author_label',         'b_author_labels'],
                ['each_entry_data["journal_name"]',      'pybtex_document_instance_name',       'b_publication'],
                ['each_entry_data["journal_name"]',      'pybtex_document_label',               'b_publication_label'],
                ['each_entry_data["publication_type"]',  'open_citations_list_minimizer_2',     'b_publication_type'],
                ['each_entry_data["publication_year"]',  'open_citations_list_minimizer',       'b_publication_year'],
                ['each_entry_data["publisher_name"]',    'pybtex_document_instance_name',       'b_publisher'],
                ['each_entry_data["publisher_name"]',    'pybtex_document_label',               'b_publisher_label'],
                ['each_entry_data["cited_by_article"]',  'none',                                'b_cited_by'],
                ['each_entry_data["cited_the_article"]', 'none',                                'b_cited']
            ]

        # if a custom conversion_arguments_list is provided, proceed without modifying the provided list
        elif type(conversion_arguments_list) is list:
            pass

        else:
            raise ValueError("Conversion_arguments_list parameter should be either left blank or be a list that "
                             "contains sublists of arguments.")

        # loop through individual reference entries in the parsed pybtex bib file
        for each_entry_id, each_entry_data in csv_container.entries.items():
            # and while doing that, also loop through each line in the conversion_arguments_list
            for each_argument_list in conversion_arguments_list:
                # try using the elements of each sub-list in conversion_arguments_list as arguments of
                # .setFormattedEntry method
                # (try-except block is necessary, as each field may not exist for each entry)
                try:
                    instance.setFormattedEntry(each_entry_id, eval(each_argument_list[0]),
                                               each_argument_list[1], each_argument_list[2])
                except:
                    # TODO: Restore this line (replaced it with a more forgiving except statement for now)
                    # except KeyError:
                    pass

            if verbose_import:
                from pprint import pprint
                pprint({each_entry_id: instance.getEntryById(each_entry_id)}, compact=True)
                print(
                    "================================================================================================================")

        ########################
        #  OPERATION SUMMARY   #
        ########################

        print('\n\n---------------------------------------------------------------------------------------------------')
        print(path_of_file_to_import + ' ' + 'imported.')

        print("\nFields added to the parsed bibliography:")
        instance.summarize()

    # def import_data(instance, path_of_file_to_import, conversion_arguments_list='defaults',
    #                 csv_import_arguments=None, verbose_import=False):
    #     # if the file name ends with '.bib'
    #     # TODO: This is a draft if statement. Condition must be updated to something like 'if re.match('$.bib'):'
    #     if '.bib' in path_of_file_to_import:
    #
    #         from builtins import KeyError
    #         from triplicator.pybtexImporter import Pybtex_import
    #
    #         # import input data into pybtex_data variable
    #         pybtex_import_instance = Pybtex_import(path_of_file_to_import)
    #         pybtex_data = pybtex_import_instance.data
    #
    #         ########################################################################
    #         #  Transfer items from pybtex parsed dictionary to output dictionary   #
    #         ########################################################################
    #
    #         # In order to shorten the code, a list of arguments is given below, and then passed to the .setFormattedEntry method
    #         # ... through a for loop. In the list, each line is a (sub-)list of three arguments to be passed.
    #
    #         # # Without the use of this shortening procedure, a function for each field should be written in try-except
    #         # # blocks
    #         # # ... as following:
    #         # for each_pybtex_entry_id, each_pybtex_entry in pybtex_data.entries.items():
    #         #     # try-except blocks are necessary for use in for loops, as specified field may not always be present in an entry
    #         #     try:
    #         #         output_bibliography.setFormattedEntry(each_pybtex_entry_id, each_pybtex_entry.fields['title'],
    #         #                                             'pybtex_document_instance_name', 'b_document')
    #         #     except:
    #         #         pass
    #
    #
    #         if conversion_arguments_list == 'defaults':
    #            conversion_arguments_list = [
    #                 # [target_field_value in existing data,     formatting_algorithm,               desired_field_name in new object]
    #                 ['each_pybtex_entry.type',                  'none',                             'b_type'],
    #                 ['each_pybtex_entry.fields["title"]',       'pybtex_document_instance_name',    'b_document'],
    #                 ['each_pybtex_entry.fields["title"]',       'pybtex_document_label',            'b_document_label'],
    #                 ['each_pybtex_entry.persons["author"]',     'pybtex_author_instance_name',      'b_authors'],
    #                 ['each_pybtex_entry.persons["author"]',     'pybtex_author_label',              'b_author_labels'],
    #                 ['each_pybtex_entry.fields["keywords"]',    'pybtex_topic_instance_name',       'b_topics'],
    #                 ['each_pybtex_entry.fields["keywords"]',    'pybtex_topic_label',               'b_topic_labels'],
    #                 ['each_pybtex_entry.fields["journal"]',     'pybtex_document_instance_name',    'b_journal'],
    #                 ['each_pybtex_entry.fields["journal"]',     'pybtex_document_label',            'b_journal_label'],
    #                 ['each_pybtex_entry.fields["booktitle"]',   'pybtex_document_instance_name',    'b_parent_book'],
    #                 ['each_pybtex_entry.fields["booktitle"]',   'pybtex_document_label',            'b_parent_book_label'],
    #                 ['each_pybtex_entry.fields["publisher"]',   'pybtex_document_instance_name',    'b_publisher'],
    #                 ['each_pybtex_entry.fields["publisher"]',   'pybtex_document_label',            'b_publisher_label'],
    #                 ['each_pybtex_entry.fields["year"]',        'none',                             'b_publication_year'],
    #                 ['each_pybtex_entry.fields["month"]',       'none',                             'b_publication_month'],
    #                 ['each_pybtex_entry.fields["number"]',      'none',                             'b_issue_number'],
    #                 ['each_pybtex_entry.fields["volume"]',      'none',                             'b_volume'],
    #                 ['each_pybtex_entry.fields["pages"]',       'none',                             'b_pages'],
    #                 ['each_pybtex_entry.fields["doi"]',         'none',                             'b_doi'],
    #                 ['each_pybtex_entry.fields["issn"]',        'none',                             'b_issn'],
    #                 ['each_pybtex_entry.fields["isbn"]',        'none',                             'b_isbn'],
    #                 ['each_pybtex_entry.fields["edition"]',     'none',                             'b_edition'],
    #                 ['each_pybtex_entry.fields["abstract"]',    'none',                             'b_abstract'],
    #                 ['each_pybtex_entry.fields["note"]',        'none',                             'b_note']
    #             ]
    #
    #         # if conversion_arguments_list is provided, proceed without modifying the provided arguments list
    #         elif type(conversion_arguments_list) is list:
    #             pass
    #         # if conversion_arguments_list is neither hardcoded nor provided, return error.
    #         else:
    #             raise ValueError("Conversion_arguments_list parameter should be either left blank or be a list that "
    #                               "contains at least one list of arguments.")
    #
    #
    #         # loop through individual reference entries in the parsed pybtex bib file
    #         for each_pybtex_entry_id, each_pybtex_entry in pybtex_data.entries.items():
    #             # loop through each line in the conversion_arguments_list
    #             for each_argument_list in conversion_arguments_list:
    #                 # try using the elements of each sub-list in conversion_arguments_list as arguments of .setFormattedEntry method
    #                 # (try-except block is necessary, as each field may not exist for each entry)
    #                 try:
    #                     instance.setFormattedEntry(each_pybtex_entry_id, eval(each_argument_list[0]),
    #                                                each_argument_list[1], each_argument_list[2])
    #                 except KeyError:
    #                     pass
    #             # if process should be printed to terminal
    #             if verbose_import:
    #                 # print each imported entry to console in {entry_id:entry_data} format
    #                 from pprint import pprint
    #                 pprint({each_pybtex_entry_id: instance.getEntryById(each_pybtex_entry_id)}, compact=True)
    #                 print(
    #                     "=============================================================================================="
    #                     "==================")
    #
    #         ########################################################################
    #
    #         # SERIES_TITLE AND ID -- To be implemented if needed
    #         # This has to be kept out of the main loop, as series is not a field, but a whole bibliography entry
    #         # themselves.
    #         # They are not nested within individual entries, and are rather parallel to them.
    #         # Some older code from previous versions, which extracts and converts series title:
    #         # try:
    #         #    # collection refers to a full reference entity, and this is why the title of the collection is nested quite
    #         #    # ...deeper than other elements parsed before in this script
    #         #    for series_id in pybtex_data.entries[each_pybtex_entry_id].collection.entries:
    #         #        print series_id, each_pybtex_entry_id
    #         #        #bibDictionary[each_pybtex_entry_id].append({"is_part_of_series_with_title":[each_pybtex_entry_id].fields["title"].encode("ascii",errors="ignore")
    #         #        bibDictionary[each_pybtex_entry_id].append({"is_part_of_series_with_id":series_id})
    #         #        #[each_pybtex_entry_id].fields["title"].encode("ascii",errors="ignore")
    #         ## field missing from bibliography
    #         # except(KeyError):
    #         #    pass
    #
    #
    #         ########################
    #         #  OPERATION SUMMARY   #
    #         ########################
    #         # Print statistics about the import operation to console
    #
    #         # display path and name of the imported file
    #         print('\n\n-----------------------------------------------------------------------------------------------'
    #               '----')
    #         print(path_of_file_to_import + ' ' + 'imported.')
    #
    #         # TODO: print total number of imported entries
    #
    #         # print how many times each field is imported
    #         print("\nFields added to the parsed bibliography:")
    #         instance.summarize()
    #
    #
    #     ########################
    #     #       CSV IMPORT     #
    #     #######################
    #     # if file to import is a .csv file
    #
    #     elif '.csv' in path_of_file_to_import:
    #         from triplicator.csvImporter import CSV_container
    #         ###### IMPORT SETTINGS #######################################
    #         # if the file type being imported is .csv, import arguments must be specified
    #         if csv_import_arguments is None:
    #             raise ValueError("For .csv import operation, a .csv import algorithm must be specified.")
    #
    #         # create a CSV_container instance with the following configuration
    #         elif csv_import_arguments == 'open citations':
    #             csv_container = CSV_container(csv_file_path             = path_of_file_to_import,
    #                                         id_column_header            = 'referenceEntry',
    #                                         field_value_list_separator  = ' | ',
    #                                         csv_delimiter_character     = ',',
    #                                         cleaning_algorithm          = "open citations"
    #             )
    #         else:
    #             raise ValueError("Unknown import algorithm.")
    #         #############################################################
    #
    #         if conversion_arguments_list is 'defaults':
    #
    #             conversion_arguments_list = [
    #                 # [target_field_value in existing data,     formatting_algorithm,                   desired_field_name in new object]
    #                 ['each_entry_data["titles"]',               'pybtex_document_instance_name',        'b_document'],
    #                 ['each_entry_data["titles"]',               'pybtex_document_label',                'b_document_label'],
    #                 ['each_entry_data["dois"]',                 'open_citations_list_minimizer',        'b_doi'],
    #                 ['each_entry_data["authors"]',              'open_citations_author_instance_name',  'b_authors'],
    #                 ['each_entry_data["authors"]',              'open_citations_author_label',          'b_author_labels'],
    #                 ['each_entry_data["publications"]',         'pybtex_document_instance_name',        'b_publication'],
    #                 ['each_entry_data["publications"]',         'pybtex_document_label',                'b_publication_label'],
    #                 ['each_entry_data["publication_types"]',    'open_citations_list_minimizer_2',      'b_publication_type'],
    #                 ['each_entry_data["types"]',                'open_citations_list_minimizer_2',      'b_type'],
    #                 ['each_entry_data["years"]',                'open_citations_list_minimizer',        'b_publication_year'],
    #                 ['each_entry_data["publishers"]',           'pybtex_document_instance_name',        'b_publisher'],
    #                 ['each_entry_data["publishers"]',           'pybtex_document_label',                'b_publisher_label']
    #             ]
    #         # if a custom conversion_arguments_list is provided, proceed without modifying the provided list
    #         elif type(conversion_arguments_list) is list:
    #             pass
    #         else:
    #             raise ValueError ("Conversion_arguments_list parameter should be either left blank or be a list that "
    #                               "contains sublists of arguments.")
    #
    #
    #         # loop through individual reference entries in the parsed pybtex bib file
    #         for each_entry_id, each_entry_data in csv_container.entries.items():
    #             # and while doing that, also loop through each line in the conversion_arguments_list
    #             for each_argument_list in conversion_arguments_list:
    #                 # try using the elements of each sub-list in conversion_arguments_list as arguments of
    #                 # .setFormattedEntry method
    #                 # (try-except block is necessary, as each field may not exist for each entry)
    #                 try:
    #                     instance.setFormattedEntry(each_entry_id, eval(each_argument_list[0]),
    #                                                each_argument_list[1], each_argument_list[2])
    #                 except:
    #                     # TODO: Restore this line (replaced it with a more forgiving except statement for now)
    #                     # except KeyError:
    #                     pass
    #
    #             if verbose_import:
    #                 from pprint import pprint
    #                 pprint({each_entry_id: instance.getEntryById(each_entry_id)}, compact=True)
    #                 print(
    #                     "================================================================================================================")
    #
    #         ########################
    #         #  OPERATION SUMMARY   #
    #         ########################
    #
    #         print('\n\n---------------------------------------------------------------------------------------------------')
    #         print(path_of_file_to_import + ' ' + 'imported.')
    #
    #         print("\nFields added to the parsed bibliography:")
    #         instance.summarize()


    ###################################################################################################################
    ############################################ MANIPULATION FUNCTIONS ###############################################
    ###################################################################################################################


    def setEntry(instance, entry_id, field_name, field_value):
        """

        Args:
            entry_id (str): desired identifier for the entry to be created
            field_name (str): name of the field to be created (e.g., 'author')
            field_value (str): value of the field to be created (e.g., 'John Doe' or ['John Doe', 'Jane Doe'])

        Returns:
            Nothing, but it adds new entries to the Bibliography object instance.

        Examples:
            >>> # preparation: import class and instantiate a Bibliography object.
            >>> from triplicator.bibTools import Bibliography
            >>> my_bibliography = Bibliography()

            >>> # add entries to the instance
            >>> my_bibliography.setEntry("01", "author", "John Can Lokman")
            >>> my_bibliography.setEntry("01", "title", "A title")
            >>> my_bibliography.setEntry("02", "title", "Another title")
            >>> my_bibliography.entries
            {'01': {'author': 'John Can Lokman', 'title': 'A title'}, '02': {'title': 'Another title'}}
        """
        # if the ID is a new entry
        if entry_id not in instance._id_registry:
            # add target id as key of a the output dictionary and a subdictionary to it as fields and values
            instance.entries[entry_id] = {field_name: field_value}
            # add an instance id to the instance._id_registry
            instance._id_registry.append(entry_id)

        # if the ID is NOT a new entry
        else:
            # call entry by id, and add value-key pair to it
            instance.entries[entry_id][field_name] = field_value

        instance.updateFieldTypesRegistry(entry_id, field_name, field_value)
        instance.updateFieldValuesRegistry(entry_id, field_name, field_value)


    def setFormattedEntry(instance, desired_entry_id, target_field_value, formatting_algorithm, desired_field_name):
        """
        Extracts specified field values from a data source, formats it according to the specified algorithm, and adds
        the formatted values to the specified Bibliography class object. Works by simply passing the arguments to
        cleanAndFormatValues() function and .setEntry method. For modification of functionality, see that function or method
        instead; .setFormattedEntry is merely  proxy method built to serve as a shorthand. A fairly comprehensive
        example that demonstrates usage of different formatting algorithms is also provided in the examples of the
        curent method.

        Args:
            desired_entry_id: the identifier of the new entry to be created
            target_field_value:  the values in the existing source bibliography or data
            formatting_algorithm: one of the formatting algorithms in cleanAndFormatValues function. See cleanAndFormatValues function
                for a list of formatting algorithms.
            desired_field_name: the name of the field to be created

        Returns:
            if target_field_value is 'author' and formatting_algorithm is 'pybtex_author...' : list of authors
            if target_field_value is 'keywords' and formatting_algorithm is 'pybtex_author...': list of keywords
            all other scenarios: formatted string

        Examples:
            >>> # import class and instantiate a Bibliography object.
            >>> from triplicator.bibTools import Bibliography
            >>> my_bibliography = Bibliography()

            >>> # import a sample .bib file and assign it to a variable
            >>> from triplicator.pybtexImporter import Pybtex_import
            >>> pybtex_entries = Pybtex_import('example_data//test.bib').data.entries
            pybtex package is parsing using bibtex.Parser()...
            pybtex package finished parsing

            >>> # extract fields and their values (from pybtex object), format them,
            >>> # ... and add them to the Bibliography class object.
            >>> for each_entry_id, each_entry in pybtex_entries.items():
            ...     my_bibliography.setFormattedEntry(each_entry_id, each_entry.fields['title'], 'pybtex_document_instance_name', 'x_document')
            ...     my_bibliography.setFormattedEntry(each_entry_id, each_entry.fields['title'], 'pybtex_document_label', 'x_document_label')
            ...     my_bibliography.setFormattedEntry(each_entry_id, each_entry.persons['author'], 'pybtex_author_instance_name', 'x_author')
            ...     my_bibliography.setFormattedEntry(each_entry_id, each_entry.persons['author'], 'pybtex_author_label', 'x_author_label')
            ...     # some fields may exist for only some entries (for none in this sample .bib file)
            ...     # this try-except block will finish with exception because there is no 'keyword' field in the sample
            ...     # ... .bib file.
            ...     try:
            ...         my_bibliography.setFormattedEntry(each_entry_id, each_entry.fields['keyword'], 'pybtex_topic_instance_name', 'x_topics')
            ...         my_bibliography.setFormattedEntry(each_entry_id, each_entry.fields['keyword'], 'pybtex_topic_label', 'x_topic_labels')
            ...     except:
            ...         pass
            ...
            ...     try:
            ...         # 'pybtex_document_instance_name' and 'pybtex_document_label' formatting algorithms are suitable
            ...         # ... for use in other fields, like 'journal'
            ...         my_bibliography.setFormattedEntry(each_entry_id, each_entry.fields['journal'], 'pybtex_document_instance_name', 'x_journal')
            ...         my_bibliography.setFormattedEntry(each_entry_id, each_entry.fields['journal'], 'pybtex_document_label', 'x_journal_label')
            ...     except KeyError:
            ...         pass
            >>> print(my_bibliography.entries)
            {'56fafbf2574947cc9cbbfae578a0a36d': {'x_document': 'Book_with_one_author', 'x_document_label': 'Book with one author', 'x_author': ['Jaschke_AC'], 'x_author_label': ['Jaschke, AC']}, 'd79d00c790984ab08240e997d077c332': {'x_document': 'Article_with_5_authors_with_and_notation', 'x_document_label': "Article with 5 authors with 'and' notation", 'x_author': ['Lohr_A', 'Beunen_R', 'Savelli_H', 'Kalz_M', 'Ragas_A', 'Van_Belleghem_F'], 'x_author_label': ['Lohr, A', 'Beunen, R', 'Savelli, H', 'Kalz, M', 'Ragas, A', 'Van_Belleghem, F'], 'x_journal': 'Current_Opinion_in_Environmental_Sustainability', 'x_journal_label': 'Current Opinion in Environmental Sustainability'}, 'a8781aa0eae047d1826a658f3545ce3f': {'x_document': 'Article_with_3_authors_with_mixed_notation', 'x_document_label': 'Article with 3 authors with mixed notation', 'x_author': ['Mendoza_Rodriguez_JP', 'Wielhouwer_JL', 'Kirchler_ESMN'], 'x_author_label': ['Mendoza_Rodriguez, JP', 'Wielhouwer, JL', 'Kirchler, ESMN'], 'x_journal': 'Journal_of_Economic_Psychology', 'x_journal_label': 'Journal of Economic Psychology'}, '01b9c957875b4a96839c1bfd05ec6a31': {'x_document': 'Article_with_non-uri_safe_characters%3A%3C%3E%5B%5D_%40%25_to_WW_%E2%88%97%E2%86%92e%CE%BD%CE%BC%CE%BD_with_the_ATLAS_detector_at_%E2%88%9As%3D8_TeV', 'x_document_label': 'Article with non-uri safe characters:<>{}()[] @% to WW ∗→eνμν with the ATLAS detector at √s=8 TeV', 'x_author': ['%40uthor_%CE%BDbn', 'Aaboud_M', 'Bentvelsen_S', 'Berge_D', 'Colijn_AP', 'de_Jong_P', 'Koffeman_E', 'Sabato_G', 'Salek_D', 'van_Vulpen_I', 'Vermeulen_JC', 'Vreeswijk_M'], 'x_author_label': ['@uthor, νbn', 'Aaboud, M', 'Bentvelsen, S', 'Berge, D', 'Colijn, AP', 'de_Jong, P', 'Koffeman, E', 'Sabato, G', 'Salek, D', 'van_Vulpen, I', 'Vermeulen, JC', 'Vreeswijk, M'], 'x_journal': 'The_Journal_of_High_Energy_Physics', 'x_journal_label': 'The Journal of High Energy Physics'}}

        """
        # if the current field exists for the current entry
        # format the extracted value (which is a string or list [e.g., if it is the values from the 'author' field])
        formatted_field_value = cleanAndFormatValues(target_field_value, formatting_algorithm)

        # add the now-formatted name to Bibliography object
        instance.setEntry(desired_entry_id, desired_field_name, formatted_field_value)

        # if the current field does not exist for the current entry




    # TODO: Enhance and clarify this function
    def enrich(instance, other_bibliography_object_to_use, field_to_match_in_bibliographies, method='left join'):
        """
        Left joins two bibliographies.

        Args:
            other_bibliography_object_to_use: The target bibliography that will be used to enrich the current
                bibliography.
            field_to_match_in_bibliographies: The field name that will be used to match entries between bibliographies
                (e.g., doi)

        Returns:

        Examples:
            >>> # initiaton
            >>> bib_one = Bibliography()
            >>> bib_one.setEntry(entry_id='01', field_name='doi', field_value='6226')
            >>> bib_one.setEntry(entry_id='01', field_name='title', field_value='This is a title')
            >>> bib_one.preview()
            <BLANKLINE>
            ----------------------------------ENTRY 1----------------------------------
            ('01', {'doi': '6226', 'title': 'This is a title'})
            <BLANKLINE>
            >>> bib_two = Bibliography()
            >>> bib_two.setEntry(entry_id='05', field_name='doi', field_value='6226')
            >>> bib_two.setEntry(entry_id='05', field_name='author', field_value='John Doe')
            >>> bib_two.preview()
            <BLANKLINE>
            ----------------------------------ENTRY 1----------------------------------
            ('05', {'author': 'John Doe', 'doi': '6226'})
            <BLANKLINE>


            >>> # enrichment
            >>> bib_one.enrich(other_bibliography_object_to_use=bib_two, field_to_match_in_bibliographies='doi')
            1 entries enriched and 0 entries appended to bibliography.
            >>> bib_one.preview()
            <BLANKLINE>
            ----------------------------------ENTRY 1----------------------------------
            ('01', {'author': 'John Doe', 'doi': '6226', 'title': 'This is a title'})
            <BLANKLINE>

            >>> # no entries appended in 'left join' mode
            >>> bib_two.setEntry(entry_id='100', field_name='doi', field_value='5000')
            >>> bib_two.setEntry(entry_id='100', field_name='note', field_value='This is a note')
            >>> bib_one.enrich(other_bibliography_object_to_use=bib_two, field_to_match_in_bibliographies='doi')
            0 entries enriched and 0 entries appended to bibliography.

            >>> # entries enriched and appended in 'merge' mode
            >>> bib_two.setEntry(entry_id='41124', field_name='doi', field_value='6226')
            >>> bib_two.setEntry(entry_id='41124', field_name='publisher', field_value='Some publisher')
            >>> bib_one.enrich(other_bibliography_object_to_use=bib_two, field_to_match_in_bibliographies='doi'
            ...         , method='merge')
            1 entries enriched and 2 entries appended to bibliography.
            >>> bib_one.preview()
            <BLANKLINE>
            ----------------------------------ENTRY 1----------------------------------
            ('01',
             {'author': 'John Doe',
              'doi': '6226',
              'publisher': 'Some publisher',
              'title': 'This is a title'})
            <BLANKLINE>
            ----------------------------------ENTRY 2----------------------------------
            ('100', {'doi': '5000', 'note': 'This is a note'})
            <BLANKLINE>

            >>> # actual bib import and merge
            >>> bib_poor = Bibliography()
            >>> bib_poor.importBib('example_data//merge_test_file_poor.bib')
            Parsing of example_data//merge_test_file_poor.bib started
            pybtex package is parsing using bibtex.Parser()...
            pybtex package finished parsing
            Calculating file length...
            <BLANKLINE>
            <BLANKLINE>
            ---------------------------------------------------------------------------------------------------
            example_data//merge_test_file_poor.bib parsed and imported as Bibliography object.
            <BLANKLINE>
            Fields added to the parsed the Bibliography object:
            {'b_author_labels': 2,
             'b_authors': 2,
             'b_document': 2,
             'b_document_label': 2,
             'b_doi': 2,
             'b_publication_month': 1,
             'b_publication_year': 2,
             'b_type': 2}
            <BLANKLINE>
            <BLANKLINE>

            >>> bib_poor.preview(100)
            <BLANKLINE>
            ----------------------------------ENTRY 1----------------------------------
            ('b56e503067994b389d4eced98fae2206',
             {'b_author_labels': ['Koning, R', 'Buraglio, N', 'de_Laat, CTAM', 'Grosso, P'],
              'b_authors': ['Koning_R', 'Buraglio_N', 'de_Laat_CTAM', 'Grosso_P'],
              'b_document': 'CoreFlow-Enriching_Bro_security_events_using_network_traffic_monitoring_data',
              'b_document_label': 'CoreFlow-Enriching Bro security events using network '
                                  'traffic monitoring data',
              'b_doi': '10.1016--j.future.2017.04.017',
              'b_publication_month': '2',
              'b_publication_year': '2018',
              'b_type': 'article'})
            <BLANKLINE>
            ----------------------------------ENTRY 2----------------------------------
            ('d0e972a611e44a80b8014f1069bfad88',
             {'b_author_labels': ['van_Spanje, J'],
              'b_authors': ['van_Spanje_J'],
              'b_document': 'Controlling_the_Electoral_Marketplace-How_Established_Parties_Ward_Off_Competition',
              'b_document_label': 'Controlling the Electoral Marketplace-How Established '
                                  'Parties Ward Off Competition',
              'b_doi': '10.1007--978-3-319-58202-3',
              'b_publication_year': '2018',
              'b_type': 'book'})
            <BLANKLINE>


            >>> bib_rich = Bibliography()
            >>> bib_rich.importBib('example_data//merge_test_file_rich.bib')
            Parsing of example_data//merge_test_file_rich.bib started
            pybtex package is parsing using bibtex.Parser()...
            pybtex package finished parsing
            Calculating file length...
            <BLANKLINE>
            <BLANKLINE>
            ---------------------------------------------------------------------------------------------------
            example_data//merge_test_file_rich.bib parsed and imported as Bibliography object.
            <BLANKLINE>
            Fields added to the parsed the Bibliography object:
            {'b_abstract': 1,
             'b_author_labels': 2,
             'b_authors': 2,
             'b_document': 2,
             'b_document_label': 2,
             'b_doi': 2,
             'b_isbn': 1,
             'b_issn': 1,
             'b_issue_number': 1,
             'b_journal': 1,
             'b_journal_label': 1,
             'b_pages': 1,
             'b_publication_month': 1,
             'b_publication_year': 2,
             'b_publisher': 2,
             'b_publisher_label': 2,
             'b_type': 2,
             'b_volume': 1}
            <BLANKLINE>
            <BLANKLINE>

            >>> bib_rich.preview(100)
            <BLANKLINE>
            ----------------------------------ENTRY 1----------------------------------
            ('b56e503067994b389d4eced98fae2206',
             {'b_abstract': 'Attacks against network infrastructures can be detected by '
                            'Intrusion Detection Systems (IDS). Still reaction to these '
                            'events are often limited by the lack of larger contextual '
                            'information in which they occurred. In this paper we present '
                            'CoreFlow, a framework for the correlation and enrichment of '
                            'IDS data with network flow information. CoreFlow ingests data '
                            'from the Bro IDS and augments this with flow data from the '
                            'devices in the network. By doing this the network providers '
                            'are able to reconstruct more precisely the route followed by '
                            'the malicious flows. This enables them to devise tailored '
                            'countermeasures, e.g. blocking close to the source of the '
                            'attack. We tested the initial CoreFlow prototype in the ESnet '
                            'network, using inputs from 3 Bro systems and more than 50 '
                            'routers.',
              'b_author_labels': ['Koning, R', 'Buraglio, N', 'de_Laat, CTAM', 'Grosso, P'],
              'b_authors': ['Koning_R', 'Buraglio_N', 'de_Laat_CTAM', 'Grosso_P'],
              'b_document': 'CoreFlow-Enriching_Bro_security_events_using_network_traffic_monitoring_data',
              'b_document_label': 'CoreFlow-Enriching Bro security events using network '
                                  'traffic monitoring data',
              'b_doi': '10.1016--j.future.2017.04.017',
              'b_issn': '0167-739X',
              'b_issue_number': '1',
              'b_journal': 'Future_Generation_Computer_Systems',
              'b_journal_label': 'Future Generation Computer Systems',
              'b_pages': '235',
              'b_publication_month': '2',
              'b_publication_year': '2018',
              'b_publisher': 'Elsevier',
              'b_publisher_label': 'Elsevier',
              'b_type': 'article',
              'b_volume': '79'})
            <BLANKLINE>
            ----------------------------------ENTRY 2----------------------------------
            ('d0e972a611e44a80b8014f1069bfad88',
             {'b_author_labels': ['van_Spanje, J'],
              'b_authors': ['van_Spanje_J'],
              'b_document': 'Controlling_the_Electoral_Marketplace-How_Established_Parties_Ward_Off_Competition',
              'b_document_label': 'Controlling the Electoral Marketplace-How Established '
                                  'Parties Ward Off Competition',
              'b_doi': '10.1007--978-3-319-58202-3',
              'b_isbn': '9783319582016',
              'b_publication_year': '2018',
              'b_publisher': 'Palgrave_Macmillan',
              'b_publisher_label': 'Palgrave Macmillan',
              'b_type': 'book'})
            <BLANKLINE>

            >>> bib_poor.enrich(other_bibliography_object_to_use=bib_rich, field_to_match_in_bibliographies='b_doi')
            12 entries enriched and 0 entries appended to bibliography.

            >>> bib_poor.preview(100)
            <BLANKLINE>
            ----------------------------------ENTRY 1----------------------------------
            ('b56e503067994b389d4eced98fae2206',
             {'b_abstract': 'Attacks against network infrastructures can be detected by '
                            'Intrusion Detection Systems (IDS). Still reaction to these '
                            'events are often limited by the lack of larger contextual '
                            'information in which they occurred. In this paper we present '
                            'CoreFlow, a framework for the correlation and enrichment of '
                            'IDS data with network flow information. CoreFlow ingests data '
                            'from the Bro IDS and augments this with flow data from the '
                            'devices in the network. By doing this the network providers '
                            'are able to reconstruct more precisely the route followed by '
                            'the malicious flows. This enables them to devise tailored '
                            'countermeasures, e.g. blocking close to the source of the '
                            'attack. We tested the initial CoreFlow prototype in the ESnet '
                            'network, using inputs from 3 Bro systems and more than 50 '
                            'routers.',
              'b_author_labels': ['Koning, R', 'Buraglio, N', 'de_Laat, CTAM', 'Grosso, P'],
              'b_authors': ['Koning_R', 'Buraglio_N', 'de_Laat_CTAM', 'Grosso_P'],
              'b_document': 'CoreFlow-Enriching_Bro_security_events_using_network_traffic_monitoring_data',
              'b_document_label': 'CoreFlow-Enriching Bro security events using network '
                                  'traffic monitoring data',
              'b_doi': '10.1016--j.future.2017.04.017',
              'b_issn': '0167-739X',
              'b_issue_number': '1',
              'b_journal': 'Future_Generation_Computer_Systems',
              'b_journal_label': 'Future Generation Computer Systems',
              'b_pages': '235',
              'b_publication_month': '2',
              'b_publication_year': '2018',
              'b_publisher': 'Elsevier',
              'b_publisher_label': 'Elsevier',
              'b_type': 'article',
              'b_volume': '79'})
            <BLANKLINE>
            ----------------------------------ENTRY 2----------------------------------
            ('d0e972a611e44a80b8014f1069bfad88',
             {'b_author_labels': ['van_Spanje, J'],
              'b_authors': ['van_Spanje_J'],
              'b_document': 'Controlling_the_Electoral_Marketplace-How_Established_Parties_Ward_Off_Competition',
              'b_document_label': 'Controlling the Electoral Marketplace-How Established '
                                  'Parties Ward Off Competition',
              'b_doi': '10.1007--978-3-319-58202-3',
              'b_isbn': '9783319582016',
              'b_publication_year': '2018',
              'b_publisher': 'Palgrave_Macmillan',
              'b_publisher_label': 'Palgrave Macmillan',
              'b_type': 'book'})
            <BLANKLINE>
        """
        other_bib = other_bibliography_object_to_use

        instance.no_of_enrichments_made_in_last_operation = 0
        instance.no_of_additions_made_in_last_operation = 0

        for each_other_id, each_other_entry_data in other_bib.entries.items():
            target_field_name_in_other_bib = field_to_match_in_bibliographies
            target_value_in_other_bib = each_other_entry_data[target_field_name_in_other_bib]

            # if a field name and value(e.g., doi) from other bibliography is found in the current one, enrich
            # the corresponding entry in the current dataset with this field name and value
            # TODO: This try-except block should either be made more specific or replaced with an if-else block
            try:

                returned_entry = instance.getEntriesByField(field_name=target_field_name_in_other_bib, field_value=target_value_in_other_bib)
                matching_ids_list = instance._field_values_registry[target_field_name_in_other_bib][target_value_in_other_bib]
                if len(matching_ids_list) > 1:
                    raise ValueError("More than one ID (%s) returned with the field name '%s' and value '%s'."
                                    % (matching_ids_list, target_field_name_in_other_bib, target_value_in_other_bib))
                else:
                    matching_id = matching_ids_list[0]

                field_names_of_current_bib = list(returned_entry[0].keys())
                for each_field_name_in_other_bib, each_field_value_in_other_bib in each_other_entry_data.items():

                    if each_field_name_in_other_bib not in field_names_of_current_bib:
                        instance.entries[matching_id][each_field_name_in_other_bib] = each_field_value_in_other_bib
                        instance.no_of_enrichments_made_in_last_operation += 1
            # TODO: Below part is not tested
            # TODO: Add kwargs to documentation
            # if the field name and value from the other bib is not found
            except:
               if method == 'merge':
                   for each_other_field, each_other_field_value in each_other_entry_data.items():
                       instance.setEntry(each_other_id, each_other_field, each_other_field_value)
                       instance.no_of_additions_made_in_last_operation += 1
               else:
                   pass

        print('%d entries enriched and %d entries appended to bibliography.'
              % (instance.no_of_enrichments_made_in_last_operation,
                 instance.no_of_additions_made_in_last_operation))
    ###################################################################################################################
    ################################################# QUERY FUNCTIONS #################################################
    ###################################################################################################################

    def getEntryById(instance, entry_id, field_name=""):
        """
        Searches bibliography instance registry for given entry id or (optionally) entry_id-field_name combination
        (e.g., '1234155125'-author), and returns a the matching entity.

        Args:
            entry_id (str): unique entry id of the bibliography entry
            field_name (str): name of the bibliography field. e.g., author, title.

        Returns:
            If field_name is not specified: The entry that matches with the provided entry_id.
            If field_name is specified: The value of the field of the entry which matches with the provided entry_id.

        Examples:
            >>> # Preparation:
            >>> from triplicator.bibTools import Bibliography
            >>> bibx = Bibliography()
            >>> bibx.setEntry("01", "author", "John Can Lokman")
            >>> bibx.setEntry("01", "title", "Test Book 1")

            >>> # Example #1:
            >>> bibx.getEntryById("01")
            {'author': 'John Can Lokman', 'title': 'Test Book 1'}

            >>> # Example #2:
            >>> bibx.getEntryById("01", "title")
            'Test Book 1'
        """
        if field_name == "":
            return instance.entries[entry_id]
        else:
            return instance.entries[entry_id][field_name]


    def getEntriesByField(instance, field_name, field_value):
        """
        Searches the bibliography instance registry for given field name-value combination (e.g., title-my_title), and returns a list of matching
        bibliography entries.

        Args:
            field_name: Name of the field to be searched (e.g., "author").
            field_value: Value of the field that is being searched (e.g., "John Lokman"

        Returns:
            A list of bibliography entries.

        Examples:
            # Example 1

                >>> # preparation
                >>> from triplicator.bibTools import Bibliography
                >>> bibx = Bibliography()
                >>> bibx.setEntry("01", "author", "John Can Lokman")
                >>> bibx.setEntry("01", "title", "Test Book 1")
                >>> bibx.setEntry("02", "author", "John Can Lokman")
                >>> bibx.setEntry("02", "title", "Test Book 2")

                >>> # method usage
                >>> bibx.getEntriesByField("author", "John Can Lokman")
                [{'author': 'John Can Lokman', 'title': 'Test Book 1'}, {'author': 'John Can Lokman', 'title': 'Test Book 2'}]

            # Example 2

                >>> # preparation:
                >>> from triplicator.pybtexImporter import Pybtex_import
                >>> pybtex_entries = Pybtex_import("example_data//test.bib").data.entries
                pybtex package is parsing using bibtex.Parser()...
                pybtex package finished parsing
                >>> biby = Bibliography()
                >>> for each_entry_id, each_entry in pybtex_entries.items():
                ...     each_year = each_entry.fields["year"]
                ...     biby.setEntry(each_entry_id, "b_year",each_year)

                >>> # calling entries that has year 2017 using the method:
                >>> biby.getEntriesByField("b_year", "2017")
                [{'b_year': '2017'}, {'b_year': '2017'}, {'b_year': '2017'}]

                >>> # a similar operation without using the method:
                >>> for each_entry_id, each_entry_data in biby.entries.items():
                ...     print(each_entry_data["b_year"])
                2017
                2017
                2017
                2016

        """
        # Get matching ids from registry based on field name-value combination
        matching_ids_list = instance._field_values_registry[field_name][field_value]

        # Use matching ids that are returned to retrieve entities these ids correspond to
        matching_entries_list = []
        for each_id in matching_ids_list:
            matching_entries_list.append(instance.getEntryById(each_id))
        return matching_entries_list


    def summarize(instance, print_header_text=False):
        """
        Prints summary statistsics of the bibliograpghy.

        Args:
            print_header_text(bool): If true, prints a line before the start of summary, such as "Fields added
   the parsed              to bibliography:"

        Returns:
            Printed string on console
        """
        from pprint import pprint

        if print_header_text:
            print('\n\n---------------------------------------------------------------------------------------------------')
            print('Summary of fields in bibliography:')

        pprint(instance._field_type_registry, compact=True)


    def preview(instance, number_of_entries_to_preview=5, print_header_text=False):
        """
        Prints a sample of entries from the bibliography.

        Args:
            number_of_entries_to_preview (int): The number of entities to be printed.
            print_header_text: If true, prints a line before the start of summary, such as "Fields added
   the parsed              to bibliography:"

        Returns:
            Printed string on console
        """
        from pprint import pprint
        if print_header_text:
            print('\n\n---------------------------------------------------------------------------------------------------')
            print("\nPreview the parsed Bibliography object:")

        for i, each_entry in enumerate(instance.entries.items()):
            if i < number_of_entries_to_preview:
                print('\n----------------------------------ENTRY ' + str(i+1) + '----------------------------------')
                pprint(each_entry, compact=True)
            else:
                break
        print('')  # blank line (using an \n causes two blank lines)

    def write_preview_to_log(instance, number_of_entries_to_preview=5, log_file_path='log.txt'):
        """
        Prints a sample of entries from the bibliography to the specified log file.
        """
        from preprocessor.Text_File import Log_File
        log_file = Log_File(log_file_path)

        log_file.append_line('Preview the parsed Bibliography object:')

        for i, each_entry_id_entry_content_pair in enumerate(instance.entries.items()):
            if i < number_of_entries_to_preview:
                log_file.append_line('\n----------------------------------ENTRY ' + str(i+1) + '----------------------------------')
                for each_key_value_pair in each_entry_id_entry_content_pair[1].items():
                        log_file.append_line(each_key_value_pair)
            else:
                break

    ###################################################################################################################
    ############################################ REGISTRY UPDATE FUNCTIONS ############################################
    ###################################################################################################################

    def updateFieldValuesRegistry(instance, entry_id, field_name, field_value):
        """
            Updates instance registry each time an entry is added to the bibliography instance. The registry allows
            fast searching entries in the bibliography.

            Args:
                 entry_id (str): id to be assigned to entry (e.g., '2341230u9078').
                 field_name(str): name of field (e.g., 'author')
                 field_value(str or list): value of the field (e.g., 'John Doe' )

            Returns:
                Nothing, but updates the instance._field_values_registry

            Examples:
                >>> # preparation
                >>> from triplicator.bibTools import Bibliography
                >>> bibx = Bibliography()

                >>> # add first entry and see how instance registry is updated afterwards
                >>> bibx.setEntry("01", "author", "John Can Lokman")
                >>> bibx.setEntry("01", "title", "Test Book 1")
                >>> print(bibx._field_values_registry)
                {'author': {'John Can Lokman': ['01']}, 'title': {'Test Book 1': ['01']}}

                >>> # add second entry and see how instance registry is updated afterwards
                >>> bibx.setEntry("02", "title", "Test Book 2")
                >>> bibx.setEntry("02", "author", "Stefan Schlobach")
                >>> print(bibx._field_values_registry)
                {'author': {'John Can Lokman': ['01'], 'Stefan Schlobach': ['02']}, 'title': {'Test Book 1': ['01'], 'Test Book 2': ['02']}}

            TODO:
                - Input should be treated as a search string rather than an exact string, so, for instance, a partial
                    author name can also be searched.
        """
        # function must be able to accept a list of items, as this is sometimes the case (e.g., multiple authors
        # ...for author field).
        # Therefore, strings inputs are converted to lists to be compatible with the list processing facilities
        field_value_list = []

        if type(field_value) == str:
            field_value_list = [field_value]

            # Debugger
            #print("input is this string:")
            #print(field_value_list)

        # Explicit statement. If the parameter is already a list, take it as it is
        elif type(field_value) == list:
            field_value_list = field_value

            # Debugger
            # print("input is this list:")
            # print(field_value_list)

        elif type(field_value) is None:
            pass

        #else:
        #    #raise Exception("'field_value' must be string or list. It is currently: " + str(field_value))

        if field_value_list != []:
            for each_field_value in field_value_list:
                # if field_name (e.g., author) has never been added to the registry
                if field_name not in instance._field_values_registry:

                    # Debugger
                    #print("SCENARIO 1")
                    #print("field_values_registry is currently:")
                    #print(instance._field_values_registry)

                    # Add dictionary entry for the field name-value pair and the entry id (e.g., {author:{"john x":[124515152])}
                    # NOTE: Below line can instead use instance._field_type_registry for more efficient search. This has to be tested
                    instance._field_values_registry[field_name] = {each_field_value: [entry_id]}

                    # Debugger
                    #print("field_name '" + str(field_name) + "' is not in registry")
                    #print("the current field value is: '" + each_field_value + "' (and it is not in registry).")
                    #print("field name and current field value is now added to registry with the following command:")
                    #print("instance._field_values_registry[field_name] = {each_field_value: [entry_id]}")
                    #print("the field_values_registry has now become:")
                    #print(instance._field_values_registry)

                # if field name (e.g., 'author' field) is previously added to the registry...
                elif field_name in instance._field_values_registry:

                    # Debugger
                    #print("SCENARIO 2")
                    #print("field_values_registry is currently:")
                    #print(instance._field_values_registry)

                    # ...but if field_value (e.g., author's name) has never been added to the registry
                    if each_field_value not in instance._field_values_registry[field_name]:
                        # add this field value (e.g., author) and set its value to a LIST that contains current entry_id
                        # so that this list can later be appended with other entry_ids.
                        # an example operation performed by the line below would be equivalent to:
                        # instance._field_values_registry[author] = {"John x": ["14578436002"]}
                        # which creates this dictionary entry:
                        # _field_values_registry:{ author:{ "John x": ["14578436002"] } }
                        instance._field_values_registry[field_name][each_field_value] = [entry_id]

                        # Debugger
                        #print("field_name '" + str(field_name) + "' has been found in the registry")
                        #print("current field value '" + each_field_value + "' has NOT been found in the registry")
                        #print("field name and current field value is now added to registry with the following command:")
                        #print("instance._field_values_registry[field_name] = {each_field_value: [entry_id]}")
                        #print("the field_values_registry has now become:")
                        #print(instance._field_values_registry)

                    # if field_value (e.g., author's name) is previously added to the registry
                    elif each_field_value in instance._field_values_registry[field_name]:
                        # Debugger
                        #print("SCENARIO 3")
                        #print("field_values_registry is currently:")
                        #print(instance._field_values_registry)

                        # append entry id to corresponding field value (e.g.,add entry_id to author name)
                        # an example operation performed by the line below would be equivalent to:
                        # instance._field_values_registry[author]["John x"].append["14578436002"]
                        # which creates this dictionary entry:
                        # _field_values_registry:{ author:{ "John x": ["some_previous_id", "14578436002"] } }
                        instance._field_values_registry[field_name][each_field_value].append(entry_id)

                        # Debugger
                        #print("field_name '" + str(field_name) + "' has been found in the registry")
                        #print("current field value '" + each_field_value + "' HAS been found in the registry")
                        #print("field name and current field value is now added to registry with the following command:")
                        #print("instance._field_values_registry[field_name] = {each_field_value: [entry_id]}")
                        #print("the field_values_registry has now become:")
                        #print(instance._field_values_registry)

                        # Debugger
                        #print("instance._field_values_registry is")
                        #print(instance._field_values_registry)
                        #print("")

    def updateFieldTypesRegistry(instance, entry_id, field_name, field_value):
        """
        """
        if field_name not in instance._field_type_registry:
            instance._field_type_registry[field_name] = 1
        else:
            instance._field_type_registry[field_name] += 1

            # two container variables for author (instance) names and author labels (which will later be needed by RDF format)


    ###################################################################################################################
    ################################################ EXPORT FUNCTIONS #################################################
    ###################################################################################################################
    def exportToCsv(instance, output_file_path, columns_to_ignore=None, new_header_names=None):
        # TODO: This is a draft method, and it must be cleaned.
        """
        Converts a Bibliography object file to CSV format with custom formatting options and writes a .csv file.

        Args:
            output_file_path(str): path of the .csv file to be written
            columns_to_ignore(list): a list of strings that consists of column headers to be ignored during
                export operation.
            new_header_names(list): a list of strings that contains replacement column headers. Must be of same
                length with the headers row in dataset.

                - If 'columns_to_ignore' is provided, the length of the new_header_names list must be equal to the length of the headers row in the dataset.
                - If 'columns_to_ignore' is not provided, the length of the new_header_names list must be equal to the length of the headers row in the dataset.

        Returns:
            New .csv file
        """
        import csv
        from preprocessor.ListData import ListData

        list_data_bibliography = ListData()
        list_data_bibliography.importBibliography(instance)
        #if columns_to_ignore != None:
        list_data_bibliography.remove_columns(columns_to_ignore)
        #if new_header_names != None:
        list_data_bibliography.replace_headers(new_header_names)

        #print(list_data_bibliography.headers_row)
        #print(list_data_bibliography.data_rows)
        #print(list_data_bibliography.dataset)
        file = open(output_file_path, 'w', newline='', encoding='UTF-8')
        writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        for row in list_data_bibliography.dataset:
            writer.writerow(row)
        print("\nBibliography is written to .csv file.")
        file.close()

        ### CLEANING ###
        import re
        csv_file = open(output_file_path, 'r', encoding='UTF-8')
        csv_string = csv_file.read()
        csv_file.close()

        csv_string_cleaned = re.sub('[\[\]\'\}{]', "", csv_string)

        csv_file = open(output_file_path, 'w', encoding='UTF-8')
        csv_file.write(csv_string_cleaned)
        csv_file.close()


###################################################################################################################
############################################## FORMATTING FUNCTIONS ###############################################
###################################################################################################################

def replacePatternsAsPerDictionary(input_string, patterns_dictionary):
    """
    Replaces patterns in an inputted string according to the key:value combinations in a dictionary. Useful for replacing
    long name segments such as "_-_" with "-" in instance names during their creation.

    Args:
        input_string (str): String to be processed
        patterns_dictionary(dict): A dictionary that contains the key:value combinations to be used in replacement.
             Keys in the patterns dictionary should be target patterns, while values of the dictionary should be
             the desired replacement patterns or characters.

    Returns:
        A string

    Examples:
        >>> patterns_dictionary = {"_-_" : "-",
        ...                        ": "  : "-" }
        >>> target_string = "Case_1_-_12:_Unknown"
        >>> formatted_string = replacePatternsAsPerDictionary(target_string, patterns_dictionary)
        >>> print(formatted_string)
        Case_1-12:_Unknown
    """
    import re

    output_string = input_string

    # replace undesired characters with the desired ones (e.g., ':' -> '-') using dictionary_of_patterns_to_replace
    for each_target_pattern, each_replacement_pattern in patterns_dictionary.items():
        output_string = re.sub(each_target_pattern, each_replacement_pattern, output_string)

    return output_string


def standardizeCapitalization(input_string, algorithm):
    """
    Converts title case words (e.g., ' The ') to lowercase e.g., ' the '). Allows conversion algorithms for multiple
    scenarios (e.g., author names vs titles) and languages via keyword arguments of 'algorithm' parameter.

    Args:
        input_string (str): the string to be converted.
        algorithm: capitalization algorithm to be used

    Keyword Args:
        "English title" (algorithm):

    Returns:
        The converted string

    Examples:
        >>> from triplicator.bibTools import standardizeCapitalization
        >>> standardizeCapitalization("Phantom Of The Opera", "en_title")
        'Phantom of the Opera'
    """
    import re

    formatted_string = input_string

    # convert title case to lowercase (DBpedia format)
    if algorithm is "en_title":
        formatted_string = re.sub(" In ", " in ", formatted_string)
        formatted_string = re.sub(" The ", " the ", formatted_string)
        formatted_string = re.sub(" A ", " a ", formatted_string)
        formatted_string = re.sub(" An ", " an ", formatted_string)
        formatted_string = re.sub(" As ", " as ", formatted_string)
        formatted_string = re.sub(" On ", " on ", formatted_string)
        formatted_string = re.sub(" At ", " at ", formatted_string)
        formatted_string = re.sub(" For ", " for ", formatted_string)
        formatted_string = re.sub(" With ", " with ", formatted_string)
        formatted_string = re.sub(" From ", " from ", formatted_string)
        formatted_string = re.sub(" By ", " by ", formatted_string)
        formatted_string = re.sub(" Of ", " of ", formatted_string)
        formatted_string = re.sub(" Vs ", " vs ", formatted_string)
        formatted_string = re.sub(" And ", " and ", formatted_string)

        formatted_string = re.sub(" Be ", " be ", formatted_string)
        formatted_string = re.sub(" Been ", " been ", formatted_string)
        formatted_string = re.sub(" Not ", " not ", formatted_string)
        formatted_string = re.sub(" Is ", " is ", formatted_string)
        formatted_string = re.sub(" Isn\'t ", " isn\'t ", formatted_string)
        formatted_string = re.sub(" Are ", " are ", formatted_string)
        formatted_string = re.sub(" Aren\'t ", " aren\'t ", formatted_string)
        formatted_string = re.sub(" Does ", " does ", formatted_string)
        formatted_string = re.sub(" Doesn\'t ", " doesn\'t ", formatted_string)
        formatted_string = re.sub(" Do ", " do ", formatted_string)
        formatted_string = re.sub(" Don\'t ", " don\'t ", formatted_string)
        formatted_string = re.sub(" Was ", " was ", formatted_string)
        formatted_string = re.sub(" Wasn\'t ", " wasn\'t ", formatted_string)
        formatted_string = re.sub(" Were ", " were ", formatted_string)
        formatted_string = re.sub(" Weren\'t ", " weren\'t ", formatted_string)
        formatted_string = re.sub(" Did ", " did ", formatted_string)
        formatted_string = re.sub(" Didn\'t ", " didn\'t ", formatted_string)
        # This list is not exhaustive

    else:
        raise Exception ('Unknown algorithm parameter: "' + algorithm + '". Please enter a valid capitalization algorithm such as "en_title".')

    return formatted_string


def cleanAndFormatValues(target_field, algorithm):
    """
    Formats the values in a given list or string according to the style specified by 'algorithm' parameter (e.g.,
    'pybtex_author_instance_name'). All algorithms follow DBPedia naming conventions. For changing which characters
    to omit, the internal variables 'pattern_of_characters_to_omit' and 'dictionary_of_patterns_to_replace' should be
    modified.

    Args:
        target_field(str or list): string or list to be formatted.
            For algorithm type 'pybtex_author_instance_name' the list contains 'person' objects.
        algorithm (str): formatting style

    Keyword Args:
        "pybtex_author_instance_name" (algorithm): takes my_pybtex_instance.persons['author'] field and outputs in the format
            ['Lastname1_Lastname1_FN1', 'Lastname2_Lastname2_FN2'] (e.g.,
            an input such as ["Van Belleghem, Frank", "Mendoza Rodriguez J.P."] would be formatted as
                             ["Van_Belleghem_F", "Mendoza_Rodriguez_JP"])

        "pybtex_author_label" (algorithm): takes my_pybtex_instance.persons['author'] field and outputs in the
            format ['Lastname1_Lastname1, FN1', 'Lastname2_Lastname2, FN2'] (e.g.,
            an input such as ["Van Belleghem, Frank", "Mendoza Rodriguez J.P."] would be formatted as
                             ["Van Belleghem, F", "Mendoza Rodriguez, JP"])

        "pybtex_document_instance_name" (algorithm): takes a given field's value
            (e.g., my_pybtex_instance.fields["title"]) (which is a string), and returns a formatted string that is
            suitable to be used as an instance name. During the operation, capitalization is standardized
            (e.g., 'In' -> 'in'), undesired characters (e.g., [,],*,^) and punctuation are removed, and spaces are
            replaced with underscores.

        "pybtex_document_label" (algorithm): takes a given field's value
            (e.g., my_pybtex_instance.fields["title"]) (which is a string), and returns a formatted string that is
            suitable to be used as a label.During the operation, capitalization is standardized
            (e.g., 'In' -> 'in').

        "pybtex_topic_instance_name" (algorithm): takes my_pybtex_instance.fields["keywords"] field's value
            (which is a string in the format of "keyword 1, keyword 2"), and returns a formatted string that is
            suitable to be used as a list of 'topics' (in the format of ["keyword_1", "keyword_2"]).During the
            operation, capitalization is standardized (e.g., 'In' -> 'in'), undesired characters (e.g., [,],*,^)
            and punctuation are removed, and spaces are replaced with underscores.

        "pybtex_topic_label" (algorithm): takes my_pybtex_instance.fields["keywords"] field's value
            (which is a string in the format of "keyword 1, keyword 2"), and returns a formatted string that is
            suitable to be used as a list of labels for 'topics' (in the format of ["keyword 1", "keyword 2"]).During the
            operation, capitalization is standardized (e.g., 'In' -> 'in').

    Raises:
        Keyword Error: Keyword for 'algorithm' parameter does not exist.

    Returns:
        A version of the inputted values that is formatted according the specified algorithm.
        Algorithms and their corresponding outputs:

            - "pybtex_author_instance_name": a list of strings
            - "pybtex_author_label" : a list of strings
            - "pybtex_document_instance_name" (algorithm): a string
            - "pybtex_topic_instance_name" (algorithm): a list of strings in the format of
                ["topic_string_1", "topic_string_2"]. (note that the input was a string of keywords, in the format of
                "topic string 1, topic string 2")

    Examples:
        >>> # preparation
        >>> from triplicator.pybtexImporter import Pybtex_import
        >>> from triplicator.bibTools import cleanAndFormatValues

        >>> # import a bib file with pybtex and and extract entries (i.e., {entry_id:entries} pairs)
        >>> pybtex_entries = Pybtex_import("example_data//test.bib").data.entries
        pybtex package is parsing using bibtex.Parser()...
        pybtex package finished parsing

        >>> # AUTHOR FORMATTING
        >>> # format all values (i.e., author names) in each entry's 'author' field
        >>> for each_id, each_entry in pybtex_entries.items():
        ...     cleanAndFormatValues(each_entry.persons["author"],"pybtex_author_instance_name")
        ...     cleanAndFormatValues(each_entry.persons["author"],"pybtex_author_label")
        ['Jaschke_AC']
        ['Jaschke, AC']
        ['Lohr_A', 'Beunen_R', 'Savelli_H', 'Kalz_M', 'Ragas_A', 'Van_Belleghem_F']
        ['Lohr, A', 'Beunen, R', 'Savelli, H', 'Kalz, M', 'Ragas, A', 'Van_Belleghem, F']
        ['Mendoza_Rodriguez_JP', 'Wielhouwer_JL', 'Kirchler_ESMN']
        ['Mendoza_Rodriguez, JP', 'Wielhouwer, JL', 'Kirchler, ESMN']
        ['%40uthor_%CE%BDbn', 'Aaboud_M', 'Bentvelsen_S', 'Berge_D', 'Colijn_AP', 'de_Jong_P', 'Koffeman_E', 'Sabato_G', 'Salek_D', 'van_Vulpen_I', 'Vermeulen_JC', 'Vreeswijk_M']
        ['@uthor, νbn', 'Aaboud, M', 'Bentvelsen, S', 'Berge, D', 'Colijn, AP', 'de_Jong, P', 'Koffeman, E', 'Sabato, G', 'Salek, D', 'van_Vulpen, I', 'Vermeulen, JC', 'Vreeswijk, M']

        >>> # AUTHOR FORMATTING + ADDING TO BIBLIOGRAPHY
        >>> # format all values (i.e., author names) in each entry's 'author' field...
        >>> # ...and this time add these formatted values to a Bibliography class instance
        >>> my_bibliography = Bibliography()
        >>> for each_id, each_entry in pybtex_entries.items():
        ...     # create a shorter name for 'author' field
        ...     each_author_field_values = each_entry.persons["author"]
        ...
        ...     # format values in 'author' fields
        ...     each_formatted_author_instance_names_list = cleanAndFormatValues(each_author_field_values, "pybtex_author_instance_name")
        ...     each_formatted_author_labels_list = cleanAndFormatValues(each_entry.persons["author"],"pybtex_author_label")
        ...
        ...     # add now-formatted entries to Bibliography object
        ...     my_bibliography.setEntry(each_id, "b_author", each_formatted_author_instance_names_list)
        ...     my_bibliography.setEntry(each_id, "b_author_labels", each_formatted_author_labels_list)
        >>>
        >>> # print the now-populated Bibliography object
        >>> my_bibliography.entries
        {'56fafbf2574947cc9cbbfae578a0a36d': {'b_author': ['Jaschke_AC'], 'b_author_labels': ['Jaschke, AC']}, 'd79d00c790984ab08240e997d077c332': {'b_author': ['Lohr_A', 'Beunen_R', 'Savelli_H', 'Kalz_M', 'Ragas_A', 'Van_Belleghem_F'], 'b_author_labels': ['Lohr, A', 'Beunen, R', 'Savelli, H', 'Kalz, M', 'Ragas, A', 'Van_Belleghem, F']}, 'a8781aa0eae047d1826a658f3545ce3f': {'b_author': ['Mendoza_Rodriguez_JP', 'Wielhouwer_JL', 'Kirchler_ESMN'], 'b_author_labels': ['Mendoza_Rodriguez, JP', 'Wielhouwer, JL', 'Kirchler, ESMN']}, '01b9c957875b4a96839c1bfd05ec6a31': {'b_author': ['%40uthor_%CE%BDbn', 'Aaboud_M', 'Bentvelsen_S', 'Berge_D', 'Colijn_AP', 'de_Jong_P', 'Koffeman_E', 'Sabato_G', 'Salek_D', 'van_Vulpen_I', 'Vermeulen_JC', 'Vreeswijk_M'], 'b_author_labels': ['@uthor, νbn', 'Aaboud, M', 'Bentvelsen, S', 'Berge, D', 'Colijn, AP', 'de_Jong, P', 'Koffeman, E', 'Sabato, G', 'Salek, D', 'van_Vulpen, I', 'Vermeulen, JC', 'Vreeswijk, M']}}

        >>> # DOCUMENT INSTANCE NAME FORMATTING
        >>> # Transform pybtex title string to document_instance_name:
        >>> pybtex_entries = Pybtex_import("example_data//test.bib").data.entries
        pybtex package is parsing using bibtex.Parser()...
        pybtex package finished parsing
        >>> my_bibliography = Bibliography()
        >>>
        >>> for each_entry_id, each_entry_data in pybtex_entries.items():
        ...     each_document_instance_name = cleanAndFormatValues(each_entry_data.fields["title"], "pybtex_document_instance_name")
        ...     my_bibliography.setEntry(each_entry_id, "document_instance_name", each_document_instance_name)
        >>> my_bibliography.entries
        {'56fafbf2574947cc9cbbfae578a0a36d': {'document_instance_name': 'Book_with_one_author'}, 'd79d00c790984ab08240e997d077c332': {'document_instance_name': 'Article_with_5_authors_with_and_notation'}, 'a8781aa0eae047d1826a658f3545ce3f': {'document_instance_name': 'Article_with_3_authors_with_mixed_notation'}, '01b9c957875b4a96839c1bfd05ec6a31': {'document_instance_name': 'Article_with_non-uri_safe_characters%3A%3C%3E%5B%5D_%40%25_to_WW_%E2%88%97%E2%86%92e%CE%BD%CE%BC%CE%BD_with_the_ATLAS_detector_at_%E2%88%9As%3D8_TeV'}}

        >>> # TOPIC FORMATTING
        >>> # transform pybtex keywords string to list of topics
        >>> # (this example depends on imports made in previous examples)
        >>> pybtex_entries = Pybtex_import("example_data//test.bib").data.entries
        pybtex package is parsing using bibtex.Parser()...
        pybtex package finished parsing
        >>> # test diagnostic. necessary because try-except block would succeed even if the code does nothing
        >>> no_of_keywords_processed = 0
        >>>
        >>> for each_pybtex_entry_id, each_pybtex_entry_data in pybtex_entries.items():
        ...    # if pybtex entry contains keywords
        ...    try:
        ...        # extract keywords
        ...        each_keyword_value_string = each_pybtex_entry_data.fields["keywords"]
        ...        # format and tokenize keywords string in order to transform it into a list of topics
        ...        each_formatted_keyword_list = cleanAndFormatValues(each_keyword_value_string, "pybtex_topic_instance_name")
        ...        # add the newly generated topics to the Bibliography instance
        ...        my_bibliography.setEntry(each_pybtex_entry_id, "b_topics", each_formatted_keyword_list)
        ...
        ...        # test diagnostic
        ...        no_of_keywords_processed = no_of_keywords_processed + 1
        ...    except:
        ...        pass
        >>>
        >>> # test diagnostic
        >>> if no_of_keywords_processed == 0:
        ...     raise Exception ("Test failed: No keywords processed inside the try-except block.")
    """
    import re
    from urllib.parse import quote

    # special characters to omit from strings
    # NOTE: currently, same characters are omitted for both labels and author names.
    # ...for richer labels, this can be changed in a future revision.
    # this variable is used by several cleaning/formatting algorithms within the current function
    pattern_of_characters_to_omit = "[.,;\'\")(}{]"

    # special character patterns to replace in strings
    # in this dictionary, keys are target patterns and values are replacements
    # note the spaces in the patterns (i.e., in keys of the dictionary)
    # this dictionary is used by several cleaning/formatting algorithms within the current function
    dictionary_of_patterns_to_replace = {
        ": ": "-",
        " - ": "-",
        # This pattern replacement is important for .bib files, as the pattern {"} is used to denote double quotation
        # marks in .bib files. It should be used (at least) for replacing this pattern in titles and abstract strings.
        # (otherwise, it leads to errors in .ttl files)
        '\{"\}': "'"
    }

    # error handling for keywords of the 'algorithm' parameter is handled this way, as an 'else'
    # statement at the end of elif block for keywords does not produce the same result ('else' too broad?)
    # if the entered 'algorithm' parameter is unrecognized
    algorithm_keywords_list = ["pybtex_author_instance_name",
                               "pybtex_author_label",
                               "pybtex_document_instance_name",
                               "pybtex_document_label",
                               "pybtex_topic_instance_name",
                               "pybtex_topic_label",
                               "open_citations_author_instance_name",
                               "open_citations_author_label"
                               "none"]

   # if algorithm not in algorithm_keywords_list:
    #    raise Exception ('Unknown algorithm parameter: "' + algorithm + '". Please enter a valid algorithm.')


    #-------------------------------------------------------------------#
    #              FORMAT: AUTHOR INSTANCE NAME AND LABEL               #
    #-------------------------------------------------------------------#
    # algorithm for pybtex author field
    if algorithm is "pybtex_author_instance_name" or algorithm is "pybtex_author_label":
    # TODO: Initial letter of last names and first name abbreviations should always be capitalized, even if this is not the case in input

        # a more descriptive name for target_field
        inputted_author_field_value_list = target_field

        # two container variables for author (instance) names and author labels (which will later be needed by RDF format)
        each_formatted_author_instance_list = []
        each_formatted_author_label_list = []

        each_abbreviated_first_names_string = ""

        # for each "author" field value (which can hold multiple authors as a list) in the pybtex bib data
        for each_author in inputted_author_field_value_list:
            # extract and format each LAST NAME (if available)
            try:
                each_last_name = str(each_author.last()[0])
                each_last_name_formatted = re.sub(pattern_of_characters_to_omit, "", each_last_name)
                each_last_name_formatted = re.sub(" ", "_", each_last_name_formatted)


                # extract and format each FIRST NAME (if available)
                try:
                    # extract first name of a single author
                    each_first_names_string = str(each_author.first()[0])
                    # omit unwanted characters
                    each_first_names_string = re.sub(pattern_of_characters_to_omit, "", each_first_names_string)
                    # placeholder for output
                    each_abbreviated_first_names_string = ""

                    # for the first name's letters (e.g., "John", but "{John Some Middle Name}" is also possible)
                    for i, each_letter in enumerate(each_first_names_string):
                        # always add the first letter of a first name to abbreviated first name (i.e., the output)
                        if i == 0:
                            each_abbreviated_first_names_string = each_abbreviated_first_names_string + each_first_names_string[i]
                        # for the other letters that may be present in the first name string
                        else:
                            # if there are spaces or uppercase letter in the first name string
                            if " " in each_first_names_string or any(letter.isupper() for letter in each_first_names_string):
                                # add the character after space, or the capital letter, to the first name
                                if each_first_names_string[i-1] == " " or each_first_names_string[i].isupper() == True:
                                    each_abbreviated_first_names_string = each_abbreviated_first_names_string + each_first_names_string[i]
                                # otherwise, don't do anything
                                else:
                                    pass
                            # if there are no spaces of uppercase letters in the first name string, don't do anything additional
                            else:
                                pass
                # if a first name is not available, don't do anything
                except:
                    pass

            except:
                pass

            # add extracted last and first names to the output variables (as author instance names or as labels, ...
            # ...depending on the 'algorithm' parameter)
            if algorithm is "pybtex_author_instance_name":
                each_formatted_fullname = each_last_name_formatted + "_" + each_abbreviated_first_names_string
                each_formatted_fullname = quote(each_formatted_fullname)  # make safe to use as URI
                each_formatted_author_instance_list.append(each_formatted_fullname)

            elif algorithm is "pybtex_author_label":
                each_formatted_fullname = each_last_name_formatted + ", " + each_abbreviated_first_names_string

                each_formatted_author_label_list.append(each_formatted_fullname)
                #each_formatted_author_label_list.append(each_last_name_formatted + ", " + each_first_name_formatted)

        # return either author instance names or author labels depending on which 'algorithm' parameter is entered
        if algorithm is "pybtex_author_instance_name":
            return each_formatted_author_instance_list
        elif algorithm is "pybtex_author_label":
            return each_formatted_author_label_list

    #-----------------------------------------------------------------------------------------------#
    #              FORMAT: OPEN CITATIONS AUTHOR INSTANCE NAME AND LABEL PREPROCESSOR               #
    #-----------------------------------------------------------------------------------------------#
    if algorithm is "open_citations_author_instance_name" or algorithm is "open_citations_author_label":
        authors_list = target_field
        each_formatted_author_instance_list = []
        each_formatted_author_label_list = []

        each_last_name_formatted = ""
        each_abbreviated_first_names_string = ""

        for each_author_full_name in authors_list:
            try:
                each_author_split_names_list = each_author_full_name.split(' - ')
                each_last_name = each_author_split_names_list[0]
                each_first_names_string = each_author_split_names_list[1]

                each_last_name_formatted = re.sub(pattern_of_characters_to_omit, "", each_last_name)
                each_last_name_formatted = re.sub(" ", "_", each_last_name_formatted)

                # extract and format each FIRST NAME (if available)
                try:
                    # omit unwanted characters
                    each_first_names_string = re.sub(pattern_of_characters_to_omit, "", each_first_names_string)
                    # placeholder for output
                    each_abbreviated_first_names_string = ""

                    # for the first name's letters (e.g., "John", but "{John Some Middle Name}" is also possible)
                    for i, each_letter in enumerate(each_first_names_string):
                        # always add the first letter of a first name to abbreviated first name (i.e., the output)
                        if i == 0:
                            each_abbreviated_first_names_string = each_abbreviated_first_names_string + \
                                                                  each_first_names_string[i]
                        # for the other letters that may be present in the first name string
                        else:
                            # if there are spaces or uppercase letter in the first name string
                            if " " in each_first_names_string or any(
                                    letter.isupper() for letter in each_first_names_string):
                                # add the character after space, or the capital letter, to the first name
                                if each_first_names_string[i - 1] == " " \
                                        or each_first_names_string[i].isupper() == True:
                                    each_abbreviated_first_names_string = each_abbreviated_first_names_string + \
                                                                          each_first_names_string[i]
                                # otherwise, don't do anything
                                else:
                                    pass
                            # if there are no spaces of uppercase letters in the first name string, don't do anything additional
                            else:
                                pass
                # if a first name is not available, don't do anything
                except:
                    pass
            except:
                pass

            # add extracted last and first names to the output variables (as author instance names or as labels, ...
            # ...depending on the 'algorithm' parameter)
            if algorithm is "open_citations_author_instance_name":
                each_formatted_fullname = each_last_name_formatted + "_" + each_abbreviated_first_names_string
                each_formatted_fullname = quote(each_formatted_fullname)  # convert to uri-safe string
                each_formatted_author_instance_list.append(each_formatted_fullname)

            elif algorithm is "open_citations_author_label":
                each_formatted_fullname = each_last_name_formatted + ", " + each_abbreviated_first_names_string
                each_formatted_author_label_list.append(each_formatted_fullname)
                # each_formatted_author_label_list.append(each_last_name_formatted + ", " + each_first_name_formatted)

        # return either author instance names or author labels depending on which 'algorithm' parameter is entered
        if algorithm is "open_citations_author_instance_name":
            return each_formatted_author_instance_list
        elif algorithm is "open_citations_author_label":
            return each_formatted_author_label_list


    # -------------------------------------------------------------------#
    #              FORMAT: DOCUMENT INSTANCE NAME AND LABEL              #
    # -------------------------------------------------------------------#
    # if the task is title to document_instance_name conversion
    elif algorithm is "pybtex_document_instance_name" or algorithm is "pybtex_document_label":
        # in this case, the input (i.e., 'target_field') will be a string

        # standardize capitalization in the string (e.g., '  At ' -> ' at ')
        document_instance_name = standardizeCapitalization(target_field, "en_title")
        # replace remaining undesired characters with the desired ones (e.g., ':' -> '-' or '{"}' with a double quote)
        # using dictionary_of_patterns_to_replace
        document_instance_name = replacePatternsAsPerDictionary(document_instance_name,
                                                                dictionary_of_patterns_to_replace)

        if algorithm is "pybtex_document_instance_name":
            # omit undesired characters from this string
            document_instance_name = re.sub(pattern_of_characters_to_omit, "", document_instance_name)
            document_instance_name = replacePatternsAsPerDictionary(document_instance_name,
                                                                    dictionary_of_patterns_to_replace)
            # replace spaces with underscores
            document_instance_name = re.sub(" ", "_", document_instance_name)

            # convert to uri-safe string
            document_instance_name = quote(document_instance_name)

        return document_instance_name


    # ---------------------------------------------------------------------------#
    #                 FORMAT: TOPIC INSTANCE NAME AND TOPIC LABEL                #
    # ---------------------------------------------------------------------------#
    elif algorithm is "pybtex_topic_instance_name" or algorithm is "pybtex_topic_label":
        # tokenize string input (which is in the format of "topic string 1, topic string 2")
        # note that the split character is ", " and not ",". if space is not included, the first character of topics
        # end up being a space e.g., " topic 1" instead of "topic 1" .
        tokenized_topics_list = target_field.split(", ")

        # placeholder for final output
        formatted_topics_list = []

        for each_topic_string in tokenized_topics_list:
            # omit unwanted characters
            each_formatted_topic = re.sub(pattern_of_characters_to_omit, "", each_topic_string)
            # standardize capitalization in the string (e.g., '  At ' -> ' at ')
            each_formatted_topic = standardizeCapitalization(each_formatted_topic, "en_title")

            # if the task is to formatting the input as an instance name
            if algorithm is "pybtex_topic_instance_name":
                each_formatted_topic = each_formatted_topic.lower()
                # replace remaining unwanted characters/patterns with the ones in dictionary_of_patterns_to_replace
                each_formatted_topic = replacePatternsAsPerDictionary(each_formatted_topic,
                                                                      dictionary_of_patterns_to_replace)
                # replace spaces with underscores
                each_formatted_topic = re.sub(" ", "_", each_formatted_topic)

                # convert to uri-safe string
                each_formatted_topic = quote(each_formatted_topic)

            # if the task is to format as a topic label
            elif algorithm is "pybtex_topic_label":
                # keep the spaces (i.e., " " character) in topic strings
                pass

            # add the formatted topics list to the output variable
            formatted_topics_list.append(each_formatted_topic)

        return formatted_topics_list


    # ---------------------------------------------------------------------------#
    #               NO FORMATTING: MINIMIZE LISTS (FOR NOW)                      #
    # ---------------------------------------------------------------------------#
    # TODO: Remove these function. This is a temporary workaround.
    elif algorithm is "open_citations_list_minimizer":
        if type(target_field) is list:
            inputted_list = target_field
            return inputted_list[0]
        else:
            return target_field

    elif algorithm is "open_citations_list_minimizer_2":
        if type(target_field) is list:
            inputted_list = target_field
            try:
                return inputted_list[1]
            except:
                return inputted_list[0]
        else:
            return target_field

    # ---------------------------------------------------------------------------#
    #               NO FORMATTING: MINIMIZE LISTS (FOR NOW)                      #
    # ---------------------------------------------------------------------------#
    elif algorithm is "none":
        # if no formatting is wanted, the target field values are returned as they are.
        return target_field