class String(str):

    def __init__(self, input_string):

        str.__init__(self)

        self.content = input_string
        self.split_to_list = []

    def __repr__(self):
        """
        >>> my_String = String('content')
        >>> my_String
        'content'
        """
        return repr(self.content)

    def __str__(self):
        """
        >>> my_String = String('a string')
        >>> print(my_String)
        a string
        """
        return str(self.content)

    def surround_with(self, pattern_1, pattern_2=None):
        """
        Surrounds a String object with given character(s) (i.e., pattern[s]).

        Returns:
            A String object

        Examples:
            >>> my_string = String('1st string')
            >>> my_string.surround_with('"').content
            '"1st string"'
            >>> my_string = String('2nd string')
            >>> my_string.surround_with('[', ']').content
            '[2nd string]'
        """
        input_string = self.content

        if pattern_2 is None:
            pattern_2 = pattern_1

        surrounded_string = pattern_1 + input_string + pattern_2

        self.content = surrounded_string
        return self

    def unsurround(self, character_1=None, character_2=None):
        """
        Removes surrounding characters from a String object either indiscriminately, or by checking
        if the right characters are being removed.

        Args:
            character_1(str): Takes a single character. If a character is specified, acts as a check to ensure the right
                characters are removed. This check could be useful for loops where not all strings may have the same
                structure (or that may contain strings that have typos, irregularities, etc.)
            character_2(str): --

        Returns:
            Rewrites self.content_sting and returns Modified object (return self).

        Examples:
            >>> my_string = String('[a string]')
            >>> my_string.unsurround().content
            'a string'

            >>> # unsurround without checking which characters being unsurrounded
            >>> my_string = String('[a string]')
            >>> my_string.unsurround().content
            'a string'

            >>> # unsurround with checking whether characters being unsurrounded are indeed the intended ones
            >>> my_string = String(' a string ')
            >>> my_string.unsurround(' ').content
            'a string'
            >>> my_string = String('[a string]')
            >>> my_string.unsurround('[', ']').content
            'a string'

            >>> # Error handling during pattern checks
            >>> my_string = String('a string')
            >>> # Uncomment following lines to test the error detection. They should give errors due to input string not
            >>> # having the specified surround pattern(s) around it'.
            >>> #my_string.unsurround('"').content
            >>> #my_string.unsurround('(', ")").content
        """
        # TODO: Could remove multi-character patterns instead of single characters (need to modify both match_input_characters_with_head_and_tail_or_raise_error and clip_head_and_tail functions)

        input_string = self.content

        head_character = ''
        tail_character = ''

        # if neither character_1 nor character_2 is provided
        if not character_1 and not character_2:
            head_character = input_string[0]
            tail_character = input_string[-1]

        # if only character_1 is provided
        elif character_1 and not character_2:
            head_character = character_1
            tail_character = character_1

        # if both character_1 and character_2 is provided
        elif character_1 and character_2:
            head_character = character_1
            tail_character = character_2

        # check if inputted characters exist in the String
        head_character_matched = self.check_character_at_index(head_character, 0)
        tail_character_matched = self.check_character_at_index(tail_character, -1)
        if not head_character_matched or not tail_character_matched:
            raise ValueError('The patterns surrounding the input "%s" does not match specified unsurround '
                             'pattern "%s".' % (input_string, character_1))

        self.remove_first_and_last_character()
        return self

    def remove_first_and_last_character(self):
        """
        Removes the first and last characters from String.

        >>> String('Xmy stringX').remove_first_and_last_character().content
        'my string'
        """
        self.content = self.content[1:-1]
        return self

    def check_character_at_index(self, character, index):
        """
        Checks whether inputted characters match to those at the head and of the string

        >>> String('my string').check_character_at_index('y',1)
        True
        >>> String('my string').check_character_at_index('y',0)
        False
        """
        if character == self[index]:
            return True
        else:
            return False

    def get_pattern_positions(self, target_pattern):
        """
        ##############################
        Obselete. Use split() instead.
        ##############################

        Searches for target_pattern in the String object and returns index positions where it starts and ends for each
        occurrence.

        Args:
            target_pattern: Pattern to search. Can consist of multiple characters.

        Returns:
            A list of tuples that contain integers

        Examples:
            >>> my_string = String('aaXaaXaa')
            >>> my_string.get_pattern_positions('X')
            [(2, 3), (5, 6)]
            >>> my_string.get_pattern_positions('aa')
            [(0, 2), (3, 5), (6, 8)]
        """
        import re

        indexes_list = []

        for each_position in re.finditer(target_pattern, self):
            indexes_list.append((each_position.start(), each_position.end()))

        return indexes_list


    def slice_with_pattern_and_CONVERT_to_list(self, target_pattern):
        """
        Slices the string into list elements and returns a list. Empty values are converted as ''.

        WARNING: After this method is used, the self.content is not overwritten, and remains in its string form
            before the method split it. What is returned is not 'self' nor String type either: the original input is
            converted from String to list, and this should be kept in mind when fluent interfacing.

        Args:
            target_pattern: Pattern to be used as dividing point in string. A pattern can consist of multiple
                characters.

        Returns:
            A list
            Does not change the original String object, and does NOT return self.

        Examples:
            >>> my_string = String('aaXaaXaa')
            >>> my_string.slice_with_pattern_and_CONVERT_to_list('X')
            ['aa', 'aa', 'aa']

            >>> my_string = String('aaXaaXaa')
            >>> my_string.slice_with_pattern_and_CONVERT_to_list('aa')
            ['', 'X', 'X', '']

            >>> my_string = String('value , value')
            >>> my_string.slice_with_pattern_and_CONVERT_to_list(' , ')
            ['value', 'value']

            >>> my_string = String('value, value, , , ')
            >>> my_string.clean_head_and_tail_from_patterns(', ', 'tail')
            'value, value, , '
            >>> my_string.slice_with_pattern_and_CONVERT_to_list(', ')
            ['value', 'value', '', '']

            >>> my_string = String('value , value ,  , ')
            >>> my_string.clean_head_and_tail_from_patterns(' , ', location='tail')
            'value , value , '
            >>> my_string.slice_with_pattern_and_CONVERT_to_list(' , ')
            ['value', 'value', '']

            >>> my_string = String('value , value , ')
            >>> my_string.slice_with_pattern_and_CONVERT_to_list(' , ')
            ['value', 'value', '']

            >>> my_string = String('value;value;;value;value;;value;;')
            >>> my_string.slice_with_pattern_and_CONVERT_to_list(';')
            ['value', 'value', '', 'value', 'value', '', 'value', '', '']
        """
        from preprocessor.csv_tools import CSV_Row

        input_string = self.content
        if target_pattern not in input_string:
            raise ValueError('Inputted target_pattern "%s" not found in string "%s".' % (target_pattern, input_string))

        list = input_string.split(target_pattern)

        return list

    # def remove_pattern_from_head_or_tail(self, pattern, location='both'):
    #     """
    #     >>> self.remove_pattern_from_head_or_tail('x', 'head')
    #     >>> self.remove_pattern_from_head_or_tail('x', 'tail')
    #     >>> self.remove_pattern_from_head_or_tail('x', 'ends')
    #     """
    #     string = self.content
    #     first_pattern_occurrence = string.find(pattern)
    #     last_pattern_occurrence  = string.content.rfind(pattern)
    #     "".
    #     if location == 'both':
    #         string.


    def clean_head_and_tail_from_patterns(self, patterns_to_remove, location='both'):
        """
        Cleans head and tail of a String object from the specified patterns. This operation is simple, but it may not
        be efficient when used for parsing large datasets.

        Args:
            patterns_to_remove(list): A list that lists the patterns to be cleaned from the begining and end of the
                input string. For instance, if '||' and '--' should be cleaned, the parameter should take the value: ['||', '--']

        Keyword Args:
            head (patterns_to_remove): Cleans the beginning of the string from specified patterns
            tail (patterns_to_remove): Cleans the end of the string from specified patterns
            ends (patterns_to_remove): Cleans both the beginning and end of the string from specified patterns

        Returns:
            Writes the new string to content, and returns the modified object (return self).

        Examples:
            >>> my_string = String('------    ---- --my string------')
            >>> my_string.clean_head_and_tail_from_patterns(['------'], location='tail')
            '------    ---- --my string'
            >>> my_string.clean_head_and_tail_from_patterns('------    ---- --', location='head')
            'my string'

            >>> my_string = String('my string--mmm')
            >>> my_string.clean_head_and_tail_from_patterns('--mmm', location='tail')
            'my string'
        """
        Parameter_Value(location).force_keyword_parameters(['head', 'tail', 'both'])
        patterns_to_remove = Parameter_Value(patterns_to_remove).convert_to_single_item_list_if_not_list()

        for each_pattern in patterns_to_remove:
            pattern_found_at_head = self.is_pattern_there(each_pattern, location='head')
            pattern_found_at_tail = self.is_pattern_there(each_pattern, location='tail')

            if location == 'head' and pattern_found_at_head:
                self.clip_at_index(divide_at=len(each_pattern), remove='head')
            elif location == 'tail' and pattern_found_at_tail:
                self.clip_at_index(divide_at=-len(each_pattern), remove='tail')
            elif location == 'both' and pattern_found_at_head and pattern_found_at_tail:
                self.clip_at_index(divide_at=len(each_pattern), remove='head')
                self.clip_at_index(divide_at=-len(each_pattern), remove='tail')

        return self


    def clean_head_and_tail_iteratively_from_characters(self, characters_to_remove, location='ends'):
        """
        Cleans head and tail of a String object from the specified characters.This operation is simple, but it may not
        be efficient when this method is used for parsing large datasets.

        Args:
            characters_to_remove(str): A string that lists the characters to be cleaned from the begining and end of the
                input string. For instance, if ',' and ';' should be cleaned, the parameter should take the value ',;'

        Keyword Args:
            head (characters_to_remove): Cleans the beginning of the string
            tail (characters_to_remove): Cleans the end of the string
            ends (characters_to_remove): Cleans both the beginning and end of the string

        Returns:
            Writes the new string to content, and returns the modified object (return self).

        >>> my_string = String('{{[[((my string))]]}}')
        >>> my_string.clean_head_and_tail_iteratively_from_characters('{}[]()', location='head')
        'my string))]]}}'
        >>> my_string.clean_head_and_tail_iteratively_from_characters('{}[]()', location='tail')
        'my string'

        >>> my_string = String('------    ---- --my string------')
        >>> my_string.clean_head_and_tail_iteratively_from_characters('- ')
        'my string'

        >>> # an empy line as input
        >>> my_string = String('')
        >>> my_string.clean_head_and_tail_iteratively_from_characters('- ')
        ''

        >>> # a one-character line as input
        >>> my_string = String('a')
        >>> my_string.clean_head_and_tail_iteratively_from_characters('- ')
        'a'

        # >>> # a line with newline characters in the end
        # >>> from preprocessor.csv_tools import CSV_File, CSV_Line
        # >>> my_csv = CSV_File('test_data//yasgui_output_100.csv', ' , ', ' | ')
        # >>> my_csv.print_line(1)
        # >>> with open(my_csv.input_file_path,encoding='utf8') as input_file:
        # ...     for each_line in input_file:
        # ...         each_line = CSV_Line(each_line)
        # ...         each_line = each_line.clean_head_and_tail('')
        # ...
        # ...         each_line = each_line.parse()
        # ...         each_line = each_line.append('test')
        # ...         print(each_line)
        """


        string = self.content

        # if the string is too short (or empty), just return itself and make no processing
        if len(string) < 1:
            return self

        slice_positions = []
        target_index = []

        # set internal variables
        # values should be in list format becase they will be iterated
        if location == 'ends':  # both 'head' and 'tail'
            target_index = [0, -1]  # first and last character
            slice_positions = [slice(1, None), slice(None, -1)]  # equivalent of [1:] and [:-1]
        elif location == 'head':
            target_index = [0]  # first character
            slice_positions = [slice(1, None)]  # equivalent of [1:]
        elif location == 'tail':
            target_index = [-1]  # last character
            slice_positions = [slice(None, -1)]  # equivalent of [:-1]
        else:
            raise ValueError('Invalid keyword argument for "location" parameter: "%s"' % location)

        for each_target_index, each_slice_position_couple in zip(target_index, slice_positions):
            while string[each_target_index] in characters_to_remove:
                string = string[each_slice_position_couple]

        self.content = string
        return self

    def clean_from_newline_characters(self):
        """
        # # THIS TEST SHOULD BE RAN MANUALLY BY UNCOMMENTING, AS THE PRESENCE OF '\n' CHARACTER IN THE OUTPUT LEADS TO AN ERROR
        # # When ran manually, newline characters can be seen at the end of each line in the output
        # >>> from preprocessor.csv_tools import CSV_File, CSV_Line
        # >>> my_csv_file = CSV_File('test_data//yasgui_output_100.csv', column_delimiter_pattern=',', cell_delimiter_pattern=' | ')
        # >>> with open(my_csv_file.input_file_path, encoding='utf8') as input_file:
        # ...     for i, each_line in enumerate(input_file):
        # ...         if i < 2:
        # ...             line = CSV_Line(each_line).clean_head_and_tail_from_patterns(' ', location='head')
        # ...             row = line.parse_line_and_CONVERT_to_CSV_Row(' , ').clean_cell_heads_and_tails_from_characters('"')
        # ...             print(row)

        >>> from preprocessor.csv_tools import CSV_File, CSV_Line
        >>> my_csv_file = CSV_File('test_data//yasgui_output_100.csv', column_delimiter_pattern=',', cell_delimiter_pattern=' | ')
        >>> with open(my_csv_file.input_file_path, encoding='utf8') as input_file:
        ...     for i, each_line in enumerate(input_file):
        ...         if i < 2:
        ...             # the clean_from_newline_characters method in the end of statement clears the string from newline characters
        ...             line = CSV_Line(each_line).clean_head_and_tail_from_patterns(' ', location='head').clean_from_newline_characters()
        ...
        ...             row = line.parse_line_and_CONVERT_to_CSV_Row(' , ').clean_cell_heads_and_tails_from_characters('"')
        ...             print(row)
        ['publication_type', 'journal_article', 'title', 'publication_year', 'author_name', 'journal_name', 'journal_issue_number', 'journal_volume_number', 'startEndPages', 'publisher_name', 'doi" ,']
        ['Journal Article', 'https://w3id.org/oc/corpus/br/45174', 'An inventory for measuring clinical anxiety: Psychometric properties.', '1988', 'Steer - Robert A.', 'Journal of Consulting and Clinical Psychology', '6', '56', '893--897', 'American Psychological Association (APA)', '10.1037//0022-006x.56.6.893" ,']

        """
        self.content = self.content.strip()
        return self


    def is_pattern_there(self, pattern, location):
        """
        >>> String('XXaXXa12a12').is_pattern_there('XX', location='head')
        True
        """
        import re

        pattern_found_at_head = re.search('^' + pattern, self.content)
        pattern_found_at_tail = re.search(pattern + '$', self.content)

        if location == 'head' and pattern_found_at_head:
            return True
        elif location == 'tail' and pattern_found_at_tail:
            return True
        elif location == 'both' and pattern_found_at_head and pattern_found_at_tail:
            return True
        else:
            return False


    def clip_at_index(self, divide_at, remove):
        """
        >>> String('aaaXXX').clip_at_index(3, 'tail')
        'aaa'

        >>> String('aaaXXX').clip_at_index(3, 'head')
        'XXX'
        """
        slice_value = slice(None, None)

        if remove == 'tail':
            slice_value = slice(None, divide_at)
        elif remove == 'head':
            slice_value = slice(divide_at, None)

        self.content = self.content[slice_value]

        return self

class File_Path(String, str):
    def __init__(self, path_string):
        """
        >>> my_file_path = File_Path('my_directory//my_file.extension')
        >>> my_file_path.content
        'my_directory//my_file.extension'

        >>> my_file_path.directory_path
        'my_directory'
        >>> my_file_path.file_name
        'my_file'
        >>> my_file_path.file_extension
        'extension'
        """

        str.__init__(self)
        String.__init__(self, path_string)

        self.content = path_string
        self.raise_error_if_single_slash()

        self.directory_path = self.get_directory_path()
        self.file_name      = self.get_file_name(include_file_extension=False)
        self.file_extension = self.get_file_extension(include_dot=False)

    def __repr__(self):
        """
        >>> print(File_Path('my_directory//my_file.file'))
        my_directory//my_file.file
        """
        return repr(self.content)

    def __str__(self):
        """
        >>> print(File_Path('my_directory//my_file.file'))
        my_directory//my_file.file
        """
        return str(self.content)

    def get_directory_path(self):
        """
        Extracts directory tree portion from entered string. This is a string operation and does not check if the
        inputted files or directories exist.

        If the input string contains only a filename and no folder tree (e.g.,
        'my_file.txt', the current working directory is returned.

        If there is a directory tree in the string (e.g.,
        'my_folder//my_sub_folder//my_file.txt'), the path until the last directory is returned (e.g.,
        'my_folder//my_sub_folder').

        Args:
            content(str): A string that specifies a file name or path + file name.

        Returns:
            A string

        Examples:
            >>> my_file_path = File_Path('example.txt')
            >>> my_file_path.get_directory_path()
            ''
            >>> my_file_path = File_Path('my_directory//my_file.txt')
            >>> my_file_path.get_directory_path()
            'my_directory'

            >>> my_file_path = File_Path('my_directory//my_sub_directory//my_file.txt')
            >>> my_file_path.get_directory_path()
            'my_directory//my_sub_directory'

        """
        directory_separator_pattern = '//'
        inferred_directory = ''

        # if there is only a file name (and no directory tree leading to it)
        if directory_separator_pattern not in self.content:
            # return empty string
            inferred_directory = ''
        # if there is a directory tree
        else:
            last_slash_index = 0
            # find the last occurrence of the directory separator character/pattern
            last_slash_index = self.content.rfind(directory_separator_pattern)
            # separate the string from there
            inferred_directory = self.content[:last_slash_index]

        return inferred_directory


    def get_file_name(self, include_file_extension=True):
        """
        Extracts file name portion (without the file extension) from entered string. This is a string operation and does not check if the
        inputted files or directories exist.

        If the string contains only a filename and no folder tree (e.g.,
        'my_file.txt', the string is returned without change.

        If there is a directory tree in the string (e.g.,
        'my_folder//my_sub_folder//my_file.txt'), the name after the last directory is returned (e.g.,
        'my_file.txt').

        Args:
            content(str): A string that specifies a file name or path + file name.
            include_file_extension = If False, returns the file name without the extension at the end.

        Returns:
            A string

        Examples:
            >>> my_file_path = File_Path('example.txt')
            >>> my_file_path.get_file_name()
            'example.txt'
            >>> my_file_path = File_Path('my_directory//my_sub_directory//my_file.txt')
            >>> my_file_path.get_file_name()
            'my_file.txt'
            >>> my_file_path.get_file_name(include_file_extension=False)
            'my_file'
        """
        directory_separator_pattern = '//'
        inferred_file_name = ''

        # if there is only a file name (and no directory tree leading to it)
        if directory_separator_pattern not in self.content:
            inferred_file_name = self.content
        # if there is a directory tree
        else:
            last_slash_index = 0
            # find the last occurrence of the directory separator character/pattern
            last_slash_index = self.content.rfind(directory_separator_pattern)
            # separate the string from there
            inferred_file_name = self.content[last_slash_index + 2:]

        file_extension_index = inferred_file_name.rfind('.')
        inferred_file_name_without_extension = inferred_file_name[:file_extension_index]

        if include_file_extension == True:
            return inferred_file_name
        else:
            return inferred_file_name_without_extension


    def get_file_extension(self, include_dot=True):
        # TODO: Should be made fluent by adding return self
        """
        Extracts extension portion (with a dot in the beginning) from entered string. Is a string operation and does not check if the
        inputted files or directories exist.

        Args:
            content(str): A string that specifies a file name or path + file name.

        Returns:
            A string

        Examples:
            # Get extension from file name
            >>> my_file_path = File_Path('test.csv')
            >>> my_file_path.get_file_extension()
            '.csv'

            # Get extension from file path
            >>> my_file_path = File_Path('my_directory//my_sub_directory//my_file.txt')
            >>> my_file_path.get_file_extension()
            '.txt'
            >>> my_file_path = File_Path('my_directory//my_sub_directory//my_file.txt')
            >>> my_file_path.get_file_extension(include_dot=False)
            'txt'

        """
        inferred_extension = ''
        dot_index = 0

        dot_index = self.content.rfind('.')

        if include_dot == True:
            inferred_extension = self.content[dot_index:]
        else:
            inferred_extension = self.content[dot_index + 1:]

        return inferred_extension


    def append_substring(self, string_to_append):
        # TODO: Should be made fluent by adding return self
        """
        Appends string_to_append to the end of a file name or path, before the extension.

        Examples:
            >>> my_path = File_Path('test.txt')
            >>> my_path.append_substring('_MODIFIED').content
            'test_MODIFIED.txt'
            >>> my_path = File_Path('my_directory//my_subdirectory//test.txt')
            >>> my_path.append_substring('_v1.2').content
            'my_directory//my_subdirectory//test_v1.2.txt'

        """
        input_directory      = self.get_directory_path()
        input_file_name      = self.get_file_name(include_file_extension=False)
        input_file_extension = self.get_file_extension()

        ## transform 'input_file.txt' to 'input_file_APPENDED.txt'
        # if input is a directory
        if '/' in self.content:
            modified_path = input_directory + '//' + input_file_name + string_to_append + input_file_extension
        # if input is a file name without a directory tree
        else:
            modified_path = input_directory + input_file_name + string_to_append + input_file_extension

        self.content = modified_path
        return self

    def raise_error_if_single_slash(self):
        """
        >>> try:
        ...     File_Path('directory/file.extension').raise_error_if_single_slash()
        ... except Exception as error_message:
        ...     print(error_message)
        Invalid path: Path contains "/" as directory separator, and should be replaced with "//".

        >>> File_Path('directory//file.extension').raise_error_if_single_slash()
        'directory//file.extension'
        """
        path = self.content

        if '/' in path and '//' not in path:
            raise ValueError('Invalid path: Path contains "/" as directory separator, and should be replaced with "//".')
        else:
            return self

class Parameter_Value():
    """
    # object call
    >>> my_parameter = Parameter_Value('parameter value')
    >>> my_parameter
    'parameter value'

    # string call
    >>> str(my_parameter)
    'parameter value'

    # modify content
    >>> my_parameter.content = 'modified parameter value'
    >>> my_parameter
    'modified parameter value'
    """

    def __init__(self, content):
        self.content = content
        self.inferred_type = type(content)

    def __repr__(self):
        return repr(self.content)

    def __str__(self):
        return str(self.content)

    def force_type(self, desired_types):
        """
        Checks if Parameter is of desired type, and returns exception if not.

        Args:
            desired_types(class): The class to be enforced.

        Returns:
            Nothing if parameter types are a match, otherwise, exception.

        Examples:
        >>> # single requirement
        >>> my_parameter = Parameter_Value('parameter value')
        >>> my_parameter.force_type(str)

        >>> # multiple requirement
        >>> my_parameter.force_type([str, int])

        >>> # requirement mismatch
        >>> try:
        ...     my_parameter.force_type([int, bool])
        ... except Exception as exception_message:
        ...      print('Exception caught:', exception_message)
        Exception caught: Parameter "parameter value" must be of type <class 'int'>, <class 'bool'>, but is currently of type <class 'str'>
        """
        desired_types = Parameter_Value(desired_types).convert_to_single_item_list_if_not_list()

        type_is_desired = False

        for each_class in desired_types:
            if self.inferred_type == each_class:
                type_is_desired = True

        if not type_is_desired:
            raise TypeError('Parameter "%s" must be of type %s, but is currently of type %s' % (self, str(desired_types)[1:-1], self.inferred_type))

    def force_keyword_parameters(self, possible_parameter_values):
        """
        Checks if Parameter is in the list of acceptable values, and returns exception if not.

        Examples:
            >>> my_parameter = Parameter_Value('both')
            >>> my_parameter.force_keyword_parameters(['head', 'tail', 'both'])

            >>> my_parameter = Parameter_Value('neither')
            >>> try:
            ...     my_parameter.force_keyword_parameters(['head', 'tail', 'both'])
            ... except Exception as error_message:
            ...     print(error_message)
            Invalid keyword argument "neither" for parameter. This parameter can only take values  "'head', 'tail', 'both'".
        """
        entered_parameter = self.content
        # transform e.g., ['a', 'b' ,'c'] to 'a', 'b', 'c' for printing it to error message output
        string_version_of_possible_parameter_values_list = str(possible_parameter_values)[1:-1]

        if entered_parameter not in possible_parameter_values:
            raise ValueError('Invalid keyword argument "%s" for parameter. This parameter can only take values  "%s".'
                             % (self, string_version_of_possible_parameter_values_list))

    def convert_to_single_item_list_if_not_list(self):
        """
        Returns:
            List (and NOT a Parameter class object)

        Examples:
            >>> my_parameter = Parameter_Value('a parameter value')
            >>> my_parameter.convert_to_single_item_list_if_not_list()
            ['a parameter value']

            >>> my_parameter = Parameter_Value(['a','b','c'])
            >>> my_parameter.convert_to_single_item_list_if_not_list()
            ['a', 'b', 'c']
        """
        if type(self.content) != list:
            self.content = [self.content]

        return self.content