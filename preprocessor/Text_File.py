
#
# TODO: Unidecode (for chars) and then URI-encode (for non-url compatible symbols) to eliminate strange names in the output, such as:
# <http://clokman.com/ontologies/pure-uva#K¿hler_K> <http://clokman.com/ontologies/scientific-research#isAuthorOf> <http://clokman.com/ontologies/pure-uva#Proceedings_of_Console_IX> .

# TODO: Specific character elimination for cleaning
# > and < and patterns in output URIs:
# and '\' patterns from output strings


class Text_File():
    def __init__(self, input_file_path):
        """
        Examples:
            # get input and output file paths
            >>> my_clean_file = Text_File('test_data//problematic_characters_test.bib')
            >>> my_clean_file.input_file_path
            'test_data//problematic_characters_test.bib'
            >>> my_clean_file.cleaned_file_path
            'test_data//problematic_characters_test_cleaned.bib'

            # get input and output file paths in a nested directory
            >>> my_clean_file_in_subdir = Text_File('test_data//test_directory_for_nested_file_system_demonstration'\
                                                    '//file_in_nested_directory.bib')
            >>> my_clean_file_in_subdir.input_file_path
            'test_data//test_directory_for_nested_file_system_demonstration//file_in_nested_directory.bib'
            >>> my_clean_file_in_subdir.cleaned_file_path
            'test_data//test_directory_for_nested_file_system_demonstration//file_in_nested_directory_cleaned.bib'
        """
        from preprocessor.string_tools import File_Path

        # parse file name and directory
        self.file_path_object = File_Path(input_file_path)
        self.input_file_path = self.file_path_object.content
        self.input_file_name = self.file_path_object.file_name
        self.input_file_extension = self.file_path_object.file_extension
        self.directory_path = self.file_path_object.directory_path

        # store generate output path for cleaned file
        self.cleaned_file_path = self.directory_path + '//' + self.input_file_name + '_cleaned.' \
                                 + self.input_file_extension


    def preview(self, number_of_lines=1, print_separators_between_lines=False):
        """
        Examples:
            >>> # prep
            >>> # a csv from yasgui.org
            >>> my_text_file = Text_File('test_data//blazegraph_output_50.csv')

            >>> my_text_file.preview(number_of_lines=2)
            <BLANKLINE>
            Journal Article,<https://w3id.org/oc/corpus/br/44074>,Improving the Blood Pressure Control With the ProActive Attitude of Hypertensive Patients Seeking Follow-up Services,2016,Fang - Haiqing,Medicine,14,95,e3233--e3233,Ovid Technologies (Wolters Kluwer Health),10.1097/md.0000000000003233
        """
        file_length = self.get_no_of_lines_in_file()

        if file_length == 0:
            print('The file "%s" has 0 lines (it is empty).' % self.input_file_path)

        else:
            for i in range(1, number_of_lines + 1):
                if print_separators_between_lines:
                    print('----------------------------------LINE %s----------------------------------' % i)
                self.print_lines(i)



    def print_lines(self, start, end=None):
        """
        Prints a specified line interval in the TextFile without reading the whole file into memory.

        Args:
            start(int): An value that can take integers starting from 0
            end(int)

        Returns:
            Output to console

        Examples:
            >>> my_text_file = Text_File('test_data//problematic_characters_test.bib')
            >>> my_text_file.print_lines(17, 23)
            @book{a350c3826d05484cb863e77166d6e17b,
            title     = "Proceedings of Console IX",
            keywords  = "international",
            author    = "C. Czinglar and K. K¿hler and {van der Torre}, E.J. and K.E. Thrift and M. Zimmermann",
            year      = "2000",
            publisher = "Kluwer",
            }

            >>> my_text_file.print_lines(18)
            title     = "Proceedings of Console IX",
        """
        if not end:
            end = start

        length = end+1 - start  # adding +1 to end to make it include the specified value, instead including all before
        for i in range(0, length):
            line = self.get_line_at_position_from_file(start + i)
            print(line)


    def print_content(self):
        """
        Examples:
            >>> my_file = Text_File('test_data//small_text_file.txt')
            >>> my_file.print_content()
            This is the first line of of the file
            This is the second line of the file
        """
        file_length = self.get_no_of_lines_in_file()

        if file_length == 0:
            print('The file "%s" is empty (file length is "%s")' % (self.input_file_path, file_length))
        else:
            self.print_lines(1, file_length)


    def return_content(self):
        """
        Returns:
            str

        Examples:
            >>> my_file = Text_File('test_data//small_text_file.txt')
            >>> my_file.return_content()[:37]  # slicing is used because otherwise '/n' (i.e., 37th character in string)
            ...                                # is returned from file and this breaks testing.
            'This is the first line of of the file'

            >>> my_file.return_content()[38:]
            'This is the second line of the file'

            >>> # Assign file contents to variable
            >>> my_variable = my_file.return_content()
            >>> print(my_variable) # printing works normally without any problems with newline characters
            This is the first line of of the file
            This is the second line of the file
        """
        from preprocessor.string_tools import String

        string = ''

        with open(self.input_file_path, encoding='utf8') as file:
            for each_line in file:
                string = string + each_line

        return string


    def get_line_at_position_from_file(self, line_number):
        """
        Returns a specified line from the TextFile without reading the whole file into memory.

        Args:
            line_index(int): A value that can take integers starting from 0.

        Returns:
            String class object (created from string at line in file).

        See Also:
            CSV_File.get_line_at_position_from_file

        Examples:
            >>> # return first line of file
            >>> my_file = Text_File('test_data//example_merged_yasgui_1000.csv')
            >>> my_file.get_line_at_position_from_file(1)
            '"publication_type" , "journal_article" , "title" , "publication_year" , "author_name" , "journal_name" , "journal_issue_number" , "journal_volume_number" , "startEndPages" , "publisher_name" , "doi" , "cited_by_article" ,'

            >>> # return another line
            >>> my_file.get_line_at_position_from_file(122)
            '"Journal Article" , "https://w3id.org/oc/corpus/br/3448" , "Perioperative Myocardial Infarction" , "2009" , "Beattie - W. S. | Mosseri - M. | Jaffe - A. S. | Alpert - J. S." , "Circulation" , "22" , "119" , "2936--2944" , "Ovid Technologies (Wolters Kluwer Health)" , "10.1161/circulationaha.108.828228" , "https://w3id.org/oc/corpus/br/3426" ,'

            >>> # return last line
            >>> my_file.get_line_at_position_from_file(267)
            '"Journal Article" , "https://w3id.org/oc/corpus/br/3437" , "Myocardial Injury after Noncardiac Surgery" , "2014" , "Niebrzegowska - Edyta | Benton - Sally | Wragg - Andrew | Archbold - Andrew | Smith - Amanda | McAlees - Eleanor | Ramballi - Cheryl | MacDonald - Neil | Januszewska - Marta | Shariffuddin - Ina I. | Vasanthan - V. | Hashim - N. H. M. | Undok - A. Wahab | Ki - Ushananthini | Lai - Hou Yee | Ahmad - Wan Azman | Ackland - Gareth | Khan - Ahsun | Almeida - Smitha | Cherian - Joseph | Furruqh - Sultana | Abraham - Valsa | Paniagua - Pilar | Urrutia - Gerard | Maestre - Mari Luz | Santaló - Miquel | Gonzalez - Raúl | Font - Adrià | Martínez - Cecilia" , "Anesthesiology" , "3" , "120" , "564--578" , "Ovid Technologies (Wolters Kluwer Health)" , "10.1097/aln.0000000000000113" , "https://w3id.org/oc/corpus/br/3522 | https://w3id.org/oc/corpus/br/300243 | https://w3id.org/oc/corpus/br/3062326 | https://w3id.org/oc/corpus/br/3271454 | https://w3id.org/oc/corpus/br/3879533 | https://w3id.org/oc/corpus/br/4205354 | https://w3id.org/oc/corpus/br/5253819 | https://w3id.org/oc/corpus/br/6332120 | https://w3id.org/oc/corpus/br/7799424 | https://w3id.org/oc/corpus/br/8003885 | https://w3id.org/oc/corpus/br/8185544" ,'

            >>> # erroneous index number entered (0)
            >>> # return first line of file
            >>> my_file = Text_File('test_data//example_merged_yasgui_1000.csv')
            >>> try:
            ...     my_file.get_line_at_position_from_file(0) #  line_number cannot be 0
            ... except Exception as error_message:
            ...     print('Exception: ' + str(error_message))
            Exception: Parameter value must be a positive integer but is "0" of <class 'int'>.


            >>> # erroneous index number entered (too high)
            >>> try:
            ...     my_file.get_line_at_position_from_file(300) # there is no 300th line in the file
            ... except IndexError as error_message:
            ...     print('Exception: ' + str(error_message))
            Exception: Requested line number '300' does not exist in file.
        """
        from preprocessor.string_tools import String, Parameter_Value
        Parameter_Value(line_number).force_positive_integer()

        with open(self.input_file_path, encoding='utf8') as input_file:
            line = None

            for i, each_line in enumerate(input_file):
                current_iteration_step = i+1  # to align index numbers (starting from 0) and line numbers (start from 1)
                if current_iteration_step == line_number:
                    line = String(each_line)
                elif current_iteration_step > line_number:
                    break

            if line == None:
                raise IndexError("Requested line number '%s' does not exist in file." % line_number)

            # if not cleaned from '\n', comparisons and operations tend to be problematic
            # write to file with base print() function to get back the new line in the end
            line.clean_from_newline_characters()

            return line


    def get_no_of_lines_in_file(self):
        """
        Returns the number of lines in the file.

        Returns:
            int

        Examples:
            # takes a long time (5-10 secs) to run
            # >>> my_file = Text_File('test_data//big_test.ttl')
            # >>> my_file.get_no_of_lines_in_file()
            # 3667384

            >>> my_file = Text_File('test_data//blazegraph_output_1000.csv')
            >>> my_file.get_no_of_lines_in_file()
            1001

            >>> my_file = Text_File('test_data//demo_data.py')
            >>> my_file.get_no_of_lines_in_file()
            1

            >>> my_file = Text_File('test_data//empty_file.txt')
            >>> my_file.get_no_of_lines_in_file()
            0
        """
        with open(self.input_file_path, encoding='utf8') as file:
            i = -1  # for handling empty files
            for i, l in enumerate(file):
                pass
        return i + 1

    def clear_contents(self):
        """
        Examples:
            >>> my_text_file = Text_File('test_data//text_file_test.txt')
            >>> my_text_file.append_line('last log message')  # in case the file is already empty
            >>> my_text_file.clear_contents()
            >>> my_text_file.preview()
            The file "test_data//text_file_test.txt" has 0 lines (it is empty).
        """
        with open(self.input_file_path, mode='w', encoding='utf8') as log_file:
            log_file.write('')


    def append_line(self, input_string, timestamp=False):
        """
        Writes a line at the end of the Text_File.

        Examples:
            >>> # create a new log file and append lines to it (and clear contents if the file is not new)
            >>> my_text_file = Text_File('test_data//text_file_test.txt')
            >>> my_text_file.clear_contents()
            >>> my_text_file.append_line('1st line string')
            >>> my_text_file.append_line('2nd line string')
            >>> my_text_file.print_lines(1, 2)
            1st line string
            2nd line string
        """
        input_string = str(input_string)

        with open(self.input_file_path, mode='a', encoding='utf8') as text_file:
            text_file.write(input_string + '\n')



class Log_File(Text_File):

    def __init__(self, log_file_path='log.txt'):
        """
        Examples:
            >>> my_log_file = Log_File('test_data//log_file_test.txt')
        """
        Text_File.__init__(self, log_file_path)

    def append_line(self, input_string, timestamp=False):
        """
        Enters a line at the end of the Log_File.

        Examples:
            >>> # create a new log file and append lines to it (and clear contents if the file is not new)
            >>> my_log_file = Log_File('test_data//log_file_test.txt')
            >>> my_log_file.clear_contents()
            >>> my_log_file.append_line('1st log message')
            >>> my_log_file.append_line('2nd log message')
            >>> my_log_file.print_lines(1, 2)
            1st log message
            2nd log message

            # append a timestamped log entry
            # Timestamp output is dynamic; it should not be included in automatic tests
            # >>> my_log_file.append_line('3rd log message', timestamp=True)
            # >>> my_log_file.print_lines(1, 3)
            # Tue Feb 14 11:25:52 2018  -  3rd log message
        """
        import time

        input_string = str(input_string)

        with open(self.input_file_path, mode='a', encoding='utf8') as log_file:
            if timestamp:
                time_stamp_and_separator = time.ctime() + '  -  '
            else:
                time_stamp_and_separator = ''

            log_file.write(time_stamp_and_separator + input_string + '\n')
