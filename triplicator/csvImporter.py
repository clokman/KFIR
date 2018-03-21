from triplicator.bibTools import Bibliography

# CSV_Bibliography is a subclass of Bibliography class
class CSV_Bibliography(Bibliography):
    def __init__(instance, csv_file_path, id_column_header,
                 field_value_list_separator, csv_delimiter_character,
                 cleaning_algorithm='parse only',
                 show_progress_bar=False):
        # TODO: add id_column_header ad field_value_list_separator arguments to Bibliography class __init__() function arguments.
        """
        A set of methods that parse a .csv file and store its variables as attributes of a Bibliography class instance.

        Args:
            csv_file_path(str): Path to csv file to be imported.
            id_column_header(str):   The name of the column that will be used as entry id for each entry
            field_value_list_separator(str): If a field's values contain multiple values, such as multiple authors,
                the separator characters are specified here (e.g., '|'or ' | ').
            csv_delimiter_character(str): The delimiter that separates columns in the .csv file. Must be only one
                character, and not a string of multiple characters.
            cleaning_algorithm(str): Cleaning algorithm to be used on the file before it is tokenized

        Keyword Args:
            "parse only" (cleaning_algorithm): Skip the cleaning and just parse data
            "open citations": (cleaning algorithm): Clean the .csv file according to the 'open citations' algorithm.

        Returns:
            A CSV_container instance

        Examples:
            >>> my_csv_bibliography = CSV_Bibliography(csv_file_path=          'example_data//test.csv',
            ...                                  id_column_header=             'referenceEntry',
            ...                                  field_value_list_separator=   ' | ',
            ...                                  csv_delimiter_character=      ',',
            ...                                  cleaning_algorithm=           'default'
            ... )
            Conversion from ListData to Bibliography object started
            Conversion completed. 7 out of 7 ListData rows converted to Bibliography object entries
            >>> my_csv_bibliography.preview(1)
            <BLANKLINE>
            ----------------------------------ENTRY 1----------------------------------
            ('https://w3id.org/oc/corpus/br/44493',
             {'': '',
              'authors': ['Sandall - Jane', 'Soltani - Hora', 'Gates - Simon',
                          'Shennan - Andrew', 'Devane - Declan'],
              'dois': '10.1002/14651858.cd004667.pub3',
              'pages': '  ',
              'pmids': '23963739',
              'publication_types': ['http://purl.org/spar/fabio/Expression',
                                    'http://purl.org/spar/fabio/ExpressionCollection'],
              'publications': 'Cochrane Database of Systematic Reviews - Reviews',
              'publishers': 'Wiley-Blackwell',
              'referenceEntry': 'https://w3id.org/oc/corpus/br/44493',
              'titles': 'Midwife-led continuity models versus other models of care for '
                        'childbearing women',
              'types': ['http://purl.org/spar/fabio/Expression',
                        'http://purl.org/spar/fabio/ReferenceEntry'],
              'urls': 'http://dx.doi.org/10.1002/14651858.cd004667.pub3',
              'years': '2013'})
            <BLANKLINE>

        """
        from preprocessor.legacy_functions.get_headers import get_headers
        from preprocessor.legacy_functions.get_data import get_data
        from preprocessor.legacy_functions.get_header_index import get_header_index

        ### Bibliography class instance attributes
        # adds the instance to the list of all instances of the class
        Bibliography._class_instance_registry.append(instance)
        # local equivalent of _class_field_values_registry. Does the same thing for the bibliography instance.
        instance._field_values_registry       = {}
        # hold all ids created within the bibliography instance. allows quick checking whether an id exists.
        instance._id_registry = []
        # dictionary for holding all field types and number of their occurrences
        instance._field_type_registry = {}

        instance._entries_with_failed_id_calls = []
        instance._no_of_ListData_rows_converted_to_Bibliography_entries = 0

        # pass parameters to instance variables
        instance.csv_file_path = csv_file_path
        instance.field_value_list_separator = field_value_list_separator
        instance.csv_delimiter_character = csv_delimiter_character
        instance.id_column_header = id_column_header
        instance.cleaning_algorithm = cleaning_algorithm

        # tokenize and store the cleaned file in a variable
        csv_file_content = instance.cleanAndTokenizeCsv()
        # get headers and data
        instance.headers = get_headers(csv_file_content)
        instance.data = get_data(csv_file_content)
        # get index positions of each header
        # this dictionary will be used to add values to appropriate index positions in rows
        instance.header_index_positions_dictionary = {}
        for each_header in instance.headers:
            instance.header_index_positions_dictionary[each_header] = get_header_index(each_header,
                                                                              csv_file_content)
        # get index position of the 'entry id' header,
        # which will be extracted to be used as 'entry id' in the new Bibliography object
        instance.id_column_index_position = get_header_index(id_column_header, csv_file_content)

        # a dictionary to hold parsed entities in a way compatible to Bibliography class
        instance.entries = {}
        instance.convertListDataToEntries(show_progress_bar)


    def convertListDataToEntries(instance, show_progress_bar):
        """
        Converts a dataset being stored in list format to instance.entries dictionary.
        """
        from meta.consoleOutput import ConsoleOutput
        console = ConsoleOutput(log_file_path='log.txt')
        maximum_progress = len(instance.data)
        console.log_message('Conversion from ListData to Bibliography object started', add_timestamp_in_file=True)

        # for each row in the imported data
        for i, each_row in enumerate(instance.data):
            if show_progress_bar:
                console.print_current_progress(i, maximum_progress, 'Converting ListData rows to Bibliography entries')

            try:
                # extract id value from each column, using the id_column_index_position to locate them.
                each_id_cell_value = each_row[instance.id_column_index_position]
                # set each id as key for entries dictionary, and let these keys hold an empty dictionary for now
                # (i.e., the ENTRY_ID in 'my_bibliography.entries = {ENTRY_ID:{FIELD_NAME:FIELD VALUE}}' ).
                instance.entries[each_id_cell_value] = {}
                # set field-value pairs as a sub-dictionary to each entry id key
                # (i.e., the FIELD_NAME and FIELD VALUE in 'my_bibliography.entries = {ENTRY_ID:{FIELD_NAME:FIELD VALUE}}' ).

                # and while iterating through each row, also iterate for each header name-index pair
                #   in the imported data
                for each_header_name, each_header_index_position in instance.header_index_positions_dictionary.items():
                    # if there is a row value (i.e., field value) corresponding to the header index position
                    # (i.e., field name), add this field_name-field_value pair to my_bibliography.entries
                    # dictionary. (a row value/field value may not always exist, for instance 'isbn' field
                    # may not be always present in the imported records.)
                    try:
                        # extract each cell value that corresponds to each header index position for each row
                        each_targeted_cell_value = each_row[each_header_index_position]

                        # if the specified list separator character exists in the current targeted cell
                        # (e.g., if the cell contains a list of authors, such as [Doe--John | Doe--Jane]
                        if instance.field_value_list_separator in each_targeted_cell_value:
                            # tokenize the targeted cell using the specified list separator character
                            each_tokenized_targeted_cell_value = \
                                (each_targeted_cell_value.split(instance.field_value_list_separator))
                            # add each header and their corresponding target value for the each row to the
                            # my_bibliography.entries dictionary, by binding the field_name-field_value pairs
                            # to entry ids already exising in the my_bibliography.entries dictionary
                            # (entry ids were empty sub-dictionary keys of my_bibliography.entries dictionary
                            # until this point).
                            instance.setEntry(each_id_cell_value, each_header_name, each_tokenized_targeted_cell_value)

                        # if there is no aggregation in the cell
                        else:
                            # simply add field_name-field_value pairs to my_bibliography.entries dictionary, as
                            # subdictionaries to entry ids.
                            instance.setEntry(each_id_cell_value, each_header_name, each_targeted_cell_value)

                    # if there is no value in a row that corresponds to the current field name in the loop, do nothing
                    except IndexError:
                        pass

                instance._no_of_ListData_rows_converted_to_Bibliography_entries += 1

            # if the id call fails, skip this entry and log the line in instance registry for diagnostic purposes. This
            # is most likely caused by an erroneous row in the CSV file ending too early (i.e., cell does not have even
            # an empty value such as "" that corresponds to the id column)
            except IndexError:
                instance._entries_with_failed_id_calls.append(each_row)

        console.log_message('Conversion completed. %d out of %d ListData rows converted to Bibliography object entries'
                            % (instance._no_of_ListData_rows_converted_to_Bibliography_entries, len(instance.data)),
                            add_timestamp_in_file=True)
        if instance._entries_with_failed_id_calls:
            console.log_list_with_caption('These ListData rows were failed in conversion (likely due to not having a '
                                          'valid cell that correspond to the specified ID column)',
                                          instance._entries_with_failed_id_calls,
                                          print_list_length_with_caption=True)


    def cleanAndTokenizeCsv(instance):
        """
        Imports the .csv file as raw text, cleans it (if cleaning algorithm is specified), and then tokenizes it.

        Returns:
            List containing parsed data from the .csv file. For each row in the .csv file (including headers row), a
                sub-list is created in the main list.

        Examples:
            >>> from preprocessor.Text_File import Text_File
            >>> my_file = Text_File('example_data//problematic_yasgui_csv_file.csv')
            >>> my_file.print_lines(2)
            "27624462" , "2016" , "Journal Article" , "Duku - Stephen Kwasiââ OpokuĂŠ | Asenso-Boadi - Francis" , "[]{}\ '<Utilization, of, healthcare services and renewal of health insurance membership: evidence of adverse selection in Ghana" , "Springer Science + Business Media" , "1" , "Health Econ Rev - Health Economics Review" , "http://dx.doi.org/10.1186/s13561-016-0122-6" , "6" , "10.1186/s13561-016-0122-6" , "" , "https://w3id.org/oc/corpus/br/3555801" , "https://w3id.org/oc/corpus/br/18754 | https://w3id.org/oc/corpus/br/18792" ,


            >>> my_csv_bibliography = CSV_Bibliography(
            ...                           csv_file_path='example_data//problematic_yasgui_csv_file.csv',
            ...                           id_column_header='journal_article',
            ...                           field_value_list_separator=' | ',
            ...                           csv_delimiter_character=',',
            ...                           cleaning_algorithm='default'
            ... )
            Conversion from ListData to Bibliography object started
            Conversion completed. 2 out of 2 ListData rows converted to Bibliography object entries
            >>> my_csv_bibliography.preview(1) # notice the character conversions in the 'authors' and 'title' fields
            <BLANKLINE>
            ----------------------------------ENTRY 1----------------------------------
            ('https://w3id.org/oc/corpus/br/3555801',
             {'': '',
              'authors': ['Duku - Stephen Kwasiaa OpokuAS', 'Asenso-Boadi - Francis'],
              'cited_by_the_articles': '',
              'cited_the_articles': ['https://w3id.org/oc/corpus/br/18754',
                                     'https://w3id.org/oc/corpus/br/18792'],
              'doi': '10.1186/s13561-016-0122-6',
              'journal_article': 'https://w3id.org/oc/corpus/br/3555801',
              'journal_issue_number': '1',
              'journal_name': 'Health Econ Rev - Health Economics Review',
              'journal_volume_number': '6',
              'pmid': '27624462',
              'publication_type': 'Journal Article',
              'publication_year': '2016',
              'publisher_name': 'Springer Science + Business Media',
              'title': ' Utilization-of-healthcare services and renewal of health '
                       'insurance membership: evidence of adverse selection in Ghana',
              'url': 'http://dx.doi.org/10.1186/s13561-016-0122-6'})
            <BLANKLINE>
        """
        import re
        import csv
        from os import remove as os_remove
        from preprocessor.string_tools import String

        # open the csv file and read it to a variable
        imported_file_raw = open(instance.csv_file_path, mode="r", encoding="utf8")
        imported_string_raw = imported_file_raw.read()

        # if no cleaning algorithm is specified, skip cleaning and just tokenize
        if instance.cleaning_algorithm == 'parse only':
            imported_string_cleaned = imported_string_raw

        # otherwise, run cleaning algorithm
        elif instance.cleaning_algorithm == 'default':
            # TODO: The current way to remove in-string commas is tuned for OpenCitations data with yasgui style CSV. Make a generic version by using a while loop (see commented out draft below).
            # clean commas that occur in entry field values (i.e., within strings)
            imported_string_cleaned = re.sub(' ,', '_-_-_', imported_string_raw)
            imported_string_cleaned = re.sub(', ', '-', imported_string_cleaned)
            imported_string_cleaned = re.sub('_-_-_', ' ,', imported_string_cleaned)

            # clean CSV file from double quotes
            imported_string_cleaned = re.sub(' "|" ', '', imported_string_cleaned)

            # clean from characters and patterns that are generally problematic for parsing operations
            imported_string_cleaned = String(imported_string_cleaned)
            imported_string_cleaned.purify(clean_from_non_ascii_characters=True,
                                           remove_problematic_patterns=True,
                                           clean_newline_characters=False)
            imported_string_cleaned = str(imported_string_cleaned)

            # # Draft while loop for a more generic future algorithm to replace in-string commas:
            #
            # between_quotes = False
            # for i, each_character in enumerate(imported_string_cleaned):
            #
            #    if between_quotes:
            #        if each_character == ",":
            #            imported_string_cleaned[i] = "-"
            #            print(imported_string_cleaned)
            #
            #    # first occurrence
            #    if each_character == '\"' and not between_quotes:
            #        between_quotes = True
            #    elif each_character == '\"' and between_quotes:
            # importCleanedCsvbetween_quotes = False
        # if the cleaning_algorithm parameter is not recognized, return error
        else:
            raise ValueError('Unknown algorithm type: ' + instance.cleaning_algorithm + '. Please enter a valid algorithm string.')

        # close the original csv file (no changes made to it)
        imported_file_raw.close()

        # create a temporary file to hold the cleaned csv file (a file is needed for csv() function)
        cleaned_file_path = "temp_cleaned.csv"
        cleaned_csv_file = open(cleaned_file_path, mode="w", encoding="utf8")
        cleaned_csv_file.write(imported_string_cleaned)
        cleaned_csv_file.close()

        # read from the temporary file and tokenize it
        cleaned_csv_file = open(cleaned_file_path, mode="r", encoding="utf8")
        cleaned_csv_file_content = list(csv.reader(cleaned_csv_file,
                                                   delimiter=instance.csv_delimiter_character))
        cleaned_csv_file.close()

        # remove the temporary file
        os_remove('temp_cleaned.csv')

        return cleaned_csv_file_content