class String(str):

    """
    >>> isinstance(String('a'), str)
    True

    >>> isinstance(String('a'), String)
    True
    """

    def __init__(self, content): # TODO: Replace __init__ with __new__. This is currently not done completely.
        self.content = content
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

    def purify(self, leave_newline_characters=False):
        """
        Replaces non-ascii characters with their ascii equivalents (e.g., 'â' with 'a') and removes patterns/characters
        that can lead to parsing errors.

        Returns:
            String

        Examples:
            >>> my_string = String('bad string ââ “ ” ’< > \ {"} () {} []')
            >>> my_string.purify()
            'bad string aa'
        """
        pattern_replacements_dictionary = {
            '<': '',
            '>': '',
            '\{"\}': '',  # to replace {"} with '
            '\\\\': '',   # to remove '\' in expressions such as '\sqrt{s}' and rogue '\'s.  unsure why '\\' does not work
            "'": '',
            '"': '',
            '“': '',
            '”': '',
            '’': '',
            '\\\\': '',
            '\[|\]|\{|\}|\(|\)': ''
        }

        self.clean_from_non_ascii_characters()
        self.replace_patterns(pattern_replacements_dictionary)
        if not leave_newline_characters:
            self.clean_from_newline_characters()

        return self


    def replace_patterns(self, pattern_conversions_dictionary):
        """
        Replaces given patterns with their replacements provided in the parameter pattern_conversions_dictionary.

        Args:
            pattern_conversions_dictionary(dict): A dictionary in the format of {target:replacement}. Targets and
                replacements can be longer than single characters, and can contain regex expressions.

        Returns:
            A modified String object (self)

        Examples:
            >>> # replace single pattern
            >>> my_problematic_string = String('an {"}example{"} string')
            >>> my_problematic_string.replace_patterns({'\{"\}':"'"})
            "an 'example' string"

            >>> # empty input
            >>> my_problematic_string = String('an example string')
            >>> my_problematic_string.replace_patterns({'':''})
            'an example string'

            >>> # replace single pattern
            >>> my_problematic_string = String('a2n 6ex6ample4 stri1ng125')
            >>> my_problematic_string.replace_patterns({'[0-9]':"_"})
            'a_n _ex_ample_ stri_ng___'

            # replace multiple patterns
            >>> my_complex_problematic_string = String('<--an {"}example{"} *string*-->')
            >>> my_complex_problematic_string.replace_patterns({
            ...    '\{"\}': "'",
            ...    '\>': '',
            ...    '\<': '',
            ...    '\*': '',
            ...    '-': ''
            ...    })
            "an 'example' string"

            >>> # erroneous target parameter
            >>> my_problematic_string_2 = String('an example *string*')
            >>> try:
            ...     my_problematic_string_2.replace_patterns({'*': ''})
            ... except ValueError as error_message:
            ...     print(error_message)
            pattern_conversions_dictionary keys likely contain an unescaped character that is wrongly interpreted as a regex expression. (e.g., '*' instead of '\*').Please check your pattern_conversions_dictionary

            >>> # a different error
            >>> my_problematic_string_2 = String('an example *string*')
            >>> try:
            ...     my_problematic_string_2.replace_patterns({1: ''})
            ... except Exception as error_message:
            ...     print(error_message)
            first argument must be string or compiled pattern
        """
        import re
        Parameter_Value(pattern_conversions_dictionary).force_type(dict)

        # pass target:replacement couples to re.sub
        for each_target_pattern in pattern_conversions_dictionary.keys():
            each_replacement_pattern = pattern_conversions_dictionary[each_target_pattern]
            try:
                self.content = re.sub(each_target_pattern, each_replacement_pattern, self.content)

        ### ERROR HANDLING ###
        # handle incorrect input dictionary
            except Exception as exception_message:
                if str(exception_message) == 'nothing to repeat at position 0':
                    raise ValueError("pattern_conversions_dictionary keys likely contain an unescaped character that "
                                     "is wrongly interpreted as a regex expression. (e.g., '*' instead of '\*')."
                                     "Please check your pattern_conversions_dictionary")
                else:
                    raise Exception(exception_message)
        #######################

        return self


    def clean_from_non_ascii_characters(self):
        """
        Converts non-ascii characters to their ascii equivalents (e.g., 'ϕ' becomes 'phs').

        Returns:
            String

        Examples:
            >>> my_string = String("In pursuit of lepton flavour violation: A search for the τ-> μγγ decay with atlas at √s=8 TeV,")
            >>> my_string.clean_from_non_ascii_characters()
            'In pursuit of lepton flavour violation: A search for the t-> mgg decay with atlas at [?]s=8 TeV,'

            >>> my_string = String("Measurement of the CP-violating phase ϕsand the Bs0meson decay width difference with Bs0→ J/ψϕ decays in ATLAS,")
            >>> my_string.clean_from_non_ascii_characters()
            'Measurement of the CP-violating phase phsand the Bs0meson decay width difference with Bs0- J/psph decays in ATLAS,'
        """
        from unidecode import unidecode
        self.content = String(unidecode(self.content))

        return self


    def clean_from_non_uri_safe_characters(self):
        """
        Converts non-ascii characters to their URI-safe equivalents (e.g., ' ' becomes '%20').

        Returns:
            String

        Examples:
            >>> my_string = String('non-uri safe_string')
            >>> my_string.clean_from_non_uri_safe_characters()
            'non-uri%20safe_string'
        """

        from urllib.parse import quote
        self.content = quote(self.content)

        return self


    def is_balanced(self):
        """
        Checks whether String has balanced parantheses, brackets, etc.

        Returns:
            Boolean. True if balanced, False if unbalanced.

        Examples:

            >>> String("<{[my string]}>").is_balanced()
            True

            >>> # missing '>'
            >>> String("<{[my string]}").is_balanced()
            False

            >>> # '>' at wrong place
            >>> String("<{[my string]>}").is_balanced()
            False

            >>> # missing '{'
            >>> String("<[my string]}>").is_balanced()
            False

            >>> # missing ']'
            >>> String("<{[my string}>").is_balanced()
            False

            >>> line = 'title     = "{Knowledge Representation for Health Care (AIME 2015 International Joint Workshop, KR4HC/ProHealth 2015)",'
            >>> String(line).is_balanced()
            False

            >>> entry_lines = [
            ...     '@book{a82caf00e1a143759c7f5543b6c84ea5,',
            ...     'title     = "{Knowledge Representation for Health Care (AIME 2015 International Joint Workshop, KR4HC/ProHealth 2015)",',
            ...     'author    = "D Riano and R. Lenz and S Miksch and M Peleg and M. Reichert and {ten Teije}, A.C.M.",',
            ...     'year      = "2015",',
            ...     'doi       = "10.1007/978-3-319-26585-8",',
            ...     'isbn      = "9783319265841",',
            ...     'series    = "LNAI",',
            ...     'publisher = "Springer",',
            ...     'number    = "9485",',
            ...     '}'
            ... ]
            >>> String(str(entry_lines)).is_balanced()
            False

            >>> entry_lines = [
            ...     '@book{a82caf00e1a143759c7f5543b6c84ea5,',
            ...     'title     = "{Knowledge Representation for Health Care (AIME 2015 International Joint Workshop, KR4HC/ProHealth 2015)}",',
            ...     'author    = "D Riano and R. Lenz and S Miksch and M Peleg and M. Reichert and {ten Teije}, A.C.M.",',
            ...     'year      = "2015",',
            ...     'doi       = "10.1007/978-3-319-26585-8",',
            ...     'isbn      = "9783319265841",',
            ...     'series    = "LNAI",',
            ...     'publisher = "Springer",',
            ...     'number    = "9485",',
            ...     '}'
            ... ]
            >>> String(str(entry_lines)).is_balanced()
            True

            >>> String(str(['@book{a82caf00e1a143759c7f5543b6c84ea5,', 'title     = "{Knowledge Representation for Health Care (AIME 2015 International Joint Workshop, KR4HC/ProHealth 2015)",', 'author    = "D Riano and R. Lenz and S Miksch and M Peleg and M. Reichert and {ten Teije}, A.C.M.",', 'year      = "2015",', 'doi       = "10.1007/978-3-319-26585-8",', 'isbn      = "9783319265841",', 'series    = "LNAI",', 'publisher = "Springer",', 'number    = "9485",', '}', ''])).is_balanced()
            False
        """
        test_items = iter('(){}[]<>')
        # create a dictionary from iter('(){}[]<>') such as: {'(': ')', '{': '}', '[': ']', '<': '>'}
        test_dictionary = dict(zip(test_items, test_items))
        closing_characters = test_dictionary.values()

        comparison_stack = []

        for each_character in self.content:
            # if the current character is an opening character, add it to comparison_stack
            each_character_that_has_a_closing_counterpart_in_test_dictionary = test_dictionary.get(each_character, None)
            if each_character_that_has_a_closing_counterpart_in_test_dictionary:
                comparison_stack.append(each_character_that_has_a_closing_counterpart_in_test_dictionary)

            # if the current character is a closing character,
            # and it has no counterpart (i.e., opening character) in comparison_stack, return false
            elif each_character in closing_characters:
                if not comparison_stack or each_character != comparison_stack.pop():
                    return False
        # if comparison_stack was never added an item (i.e., test characters are not found in string), return true
        return not comparison_stack


    def clean_from_newline_characters(self):
        """
        Cleans the String from newline characters using str.strip() method.

        Returns:
            - Modifies self.content
            - Returns the modified self

        Examples:

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
            >>> my_csv_file = CSV_File('test_data//yasgui_output_100.csv', column_delimiter_pattern_in_input_file=',')
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


    def clean_head_and_tail_from_patterns(self, patterns_to_remove, location='both', clean_newline_characters=False):
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

            >>> my_string = String('my string--mmm')
            >>> my_string.clean_head_and_tail_from_patterns('', location='tail', clean_newline_characters=True)
            'my string--mmm'
        """
        Parameter_Value(location).force_keyword_parameters(['head', 'tail', 'both'])
        patterns_to_remove = Parameter_Value(patterns_to_remove).convert_to_single_item_list_if_not_list()
        if patterns_to_remove == ['']:
            return self


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

            if clean_newline_characters:
                self.clean_from_newline_characters()

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
        # >>> my_csv.print_lines(1)
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


    def append(self, string_to_append):
        """
        Args:
            string_to_append(str)

        Returns:
            self

        Examples:
            >>> my_String = String('String')
            >>> my_String.append(' object.')
            'String object.'
        """
        self.content = self.content + string_to_append
        return self


    def prepend(self, string_to_prepend):
        """
        Args
            string_to_prepend(str)

        Returns:
            self

        Examples:
            >>> my_String = String('String object.')
            >>> my_String.prepend('This is a ')
            'This is a String object.'
        """
        self.content = string_to_prepend + self.content
        return self


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


    def is_line_type(self, syntax, query):
        """
        Checks the type of the current String against the query parameter and returns either True or False

        Args:
            syntax(str): the syntax that string being queried is written in
            query(str): the query to check the string against

        Keyword Args:
            - bibtex(syntax):

            - comment:
            - start of entry:
            - end of entry:

        Returns:
            boolean

        Examples:
            >>> # start of entry
            >>> String('@article{79948f66cc82409a8978d14c9131346a,').is_line_type('bibtex', 'start of entry')
            True
            >>> String('@article{79948f66cc82409a8978d14c9131346a,').is_line_type('bibtex', 'end of entry')
            False
            >>> String('@article{79948f66cc82409a8978d14c9131346a,').is_line_type('bibtex', 'comment')
            False

            >>> # end of entry
            >>> my_end_of_entry = String('}')
            >>> my_end_of_entry.is_line_type('bibtex', 'end of entry')
            True
            >>> my_end_of_entry.is_line_type('bibtex', 'start of entry')
            False
            >>> my_end_of_entry.is_line_type('bibtex', 'comment')
            False

            >>> # comment
            >>> my_comment = String('% This is a comment line.')
            >>> my_comment.is_line_type('bibtex', 'comment')
            True
            >>> my_comment.is_line_type('bibtex', 'start of entry')
            False
            >>> my_comment.is_line_type('bibtex', 'end of entry')
            False

            >>> # regular line
            >>> my_regular_string = String('  author    = "M. Acciarri and O. Adriani and M. Aguilar-Benitez and S.P. Ahlen and J. Alcaraz and G. Alemanni and J. Allaby and A. Aloisio and F.L. Linde",')
            >>> my_regular_string.is_line_type ('bibtex', 'start of entry')
            False
            >>> my_regular_string.is_line_type ('bibtex', 'end of entry')
            False
            >>> my_regular_string.is_line_type ('bibtex', 'comment')
            False

            >>> # regular line with '@' symbol
            >>> my_regular_string_with_at_symbol = String('  abstract  = "We report here the Einstein@Home discovery of PSR J1913+1102, a 27.3 ms pulsar found in data from the ongoing Arecibo PALFA pulsar survey. The pulsar is in a 4.95 hr double neutron star (DNS) system with an eccentricity of 0.089. From radio timing with the Arecibo 305 m telescope, we measure the rate of advance of periastron to be \dot{ω }=5.632(18)° yr-1. Assuming general relativity accurately models the orbital motion, this corresponds to a total system mass of M tot = 2.875(14) {M}⊙ , similar to the mass of the most massive DNS known to date, B1913+16, but with a much smaller eccentricity. The small eccentricity indicates that the second-formed neutron star (NS) (the companion of PSR J1913+1102) was born in a supernova with a very small associated kick and mass loss. In that case, this companion is likely, by analogy with other systems, to be a light (˜1.2 {M}⊙ ) NS; the system would then be highly asymmetric. A search for radio pulsations from the companion yielded no plausible detections, so we cannot yet confirm this mass asymmetry. By the end of 2016, timing observations should permit the detection of two additional post-Keplerian parameters: the Einstein delay (γ), which will enable precise mass measurements and a verification of the possible mass asymmetry of the system, and the orbital decay due to the emission of gravitational waves ({\dot{P}}b), which will allow another test of the radiative properties of gravity. The latter effect will cause the system to coalesce in ˜0.5 Gyr.",')
            >>> my_regular_string_with_at_symbol.is_line_type('bibtex', 'start of entry')
            False
        """
        string = self.content

        if syntax == 'bibtex':
            comment_pattern = '%'
            pattern_that_signals_beginning_of_entry = '@'
            pattern_that_signals_end_of_entry = '}'

            try:
                if string[0] == comment_pattern and query == 'comment':
                    return True

                elif string[0] == pattern_that_signals_beginning_of_entry and query == 'start of entry':
                    return True

                elif string == pattern_that_signals_end_of_entry and query == 'end of entry':
                    return True
                else:
                    return False
            except IndexError:
                return False


    def capitalize_first_letter(self):
        """
        Returns:
            modified String object (self)

        Examples:
            >>> String('my string').capitalize_first_letter()
            'My string'

        """
        string = self.content

        string = string[0].upper() + string[1:]

        self.content = string
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
    >>> # object call
    >>> my_parameter = Parameter_Value('parameter value')
    >>> my_parameter
    'parameter value'

    >>> # string call
    >>> str(my_parameter)
    'parameter value'

    >>> # modify content
    >>> my_parameter.content = 'modified parameter value'
    >>> my_parameter
    'modified parameter value'
    """

    def __init__(self, content=''):
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
            >>> # single requirement (str)
            >>> my_parameter = Parameter_Value('parameter value')
            >>> my_parameter.force_type(str)

            >>> # multiple requirement
            >>> my_parameter.force_type([str, int])

            >>> # requirement mismatch (does not match to the single requirement)
            >>> try:
            ...     my_parameter.force_type(int)
            ... except Exception as exception_message:
            ...      print('Exception caught:', exception_message)
            Exception caught: Parameter "parameter value" must be of type <class 'int'>, but is currently of type <class 'str'>

            >>> # requirement mismatch (none of the multiple)
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


    def force_positive_integer(self):
        """
        Examples:
            >>> # valid case
            >>> my_parameter = Parameter_Value(1)

            >>> # invalid case (not a positive integer)
            >>> my_parameter = Parameter_Value(0)
            >>> try:
            ...     my_parameter.force_positive_integer()  # parameter cannot be a non-positive integer
            ... except Exception as error_message:
            ...     print('Exception: ' + str(error_message))
            Exception: Parameter value must be a positive integer but is "0" of <class 'int'>.

            >>> # invalid case (not an integer)
            >>> my_parameter = Parameter_Value('a')
            >>> try:
            ...     my_parameter.force_positive_integer() #  cannot be a string
            ... except Exception as error_message:
            ...     print('Exception: ' + str(error_message))
            Exception: Parameter "a" must be of type <class 'int'>, but is currently of type <class 'str'>
        """
        self.force_type(int)
        entered_parameter_value = self.content
        if entered_parameter_value < 1:
            raise ValueError('Parameter value must be a positive integer but is "%s" of %s.'
                             % (str(self), str(type(entered_parameter_value))))


    def convert_to_single_item_list_if_not_list(self):
        """
        Converts a parameter to a list (if it is not already a list). If the parameters is already a list, it is
        returned as it is.

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


    @staticmethod
    def require_parameters(parameters_list, parameter_names):
        """"
        Args:
            parameters_list(list): List of parameters to check
            parameter_names(list): Names of parameters to be printed to the error message

        Examples:
            >>> # All required parameters specified:
            >>> parameter_1 = 'a value'
            >>> parameter_2 = 'another value'
            >>> Parameter_Value().require_parameters(parameters_list = [parameter_1, parameter_2],
            ...                                         parameter_names = ['parameter_1', 'parameter_2'])

            >>> # Missing required parameter
            >>> parameter_1 = 'a value'
            >>> parameter_2 = ''
            >>> try:
            ...     Parameter_Value().require_parameters(parameters_list = [parameter_1, parameter_2],
            ...                                             parameter_names = ['parameter_1', 'parameter_2'])
            ... except Exception as error_message:
            ...     print("Exception caught: " + str(error_message))
            Exception caught: Parameters '['parameter_1', 'parameter_2']' must be specified before this method is called. The current values of the parameters are ['a value', '']

            >>> # Comparison of various null values
            >>> parameter_specified = 'a value'

            >>> parameter_empty_string = ''
            >>> try:
            ...     Parameter_Value().require_parameters([parameter_specified, parameter_empty_string],
            ...                                             ['parameter specified', 'parameter_empty_string'])
            ... except Exception as error_message:
            ...     print('Exception caught: ' + str(error_message))
            Exception caught: Parameters '['parameter specified', 'parameter_empty_string']' must be specified before this method is called. The current values of the parameters are ['a value', '']

            >>> parameter_empty_tuple = ()
            >>> try:
            ...     Parameter_Value().require_parameters([parameter_specified, parameter_empty_tuple],
            ...                                             ['parameter specified', 'parameter_empty_tuple'])
            ... except Exception as error_message:
            ...     print('Exception caught: ' + str(error_message))
            Exception caught: Parameters '['parameter specified', 'parameter_empty_tuple']' must be specified before this method is called. The current values of the parameters are ['a value', ()]

            >>> parameter_empty_list = []
            >>> try:
            ...     Parameter_Value().require_parameters([parameter_specified, parameter_empty_list],
            ...                                             ['parameter specified', 'parameter_empty_list'])
            ... except Exception as error_message:
            ...     print('Exception caught: ' + str(error_message))
            Exception caught: Parameters '['parameter specified', 'parameter_empty_list']' must be specified before this method is called. The current values of the parameters are ['a value', []]

            >>> parameter_empty_dictionary = {}
            >>> try:
            ...     Parameter_Value().require_parameters([parameter_specified, parameter_empty_dictionary],
            ...                                             ['parameter specified', 'parameter_empty_dictionary'])
            ... except Exception as error_message:
            ...     print('Exception caught: ' + str(error_message))
            Exception caught: Parameters '['parameter specified', 'parameter_empty_dictionary']' must be specified before this method is called. The current values of the parameters are ['a value', {}]

            >>> parameter_none = None
            >>> try:
            ...     Parameter_Value().require_parameters([parameter_specified, parameter_none],
            ...                                             ['parameter_specified', 'parameter_none'])
            ... except Exception as error_message:
            ...     print('Exception caught: ' + str(error_message))
            Exception caught: Parameters '['parameter_specified', 'parameter_none']' must be specified before this method is called. The current values of the parameters are ['a value', None]

            >>> parameter_zero = 0
            >>> Parameter_Value().require_parameters([parameter_specified, parameter_zero],
            ...                                         ['parameter_specified', 'parameter_zero'])

            >>> parameter_false = False
            >>> Parameter_Value().require_parameters([parameter_specified, parameter_false],
            ...                                         ['parameter_specified', 'parameter_false'])
        """
        no_of_parameters_specified = 0

        for each_item in parameters_list:
            if each_item is not None and each_item != '' and each_item != [] and each_item != {} and each_item != ():
                no_of_parameters_specified += 1

        if no_of_parameters_specified < len(parameters_list):
            raise ValueError("Parameters '%s' must be specified before this method is called. The current values of the parameters are %s" % (parameter_names, parameters_list))


    @staticmethod
    def cannot_be_specified_at_the_same_time(parameters_list):
        """
        Examples:
            >>> # Comparison of two non-empty parameter values
            >>> parameter_1 = 'a value'
            >>> parameter_2 = 'another value'
            >>> try:
            ...     Parameter_Value().cannot_be_specified_at_the_same_time([parameter_1, parameter_2])
            ... except Exception as error_message:
            ...     print("Exception: " + str(error_message))
            Exception: Too many parameters. These parameter values cannot be specified at the same time: ['a value', 'another value']

            >>> # Comparison of various null values
            >>> parameter_specified = 'a value'

            >>> parameter_empty_string = ''
            >>> Parameter_Value().cannot_be_specified_at_the_same_time([parameter_specified, parameter_empty_string])

            >>> parameter_empty_tuple = ()
            >>> Parameter_Value().cannot_be_specified_at_the_same_time([parameter_specified, parameter_empty_tuple])

            >>> parameter_empty_list = []
            >>> Parameter_Value().cannot_be_specified_at_the_same_time([parameter_specified, parameter_empty_list])

            >>> parameter_empty_dictionary = {}
            >>> Parameter_Value().cannot_be_specified_at_the_same_time([parameter_specified, parameter_empty_dictionary])

            >>> parameter_none = None
            >>> Parameter_Value().cannot_be_specified_at_the_same_time([parameter_specified, parameter_none])

            >>> parameter_zero = 0
            >>> try:
            ...     Parameter_Value().cannot_be_specified_at_the_same_time([parameter_specified, parameter_zero])
            ... except Exception as error_message:
            ...     print('Exception: ' + str(error_message))
            Exception: Too many parameters. These parameter values cannot be specified at the same time: ['a value', 0]

            >>> parameter_false = False
            >>> try:
            ...     Parameter_Value().cannot_be_specified_at_the_same_time([parameter_specified, parameter_false])
            ... except Exception as error_message:
            ...     print('Exception: ' + str(error_message))
            Exception: Too many parameters. These parameter values cannot be specified at the same time: ['a value', False]
        """
        no_of_parameters_specified = 0

        for each_item in parameters_list:
            if each_item is not None and each_item != '' and each_item != [] and each_item != {} and each_item != ():
                no_of_parameters_specified += 1

        if no_of_parameters_specified > 1:
            raise ValueError("Too many parameters. These parameter values cannot be specified at the same time: %s" % parameters_list)



