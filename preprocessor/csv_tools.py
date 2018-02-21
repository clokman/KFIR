from preprocessor.string_tools import String
from preprocessor.ListData import ListData
from preprocessor.Text_File import Text_File

class CSV_File(Text_File):
    """
    Holds location and properties of a .csv file, but does not parse it upon instantiation. This non-parsing
    initialization algorithm allows to keep memory usage low. Unless the file is not parsed afterwards by a class
    method, it will be processed as the loops iterate the lines of the file (e.g., .merge_rows_by_identifier method
    uses this strategy instead of reading and parsing the entire .csv file into memory.

    Args:
        input_file_path (str): path to .csv file to be processed
        column_delimiter_pattern (str): The separator used in the input .csv file (e.g., ','). Can consist of multiple
            characters
        cell_delimiter_pattern (str): The delimiter character used in the input file (e.g., 'author_1 | author_2')

    Examples:
        >>> my_obj = CSV_File('my_dir//my_subdir//my_file.txt', column_delimiter_pattern_in_input_file=',')
        >>> my_obj.input_file_path
        'my_dir//my_subdir//my_file.txt'
        >>> my_obj.row_merged_output_file_path_object
        'my_dir//my_subdir//my_file_rows_merged.txt'
    """

    def __init__(self, input_file_path, column_delimiter_pattern_in_input_file):
        from preprocessor.string_tools import File_Path
        from preprocessor.dict_tools import Registry

        Text_File.__init__(self, input_file_path)

        self.index_position_of_id_column = ''

        self.registry = Registry()
        self.registry_is_built = False

        # path to write the new row-merged .csv file (uses File_Path values from superclass)
        self.row_merged_output_file_path_object  = File_Path(self.input_file_path).append_substring('_rows_merged')
        self.row_merged_output_file_path = self.row_merged_output_file_path_object.content

        # TODO: This is a quick adaptation for ttl cleaning. Consider implementing it more gracefully.
        # path to write the new uri cleaned (uri encoded) .ttl file
        self.uri_cleaned_output_file_path_object = File_Path(self.input_file_path).append_substring('_uri_cleaned')
        self.uri_cleaned_output_file_path_object.file_extension = 'ttl'
        self.uri_cleaned_output_file_path = self.uri_cleaned_output_file_path_object.content

        # parsing parameters (provided during init)
        self.input_column_separator_pattern = column_delimiter_pattern_in_input_file

        # cleaning parameter defaults (updated by CSV_File.set_cleaning_and_parsing_parameters())
        self.cleaning_parameters_are_set = False
        self.line_head_artefact = ''
        self.line_tail_artefact = ''
        self.cell_ends_artefact = ''

        # formatting parameters defaults for output (updated by CSV_File.set_output_formatting_parameters())
        self.formatting_parameters_are_set = False
        self.output_cell_value_separator = ''
        self.output_column_separator = column_delimiter_pattern_in_input_file  # same with input, otherwise could look like regular commas, if separator is a comma
        self.output_line_head = ''
        self.output_line_tail = ''
        self.output_cell_wrapper = ''


    def set_cleaning_and_parsing_parameters(self, line_head_pattern_to_remove='', line_tail_pattern_to_remove='',
                                            cell_head_and_tail_characters_to_remove=''):
        """
        Sets cleaning parameters to be used in various methods in CSV_File class. After setting the
        parameters, prints the results of a demo cleaning procedure performed with the parameters set.

        Returns:
            - None
            - Console output

        Examples:
            >>> # prep: a csv with artefacts (yasgui.org style)
            >>> my_csv_file = CSV_File('test_data//data_with_head_and_tail_artefacts.csv',
            ...                    column_delimiter_pattern_in_input_file=' , ')
            >>> my_csv_file.preview(number_of_lines=2, print_separators_between_lines=True)
            ----------------------------------LINE 1----------------------------------
            head artefact "*publication_type*" , "journal_article" , "title" , "publication_year" , "author_name" , "journal_name" , "journal_issue_number" , "journal_volume_number" , "startEndPages" , "publisher_name" , "doi" , tail artefact
            ----------------------------------LINE 2----------------------------------
            head artefact "*Journal Article*" , "https://w3id.org/oc/corpus/br/45174" , "An inventory for measuring clinical anxiety: Psychometric properties." , "1988" , "Steer - Robert A." , "Journal of Consulting and Clinical Psychology" , "6" , "56" , "893--897" , "American Psychological Association (APA)" , "10.1037//0022-006x.56.6.893" , tail artefact


            >>> # blank parameters
            >>> my_csv_file.set_cleaning_and_parsing_parameters(line_head_pattern_to_remove='',
            ...                                     line_tail_pattern_to_remove='',
            ...                                     cell_head_and_tail_characters_to_remove='')
            Cleaning parameters are set. Output resulting from a demo parsing operation is as following:
            ----------------------------------LINE 0----------------------------------
            <BLANKLINE>
            ----------------------------------LINE 1----------------------------------
            ['head artefact "*publication_type*"', '"journal_article"', '"title"', '"publication_year"', '"author_name"', '"journal_name"', '"journal_issue_number"', '"journal_volume_number"', '"startEndPages"', '"publisher_name"', '"doi"', 'tail artefact']
            ----------------------------------LINE 2----------------------------------
            ['head artefact "*Journal Article*"', '"https://w3id.org/oc/corpus/br/45174"', '"An inventory for measuring clinical anxiety: Psychometric properties."', '"1988"', '"Steer - Robert A."', '"Journal of Consulting and Clinical Psychology"', '"6"', '"56"', '"893--897"', '"American Psychological Association (APA)"', '"10.1037//0022-006x.56.6.893"', 'tail artefact']

            >>> # parameters provided
            >>> my_csv_file.set_cleaning_and_parsing_parameters(line_head_pattern_to_remove='head artefact ',
            ...                                     line_tail_pattern_to_remove=' , tail artefact',
            ...                                     cell_head_and_tail_characters_to_remove='"*')
            Cleaning parameters are set. Output resulting from a demo parsing operation is as following:
            ----------------------------------LINE 0----------------------------------
            <BLANKLINE>
            ----------------------------------LINE 1----------------------------------
            ['publication_type', 'journal_article', 'title', 'publication_year', 'author_name', 'journal_name', 'journal_issue_number', 'journal_volume_number', 'startEndPages', 'publisher_name', 'doi']
            ----------------------------------LINE 2----------------------------------
            ['Journal Article', 'https://w3id.org/oc/corpus/br/45174', 'An inventory for measuring clinical anxiety: Psychometric properties.', '1988', 'Steer - Robert A.', 'Journal of Consulting and Clinical Psychology', '6', '56', '893--897', 'American Psychological Association (APA)', '10.1037//0022-006x.56.6.893']


            >>> # prep: another_csv
            >>> my_csv_file = CSV_File('test_data//data_for_formatting_test.csv',
            ...                    column_delimiter_pattern_in_input_file=',')
            >>> my_csv_file.preview(number_of_lines=2, print_separators_between_lines=True)
            ----------------------------------LINE 1----------------------------------
            <BLANKLINE>
            ----------------------------------LINE 2----------------------------------
            Journal Article,<https://w3id.org/oc/corpus/br/44074>,Improving the Blood Pressure Control With the ProActive Attitude of Hypertensive Patients Seeking Follow-up Services,2016,Fang - Haiqing,Medicine,14,95,e3233--e3233,Ovid Technologies (Wolters Kluwer Health),10.1097/md.0000000000003233

            >>> # clean it
            >>> my_csv_file.set_cleaning_and_parsing_parameters(line_head_pattern_to_remove='',
            ...                                     line_tail_pattern_to_remove='',
            ...                                     cell_head_and_tail_characters_to_remove='')
            Cleaning parameters are set. Output resulting from a demo parsing operation is as following:
            ----------------------------------LINE 0----------------------------------
            <BLANKLINE>
            ----------------------------------LINE 1----------------------------------
            ['Journal Article', '<https://w3id.org/oc/corpus/br/44074>', 'Improving the Blood Pressure Control With the ProActive Attitude of Hypertensive Patients Seeking Follow-up Services', '2016', 'Fang - Haiqing', 'Medicine', '14', '95', 'e3233--e3233', 'Ovid Technologies (Wolters Kluwer Health)', '10.1097/md.0000000000003233']

        """
        # set instance cleaning parameters
        self.line_head_artefact          = line_head_pattern_to_remove
        self.line_tail_artefact          = line_tail_pattern_to_remove
        self.cell_ends_artefact          = cell_head_and_tail_characters_to_remove

        # initiate internal values
        line = CSV_Line('')
        first_lines = ['']

        # test parameters on a few lines of file
        with open(self.input_file_path, encoding='utf8') as input_file:
            for i, each_line in enumerate(input_file):
                if each_line != '\n':
                    if i < 2:
                        cleaned_line = self.clean_and_parse_line_to_CSV_Row_using_cleaning_parameters(each_line)
                        first_lines.append(cleaned_line)
                    else:
                        break

        # print the cleaned lines
        print("Cleaning parameters are set. Output resulting from a demo parsing operation is as following:")
        for i, each_line in enumerate(first_lines):
            print('----------------------------------LINE %s----------------------------------' % i)
            print(each_line)


    def set_output_formatting_parameters(self, column_separator='same as input', cell_value_separator=' | ',
                                         line_head=' ', line_tail=' ,',
                                         cell_wrapper='"'):
        """
        Sets line formatting parameters to be used in various methods in CSV_File class. After setting the
        parameters, prints the results of a demo formatting procedure performed with the parameters set.

        Returns:
            - None
            - Console output

        Examples:
            >>> # prep: a csv from blazegraph
            >>> my_csv_file = CSV_File('test_data//data_for_formatting_test.csv',
            ...                    column_delimiter_pattern_in_input_file=',')
            >>> my_csv_file.preview(number_of_lines=2, print_separators_between_lines=True)
            ----------------------------------LINE 1----------------------------------
            <BLANKLINE>
            ----------------------------------LINE 2----------------------------------
            Journal Article,<https://w3id.org/oc/corpus/br/44074>,Improving the Blood Pressure Control With the ProActive Attitude of Hypertensive Patients Seeking Follow-up Services,2016,Fang - Haiqing,Medicine,14,95,e3233--e3233,Ovid Technologies (Wolters Kluwer Health),10.1097/md.0000000000003233


            >>> # prep: set cleaning and parsing parameters (must be done before formatting)
            >>> my_csv_file.set_cleaning_and_parsing_parameters(line_head_pattern_to_remove='',
            ...                                     line_tail_pattern_to_remove='',
            ...                                     cell_head_and_tail_characters_to_remove='')
            Cleaning parameters are set. Output resulting from a demo parsing operation is as following:
            ----------------------------------LINE 0----------------------------------
            <BLANKLINE>
            ----------------------------------LINE 1----------------------------------
            ['Journal Article', '<https://w3id.org/oc/corpus/br/44074>', 'Improving the Blood Pressure Control With the ProActive Attitude of Hypertensive Patients Seeking Follow-up Services', '2016', 'Fang - Haiqing', 'Medicine', '14', '95', 'e3233--e3233', 'Ovid Technologies (Wolters Kluwer Health)', '10.1097/md.0000000000003233']


            >>> # set formatting parameters for yasgui.org-like style (same with defaults, but entered for demonstration)
            >>> my_csv_file.set_output_formatting_parameters(column_separator=' , ',
            ...                                             cell_value_separator=' | ', #same with default value
            ...                                             line_head=' ',
            ...                                             line_tail=' ,',
            ...                                             cell_wrapper='"')
            Formatting parameters are set. Output resulting from a demo formatting operation, as a preview of how lines would be printed to a CSV file (except horizontal line separators) is as following:
            ----------------------------------LINE 0----------------------------------
            <BLANKLINE>
            ----------------------------------LINE 1----------------------------------
             "Journal Article" , "<https://w3id.org/oc/corpus/br/44074>" , "Improving the Blood Pressure Control With the ProActive Attitude of Hypertensive Patients Seeking Follow-up Services" , "2016" , "Fang - Haiqing" , "Medicine" , "14" , "95" , "e3233--e3233" , "Ovid Technologies (Wolters Kluwer Health)" , "10.1097/md.0000000000003233" ,

            >>> # set formatting parameters (blazegraph style)
            >>> my_csv_file.set_output_formatting_parameters(column_separator=' , ', line_head='', line_tail='', cell_wrapper='')
            Formatting parameters are set. Output resulting from a demo formatting operation, as a preview of how lines would be printed to a CSV file (except horizontal line separators) is as following:
            ----------------------------------LINE 0----------------------------------
            <BLANKLINE>
            ----------------------------------LINE 1----------------------------------
            Journal Article , <https://w3id.org/oc/corpus/br/44074> , Improving the Blood Pressure Control With the ProActive Attitude of Hypertensive Patients Seeking Follow-up Services , 2016 , Fang - Haiqing , Medicine , 14 , 95 , e3233--e3233 , Ovid Technologies (Wolters Kluwer Health) , 10.1097/md.0000000000003233

            >>> ### format another file
            >>> # prep: a csv with artefacts
            >>> my_csv_file = CSV_File('test_data//data_with_head_and_tail_artefacts.csv',
            ...                    column_delimiter_pattern_in_input_file=' , ')
            >>> my_csv_file.preview(number_of_lines=2, print_separators_between_lines=True)
            ----------------------------------LINE 1----------------------------------
            head artefact "*publication_type*" , "journal_article" , "title" , "publication_year" , "author_name" , "journal_name" , "journal_issue_number" , "journal_volume_number" , "startEndPages" , "publisher_name" , "doi" , tail artefact
            ----------------------------------LINE 2----------------------------------
            head artefact "*Journal Article*" , "https://w3id.org/oc/corpus/br/45174" , "An inventory for measuring clinical anxiety: Psychometric properties." , "1988" , "Steer - Robert A." , "Journal of Consulting and Clinical Psychology" , "6" , "56" , "893--897" , "American Psychological Association (APA)" , "10.1037//0022-006x.56.6.893" , tail artefact

            >>> # set cleaning parameters
            >>> my_csv_file.set_cleaning_and_parsing_parameters(line_head_pattern_to_remove='head artefact ',
            ...                                     line_tail_pattern_to_remove=' , tail artefact',
            ...                                     cell_head_and_tail_characters_to_remove='"*')
            Cleaning parameters are set. Output resulting from a demo parsing operation is as following:
            ----------------------------------LINE 0----------------------------------
            <BLANKLINE>
            ----------------------------------LINE 1----------------------------------
            ['publication_type', 'journal_article', 'title', 'publication_year', 'author_name', 'journal_name', 'journal_issue_number', 'journal_volume_number', 'startEndPages', 'publisher_name', 'doi']
            ----------------------------------LINE 2----------------------------------
            ['Journal Article', 'https://w3id.org/oc/corpus/br/45174', 'An inventory for measuring clinical anxiety: Psychometric properties.', '1988', 'Steer - Robert A.', 'Journal of Consulting and Clinical Psychology', '6', '56', '893--897', 'American Psychological Association (APA)', '10.1037//0022-006x.56.6.893']

            >>> # set formatting parameters for yasgui.org-like style
            >>> my_csv_file.set_output_formatting_parameters(column_separator=' , ',
            ...                                             cell_value_separator=' | ', #same with default value
            ...                                             line_head=' ',
            ...                                             line_tail=' ,',
            ...                                             cell_wrapper='"')
            Formatting parameters are set. Output resulting from a demo formatting operation, as a preview of how lines would be printed to a CSV file (except horizontal line separators) is as following:
            ----------------------------------LINE 0----------------------------------
            <BLANKLINE>
            ----------------------------------LINE 1----------------------------------
             "publication_type" , "journal_article" , "title" , "publication_year" , "author_name" , "journal_name" , "journal_issue_number" , "journal_volume_number" , "startEndPages" , "publisher_name" , "doi" ,
            ----------------------------------LINE 2----------------------------------
             "Journal Article" , "https://w3id.org/oc/corpus/br/45174" , "An inventory for measuring clinical anxiety: Psychometric properties." , "1988" , "Steer - Robert A." , "Journal of Consulting and Clinical Psychology" , "6" , "56" , "893--897" , "American Psychological Association (APA)" , "10.1037//0022-006x.56.6.893" ,

        """
        # error handling
        from preprocessor.string_tools import Parameter_Value
        for each_parameter in [column_separator, line_head, line_tail, cell_wrapper, cell_value_separator]:
            Parameter_Value(each_parameter).force_type(str)

        # change default instance parameters
        if column_separator != 'same as input':
            self.output_column_separator = column_separator
        self.output_line_head            = line_head
        self.output_line_tail            = line_tail
        self.output_cell_wrapper         = cell_wrapper
        self.output_cell_value_separator = cell_value_separator
        self.formatting_parameters_are_set = True

        # initiate internal values
        line = CSV_Line('')
        first_lines = ['']

        # test parameters on a few lines of file
        with open(self.input_file_path, encoding='utf8') as input_file:
            for i, each_line in enumerate(input_file):
                if each_line != '\n':
                    if i < 2:
                        # clean and parse line
                        cleaned_line = self.clean_and_parse_line_to_CSV_Row_using_cleaning_parameters(each_line)
                        # format line for output
                        formatted_line = self.format_line_using_output_formatting_parameters(cleaned_line)
                        first_lines.append(formatted_line)
                    else:
                        break

        # print the formatted lines
        print("Formatting parameters are set. Output resulting from a demo formatting operation, as a preview of how lines would be printed to a CSV file (except horizontal line separators) is as following:")
        for i, each_line in enumerate(first_lines):
            print('----------------------------------LINE %s----------------------------------' % i)
            print(each_line)


    def clean_and_parse_line_to_CSV_Row_using_cleaning_parameters(self, input_string_or_CSV_line):
        """
        Cleans input using parameters cleaning parameters set by set_cleaning_and_parsing_parameters() method.
        Because this method is only used internally in live (i.e., line-by-line) parsing class methods, its
        parameters are not directly set. They are rather passed from the previously set instance variables, that
        define how the file is to be cleaned each time this method is called internally by another method (which happens
        multiple times).

        Args:
            input_string_or_CSV_line(str, CSV_Line): Input line to be cleaned

        Returns:
            CSV_Line object

        Examples:
            See CSV_File.set_cleaning_and_parsing_parameters() for tests
        """
        # clean line ends and beginnings
        csv_line = CSV_Line(input_string_or_CSV_line). \
            clean_from_newline_characters(). \
            clean_head_and_tail_from_patterns([self.line_tail_artefact], location='tail'). \
            clean_head_and_tail_from_patterns([self.line_head_artefact], location='head')

        # clean cells
        csv_row = csv_line.parse_line_and_CONVERT_to_CSV_Row(self.input_column_separator_pattern). \
            clean_cell_heads_and_tails_from_characters(self.cell_ends_artefact)

        return csv_row


    def format_line_using_output_formatting_parameters(self, listlike_input_string_or_CSV_row):
        """
        Formats input using output formatting parameters (which are instance variables set by set_cleaning_and_parsing_parameters()
        method). Because this method is only used internally in live (i.e., line-by-line) parsing class methods, its
        parameters are not directly set. They are rather passed from the previously set instance variables, that define
        how the file is to be cleaned each time this method is called internally by another method (which happens
        multiple times).

        Args:
            listlike_input_string_or_CSV_row(str, CSV_Row): Input line to be formatted

        Returns:
            CSV_Line object

        Examples:
            See CSV_File.set_output_formatting_parameters() for tests
        """
        # require formatting parameters to be set beforehand
        if not self.formatting_parameters_are_set:
            raise ValueError('This method requires formatting parameters to be previously set using '
                             '"set_output_formatting_parameters" method')

        # format line ends and beginnings
        formatted_csv_line = listlike_input_string_or_CSV_row.format_for_print_and_CONVERT_to_CSV_Line(
                                            column_separator=self.output_column_separator,
                                            line_head=self.output_line_head,
                                            line_tail=self.output_line_tail,
                                            cell_wrapper=self.output_cell_wrapper)
        return formatted_csv_line


    def build_id_registry(self, index_position_of_id_column):
        """
        Adds entries to self.registry in {ROW_ID:[OCCURENCE_LINE_NO_1, OCCURENCE_LINE_NO_2]} format.

        Args:
            index_position_of_id_column(int): The index position of the column in the csv file where row id exists.

        Returns:
            - Nothing
            - Modifies self.registry
            - Sets self.registry_is_built to True
            - Prints success message to console


        Examples:
            >>> # a csv from yasgui.org
            >>> my_csv_file = CSV_File('test_data//yasgui_output_100.csv',
            ...                         column_delimiter_pattern_in_input_file=' , ')
            >>> my_csv_file.set_cleaning_and_parsing_parameters(line_head_pattern_to_remove=' ',
            ...                                     line_tail_pattern_to_remove=' ,',
            ...                                     cell_head_and_tail_characters_to_remove='"')
            Cleaning parameters are set. Output resulting from a demo parsing operation is as following:
            ----------------------------------LINE 0----------------------------------
            <BLANKLINE>
            ----------------------------------LINE 1----------------------------------
            ['publication_type', 'journal_article', 'title', 'publication_year', 'author_name', 'journal_name', 'journal_issue_number', 'journal_volume_number', 'startEndPages', 'publisher_name', 'doi']
            ----------------------------------LINE 2----------------------------------
            ['Journal Article', 'https://w3id.org/oc/corpus/br/45174', 'An inventory for measuring clinical anxiety: Psychometric properties.', '1988', 'Steer - Robert A.', 'Journal of Consulting and Clinical Psychology', '6', '56', '893--897', 'American Psychological Association (APA)', '10.1037//0022-006x.56.6.893']

            >>> my_csv_file.build_id_registry(1)
            ID registry "self.registry" is built successfully.
            >>> my_csv_file.registry.content
            {'journal_article': [0], 'https://w3id.org/oc/corpus/br/45174': [1, 2], 'https://w3id.org/oc/corpus/br/46047': [3, 4, 5], 'https://w3id.org/oc/corpus/br/46375': [6, 7, 8, 9], 'https://w3id.org/oc/corpus/br/46408': [10, 11], 'https://w3id.org/oc/corpus/br/46641': [12, 13, 14, 15, 16, 17], 'https://w3id.org/oc/corpus/br/46650': [18, 19], 'https://w3id.org/oc/corpus/br/47542': [20, 93, 94, 95, 96], 'https://w3id.org/oc/corpus/br/14581': [21, 22, 23], 'https://w3id.org/oc/corpus/br/14585': [24, 25], 'https://w3id.org/oc/corpus/br/14610': [26, 27, 28, 29, 30], 'https://w3id.org/oc/corpus/br/14626': [31, 32, 33, 34, 35, 36, 37, 38], 'https://w3id.org/oc/corpus/br/14839': [39, 40], 'https://w3id.org/oc/corpus/br/14895': [41, 42, 43, 44], 'https://w3id.org/oc/corpus/br/14910': [45, 46, 47, 48], 'https://w3id.org/oc/corpus/br/14922': [49, 50], 'https://w3id.org/oc/corpus/br/14956': [51, 52, 53, 54], 'https://w3id.org/oc/corpus/br/14962': [55, 56, 57, 58], 'https://w3id.org/oc/corpus/br/15109': [59, 60, 61, 62, 63, 64], 'https://w3id.org/oc/corpus/br/15411': [65, 66, 67, 68], 'https://w3id.org/oc/corpus/br/15886': [69, 70, 71, 72, 73], 'https://w3id.org/oc/corpus/br/15895': [74], 'https://w3id.org/oc/corpus/br/15926': [75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92], 'https://w3id.org/oc/corpus/br/11631': [97, 98], 'https://w3id.org/oc/corpus/br/11646': [99]}


            >>> # a csv from blazegraph
            >>> my_csv_file = CSV_File('test_data//blazegraph_output_50.csv',
            ...                         column_delimiter_pattern_in_input_file=',')
            >>> my_csv_file.set_cleaning_and_parsing_parameters(line_head_pattern_to_remove='',
            ...                                     line_tail_pattern_to_remove='',
            ...                                     cell_head_and_tail_characters_to_remove='<>')
            Cleaning parameters are set. Output resulting from a demo parsing operation is as following:
            ----------------------------------LINE 0----------------------------------
            <BLANKLINE>
            ----------------------------------LINE 1----------------------------------
            ['Journal Article', 'https://w3id.org/oc/corpus/br/44074', 'Improving the Blood Pressure Control With the ProActive Attitude of Hypertensive Patients Seeking Follow-up Services', '2016', 'Fang - Haiqing', 'Medicine', '14', '95', 'e3233--e3233', 'Ovid Technologies (Wolters Kluwer Health)', '10.1097/md.0000000000003233']

            >>> my_csv_file.build_id_registry(index_position_of_id_column=1)
            ID registry "self.registry" is built successfully.
            >>> my_csv_file.registry.content
            {'https://w3id.org/oc/corpus/br/44074': [1, 2, 3, 4, 5, 6, 7], 'https://w3id.org/oc/corpus/br/44393': [8, 9, 10], 'https://w3id.org/oc/corpus/br/44409': [11, 12, 13, 14], 'https://w3id.org/oc/corpus/br/41995': [15], 'https://w3id.org/oc/corpus/br/42007': [16, 17, 18, 19, 20, 21], 'https://w3id.org/oc/corpus/br/42026': [22, 23, 24, 25, 26, 27], 'https://w3id.org/oc/corpus/br/42038': [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47], 'https://w3id.org/oc/corpus/br/42064': [48, 49, 50]}

        """
        from preprocessor.dict_tools import Registry
        self.index_position_of_id_column = index_position_of_id_column
        registry = self.registry

        with open(self.input_file_path, encoding='utf8') as input_file:
            for i, each_line in enumerate(input_file):
                if each_line != '\n':
                    csv_row = self.clean_and_parse_line_to_CSV_Row_using_cleaning_parameters(each_line)
                    id_of_current_row = csv_row[index_position_of_id_column]
                    # TODO: [REF4] Must make it possible to use CSV_Cell as dictionary keys. Instead of id_of_current_row,
                    # "str(id_of_current_row)" or "id_of_current_row.content" must be called. This is because CSV_Cell
                    # objects cannot be used in dictionary keys, possibly due to a missing override in CSV_Cell class.
                    registry.add(key=id_of_current_row.content, value=i)  # .content or wrapping id_of_current_row in
                    # str() is necessary as id_of_current_row is a CSV_Cell object, and when CSV_Cell objects are
                    # extracted from CSV_Row objects they seem to cause comparison problems Also see: REF1, REF2, REF3, REF 4.

        self.registry = registry
        self.registry_is_built = True
        print('ID registry "self.registry" is built successfully.')


    def get_line_numbers_where_id_occurs(self, target_id):
        """
        Retrieves the value that matches target_id from self.registry. This value is a list of line numbers
        where the target_id occurs.

        Returns:
            list

        Examples:
            >>> # prep: a csv from yasgui.org
            >>> my_csv_file = CSV_File('test_data//yasgui_output_100.csv',
            ...                         column_delimiter_pattern_in_input_file=' , ')
            >>> my_csv_file.set_cleaning_and_parsing_parameters(line_head_pattern_to_remove=' ',
            ...                                     line_tail_pattern_to_remove=' ,',
            ...                                     cell_head_and_tail_characters_to_remove='"')
            Cleaning parameters are set. Output resulting from a demo parsing operation is as following:
            ----------------------------------LINE 0----------------------------------
            <BLANKLINE>
            ----------------------------------LINE 1----------------------------------
            ['publication_type', 'journal_article', 'title', 'publication_year', 'author_name', 'journal_name', 'journal_issue_number', 'journal_volume_number', 'startEndPages', 'publisher_name', 'doi']
            ----------------------------------LINE 2----------------------------------
            ['Journal Article', 'https://w3id.org/oc/corpus/br/45174', 'An inventory for measuring clinical anxiety: Psychometric properties.', '1988', 'Steer - Robert A.', 'Journal of Consulting and Clinical Psychology', '6', '56', '893--897', 'American Psychological Association (APA)', '10.1037//0022-006x.56.6.893']
            >>> my_csv_file.build_id_registry(1)
            ID registry "self.registry" is built successfully.
            >>> my_csv_file.registry.content
            {'journal_article': [0], 'https://w3id.org/oc/corpus/br/45174': [1, 2], 'https://w3id.org/oc/corpus/br/46047': [3, 4, 5], 'https://w3id.org/oc/corpus/br/46375': [6, 7, 8, 9], 'https://w3id.org/oc/corpus/br/46408': [10, 11], 'https://w3id.org/oc/corpus/br/46641': [12, 13, 14, 15, 16, 17], 'https://w3id.org/oc/corpus/br/46650': [18, 19], 'https://w3id.org/oc/corpus/br/47542': [20, 93, 94, 95, 96], 'https://w3id.org/oc/corpus/br/14581': [21, 22, 23], 'https://w3id.org/oc/corpus/br/14585': [24, 25], 'https://w3id.org/oc/corpus/br/14610': [26, 27, 28, 29, 30], 'https://w3id.org/oc/corpus/br/14626': [31, 32, 33, 34, 35, 36, 37, 38], 'https://w3id.org/oc/corpus/br/14839': [39, 40], 'https://w3id.org/oc/corpus/br/14895': [41, 42, 43, 44], 'https://w3id.org/oc/corpus/br/14910': [45, 46, 47, 48], 'https://w3id.org/oc/corpus/br/14922': [49, 50], 'https://w3id.org/oc/corpus/br/14956': [51, 52, 53, 54], 'https://w3id.org/oc/corpus/br/14962': [55, 56, 57, 58], 'https://w3id.org/oc/corpus/br/15109': [59, 60, 61, 62, 63, 64], 'https://w3id.org/oc/corpus/br/15411': [65, 66, 67, 68], 'https://w3id.org/oc/corpus/br/15886': [69, 70, 71, 72, 73], 'https://w3id.org/oc/corpus/br/15895': [74], 'https://w3id.org/oc/corpus/br/15926': [75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92], 'https://w3id.org/oc/corpus/br/11631': [97, 98], 'https://w3id.org/oc/corpus/br/11646': [99]}

            >>> # get line numbers from id
            >>> my_csv_file.get_line_numbers_where_id_occurs(target_id='https://w3id.org/oc/corpus/br/45174')
            [1, 2]

            >>> # prep: a csv from blazegraph
            >>> my_csv_file = CSV_File('test_data//blazegraph_output_50.csv',
            ...                         column_delimiter_pattern_in_input_file=',')
            >>> my_csv_file.set_cleaning_and_parsing_parameters(line_head_pattern_to_remove='',
            ...                                     line_tail_pattern_to_remove='',
            ...                                     cell_head_and_tail_characters_to_remove='<>')
            Cleaning parameters are set. Output resulting from a demo parsing operation is as following:
            ----------------------------------LINE 0----------------------------------
            <BLANKLINE>
            ----------------------------------LINE 1----------------------------------
            ['Journal Article', 'https://w3id.org/oc/corpus/br/44074', 'Improving the Blood Pressure Control With the ProActive Attitude of Hypertensive Patients Seeking Follow-up Services', '2016', 'Fang - Haiqing', 'Medicine', '14', '95', 'e3233--e3233', 'Ovid Technologies (Wolters Kluwer Health)', '10.1097/md.0000000000003233']

            >>> my_csv_file.build_id_registry(index_position_of_id_column=1)
            ID registry "self.registry" is built successfully.
            >>> my_csv_file.registry.content
            {'https://w3id.org/oc/corpus/br/44074': [1, 2, 3, 4, 5, 6, 7], 'https://w3id.org/oc/corpus/br/44393': [8, 9, 10], 'https://w3id.org/oc/corpus/br/44409': [11, 12, 13, 14], 'https://w3id.org/oc/corpus/br/41995': [15], 'https://w3id.org/oc/corpus/br/42007': [16, 17, 18, 19, 20, 21], 'https://w3id.org/oc/corpus/br/42026': [22, 23, 24, 25, 26, 27], 'https://w3id.org/oc/corpus/br/42038': [28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47], 'https://w3id.org/oc/corpus/br/42064': [48, 49, 50]}

            >>> # get line numbers from id
            >>> my_csv_file.get_line_numbers_where_id_occurs('https://w3id.org/oc/corpus/br/44074')
            [1, 2, 3, 4, 5, 6, 7]

            >>> # type of line numbers
            >>> result_list = my_csv_file.get_line_numbers_where_id_occurs('https://w3id.org/oc/corpus/br/44074')
            >>> type(result_list)
            <class 'list'>
            >>> type(result_list[0])
            <class 'int'>


        """
        if not self.registry_is_built:
            raise Exception('get_line_numbers_where_id_occurs() method requires an id registry to be built '
                            'before it can operate. Build a registry first with build_id_registry() method.')

        registry = self.registry
        return registry.get_values_from_key(target_id)


    def get_line_at_position_from_file(self, line_index):
        """
        Returns a specified line from the CSV file without reading the whole file into memory. Is an override
        of the method with the same name in the superclass 'Text_File'. The override reuses the superclass'
        method, but simply converts the returning output from String object to CSV_Line object

        Args:
            line_index(int): A value that can take integers starting from 0.

        Returns:
            CSV_Line object (created from string at line in file).

        Examples:
            >>> # return first line of file
            >>> my_file = CSV_File('test_data//example_merged_yasgui_1000.csv', ' , ')
            >>> my_file.get_line_at_position_from_file(0)
            '"publication_type" , "journal_article" , "title" , "publication_year" , "author_name" , "journal_name" , "journal_issue_number" , "journal_volume_number" , "startEndPages" , "publisher_name" , "doi" , "cited_by_article" ,'

            >>> # return another line
            >>> my_file.get_line_at_position_from_file(121)
            '"Journal Article" , "https://w3id.org/oc/corpus/br/3448" , "Perioperative Myocardial Infarction" , "2009" , "Beattie - W. S. | Mosseri - M. | Jaffe - A. S. | Alpert - J. S." , "Circulation" , "22" , "119" , "2936--2944" , "Ovid Technologies (Wolters Kluwer Health)" , "10.1161/circulationaha.108.828228" , "https://w3id.org/oc/corpus/br/3426" ,'

            >>> # return last line
            >>> my_file.get_line_at_position_from_file(266)
            '"Journal Article" , "https://w3id.org/oc/corpus/br/3437" , "Myocardial Injury after Noncardiac Surgery" , "2014" , "Niebrzegowska - Edyta | Benton - Sally | Wragg - Andrew | Archbold - Andrew | Smith - Amanda | McAlees - Eleanor | Ramballi - Cheryl | MacDonald - Neil | Januszewska - Marta | Shariffuddin - Ina I. | Vasanthan - V. | Hashim - N. H. M. | Undok - A. Wahab | Ki - Ushananthini | Lai - Hou Yee | Ahmad - Wan Azman | Ackland - Gareth | Khan - Ahsun | Almeida - Smitha | Cherian - Joseph | Furruqh - Sultana | Abraham - Valsa | Paniagua - Pilar | Urrutia - Gerard | Maestre - Mari Luz | Santaló - Miquel | Gonzalez - Raúl | Font - Adrià | Martínez - Cecilia" , "Anesthesiology" , "3" , "120" , "564--578" , "Ovid Technologies (Wolters Kluwer Health)" , "10.1097/aln.0000000000000113" , "https://w3id.org/oc/corpus/br/3522 | https://w3id.org/oc/corpus/br/300243 | https://w3id.org/oc/corpus/br/3062326 | https://w3id.org/oc/corpus/br/3271454 | https://w3id.org/oc/corpus/br/3879533 | https://w3id.org/oc/corpus/br/4205354 | https://w3id.org/oc/corpus/br/5253819 | https://w3id.org/oc/corpus/br/6332120 | https://w3id.org/oc/corpus/br/7799424 | https://w3id.org/oc/corpus/br/8003885 | https://w3id.org/oc/corpus/br/8185544" ,'

            >>> # erroneous index number entered
            >>> try:
            ...     my_file.get_line_at_position_from_file(300) # there is no 300th line in the file
            ... except IndexError as error_message:
            ...     print('Exception: ' + str(error_message))
            Exception: Requested line number '300' does not exist in file.
        """
        from preprocessor.Text_File import Text_File
        # use the same method from superclass but convert output to CSV_line
        String_line = Text_File.get_line_at_position_from_file(self, line_index)
        csv_line = CSV_Line(String_line.content)
        return csv_line

        # with open(self.input_file_path, encoding='utf8') as input_file:
        #     line = None
        #
        #     for i, each_line in enumerate(input_file):
        #         if i == line_index:
        #             line = CSV_Line(each_line)
        #         elif i > line_index:
        #             break
        #
        #     if line == None:
        #         raise IndexError("Requested line number '%s' does not exist in file." % line_index)
        #
        #     # if not cleaned from '\n', comparisons and operations tend to be problematic
        #     # write to file with base print() function to get back the new line in the end
        #     line.clean_from_newline_characters()
        #
        #     return line

    def live_clean_and_row_merge(self, index_position_of_id_column):
        """
        Reads and parses a file line by line, cleans lines and cells from specified patterns, and merges rows by id
        on-the go without having to parse all of the file or read it into memory.

        Args:
            index_position_of_id_column(int): The index of row identifier column in csv file. The value is passed
                directly to build_id_registry method, which uses a parameter of the same name to parse ids, and builds an
                id vs row registry.


        Examples:
            >>> ########### prep: a csv from yasgui.org ###########
            >>> # initiate
            >>> my_csv_file = CSV_File('test_data//yasgui_output_100.csv',
            ...                    column_delimiter_pattern_in_input_file=' , ')

            >>> # set cleaning parameters
            >>> my_csv_file.set_cleaning_and_parsing_parameters(line_tail_pattern_to_remove=' ,',
            ...                                           cell_head_and_tail_characters_to_remove='"')
            Cleaning parameters are set. Output resulting from a demo parsing operation is as following:
            ----------------------------------LINE 0----------------------------------
            <BLANKLINE>
            ----------------------------------LINE 1----------------------------------
            ['publication_type', 'journal_article', 'title', 'publication_year', 'author_name', 'journal_name', 'journal_issue_number', 'journal_volume_number', 'startEndPages', 'publisher_name', 'doi']
            ----------------------------------LINE 2----------------------------------
            ['Journal Article', 'https://w3id.org/oc/corpus/br/45174', 'An inventory for measuring clinical anxiety: Psychometric properties.', '1988', 'Steer - Robert A.', 'Journal of Consulting and Clinical Psychology', '6', '56', '893--897', 'American Psychological Association (APA)', '10.1037//0022-006x.56.6.893']

            >>> # set formatting parameters
            >>> my_csv_file.set_output_formatting_parameters(column_separator=' , ', cell_value_separator=' | ',
            ...                                              line_head=' ', line_tail=' ,', cell_wrapper='"')
            Formatting parameters are set. Output resulting from a demo formatting operation, as a preview of how lines would be printed to a CSV file (except horizontal line separators) is as following:
            ----------------------------------LINE 0----------------------------------
            <BLANKLINE>
            ----------------------------------LINE 1----------------------------------
             "publication_type" , "journal_article" , "title" , "publication_year" , "author_name" , "journal_name" , "journal_issue_number" , "journal_volume_number" , "startEndPages" , "publisher_name" , "doi" ,
            ----------------------------------LINE 2----------------------------------
             "Journal Article" , "https://w3id.org/oc/corpus/br/45174" , "An inventory for measuring clinical anxiety: Psychometric properties." , "1988" , "Steer - Robert A." , "Journal of Consulting and Clinical Psychology" , "6" , "56" , "893--897" , "American Psychological Association (APA)" , "10.1037//0022-006x.56.6.893" ,

                    with open(self.input_file_path, encoding='utf8') as input_file:
            >>> #################################################

            >>> my_csv_file.live_clean_and_row_merge(1)
            ID registry "self.registry" is built successfully.
            iteration 1   row id:  journal_article   merging lines:  [0]
            iteration 2   row id:  https://w3id.org/oc/corpus/br/45174   merging lines:  [1, 2]
            iteration 3   row id:  https://w3id.org/oc/corpus/br/46047   merging lines:  [3, 4, 5]
            iteration 4   row id:  https://w3id.org/oc/corpus/br/46375   merging lines:  [6, 7, 8, 9]
            iteration 5   row id:  https://w3id.org/oc/corpus/br/46408   merging lines:  [10, 11]
            iteration 6   row id:  https://w3id.org/oc/corpus/br/46641   merging lines:  [12, 13, 14, 15, 16, 17]
            iteration 7   row id:  https://w3id.org/oc/corpus/br/46650   merging lines:  [18, 19]
            iteration 8   row id:  https://w3id.org/oc/corpus/br/47542   merging lines:  [20, 93, 94, 95, 96]
            iteration 9   row id:  https://w3id.org/oc/corpus/br/14581   merging lines:  [21, 22, 23]
            iteration 10   row id:  https://w3id.org/oc/corpus/br/14585   merging lines:  [24, 25]
            iteration 11   row id:  https://w3id.org/oc/corpus/br/14610   merging lines:  [26, 27, 28, 29, 30]
            iteration 12   row id:  https://w3id.org/oc/corpus/br/14626   merging lines:  [31, 32, 33, 34, 35, 36, 37, 38]
            iteration 13   row id:  https://w3id.org/oc/corpus/br/14839   merging lines:  [39, 40]
            iteration 14   row id:  https://w3id.org/oc/corpus/br/14895   merging lines:  [41, 42, 43, 44]
            iteration 15   row id:  https://w3id.org/oc/corpus/br/14910   merging lines:  [45, 46, 47, 48]
            iteration 16   row id:  https://w3id.org/oc/corpus/br/14922   merging lines:  [49, 50]
            iteration 17   row id:  https://w3id.org/oc/corpus/br/14956   merging lines:  [51, 52, 53, 54]
            iteration 18   row id:  https://w3id.org/oc/corpus/br/14962   merging lines:  [55, 56, 57, 58]
            iteration 19   row id:  https://w3id.org/oc/corpus/br/15109   merging lines:  [59, 60, 61, 62, 63, 64]
            iteration 20   row id:  https://w3id.org/oc/corpus/br/15411   merging lines:  [65, 66, 67, 68]
            iteration 21   row id:  https://w3id.org/oc/corpus/br/15886   merging lines:  [69, 70, 71, 72, 73]
            iteration 22   row id:  https://w3id.org/oc/corpus/br/15895   merging lines:  [74]
            iteration 23   row id:  https://w3id.org/oc/corpus/br/15926   merging lines:  [75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92]
            iteration 24   row id:  https://w3id.org/oc/corpus/br/11631   merging lines:  [97, 98]
            iteration 25   row id:  https://w3id.org/oc/corpus/br/11646   merging lines:  [99]
            Cleaning/row-merging successful. The output is written to "test_data//yasgui_output_100_rows_merged.csv"

            >>> # also read and print from the file to make sure (in case the previews from preeding functions are faulty_
            >>> my_csv_file.preview(number_of_lines=2, print_separators_between_lines=True)
            ----------------------------------LINE 1----------------------------------
            "publication_type" , "journal_article" , "title" , "publication_year" , "author_name" , "journal_name" , "journal_issue_number" , "journal_volume_number" , "startEndPages" , "publisher_name" , "doi" ,
            ----------------------------------LINE 2----------------------------------
            "Journal Article" , "https://w3id.org/oc/corpus/br/45174" , "An inventory for measuring clinical anxiety: Psychometric properties." , "1988" , "Steer - Robert A." , "Journal of Consulting and Clinical Psychology" , "6" , "56" , "893--897" , "American Psychological Association (APA)" , "10.1037//0022-006x.56.6.893" ,


        """
        # build a registry of id vs. row numbers
        if not self.registry_is_built:
            self.build_id_registry(index_position_of_id_column=index_position_of_id_column)
            #raise Exception('get_line_numbers_where_id_occurs() method requires an id registry to be built '
            #                'before it can operate. Build a registry first with build_id_registry() method.')


        with open(self.input_file_path, encoding='utf8') as input_file:
            with open(self.row_merged_output_file_path, 'w', encoding='utf8') as output_file:
                registry = self.registry

                buffer = Row_Merge_Buffer(1)
                merged_row = []
                iteration_counter = 0

                # iterate over the id-line_no dictionary
                for each_id, each_line_numbers_list in registry.content.items():
                    iteration_counter += 1
                    print('iteration', iteration_counter, '  row id: ', each_id,
                          '  merging lines: ', each_line_numbers_list)

                    buffer.id_of_current_rows_in_buffer = each_id
                    # append all lines that an id occurs to buffer
                    for each_line_number in each_line_numbers_list:

                        csv_line = self.get_line_at_position_from_file(each_line_number)
                        csv_row = self.clean_and_parse_line_to_CSV_Row_using_cleaning_parameters(csv_line)

                        # TODO: [REF2] CSV_Row and CSV_Cell objects both fail with comparison operators, and thus,
                        # create problems when compared with ids in buffer. Adding to the buffer with comparison was
                        # possible only when the comparison method is_id_of_rows_in_buffer_same_with_outside_row first
                        # transformed the CSV_Cell id (which was one of the ids being compared) to str.
                        # Also see: REF1, REF2, REF3, REF 4
                        buffer.append_row_if_ids_match(csv_row, raise_error_on_id_mismatch=True)


                    merged_row = buffer.merge_all_rows_to_one(' | ').dataset
                    formatted_row = self.format_line_using_output_formatting_parameters(merged_row)
                    print(formatted_row, file=output_file)
                    buffer.clear_all()

        print('Cleaning/row-merging successful. The output is written to "%s"' % self.row_merged_output_file_path)

    def clean_ttl_uri_strings(self):
        # TODO: Add docstring
        from urllib.parse import quote
        output_file_path = self.uri_cleaned_output_file_path

        with open(self.input_file_path, encoding='utf8') as input_file:
            with open(output_file_path, 'w', encoding='utf8') as output_file:
                for each_line in input_file:
                    csv_line = CSV_Line(each_line)
                    csv_row  = self.clean_and_parse_line_to_CSV_Row_using_cleaning_parameters(csv_line)

                    cleaned_line = ''
                    for each_uri in csv_row:
                        # print('each_uri:', each_uri)
                        cleaned_uri = quote(str(each_uri), safe=' <>_:-#//.@"\'')
                        # TODO: The '<' and '>' and other static characters are workarounds, because set_output_formatting_paramters method could not wrap each uri with two different characters
                        # This is a workaround. For it to work properly, the uris should be cleaned from '<' and '>' during parsing
                        cleaned_line = cleaned_line + '<' + cleaned_uri + '>' + ' '

                    # TODO: This static '.' is also a workaround
                    if '> <http://www.w3.org/2000/01/rdf-schema#label> "' in cleaned_line or '> <http://clokman.com/ontologies/scientific-research#isPublishedOnYear> "' in cleaned_line or '> <http://clokman.com/ontologies/scientific-research#hasDOI> "' in cleaned_line or '> <http://clokman.com/ontologies/scientific-research#hasISBN> "' in cleaned_line or '> <http://clokman.com/ontologies/scientific-research#hasISSN> "' in cleaned_line or '> <http://clokman.com/ontologies/scientific-research#isPublishedOnMonth> "' in cleaned_line or '> <http://clokman.com/ontologies/scientific-research#isPublishedOnDate> "' in cleaned_line:
                        cleaned_line = cleaned_line[:-2]
                        cleaned_line = cleaned_line + ' .'
                    else:
                        cleaned_line = cleaned_line + '.'
                    print('cleaned_line: ', cleaned_line)
                    print(cleaned_line, file=output_file)
        print('A file with cleaned URIs is written to %s' % output_file_path )


class CSV_Line (String, str):
    def __init__(self, content):
        """
        Converts an object into CSV_Line.

        Examples:
            >>> CSV_Line('a b c')
            'a b c'
            >>> CSV_Line(2)
            2

            >>> CSV_Line(['1', 2])
            ['1', 2]

            >>> CSV_Line([1, 2, 3])
            [1, 2, 3]

            >>> a = CSV_Line([1, 2, 3])
            >>> type(a)
            <class 'csv_tools.CSV_Line'>

            >>> a = a[1:]
            >>> a
            '1, 2, 3]'

            >>> type(a)
            <class 'str'>


        """
        String.__init__(self, content)
        str.__init__(self)

        self =  str(content)


    # def __str__(self):
    #     if type(self) == list or type(self) == CSV_Row:
    #         input_list = self
    #         separator = self.list_item_separator_pattern
    #         element_wrapper = self.list_item_wrapper_pattern
    #         line_head = self.line_head_pattern
    #         line_tail = self.line_tail_pattern
    #
    #         string_representation = ''
    #
    #         # surround list items with wrappers (if available)
    #         # concatenate all items to string_representation
    #         for each_element in input_list:
    #             string_representation = string_representation + element_wrapper + each_element + element_wrapper + separator
    #
    #         # prevent the separators at the end (e.g., comma at the end in "a,b,c,")
    #         string_representation = string_representation.strip(self.list_item_separator_pattern)
    #         # add line head and tail
    #         string_representation = line_head + string_representation + line_tail
    #
    #
    #         return string_representation
    #     else:
    #         return self

    def parse_line_and_CONVERT_to_CSV_Row(self, column_delimiter_pattern):
        """
        Parses a line using column_delimiter_pattern. If clean_cell_head_and_tails_from is specified, a
        cleaning operation is performed after parsing. This operation is simple, but it may not be efficient when this
        method is used for parsing large datasets.

        Args:
            column_delimiter_pattern(str): Delimiter used to separate columns in the inputted string. Can consist of
                multiple characters
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

            >>> # blazegraph csv line example
            >>> my_line = CSV_Line('Journal Article,<https://w3id.org/oc/corpus/br/802>,Improving health information systems for decision making across five sub-Saharan African countries: Implementation strategies from the African Health Initiative,2013,Mutale - Wilbroad,BMC Health Services Research - BMC Health Serv Res,Suppl 2,13,S9--S9,Springer Science + Business Media,10.1186/1472-6963-13-s2-s9,<https://w3id.org/oc/corpus/id/1032>,<https://w3id.org/oc/corpus/id/1030>')
            >>> my_line.parse_line_and_CONVERT_to_CSV_Row(',')
            ['Journal Article', '<https://w3id.org/oc/corpus/br/802>', 'Improving health information systems for decision making across five sub-Saharan African countries: Implementation strategies from the African Health Initiative', '2013', 'Mutale - Wilbroad', 'BMC Health Services Research - BMC Health Serv Res', 'Suppl 2', '13', 'S9--S9', 'Springer Science + Business Media', '10.1186/1472-6963-13-s2-s9', '<https://w3id.org/oc/corpus/id/1032>', '<https://w3id.org/oc/corpus/id/1030>']

            >>> # yasgui csv line example
            >>> my_line = CSV_Line(' "Journal Article" , "https://w3id.org/oc/corpus/br/1446" , "To IRB or Not to IRB?" , "2004" , "Gunderson - Anne J." , "Academic Medicine" , "7" , "79" , "628--632" , "Ovid Technologies (Wolters Kluwer Health)" , "10.1097/00001888-200407000-00004" ,')

            >>> # in this formatting, artefacts appear around cells after parsing
            >>> my_line.parse_line_and_CONVERT_to_CSV_Row(' , ')
            [' "Journal Article"', '"https://w3id.org/oc/corpus/br/1446"', '"To IRB or Not to IRB?"', '"2004"', '"Gunderson - Anne J."', '"Academic Medicine"', '"7"', '"79"', '"628--632"', '"Ovid Technologies (Wolters Kluwer Health)"', '"10.1097/00001888-200407000-00004" ,']

            >>> # these artefacts can be cleaned
            >>> my_row = my_line.parse_line_and_CONVERT_to_CSV_Row(' , ')
            >>> my_row.clean_cell_heads_and_tails_from_characters(', "')
            ['Journal Article', 'https://w3id.org/oc/corpus/br/1446', 'To IRB or Not to IRB?', '2004', 'Gunderson - Anne J.', 'Academic Medicine', '7', '79', '628--632', 'Ovid Technologies (Wolters Kluwer Health)', '10.1097/00001888-200407000-00004']
        """
        from preprocessor.string_tools import Parameter_Value
        Parameter_Value(self).force_type(CSV_Line)

        line = self
        list = line.slice_with_pattern_and_CONVERT_to_list(column_delimiter_pattern)

        row = CSV_Row(list)
        return row


class CSV_Cell(String):
    """
    Elements that comprise CSV_Row objects. Representation of each cell in a csv file.
    
    WARNING: This class should be used with str(CSV_Cell) in comparisons and modification operations. Otherwise, it may lead to
    issues as it is designed as an experiment in mutability/immutability.

    Example:
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

        >>> CSV_Cell('a') == 'a'
        True

        >>> CSV_Row([CSV_Cell('a')]) == CSV_Row(['a'])
        True

        >>> # WARNING: Not all comparisons may return true, as below, and should always be tested thoroughly before
        >>> # implementing.
        >>> # TODO: [REF1] This comparison should return True. Also see: REF1, REF2, REF3, REF4, REF5
        >>> CSV_Row([CSV_Cell('a')]) == ['a']
        False

        >>> for each_CSV_Cell in CSV_Row([CSV_Cell('a')]):
        ...     each_CSV_Cell == 'a'
        True
    """
    def __new__(cls, content):
        """ Return a string instance"""
        content = str(content)  # for other content types that may be inputted
        return str.__new__(cls, content)



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
        Exception caught:  Parameter "abc" must be of type <class 'csv_tools.CSV_Row'>, <class 'list'>, but is currently of type <class 'str'>
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


    def format_for_print_and_CONVERT_to_CSV_Line(self, column_separator=' , ', line_head=' ', line_tail=' ,', cell_wrapper='"'):
        """
        Takes a list or CSV_Row object, formats it and converts it to CSV_Line object.

        Args:
              column_separator(str): The pattern to to be used as column delimiter. Can take multiple characters.
              line_head(str): The pattern to to be added at the beginning of line. Can take multiple characters.
              line_tail(str): The pattern to to be used at the end of line. Can take multiple characters.
              call_wrapper(str): The pattern to to be used to surround each cell. Can take multiple characters.

        Returns:
            CSV_Line object (self)

        Examples:
            >>> # a CSV_Line's string representation of a string input
            >>> # strings are converted literally
            >>> my_row = CSV_Row(['a','b','c'])
            >>> print(my_row)
            ['a', 'b', 'c']
            >>> print(type(my_row))
            <class 'csv_tools.CSV_Row'>

            >>> # convert CSV_Row to CSV_Line
            >>> my_csv_line = my_row.format_for_print_and_CONVERT_to_CSV_Line()
            >>> my_csv_line
            ' "a" , "b" , "c" ,'
            >>> print(my_csv_line)
             "a" , "b" , "c" ,
            >>> print(type(my_csv_line))
            <class 'csv_tools.CSV_Line'>

            >>> # conversion does not change the original object
            >>> print(my_row)
            ['a', 'b', 'c']
            >>> print(type(my_row))
            <class 'csv_tools.CSV_Row'>

            #>>> my_line = CSV_Line('a,b,c')
            #>>> print(my_line)
            a,b,c

            >>> # this is as close as it gets with normal lists to a csv-like representation (unless additional substring
            >>> # is to be performed)
            >>> print(str(CSV_Row(['a', 'b', 'c']))[1:-1])
            'a', 'b', 'c'

            >>> # the method achieves this result if no parameters are provided
            >>> my_row = CSV_Row(['a', 'b', 'c'])
            >>> print(my_row.format_for_print_and_CONVERT_to_CSV_Line())
             "a" , "b" , "c" ,

            >>> # the parameters can be used to modify formatting
            >>> # e.g., Yasgui style csv line formatting:
            >>> my_row = CSV_Row(['a', 'b', 'c'])
            >>> print(my_row.format_for_print_and_CONVERT_to_CSV_Line(column_separator=' , ',
            ...                                                 line_head=' ',
            ...                                                 line_tail=' ,',
            ...                                                 cell_wrapper='"'))
             "a" , "b" , "c" ,
        """
        # handle exceptions
        from preprocessor.string_tools import Parameter_Value
        Parameter_Value(self).force_type([CSV_Row, list])

        # set internal parameters
        input_list = self

        # initiate internal variable
        string_representation = ''
        # surround list items with wrappers (if available)
        # and concatenate all items to string_representation
        for each_element in input_list:
            # REF: TSOBMML1D
            # TODO: [REF5] BUG and WORKAROUND: instead of CSV_Cell, str(CSV_Cell) is being used for this to work.
            # If str() wrapper is not used, when using set_output_formatting_parameters method changing cell_wrapper
            # parameter to '"' results in ""cell value"" instead of "cell value". Changing it to '-' results in -"cell
            # value"-.
            # It seems that the issue is related to nothing being changed in the original state of the CSV_Cell, as it is an
            # immutable string. Perhaps it's a good idea to redirect CSV_Cell's string and repr calls to CSV_
            # Cell.content instead of doing this each time CSV_Cell is referred.
            # Also see [REF1, REF2, REF3, REF4, REF5] (if they are still on this file [if fixed, removed])
            string_representation = string_representation + cell_wrapper + str(each_element) + cell_wrapper + column_separator

        # separators at the end (e.g., comma at the end in "a,b,c,")
        string_representation = string_representation.strip(column_separator)
        # add line head and tail
        string_representation = line_head + string_representation + line_tail

        # update self with its formatted version
        string_representation = CSV_Line(string_representation)

        return string_representation


class Row_Merge_Buffer(ListData):
    """
    A container that contains lists (or CSV_CSV_Row objects) and their associated ids.

    Args:
        id_column_index(int): Index position of id column of rows to be added to the buffer.
        content(list or CSV_Row): A list of lists or a list of CSV_Rows

    Examples:
        >>> # empty init
        >>> my_buffer = Row_Merge_Buffer(0)
        >>> my_buffer
        'None: []'

        >>> # append as first row and reset buffer
        >>> my_buffer.append_as_first_row_and_reset_buffer(['id52','a','b','c'])
        "id52: [['id52', 'a', 'b', 'c']]"

        >>> # append a second row
        >>> my_buffer.append_row_if_ids_match(['id52','A','B','C'])
        "id52: [['id52', 'a', 'b', 'c'], ['id52', 'A', 'B', 'C']]"

        >>> # string call
        >>> str(my_buffer)
        "id52: [['id52', 'a', 'b', 'c'], ['id52', 'A', 'B', 'C']]"

        >>> # modify content
        >>> my_buffer.dataset = [['id12', 1, 2], ['id12', 3, 4]]
        >>> my_buffer.set_id_of_current_rows_in_buffer('idXX')
        "idXX: [['id12', 1, 2], ['id12', 3, 4]]"

        >>> # CSV_Row as input
        >>> my_buffer.append_as_first_row_and_reset_buffer(CSV_Row(['id42', 1, 2, 3, 4]))
        "id42: [['id42', 1, 2, 3, 4]]"
    """

    def __init__(self, index_of_id_column_in_rows_to_be_added):
        from preprocessor.string_tools import Parameter_Value
        Parameter_Value(index_of_id_column_in_rows_to_be_added).force_type(int)

        #super().__init__()
        ListData.__init__(self)

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
        from preprocessor.string_tools import Parameter_Value
        Parameter_Value(new_row).force_type([list, CSV_Row])

        new_id = new_row[self.index_of_id_column]

        self.clear_all()
        self.set_id_of_current_rows_in_buffer(new_id)
        self.append_row_if_ids_match(new_row)

        return self


    def append_row_if_ids_match(self, new_row, raise_error_on_id_mismatch=True):
        """
        Appends a row at the end of the buffer. This is an override of the append() method of ListData class. In this
        overridden version, append_row appends only if the id of the row being added and the id of the rows in the
        buffer are a match. The id column's index is read from 'self.index_of_id_column' variable.

        Args:
            new_row(list or CSV_Row): The row to be added
            raise_error_on_id_mismatch(bool): Passes the argument to is_id_of_rows_in_buffer_same_with_outside_row()
                method. If set to True, the latter method raises error instead of returning False in case of mismatch.

        Returns:
            - If id of rows in the buffer and the row being added are matching, list or CSV_Row (self).
            - If no match, ValueError

        Examples:
            >>> # empty init
            >>> my_buffer = Row_Merge_Buffer(0)
            >>> my_buffer
            'None: []'

            >>> # append as first row and reset buffer
            >>> my_buffer.append_as_first_row_and_reset_buffer(['id52','a','b','c'])
            "id52: [['id52', 'a', 'b', 'c']]"

            >>> # append a second row
            >>> my_buffer.append_row_if_ids_match(['id52','A','B','C'])
            "id52: [['id52', 'a', 'b', 'c'], ['id52', 'A', 'B', 'C']]"

            >>> # append a row made of CSV_Cell objects
            >>> my_buffer.append_row_if_ids_match([CSV_Cell('id52'), CSV_Cell('csv-A'), CSV_Cell('csv-B'), CSV_Cell('csv-C')])
            "id52: [['id52', 'a', 'b', 'c'], ['id52', 'A', 'B', 'C'], ['id52', 'csv-A', 'csv-B', 'csv-C']]"

            >>> # id mismatch when comparing buffer id with id contained in a CSV_Cell object (whose in a list)
            >>> try:
            ...     my_buffer.append_row_if_ids_match([CSV_Cell('BAD_ID'), CSV_Cell('csv-A'), CSV_Cell('csv-B'), CSV_Cell('csv-C')]) #  BAD_ID will mismatch
            ... except ValueError as error_message:
            ...     print('Exception: ' + str(error_message))
            Exception: ID "BAD_ID" of row "['BAD_ID', 'csv-A', 'csv-B', 'csv-C']" does not match the current id of rows in Row_Merge_Buffer "id52"(comparison of "id_outside_row" and "id_in_buffer" returns: False). Type of id_of_outside_row is <class 'str'>, and type of id_in_buffer is <class 'str'>.

            >>> # append a CSV_Row
            >>> my_buffer.append_row_if_ids_match(CSV_Row([CSV_Cell('id52'), CSV_Cell('csv-row-item-A'), CSV_Cell('csv-row-item-B'), CSV_Cell('csv-row-item-C')]))
            "id52: [['id52', 'a', 'b', 'c'], ['id52', 'A', 'B', 'C'], ['id52', 'csv-A', 'csv-B', 'csv-C'], ['id52', 'csv-row-item-A', 'csv-row-item-B', 'csv-row-item-C']]"

            >>> # id mismatch when comparing buffer id between buffer and a CSV_Row object that is made of CSV_Cells
            >>> try:
            ...     my_buffer.append_row_if_ids_match(CSV_Row([CSV_Cell('BAD ID'), CSV_Cell('csv-row-item-A'),
            ...                      CSV_Cell('csv-row-item-B'), CSV_Cell('csv-row-item-C')])) #  ids will mismatch
            ... except ValueError as error_message:
            ...     print('Exception: ' + str(error_message))
            Exception: ID "BAD ID" of row "['BAD ID', 'csv-row-item-A', 'csv-row-item-B', 'csv-row-item-C']" does not match the current id of rows in Row_Merge_Buffer "id52"(comparison of "id_outside_row" and "id_in_buffer" returns: False). Type of id_of_outside_row is <class 'str'>, and type of id_in_buffer is <class 'str'>.


            >>> # manually set self.id_of_current_rows_in_buffer a CSV_Row and then append
            >>> my_buffer = Row_Merge_Buffer(0)
            >>> my_buffer.id_of_current_rows_in_buffer = 'id12'
            >>> my_buffer.append_row_if_ids_match(CSV_Row([CSV_Cell('id12'), CSV_Cell('csv-row-item-A'), CSV_Cell('csv-row-item-B'), CSV_Cell('csv-row-item-C')]))
            "id12: [['id12', 'csv-row-item-A', 'csv-row-item-B', 'csv-row-item-C']]"

            >>> # csv cell as id, str as row
            >>> my_buffer = Row_Merge_Buffer(0)
            >>> my_buffer.id_of_current_rows_in_buffer = CSV_Cell('id12')
            >>> my_buffer.append_row_if_ids_match(['id12', 'a', 'b'])
            "id12: [['id12', 'a', 'b']]"

            >>> # append row with different size
            >>> my_buffer.append_row(['id12', 'a', 'b', 'c', 'd'])
            "id12: [['id12', 'a', 'b'], ['id12', 'a', 'b', 'c', 'd']]"

        """
        from preprocessor.string_tools import Parameter_Value
        Parameter_Value(new_row).force_type([list, CSV_Row])


        ids_are_same = self.is_id_of_rows_in_buffer_same_with_outside_row(new_row, raise_error_on_id_mismatch=raise_error_on_id_mismatch)

        if ids_are_same:
            self.append_row(new_row)

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
            value_separator_pattern(str): desired value to be used to separate cell values in merged cells.
                Can consist of multiple characters

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

        #for i, each_cell in enumerate(merged_row):
        #    if type(each_cell) != CSV_Cell:
        #        merged_row[i] = CSV_Cell(merged_row[i])

        merged_row = CSV_Row(merged_row)

        self.dataset = merged_row
        return self




    def is_id_of_rows_in_buffer_same_with_outside_row(self, outside_row, raise_error_on_id_mismatch=False):
        """
        Compares the self.id_of_current_rows_in_buffer with the value in the id cell of the inputted row. The index
        of id cell is assumed to be the same with the index of id cells in the buffer, and its value is gathered from
        self.id_index_of_id_column

        Args:
            outside_row(list or CSV_Row): Row that is being compared with the rows in buffer
            raise_error_on_id_mismatch(bool): If set to True, raises error instead of returning False in case of
                mismatch.

        Returns:
            Boolean

        Examples:
            >>> my_buffer = Row_Merge_Buffer(0)
            >>> my_buffer.append_as_first_row_and_reset_buffer(CSV_Row(['id23', 'a','b']))
            "id23: [['id23', 'a', 'b']]"
            >>> my_buffer.id_of_current_rows_in_buffer
            'id23'

            >>> # matching ids
            >>> my_buffer = Row_Merge_Buffer(0).append_as_first_row_and_reset_buffer(CSV_Row(['id23', 'a','b','c']))
            >>> my_row = CSV_Row(['id23', 'X', 'Y', 'Z'])
            >>> my_buffer.is_id_of_rows_in_buffer_same_with_outside_row(my_row)
            True

            >>> # non-matching ids
            >>> my_buffer = Row_Merge_Buffer(0).append_as_first_row_and_reset_buffer(CSV_Row(['id23', 'a','b','c']))
            >>> my_row = CSV_Row(['1003', 'X', 'Y', 'Z'])
            >>> my_buffer.is_id_of_rows_in_buffer_same_with_outside_row(my_row)
            False

            >>> # CSV_CSV_Row and list comparison
            >>> my_buffer = Row_Merge_Buffer(0).append_as_first_row_and_reset_buffer(CSV_Row(['id23', 'a','b','c']))
            >>> my_row = ['id23', 'X', 'Y', 'Z']
            >>> my_buffer.is_id_of_rows_in_buffer_same_with_outside_row(my_row)
            True

        """
        # REF TSOBMMWF2D: str()
        # TODO: [REF3] If str() around the two statements below are removed, live_clean_and_row_merge method gives error.
        # This seems to be an error related to failure in accurate comparison of CSV_Cell and str types.
        # This is a mostly hidden error, as CSV_Cell to str comparisons work fine in above examples.
        # Also see: REF1, REF2, REF3, REF 4

        id_in_buffer = str(self.id_of_current_rows_in_buffer)
        id_of_outside_row = str(outside_row[self.index_of_id_column])

        if id_in_buffer == id_of_outside_row:
            return True
        else:
            if raise_error_on_id_mismatch:
                raise ValueError ('ID "%s" of row "%s" does not match the current id of rows in Row_Merge_Buffer "%s"'
                                  '(comparison of "id_outside_row" and "id_in_buffer" returns: %s). '
                                  'Type of id_of_outside_row is %s, and type of id_in_buffer is %s.'
                                % (id_of_outside_row, outside_row, id_in_buffer, str(id_of_outside_row==id_in_buffer),
                                   type(id_of_outside_row), type(id_in_buffer)))
            else:
                return False