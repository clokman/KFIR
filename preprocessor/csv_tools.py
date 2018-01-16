from preprocessor.string_tools import String
from preprocessor.ListData import ListData

class CSV_File():
    def __init__(self, input_file_path, column_delimiter_pattern_in_input_file, desired_cell_value_delimiter_pattern):
        """
        Holds location and properties of a .csv file, but does not parse it upon instantiation. This non-parsing
        initialization algorithm allows to keep memory usage low. Unless the file is not parsed afterwards by a class
        method, it will be processed as the loops iterate the lines of the file (e.g., .merge_rows_by_identifier method
        uses this strategy instead of reading and parsing the entire .csv file into memory.

        Args:
            input_file_path (str): path to .csv file to be processed
            column_delimiter_pattern (str): The delimiter character used in the input .csv file (e.g., ',')
            cell_delimiter_pattern (str): The delimiter character used in the input file (e.g., 'author_1 | author_2')

        Examples:
            >>> my_obj = CSV_File('my_dir//my_subdir//my_file.txt', column_delimiter_pattern_in_input_file=',', desired_cell_value_delimiter_pattern=' | ')
            >>> my_obj.input_file_path
            'my_dir//my_subdir//my_file.txt'
            >>> my_obj.row_merged_output_file_path_object
            'my_dir//my_subdir//my_file_rows_merged.txt'

        """
        from preprocessor.string_tools import File_Path
        self.file_path_object = File_Path(input_file_path)

        self.input_file_path  = self.file_path_object.content
        self.directory_path   = self.file_path_object.directory_path
        self.file_name        = self.file_path_object.file_name
        self.file_extension   = self.file_path_object.file_extension

        # path to write the new .csv file
        self.row_merged_output_file_path_object  = File_Path(self.input_file_path).append_substring('_rows_merged')
        self.row_merged_output_file_path = self.row_merged_output_file_path_object.content

        self.column_delimiter_pattern = column_delimiter_pattern_in_input_file
        self.cell_delimiter_pattern = desired_cell_value_delimiter_pattern

    def live_clean_and_merge(self, id_column_index,
                             clean_line_heads_from_pattern='',
                             clean_line_tails_from_pattern='',
                             clean_cell_heads_and_tails_from_characters=''):
        """
        Reads and parses a file line by line, cleans lines and cells from specified patterns, and merges rows by id on-the go
        without having to parse all of the file or read it into memory.

        Examples:
            >>> # a csv from yasgui.org
            >>> my_obj = CSV_File('test_data//yasgui_output_100.csv',
            ...                    column_delimiter_pattern_in_input_file=' , ',
            ...                    desired_cell_value_delimiter_pattern=' | ')
            >>> my_obj.live_clean_and_merge(id_column_index=1,
            ...                                           clean_line_tails_from_pattern=' ,',
            ...                                           clean_cell_heads_and_tails_from_characters='"')
            A row merged version of the data is written to 'test_data//yasgui_output_100_rows_merged.csv'.
            >>> my_output_file = CSV_File('test_data//yasgui_output_100_rows_merged.csv',
            ...                           column_delimiter_pattern_in_input_file=',',
            ...                           desired_cell_value_delimiter_pattern=' | ')
            >>> my_output_file.print_line(2)
            "Journal Article" , "https://w3id.org/oc/corpus/br/46047" , "Transformational, transactional, and laissez-faire leadership styles: A meta-analysis comparing women and men." , "2003" , "Johannesen-Schmidt - Mary C. | van Engen - Marloes L." , "Psychological Bulletin" , "4" , "129" , "569--591" , "American Psychological Association (APA)" , "10.1037/0033-2909.129.4.569"
            <BLANKLINE>

            >>> # a csv file exported from blazegraph
            >>> my_obj = CSV_File('test_data//blazegraph_output_1000.csv',
            ...                   column_delimiter_pattern_in_input_file=',',
            ...                   desired_cell_value_delimiter_pattern=' | ')
            >>> my_obj.live_clean_and_merge(id_column_index=1,
            ...                                           clean_line_tails_from_pattern=' ,',
            ...                                           clean_cell_heads_and_tails_from_characters='"')
            A row merged version of the data is written to 'test_data//blazegraph_output_1000_rows_merged.csv'.
            >>> my_output_file = CSV_File('test_data//yasgui_output_100_rows_merged.csv',
            ...                            column_delimiter_pattern_in_input_file=',',
            ...                            desired_cell_value_delimiter_pattern=' | ')
            >>> my_output_file.print_line(2)
            "Journal Article" , "https://w3id.org/oc/corpus/br/46047" , "Transformational, transactional, and laissez-faire leadership styles: A meta-analysis comparing women and men." , "2003" , "Johannesen-Schmidt - Mary C. | van Engen - Marloes L." , "Psychological Bulletin" , "4" , "129" , "569--591" , "American Psychological Association (APA)" , "10.1037/0033-2909.129.4.569"
            <BLANKLINE>
        """
        line_head_pattern_to_remove = clean_line_heads_from_pattern
        line_tail_pattern_to_remove = clean_line_tails_from_pattern
        cell_head_and_tail_characters_to_remove = clean_cell_heads_and_tails_from_characters


        with open(self.input_file_path, encoding='utf8') as input_file:
            with open(self.row_merged_output_file_path, 'w', encoding='utf8') as output_file:

                buffer = Row_Merge_Buffer(id_column_index)

                for each_line in input_file:
                    # skip empty lines (e.g., the first line of some csv files)
                    if each_line != '\n':
                        # TODO: Add the hardcoded parameters below as parameters of the method
                        line = CSV_Line(each_line).\
                            clean_head_and_tail_from_patterns([line_tail_pattern_to_remove], location='tail').\
                            clean_head_and_tail_from_patterns([line_head_pattern_to_remove], location='head').\
                            clean_from_newline_characters()

                        row = line.\
                            parse_line_and_CONVERT_to_CSV_Row(self.column_delimiter_pattern).\
                            clean_cell_heads_and_tails_from_characters(cell_head_and_tail_characters_to_remove)

                        # if buffer is empty (i.e., initialized for the first time or reset)
                        if buffer.id_of_current_rows_in_buffer == None:
                            buffer.append_as_first_row_and_reset_buffer(row)

                        else:
                            # if row id is the same
                            if buffer.is_id_of_rows_in_buffer_same_with_outside_row(row):
                                buffer.append_row(row)

                            # if a new row id is reached
                            else:
                                merged_row = buffer.merge_all_rows_to_one(self.cell_delimiter_pattern)
                                merged_line = CSV_Line(merged_row.dataset)
                                # CSV format compatibility changes (yasgui template)
                                #merged_line = merged_line.replace("'", '"')

                                print(merged_line, file=output_file)
                                #output_file.writelines(merged_row)
                                #self.update_registry(row_id, row_line_in_file)
                                buffer.clear_all()

        print("A row merged version of the data is written to '%s'."
              % self.row_merged_output_file_path)


    def print_line(self, line_index_number):
        """
        Prints a specified line in the CSV file without reading the whole file into memory.

        Args:
            line_index_number(int): An value that can take integers starting from 0.

        Returns:
            Output to console.

        Examples:
            >>> my_csv = CSV_File('test_data//blazegraph_output_50.csv', ',', ' | ')
            >>> my_csv.print_line(2)
            Journal Article,<https://w3id.org/oc/corpus/br/44074>,Improving the Blood Pressure Control With the ProActive Attitude of Hypertensive Patients Seeking Follow-up Services,2016,Fu - Hang,Medicine,14,95,e3233--e3233,Ovid Technologies (Wolters Kluwer Health),10.1097/md.0000000000003233
            <BLANKLINE>
        """
        with open(self.input_file_path, encoding='utf8') as input_file:
            for i, each_line in enumerate(input_file):
                if i == line_index_number:
                    print(each_line)
                elif i > line_index_number:
                    break


class CSV_Line (String, str):
    def __init__(self, input_string_or_list):
        """
        Converts a string, String, or list object into CSV_Line.

        Strings and strings are converted as they are, and require no arguments.

        Lists in CSV_Line are represented as string not as ['a', 'b', 'c'], but as e.g., "a" , "b" , "c", but
        are not actually changed. This is intended for CSV-like printing and presentation, but not for modification
        of list object's data. In other words, __str__() is overriden, and not __repr__(), even though no data in the list is unchanged. The change is only in __str__ method, and not
        in __repr)). String representation of lists can be further modified to look like a CSV line, sch as 'a' ; 'b' ; 'c'
        by changing the internal function parameters.

        Returns:
            CSV_Line object

        Examples:
            # a CSV_Line's string representation of a string input
            # strings are converted literally
            >>> my_line = CSV_Line('a,b,c')
            >>> print(my_line)
            a,b,c

            # a CSV_Line's string representation for a list, to be used when printing to a file
            >>> my_line = CSV_Line(['a', 'b', 'c'])
            >>> print(my_line)
            "a" , "b" , "c"
            >>> type(my_line)
            <class 'csv_tools.CSV_Line'>

            # a list's string representation
            >>> print(['a', 'b', 'c'])
            ['a', 'b', 'c']

            # a CSV_Row's string representation
            >>> print(CSV_Row(['a', 'b', 'c']))
            ['a', 'b', 'c']

            # this is as close as it gets with normal lists to a csv-like representation (unless additional substring
            # is to be performed)
            >>> print(str(CSV_Row(['a', 'b', 'c']))[1:-1])
            'a', 'b', 'c'

            >>> # repr does not change; it shows content
            >>> CSV_Line(['a', 'b', 'c'])
            ['a', 'b', 'c']

            >>> # repr does not change
            >>> CSV_Line(['a', 'b', 'c']).content
            ['a', 'b', 'c']



        """
        String.__init__(self, input_string_or_list)
        str.__init__(self)

        self.list_item_separator_pattern  = ' , '
        self.list_item_wrapper_pattern = '"'
        self.input_string_or_list =  input_string_or_list

    def __str__(self):
        if type(self.input_string_or_list) == list or type(self.input_string_or_list) == CSV_Row:
            input_list = self.input_string_or_list
            separator = self.list_item_separator_pattern
            wrapper = self.list_item_wrapper_pattern
            string_representation = ''
            for each_element in input_list:
                string_representation = string_representation + wrapper + each_element + wrapper + separator

            # prevent the separators at the end (e.g., comma at the end in "a,b,c,")
            string_representation = string_representation.strip(self.list_item_separator_pattern)

            return string_representation
        else:
            return self


    def parse_line_and_CONVERT_to_CSV_Row(self, column_delimiter_pattern):
        """
        Parses a line using column_delimiter_pattern. If clean_cell_head_and_tails_from is specified, a
        cleaning operation is performed after parsing. This operation is simple, but it may not be efficient when this
        method is used for parsing large datasets.

        Args:
            column_delimiter_pattern(str): Delimiter used to separate columns in the inputted string.
            clean_cell_heads_and_tails_from_characters(str): A string that lists the characters to be cleaned from the
                begining and end of cells. For instance, if ',' and ';' should be cleaned, the parameter should take the
                value ',;'
        Returns:
            CSV_Line object

        Examples:
            >>> my_line = CSV_Line('a,b,c')
            >>> my_line.parse_line_and_CONVERT_to_CSV_Row(',')
            ['a', 'b', 'c']

            >>> my_line = CSV_Line('a,b,c,')
            >>> my_line.clean_head_and_tail_from_patterns(',',location='tail').parse_line_and_CONVERT_to_CSV_Row(',')
            ['a', 'b', 'c']

            >>> my_line = CSV_Line('a, b, c')
            >>> my_line.parse_line_and_CONVERT_to_CSV_Row(', ')
            ['a', 'b', 'c']

            >>> my_line = CSV_Line('a, b, c, ')
            >>> my_line.clean_head_and_tail_from_patterns(', ',location='tail').parse_line_and_CONVERT_to_CSV_Row(', ')
            ['a', 'b', 'c']

            >>> my_line = CSV_Line('a, b, c, , ')
            >>> my_line.clean_head_and_tail_from_patterns(', ',location='tail').parse_line_and_CONVERT_to_CSV_Row(', ')
            ['a', 'b', 'c', '']

            # blazegraph csv line example
            >>> my_line = CSV_Line('Journal Article,<https://w3id.org/oc/corpus/br/802>,Improving health information systems for decision making across five sub-Saharan African countries: Implementation strategies from the African Health Initiative,2013,Mutale - Wilbroad,BMC Health Services Research - BMC Health Serv Res,Suppl 2,13,S9--S9,Springer Science + Business Media,10.1186/1472-6963-13-s2-s9,<https://w3id.org/oc/corpus/id/1032>,<https://w3id.org/oc/corpus/id/1030>')
            >>> my_line.parse_line_and_CONVERT_to_CSV_Row(',')
            ['Journal Article', '<https://w3id.org/oc/corpus/br/802>', 'Improving health information systems for decision making across five sub-Saharan African countries: Implementation strategies from the African Health Initiative', '2013', 'Mutale - Wilbroad', 'BMC Health Services Research - BMC Health Serv Res', 'Suppl 2', '13', 'S9--S9', 'Springer Science + Business Media', '10.1186/1472-6963-13-s2-s9', '<https://w3id.org/oc/corpus/id/1032>', '<https://w3id.org/oc/corpus/id/1030>']

            # yasgui csv line example
            >>> my_line = CSV_Line(' "Journal Article" , "https://w3id.org/oc/corpus/br/1446" , "To IRB or Not to IRB?" , "2004" , "Gunderson - Anne J." , "Academic Medicine" , "7" , "79" , "628--632" , "Ovid Technologies (Wolters Kluwer Health)" , "10.1097/00001888-200407000-00004" ,')

            # in this formatting, artefacts appear around cells after parsing
            >>> my_line.parse_line_and_CONVERT_to_CSV_Row(' , ')
            [' "Journal Article"', '"https://w3id.org/oc/corpus/br/1446"', '"To IRB or Not to IRB?"', '"2004"', '"Gunderson - Anne J."', '"Academic Medicine"', '"7"', '"79"', '"628--632"', '"Ovid Technologies (Wolters Kluwer Health)"', '"10.1097/00001888-200407000-00004" ,']

            # these artefacts can be cleaned
            >>> my_row = my_line.parse_line_and_CONVERT_to_CSV_Row(' , ')
            >>> my_row.clean_cell_heads_and_tails_from_characters(', "')
            ['Journal Article', 'https://w3id.org/oc/corpus/br/1446', 'To IRB or Not to IRB?', '2004', 'Gunderson - Anne J.', 'Academic Medicine', '7', '79', '628--632', 'Ovid Technologies (Wolters Kluwer Health)', '10.1097/00001888-200407000-00004']
        """
        line = self
        list = line.slice_with_pattern_and_CONVERT_to_list(column_delimiter_pattern)

        row = CSV_Row(list)
        return row


class CSV_Cell(String, str):
    """
    >>> my_cell = CSV_Cell('my cell content')
    >>> my_cell
    'my cell content'

    >>> print(my_cell)
    my cell content

    >>> my_cell.content = 'modified content'

    >>> my_cell
    'modified content'

    >>> print(my_cell)
    modified content
    """

    def __init__(self, input_string):

        String.__init__(self, input_string)
        str.__init__(self)

        self.content = input_string

    def __repr__(self):
        return repr(self.content)

    def __str__(self):
        return str(self.content)


class CSV_Row(list):
    """
    Takes a list as input and converts it to a CSV_Row object

    Examples:
        >>> # object call
        >>> my_row = CSV_Row(['1','2','3'])
        >>> my_row
        ['1', '2', '3']

        >>> # string call
        >>> str(my_row)
        "['1', '2', '3']"

        >>> # modify content
        >>> my_row.content = ['a', 'b', 'c']
        >>> my_row
        ['a', 'b', 'c']

        >>> # indexing
        >>> my_row[0]
        'a'

        >>> # iteration
        >>> for each_item in my_row:
        ...     print(each_item)
        a
        b
        c


    """
    def __init__(self, input_list):
        super().__init__()
        self.content = input_list
        self.convert_cell_strings_to_CSV_Cells()

    # overrides
    def __repr__(self):
        return repr(self.content)
    def __str__(self):
        return str(self.content)
    def __getitem__(self, index):
        return self.content[index]
    def __setitem__(self, index, value):
        self.content[index] = value
    def __iter__(self):
        return iter(self.content)


    def convert_cell_strings_to_CSV_Cells(self):
        """
        >>> my_row = CSV_Row(['1','2','3','4','5'])
        >>> print(my_row)
        ['1', '2', '3', '4', '5']

        >>> try:
        ...     CSV_Row('abc').convert_cell_strings_to_CSV_Cells()
        ... except Exception as exception_message:
        ...     print('Exception caught: ', exception_message)
        Exception caught:  Parameter "abc" must be of type <class 'list'>, but is currently of type <class 'str'>
        """
        from preprocessor.string_tools import Parameter_Value
        Parameter_Value(self.content).force_type([CSV_Row, list])

        row = self.content

        for i, each_element in enumerate(row):
                each_element = CSV_Cell(each_element)
                row[i] = each_element

        self.content = row
        return self


    def clean_cell_heads_and_tails_from_characters(self, characters_to_be_cleaned):
        """
        >>> my_row = CSV_Row(['..a','b.','......c'])
        >>> my_row.clean_cell_heads_and_tails_from_characters('.')
        ['a', 'b', 'c']
        """
        row_cells = self.content

        for i, each_cell in enumerate(row_cells):
            # and clean them from characters_to_be_cleaned
            each_cell.clean_head_and_tail_iteratively_from_characters(characters_to_be_cleaned)
            row_cells[i] = each_cell
        self.content = row_cells
        return self


class Row_Merge_Buffer(ListData):
    """
    A container that contains lists (or CSV_CSV_Row objects) and their associated ids.

    Args:
        id_column_index(int): Index position of id column of rows to be added to the buffer.
        content(list or CSV_Row): A list of lists or a list of CSV_Rows

    Examples:
        # empty init
        >>> my_buffer = Row_Merge_Buffer(0)
        >>> my_buffer
        'None: []'

        # append as first row and reset buffer
        >>> my_buffer.append_as_first_row_and_reset_buffer(['id52','a','b','c'])
        "id52: [['id52', 'a', 'b', 'c']]"

        # append a second row
        >>> my_buffer.append_row(['id52','A','B','C'])
        "id52: [['id52', 'a', 'b', 'c'], ['id52', 'A', 'B', 'C']]"

        # string call
        >>> str(my_buffer)
        "id52: [['id52', 'a', 'b', 'c'], ['id52', 'A', 'B', 'C']]"

        # modify content
        >>> my_buffer.dataset = [['id12', 1, 2], ['id12', 3, 4]]
        >>> my_buffer.set_id_of_current_rows_in_buffer('idXX')
        "idXX: [['id12', 1, 2], ['id12', 3, 4]]"

        # CSV_Row as input
        >>> my_buffer.append_as_first_row_and_reset_buffer(CSV_Row(['id42', 1, 2, 3, 4]))
        "id42: [['id42', 1, 2, 3, 4]]"
    """

    def __init__(self, index_of_id_column_in_rows_to_be_added):
        from preprocessor.string_tools import Parameter_Value
        Parameter_Value(index_of_id_column_in_rows_to_be_added).force_type(int)

        #super().__init__()
        ListData.__init__(self)
        # ListData initiates empty. This line adds the content to 'dataset' variable
        self.dataset = []

        self.index_of_id_column = index_of_id_column_in_rows_to_be_added
        self.id_of_current_rows_in_buffer = None

    def __repr__(self):
        # self.dataset is imported from ListData with self.__init__()
        return repr(str(self.id_of_current_rows_in_buffer) + ': ' + str(self.dataset))
    def __str__(self):
        # self.dataset is imported from ListData with self.__init__()
        return str(self.id_of_current_rows_in_buffer) + ': ' + str(self.dataset)

    def append_as_first_row_and_reset_buffer(self, new_row):
        """
        Clears all the rows in the buffer, sets a new 'id_of_current_rows_in_buffer' variable from the id of the new
        row, and adds the new row to the buffer. Should be used when adding a row with a differing id.

        Args:
            new_row(list or CSV_Row): Row to be added to buffer as first row

        Returns:
            list or CSV_Row (self)

        Examples:
            >>> Row_Merge_Buffer(0).append_as_first_row_and_reset_buffer(['id123', 1,2,3])
            "id123: [['id123', 1, 2, 3]]"

        """
        new_id = new_row[self.index_of_id_column]

        self.clear_all()
        self.set_id_of_current_rows_in_buffer(new_id)
        self.append_row(new_row)

        return self


    def append_row(self, new_row):
        """
        Appends a row at the end of the buffer. This is an override of the append() method of ListData class. In this
        overridden version, append_row appends only if the id of the row being added and the id of the rows in the
        buffer are a match. The id column's index is read from 'self.index_of_id_column' variable.

        Args:
            new_row(list or CSV_Row): The row to be added

        Returns:
            - If id of rows in the buffer and the row being added are matching, list or CSV_Row (self).
            - If no match, ValueError
        """
        ids_are_same = self.is_id_of_rows_in_buffer_same_with_outside_row(new_row)

        if ids_are_same:
            ListData.append_row(self, new_row)
        else:
            raise ValueError ("ID ('%s') of row '%s' does not match the current id of rows in Row_Merge_Buffer ('%s')"
                              % (new_row[self.index_of_id_column], new_row, self.id_of_current_rows_in_buffer))
        return self


    def clear_all(self):
        """
        Clears all rows in buffer and resets the id variable of the buffer (id_of_current_rows_in_buffer).

        Returns:
            Row_Merge_Buffer object (self, for fluent interfacing)

        Examples:
            >>> my_buffer = Row_Merge_Buffer(0).append_as_first_row_and_reset_buffer(['id124', 'a','b','c'])
            >>> my_buffer
            "id124: [['id124', 'a', 'b', 'c']]"

            >>> my_buffer.clear_all()
            'None: []'

        """
        ListData.clear_all(self)
        self.id_of_current_rows_in_buffer = None
        return self


    def get_id_of_current_rows_in_buffer(self):
        """
        Retrieves the id of current rows in buffer by reading it from self.id_of_current_rows_in_buffer variable.

        Returns:
            str

        Examples:
            >>> my_buffer = Row_Merge_Buffer(index_of_id_column_in_rows_to_be_added=3)
            >>> my_buffer.append_as_first_row_and_reset_buffer(['a','b','c', 'ax21'])
            "ax21: [['a', 'b', 'c', 'ax21']]"
            >>> my_buffer.get_id_of_current_rows_in_buffer()
            'ax21'

        """
        return self.id_of_current_rows_in_buffer


    def set_id_of_current_rows_in_buffer(self, new_id):
        """
        Changes the self.id_of_current_rows_in_buffer variable.

        Returns:
            Row_Merge_Buffer object (self) for fluent interfacing.

        Examples:
            >>> my_buffer = Row_Merge_Buffer(3).append_as_first_row_and_reset_buffer(['a', 'b', 'c', 'ax21'])
            >>> my_buffer
            "ax21: [['a', 'b', 'c', 'ax21']]"

            >>> my_buffer.set_id_of_current_rows_in_buffer('x')
            "x: [['a', 'b', 'c', 'ax21']]"
        """
        self.id_of_current_rows_in_buffer = new_id
        return self

    def merge_all_rows_to_one(self, value_separator_pattern=' | '):
        """
        Overrides the ListData method of same name. This version returns a CSV_Row
        object that consists of CSV_Cell items, instead of a list that
        consists of strings.

        Args:
            value_separator_pattern(str): desired value to be used to separate
                cell values in merged cells

        Returns:
            - Modifies self.dataset
            - returns self: a Row_Merge_Buffer object that holds a CSV_Row object with
                CSV_Cell objects in it

            type structure in the returned object is as following:
            Row_Merge_Buffer(CSV_Row([CSV_Cell, CSV_Cell, CSV_Cell]))

        Examples:
            >>> my_buffer = Row_Merge_Buffer(0).append_as_first_row_and_reset_buffer(['id11','a','b'])
            >>> my_buffer.merge_all_rows_to_one(' | ')
            "id11: ['id11', 'a', 'b']"

            >>> print(type(my_buffer))
            <class 'csv_tools.Row_Merge_Buffer'>

            >>> my_buffer.dataset
            ['id11', 'a', 'b']
            >>> print(type(my_buffer.dataset))
            <class 'csv_tools.CSV_Row'>

            >>> for each_cell in my_buffer.dataset:
            ...     print(each_cell, type(each_cell))
            id11 <class 'csv_tools.CSV_Cell'>
            a <class 'csv_tools.CSV_Cell'>
            b <class 'csv_tools.CSV_Cell'>
        """
        merged_row = ListData.merge_all_rows_to_one(self, value_separator_pattern).dataset
        # print(type(merged_row), merged_row)

        for i, each_cell in enumerate(merged_row):
            if type(each_cell) != CSV_Cell:
                merged_row[i] = CSV_Cell(merged_row[i])

        merged_row = CSV_Row(merged_row)

        self.dataset = merged_row
        return self




    def is_id_of_rows_in_buffer_same_with_outside_row(self, outside_row):
        """
        Compares the self.id_of_current_rows_in_buffer with the value in the id cell of the inputted row. The index
        of id cell is assumed to be the same with the index of id cells in the buffer, and its value is gathered from
        self.id_index_of_id_column

        Args:
            outside_row(list or CSV_Row): Row that is being compared with the rows in buffer

        Returns:
            Boolean

        Examples:
            >>> my_buffer = Row_Merge_Buffer(0)
            >>> my_buffer.append_as_first_row_and_reset_buffer(CSV_Row(['id23', 'a','b']))
            "id23: [['id23', 'a', 'b']]"
            >>> my_buffer.id_of_current_rows_in_buffer
            'id23'

            # matching ids
            >>> my_buffer = Row_Merge_Buffer(0).append_as_first_row_and_reset_buffer(CSV_Row(['id23', 'a','b','c']))
            >>> my_row = CSV_Row(['id23', 'X', 'Y', 'Z'])
            >>> my_buffer.is_id_of_rows_in_buffer_same_with_outside_row(my_row)
            True

            # non-matching ids
            >>> my_buffer = Row_Merge_Buffer(0).append_as_first_row_and_reset_buffer(CSV_Row(['id23', 'a','b','c']))
            >>> my_row = CSV_Row(['1003', 'X', 'Y', 'Z'])
            >>> my_buffer.is_id_of_rows_in_buffer_same_with_outside_row(my_row)
            False

            # CSV_CSV_Row and list comparison
            >>> my_buffer = Row_Merge_Buffer(0).append_as_first_row_and_reset_buffer(CSV_Row(['id23', 'a','b','c']))
            >>> my_row = ['id23', 'X', 'Y', 'Z']
            >>> my_buffer.is_id_of_rows_in_buffer_same_with_outside_row(my_row)
            True

        """
        id_in_buffer  = self.id_of_current_rows_in_buffer
        id_of_new_row = outside_row[self.index_of_id_column]

        if id_in_buffer == id_of_new_row:
            return True
        else:
            return False


# class Table(ListData, list):
#     """
#     # object call
#     >>> my_table = Table([[1,2,3],[1,2,3]])
#     >>> my_table
#     [[1,2,3],[1,2,3]]
#
#     # string call
#     >>> str(my_table)
#     "[[1,2,3],[1,2,3]]"
#
#     # modify content
#     >>> my_table.content = [['a','b','c'],['A','B','C']]
#     >>> my_table
#     [['a','b','c'],['A','B','C']]
#
#     """
#
#     def __init__(self, content):
#         list.__init__(self)
#         ListData.__init__(self)
#         self.content = content
#
#     def __repr__(self):
#         return repr(self.content)
