class ListData():
    def __init__(instance):

        ### INTERNAL PARAMETERS #############
        instance.missing_data_character = " "
        #####################################

        instance.dataset = []

    def headers(instance):
        """
        Returns the first row of the instance.dataset

        Returns:
            List

        """
        return instance.dataset[0]


    def data_rows(instance):
        """
        Returns the rows of the instance.dataset except the first rows.

        Returns:
            List
        """
        return instance.dataset[1:len(instance.dataset)]


    def importBibliography(instance, input_Bibliography_instance):
        """
        Converts a Bibliography class object to a ListData object.

        Returns:
            ListData class object

        Examples:
            >>> from triplicator.bibliographyInstantiator import Bibliography
            >>> my_bibliography = Bibliography()
            >>> my_bibliography.setEntry('01', 'author', 'John Doe')
            >>> my_bibliography.setEntry('02', 'author', 'Jane Doe')
            >>> #my_bibliography.import_data('..//triplicator//example_data//test.bib')
            >>> print(my_bibliography.entries)
            {'01': {'author': 'John Doe'}, '02': {'author': 'Jane Doe'}}
            >>> my_list_data = ListData()
            >>> my_list_data.importBibliography(my_bibliography)
            >>> print(my_list_data.dataset)
            [['author'], ['John Doe'], ['Jane Doe']]

        """
        from preprocessor.get_header_index import get_header_index

        # iterate through all entries and their ids in the input Bibliography
        # (this first iteration is only for indexing all headers in the instance.headers_row. all headers must be
        # indexed first before starting to add data rows, because adding header names on-the-go would create data rows
        # of differing lengths)

        # instance.headers should be empty (and thus, should give an error if attempted to be indexed)
        try:
            # if instance.headers is not empty (and thus, does not give an index error) raise exception
            if instance.headers():
                raise Exception('Instance.headers not empty prior to append operation. This method is not compatible '
                                'with adding new headers/columns.')
        # if there an index error, this indicates that the instance.headers() is indeed empty (and therefore cannot
        # be indexed).
        except IndexError:

            headers_list = []

            for each_entry_id, each_entry_data in input_Bibliography_instance.entries.items():
                # add each field name in the input Bibliography to instance.headers_row
                for each_field_name in each_entry_data.keys():
                    if each_field_name not in headers_list:
                        # add to headers row
                        headers_list.append(each_field_name)

        # add the now fully populated instance.headers_row as the first row of the full dataset (instance.dataset)
        instance.dataset.append(headers_list)

        # iterate (once again) through all entries and their ids in the input Bibliography
        # (this second iteration is for adding data rows)

        for each_entry_id, each_entry_data in input_Bibliography_instance.entries.items():
            # add a blank list to represent a new row per each entry in inputted Bibliography object.
            instance.dataset.append([])
            # select the last added row
            current_row = instance.dataset[-1]
            # make this last added row (i.e., each row) as long as the header row
            while len(current_row) < len(instance.headers()):
                current_row.append(instance.missing_data_character)

            # for each field_name-field_value pair in the input Bibliography
            for each_field_name, each_field_value in each_entry_data.items():
                # extract the index number of the field name's representation in the headers row
                current_field_name_header_index = get_header_index(each_field_name, instance.dataset)
                current_row[current_field_name_header_index] = each_field_value

    def get_column_at_index(instance, index):
        '''
        Allows columns to be selected (i.e., returned) by entering their index position.
        
        :return: A list vector that contains values from the queried column
        
        :example:
            >>> my_listdata = ListData()
            >>> my_listdata.dataset = [['name', 'birth_date'], ['john', 2084], ['jane', 2054]]
            >>> my_listdata.get_column_at_index(1)
            ['birth_date', 2084, 2054]
        '''

        #############################################################################################################

        # assign the column matching the current_index to a variable
        column = [each_row[index] for each_row in instance.dataset]
        return column

    def get_row_length(instance):
        """
        Gets the length of a sample row from the dataset.

        Returns:
            Integer

        Examples:
        >>> my_listdata = ListData()
        >>> my_listdata.dataset = [['name', 'birth_date'], ['john', 2084], ['jane', 2054]]
        >>> my_listdata.get_row_length()
        2
        """

        probe_index = 0
        row_length = 0

        try:
            row_length = len(instance.dataset[probe_index])
        except IndexError:
            raise ('Not possible to probe row at index %s. Nothing found at this index position.' % probe_index)

        return row_length

    def transpose_dataset(instance):
        """

        >>> my_listdata = ListData()
        >>> my_listdata.dataset = [['name', 'birth_date'], ['john', 2084], ['jane', 2054]]
        >>> my_listdata.transpose_dataset().dataset
        [['name', 'john', 'jane'], ['birth_date', 2084, 2054]]
        >>> my_listdata.transpose_dataset().dataset
        [['name', 'birth_date'], ['john', 2084], ['jane', 2054]]

        >>> my_listdata.transpose_dataset().dataset == my_listdata.transpose_dataset().transpose_dataset().dataset
        True
        """
        row_length = instance.get_row_length()
        columns = [instance.get_column_at_index(i) for i in range(0, row_length)]

        instance.dataset = columns
        return instance

    def merge_all_rows_to_one(instance, value_separator_pattern=' | '):
        """
        >>> my_listdata = ListData().append_row(['john', 2054]).append_row(['john', 3254])
        >>> my_listdata.merge_all_rows_to_one().dataset
        ['john', '2054 | 3254']

        >>> my_listdata = ListData()
        >>> my_listdata.dataset = [['john', 2054], ['john', 3254], ['john', 2672]]
        >>> my_listdata.merge_all_rows_to_one().dataset
        ['john', '2054 | 3254 | 2672']

        # method does not deal with headers
        >>> my_listdata.dataset = [['name', 'birth_date'], ['john', 2084], ['john', 2054]]
        >>> my_listdata.merge_all_rows_to_one().dataset
        ['name | john', 'birth_date | 2084 | 2054']

        # but headers can be easily managed
        >>> my_listdata.dataset = [['name', 'birth_date'], ['john', 2084], ['john', 2054]]
        >>> my_listdata.dataset = my_listdata.dataset[1:]
        >>> my_listdata.merge_all_rows_to_one().dataset
        ['john', '2084 | 2054']

        # different separator pattern (and a transpose-like operation)
        >>> my_listdata.dataset = [['name', 'birth_date'], ['john', 2084], ['john', 2054], ['jane', 2054]]
        >>> my_listdata.merge_all_rows_to_one('; ').dataset
        ['name; john; jane', 'birth_date; 2084; 2054']

        >>> type(my_listdata.dataset)
        <class 'list'>

        >>> from preprocessor.csv_tools import CSV_Line, CSV_Row, Row_Merge_Buffer
        >>> line_1 = CSV_Line(' "Journal Article" , "https://w3id.org/oc/corpus/br/45174" , "An inventory for measuring clinical anxiety: Psychometric properties." , "1988" , "Steer - Robert A." , "Journal of Consulting and Clinical Psychology" , "6" , "56" , "893--897" , "American Psychological Association (APA)" , "10.1037//0022-006x.56.6.893" ,')
        >>> line_2 = CSV_Line(' "Journal Article" , "https://w3id.org/oc/corpus/br/45174" , "An inventory for measuring clinical anxiety: Psychometric properties." , "1988" , "John - Doe B." , "Journal of Consulting and Clinical Psychology" , "6" , "56" , "893--897" , "American Psychological Association (APA)" , "https://doi.org/10.1037//0022-006x.56.6.893" ,')
        >>> line_1.clean_head_and_tail_from_patterns(' ,', location='tail').clean_head_and_tail_from_patterns(' ', location='head')
        '"Journal Article" , "https://w3id.org/oc/corpus/br/45174" , "An inventory for measuring clinical anxiety: Psychometric properties." , "1988" , "Steer - Robert A." , "Journal of Consulting and Clinical Psychology" , "6" , "56" , "893--897" , "American Psychological Association (APA)" , "10.1037//0022-006x.56.6.893"'
        >>> line_2.clean_head_and_tail_from_patterns(' ,', location='tail').clean_head_and_tail_from_patterns(' ', location='head')
        '"Journal Article" , "https://w3id.org/oc/corpus/br/45174" , "An inventory for measuring clinical anxiety: Psychometric properties." , "1988" , "John - Doe B." , "Journal of Consulting and Clinical Psychology" , "6" , "56" , "893--897" , "American Psychological Association (APA)" , "https://doi.org/10.1037//0022-006x.56.6.893"'
        >>> row_1 = line_1.parse_line_and_CONVERT_to_CSV_Row(' , ').clean_cell_heads_and_tails_from_characters('"')
        >>> row_2 = line_2.parse_line_and_CONVERT_to_CSV_Row(' , ').clean_cell_heads_and_tails_from_characters('"')
        >>> buffer = Row_Merge_Buffer(1)
        >>> buffer.append_as_first_row_and_reset_buffer(row_1)
        "https://w3id.org/oc/corpus/br/45174: [['Journal Article', 'https://w3id.org/oc/corpus/br/45174', 'An inventory for measuring clinical anxiety: Psychometric properties.', '1988', 'Steer - Robert A.', 'Journal of Consulting and Clinical Psychology', '6', '56', '893--897', 'American Psychological Association (APA)', '10.1037//0022-006x.56.6.893']]"
        >>> buffer.append_row_if_ids_match(row_2)
        "https://w3id.org/oc/corpus/br/45174: [['Journal Article', 'https://w3id.org/oc/corpus/br/45174', 'An inventory for measuring clinical anxiety: Psychometric properties.', '1988', 'Steer - Robert A.', 'Journal of Consulting and Clinical Psychology', '6', '56', '893--897', 'American Psychological Association (APA)', '10.1037//0022-006x.56.6.893'], ['Journal Article', 'https://w3id.org/oc/corpus/br/45174', 'An inventory for measuring clinical anxiety: Psychometric properties.', '1988', 'John - Doe B.', 'Journal of Consulting and Clinical Psychology', '6', '56', '893--897', 'American Psychological Association (APA)', 'https://doi.org/10.1037//0022-006x.56.6.893']]"
        >>> buffer.merge_all_rows_to_one(' | ')
        "https://w3id.org/oc/corpus/br/45174: ['Journal Article', 'https://w3id.org/oc/corpus/br/45174', 'An inventory for measuring clinical anxiety: Psychometric properties.', '1988', 'Steer - Robert A. | John - Doe B.', 'Journal of Consulting and Clinical Psychology', '6', '56', '893--897', 'American Psychological Association (APA)', '10.1037//0022-006x.56.6.893 | https://doi.org/10.1037//0022-006x.56.6.893']"

        # List conversion with actual rows
        >>> a = ListData()
        >>> a.dataset = [['Journal Article', 'https://w3id.org/oc/corpus/br/45174', 'An inventory for measuring clinical anxiety: Psychometric properties.', '1988', 'Steer - Robert A.', 'Journal of Consulting and Clinical Psychology', '6', '56', '893--897', 'American Psychological Association (APA)', '10.1037//0022-006x.56.6.893'], ['Journal Article', 'https://w3id.org/oc/corpus/br/45174', 'An inventory for measuring clinical anxiety: Psychometric properties.', '1988', 'John - Doe B.', 'Journal of Consulting and Clinical Psychology', '6', '56', '893--897', 'American Psychological Association (APA)', 'https://doi.org/10.1037//0022-006x.56.6.893']]
        >>> a.merge_all_rows_to_one(' | ').dataset
        ['Journal Article', 'https://w3id.org/oc/corpus/br/45174', 'An inventory for measuring clinical anxiety: Psychometric properties.', '1988', 'Steer - Robert A. | John - Doe B.', 'Journal of Consulting and Clinical Psychology', '6', '56', '893--897', 'American Psychological Association (APA)', '10.1037//0022-006x.56.6.893 | https://doi.org/10.1037//0022-006x.56.6.893']

        # Row_Merge_Buffer class conversion with actual rows
        >>> a = Row_Merge_Buffer(1)
        >>> a.dataset = [['Journal Article', 'https://w3id.org/oc/corpus/br/45174', 'An inventory for measuring clinical anxiety: Psychometric properties.', '1988', 'Steer - Robert A.', 'Journal of Consulting and Clinical Psychology', '6', '56', '893--897', 'American Psychological Association (APA)', '10.1037//0022-006x.56.6.893'], ['Journal Article', 'https://w3id.org/oc/corpus/br/45174', 'An inventory for measuring clinical anxiety: Psychometric properties.', '1988', 'John - Doe B.', 'Journal of Consulting and Clinical Psychology', '6', '56', '893--897', 'American Psychological Association (APA)', 'https://doi.org/10.1037//0022-006x.56.6.893']]
        >>> a.merge_all_rows_to_one(' | ').dataset
        ['Journal Article', 'https://w3id.org/oc/corpus/br/45174', 'An inventory for measuring clinical anxiety: Psychometric properties.', '1988', 'Steer - Robert A. | John - Doe B.', 'Journal of Consulting and Clinical Psychology', '6', '56', '893--897', 'American Psychological Association (APA)', '10.1037//0022-006x.56.6.893 | https://doi.org/10.1037//0022-006x.56.6.893']

        # Error from empty dataset
        >>> a = ListData()
        >>>
        >>> try:
        ...     a.merge_all_rows_to_one(' | ') #  no item to index in empty dataset
        ... except Exception as error_message:
        ...     print('Exception: ' + str(error_message))
        Exception: Dataset to be merged is either empty or not indexable (no item at index [0]).
        The input dataset is:
        []
        """
        try:
            instance.dataset[0]
        except IndexError:
            raise IndexError('Dataset to be merged is either empty or not indexable (no item at index [0]).\nThe input dataset is:\n%s' % str(instance.dataset))


        dataset = instance.dataset
        # initiate merged_row with the first row of the dataset
        merged_row   = dataset[0]

        for each_row in dataset:
            current_row = each_row
            current_cell_position = 0
            for each_current_cell, each_merged_cell in zip(current_row, merged_row):
                if str(each_current_cell) not in str(each_merged_cell): # str conversion needed for 'in' comparison
                    merged_cell = str(each_merged_cell) + value_separator_pattern + str(each_current_cell)
                    merged_row[current_cell_position] = merged_cell
                current_cell_position += 1

                # no need to specify an else scenario, as if compared cells are the same, merged row can stay as is

        instance.dataset = merged_row
        return instance


    def append_row(instance, new_row):
        """
        Appends a row the ListData object's dataset variable.

        Returns:
            ListData object (instance)

        Examples:
            >>> my_listdata = ListData()
            >>> my_listdata.append_row([1,2,3]).dataset
            [[1, 2, 3]]

            >>> my_listdata.dataset
            [[1, 2, 3]]
            >>> my_listdata.append_row(['a','b','c']).dataset
            [[1, 2, 3], ['a', 'b', 'c']]

            >>> my_listdata.dataset
            [[1, 2, 3], ['a', 'b', 'c']]

            >>> my_listdata.append_row(['x', 'y']).append_row(['z', 't']).append_row(['m', 'n']).dataset
            [[1, 2, 3], ['a', 'b', 'c'], ['x', 'y'], ['z', 't'], ['m', 'n']]

        """
        instance.dataset.append(new_row)
        return instance

    def clear_all(instance):
        """
        Resets ListData object's dataset variable to its empty state.

        Returns:
            ListData object

        Examples:
            >>> my_listdata = ListData()
            >>> my_listdata.append_row([1,2,3]).dataset
            [[1, 2, 3]]
            >>> my_listdata.dataset
            [[1, 2, 3]]
            >>> my_listdata.clear_all().dataset
            []
            >>> my_listdata.dataset
            []
        """
        instance.dataset = []
        return instance

    def append_column(instance, new_column_values, new_column_name):
        """

        :param new_column_values:
        :param new_column_name:
        :param dataset:
        :return: Changes the inputted dataset when ran (no need for assigning the output to a variable).
        :usage: append_column(NEW_COLUMN_VARIABLES_LIST, NEW_COLUMN_NAME_STRING, DATASET)

        :example:
            >>> my_list_data = ListData()
            >>> my_list_data.dataset = [['day', 'month'], [1, 'June'], [3, 'May'], [4, 'Jun']]
            >>> years_column = [2149, 2150, 2151]
            >>> my_list_data.append_column(years_column, "year")
            >>> print(my_list_data.dataset) # changes the original data set without a need to assign the output to a new variable, etc.
            [['day', 'month', 'year'], [1, 'June', 2149], [3, 'May', 2150], [4, 'Jun', 2151]]
        """

        #############################################################################################################

        # Check for duplicate header names
        if new_column_name in instance.headers():  # if this duplicate check is not included, things go wrong (the duplicate header gets added to column values—a strange behavior, but it is prevented with not allowing duplicate headers).
            print(
                "ERROR: Header name already in dataset. Re-run all code up to this point or change header name.\nError "
                "occured while processing new_column_name: " + str(
                    new_column_name))
            raise ValueError(
                "Header name already in dataset. Please choose a different name. If name is correct, try re-running "
                "all code up to this point. (See console output for last header name processed.)")

        if len(new_column_values) != len(instance.data_rows()):
            raise Exception("Inputted column length must be equal to instance.dataset column length.\n" +
                            'new_column_values length: ' + str(len(new_column_values)) + '\n' +
                            'instance.data_rows() length: ' + str(len(instance.data_rows()))
            )

        # Append the inputted column to specified dataset
        # pass argument to variable
        new_column = new_column_values
        # new column = merging of column name and column values
        new_column.insert(0, new_column_name)
        # for each row in the dataset, append the new column at the end
        for i, row in enumerate(instance.dataset):
            instance.dataset[i].append(new_column[i])

    def remove_column(instance, target_column_header):
        """
        Removes a column from dataset.

        Args:
            target_column_header(str): Name of the column to be removed.

        Returns:
            Nothing; modifies dataset.

        Examples:
            >>> example_data = [['day', 'month', 'hour'], ['1', 'June', '12.00'], ['3', 'May', '11.00'],
            ...                ['4', 'Jun', '15.00']]
            >>> my_list_data = ListData()
            >>> my_list_data.dataset = example_data
            >>> print(my_list_data.dataset)
            [['day', 'month', 'hour'], ['1', 'June', '12.00'], ['3', 'May', '11.00'], ['4', 'Jun', '15.00']]
            >>> my_list_data.remove_column('hour')
            >>> print(my_list_data.dataset)
            [['day', 'month'], ['1', 'June'], ['3', 'May'], ['4', 'Jun']]

        """

        #############################################################################################################

        # the column header also needs to be included in removal process
        from preprocessor.get_header_index import get_header_index
        target_index = get_header_index(target_column_header, instance.dataset)
        for i, row in enumerate(instance.dataset):
            del (instance.dataset[i][target_index])

    def remove_columns(instance, target_column_headers_list):
        """
        Removes multiple columns from dataset. Is a variation of .remove_column() method to support efficient removal
        of multiple columns.

        Args:
            target_column_headers_list(list): A list of strings whose items are the header names of columns to
                be removed

        Returns:
            Nothing; modifies dataset.
        """
        if type(target_column_headers_list) == list:
            pass
        else:
            raise Exception('The argument "target_column_headers_list" must be of "list" type.')

        for each_column_header in target_column_headers_list:
            instance.remove_column(each_column_header)

    def replace_headers(instance, header_replacements_list):
        """
        Replaces headers of a dataset.

        Args:
            header_replacements_list(list): A list of strings to replace headers

        Returns:
            Nothing; modifies the provided dataset.

        Examples:
            >>> example_data = [['day', 'month'], ['1', 'June'], ['3', 'May'], ['4', 'Jun']]
            >>> my_list_data = ListData()
            >>> my_list_data.dataset = example_data
            >>> print(my_list_data.dataset)
            [['day', 'month'], ['1', 'June'], ['3', 'May'], ['4', 'Jun']]
            >>> my_list_data.replace_headers(['d', 'm'])
            >>> print(my_list_data.dataset)
            [['d', 'm'], ['1', 'June'], ['3', 'May'], ['4', 'Jun']]
        """
        # number of headers inputted should match the number of headers in the dataset
        if len(header_replacements_list) == len(instance.headers()):
            pass
        else:
            raise Exception('header_replacements_list should be the same length with instance.headers()' + '\n' +
                            'header_replacements_list length: ' + str(len(header_replacements_list)) + '\n' +
                            'instance.headers() length: ' + str(len(instance.headers()))
            )

        for i, each_header in enumerate(header_replacements_list):
            instance.dataset[0][i] = each_header


class ListBuffer(ListData):
    def __init__(self):
        ListData.__init__(self)

        # states
        self.is_empty = True

    def append_row(self, new_row):
        """
        Overrides the ListData method of the same name to change buffer state to 'not empty' after adding something to
        the buffer

        Args:
            new_row(list, bool, str, int): The object to be added as a new row to buffer

        Returns:
            ListData object (self)

        Examples:
            # initiate
            >>> my_buffer = ListBuffer()

            # empty?
            >>> my_buffer.is_empty
            True

            # simple add
            >>> a = my_buffer.append_row(['item 1', 'item 2', 'item 3']) # variable assignment is to suppress output

            # fluent interface
            >>> my_buffer.append_row(['item 4', 'item 5', 'item 6']). \
                    append_row(['item 7', 'item 8', 'item 9']).dataset
            [['item 1', 'item 2', 'item 3'], ['item 4', 'item 5', 'item 6'], ['item 7', 'item 8', 'item 9']]

            # empty now?
            >>> my_buffer.is_empty
            False

        """
        ListData.append_row(self, new_row)
        self.is_empty = False
        return self

    def is_each_row_balanced(self, exclude_special_rows_of_syntax=None):
        """
        Checks whether each row in buffer is balanced (i.e., does not have unmatched parantheses, brackets, etc). Can
        exclude special row types (e.g., comment) from evaluation.

        Args:
            exclude_special_rows_of_syntax(str): specifies what type of rows to exclude from evaluation
                (e.g., comment rows). Uses predefined syntax settings per specified syntax (e.g., 'bibtex').

        Keyword Args:
            - bibtex (exclude_special_rows_of_syntax): sets evaluation exclusion criteria for bibtex syntax

        Returns:
            boolean

        Examples:
            >>> # an unbalanced row is present
            >>> my_buffer = ListBuffer()
            >>> my_buffer.append_row(['a', 'b', 'c']).append_row(['d', 'e', 'f']).dataset
            [['a', 'b', 'c'], ['d', 'e', 'f']]
            >>> my_buffer.append_row(['g', 'h' , '>'])\
                    .is_each_row_balanced()
            False

            >>> # single row from a bib file
            >>> my_buffer = ListBuffer()
            >>> my_buffer.append_row('            year      = "2017",')\
                .is_each_row_balanced()
            True

            >>> # bibtex entry start (no exception vs. exception)
            >>> my_buffer.append_row('@article{96d9add3e2f44e8abbf030170689bc30,')\
                .is_each_row_balanced()
            False
            >>> my_buffer.is_each_row_balanced(exclude_special_rows_of_syntax='bibtex')
            True

            >>> # bibtex comment (no exception vs. exception)
            >>> my_buffer = ListBuffer()
            >>> my_buffer.append_row('% This is a comment with an unbalanced characters }]>')\
                .is_each_row_balanced()
            False
            >>> my_buffer.is_each_row_balanced(exclude_special_rows_of_syntax='bibtex')
            True

            >>> # a full bibtex entry with an unbalanced curly bracket at title field
            >>> my_buffer = ListBuffer()
            >>> my_buffer.dataset = ['@book{a82caf00e1a143759c7f5543b6c84ea5,', 'title     = "{Knowledge Representation for Health Care (AIME 2015 International Joint Workshop, KR4HC/ProHealth 2015)",', 'author    = "D Riano and R. Lenz and S Miksch and M Peleg and M. Reichert and {ten Teije}, A.C.M.",', 'year      = "2015",', 'doi       = "10.1007/978-3-319-26585-8",', 'isbn      = "9783319265841",', 'series    = "LNAI",', 'publisher = "Springer",', 'number    = "9485",', '}', '']
            >>> my_buffer.is_each_row_balanced(exclude_special_rows_of_syntax='bibtex')  # error
            False
            >>> # the same entry with unbalanced curly bracket removed
            >>> my_buffer.dataset = ['@book{a82caf00e1a143759c7f5543b6c84ea5,', 'title     = "Knowledge Representation for Health Care (AIME 2015 International Joint Workshop, KR4HC/ProHealth 2015)",', 'author    = "D Riano and R. Lenz and S Miksch and M Peleg and M. Reichert and {ten Teije}, A.C.M.",', 'year      = "2015",', 'doi       = "10.1007/978-3-319-26585-8",', 'isbn      = "9783319265841",', 'series    = "LNAI",', 'publisher = "Springer",', 'number    = "9485",', '}', '']
            >>> my_buffer.is_each_row_balanced(exclude_special_rows_of_syntax='bibtex')
            True

        """

        from preprocessor.string_tools import String

        buffer = self.dataset

        is_balanced_log = []

        for each_row in buffer:
            each_row = String(str(each_row))

            if not each_row.is_balanced():
                    # print('row is not balanced: ', each_row)
                    ### EXCLUSIONS FOR BIBTEX ###########################################
                    if exclude_special_rows_of_syntax == 'bibtex':
                            # print('special syntax = bibtex recognized')
                            # forgive these row types
                            if each_row.is_line_type('bibtex', 'start of entry') \
                                    or each_row.is_line_type('bibtex', 'end of entry') \
                                    or each_row.is_line_type('bibtex', 'comment'):
                                is_balanced_log.append(True)
                                # print("01: appended True to log, because the row is unbalanced but it passed exclusion rules", "the current row (each_row) is: ", "(", type(each_row) ,")",  each_row)
                            else:
                                is_balanced_log.append(False)

                    ######################################################################
                    else:
                        is_balanced_log.append(False)
                        # print("02: appended False to log because row is unbalanced (no exclusion keyword specified) ", "the current row (each_row) is: ", "(", type(each_row) ,")",  each_row)

            else:
                is_balanced_log.append(True)
                # print("03: appended True to log because row is balanced ", "the current row (each_row) is: ", "(", type(each_row) ,")",  each_row)

        if False in is_balanced_log:
            return False
        else:
            return True


    def is_parsable(self, syntax_to_parse_by='bibtex'):
        """

        Args:
            syntax_to_parse_by:

        Returns:
            boolean

        Examples:
            # bibtex entry with no issues
            >>> my_buffer = ListBuffer()
            >>> my_buffer.dataset = ['@article{5f3ed8a5037f4837be0c7e8e5a1f0948,',
            ...    'title   = "New Horizons biedt eindelijk goede blik op Pluto",',
            ...    'author  = "B. Andeweg",',
            ...    'year    = "2015",',
            ...    'month   = "7",',
            ...    'journal = "Volkskrant",',
            ...    '}']
            >>> my_buffer.is_parsable()
            True

            # unmatched " in author field
            >>> my_buffer = ListBuffer()
            >>> my_buffer.dataset = ['@article{5f3ed8a5037f4837be0c7e8e5a1f0948,',
            ...    'title   = "New Horizons biedt eindelijk goede blik op Pluto",',
            ...    'author  = "B. "Andeweg",',
            ...    'year    = "2015",',
            ...    'month   = "7",',
            ...    'journal = "Volkskrant",',
            ...    '}']
            >>> my_buffer.is_parsable()
            False
        """
        if syntax_to_parse_by == 'bibtex':
            # import and shorten bibtex parser function
            # import and shorten bibtex parser function
            from pybtex.database.input import bibtex
            parser = bibtex.Parser()

            # TODO: test can be made in memory instead of via temporary file (could use 'parser.parse_bytes')
            with open('temp_buffer_dump.bib', 'w', encoding='utf8') as temp_buffer_dump_file:
                for each_buffer_row in self.dataset:
                    print(each_buffer_row, file=temp_buffer_dump_file)

            with open('temp_buffer_dump.bib', encoding='utf8') as temp_buffer_dump_file:
                try:
                    parsed_file = parser.parse_file(temp_buffer_dump_file)
                    return True
                except:
                    return False


