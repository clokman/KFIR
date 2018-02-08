
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
            >>> my_clean_file.output_file_path
            'test_data//problematic_characters_test_cleaned.bib'

            # get input and output file paths in a nested directory
            >>> my_clean_file_in_subdir = Text_File('test_data//test_directory_for_nested_file_system_demonstration'\
                                                    '//file_in_nested_directory.bib')
            >>> my_clean_file_in_subdir.input_file_path
            'test_data//test_directory_for_nested_file_system_demonstration//file_in_nested_directory.bib'
            >>> my_clean_file_in_subdir.output_file_path
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
        self.output_file_path = self.directory_path + '//' + self.input_file_name + '_cleaned.' \
                                + self.input_file_extension

    def preview(self, number_of_lines=2, print_separators_between_lines=False):
        """
        Examples:
            >>> # prep
            >>> # a csv from yasgui.org
            >>> my_text_file = Text_File('test_data//blazegraph_output_50.csv')

            >>> my_text_file.preview()
            <BLANKLINE>
            Journal Article,<https://w3id.org/oc/corpus/br/44074>,Improving the Blood Pressure Control With the ProActive Attitude of Hypertensive Patients Seeking Follow-up Services,2016,Fang - Haiqing,Medicine,14,95,e3233--e3233,Ovid Technologies (Wolters Kluwer Health),10.1097/md.0000000000003233
        """
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

        start = start - 1  # because file lines start at 1, not 0 (e.g., 5th position is 4th line in file)
        length = end - start
        for i in range(0, length):
            line = self.get_line_at_position_from_file(start + i)
            print(line)


    def get_line_at_position_from_file(self, line_index):
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
        from preprocessor.string_tools import String

        with open(self.input_file_path, encoding='utf8') as input_file:
            line = None

            for i, each_line in enumerate(input_file):
                if i == line_index:
                    line = String(each_line)
                elif i > line_index:
                    break

            if line == None:
                raise IndexError("Requested line number '%s' does not exist in file." % line_index)

            # if not cleaned from '\n', comparisons and operations tend to be problematic
            # write to file with base print() function to get back the new line in the end
            line.clean_from_newline_characters()

            return line

    def clean_bibtex_file_and_output_cleaned_file(self, remove_unbalanced_entries = True, convert_to_ascii = True, patterns_to_replace={'': ''}):
        """

        Args:
            input_file_path:
            output_file_path:

        Examples:
            ### CLEANING ###############################################################################################

            >>> # init and preview targets
            >>> my_unclean_file = Text_File('test_data//problematic_characters_test.bib')
            >>> my_unclean_file.print_lines(46)
            title  = "Contribution to {"}Multimedia as bridges for language and literacy for young children{"}, SSSR:: Do multimedia in digital storybooks contribute to vocabulary development and which features are particularly supportive?",
            >>> my_unclean_file.print_lines(32)
            title     = "Test of CP invariance in Z ---> mu+ mu- gamma decay",
            >>> #remove unbalanced entries and clean specified patterns
            >>> my_unclean_file.clean_bibtex_file_and_output_cleaned_file(remove_unbalanced_entries=True,
            ...                                                           patterns_to_replace={'\{"\}': "'",
            ...                                                                '>': '',
            ...                                                                '<': ''})
            >>> # view results
            >>> my_cleaned_file = Text_File('test_data//problematic_characters_test_cleaned.bib')
            >>> my_cleaned_file.print_lines(22) # line 46 is now line 22 because unbalanced entries excluded in output
            title  = "Contribution to 'Multimedia as bridges for language and literacy for young children', SSSR:: Do multimedia in digital storybooks contribute to vocabulary development and which features are particularly supportive?",

            >>> # init and preview targets
            >>> my_unclean_file = Text_File('test_data//problematic_characters_test.bib')
            >>> my_unclean_file.print_lines(46)
            title  = "Contribution to {"}Multimedia as bridges for language and literacy for young children{"}, SSSR:: Do multimedia in digital storybooks contribute to vocabulary development and which features are particularly supportive?",
            >>> my_unclean_file.print_lines(32)
            title     = "Test of CP invariance in Z ---> mu+ mu- gamma decay",

            >>> #do NOT remove unbalanced entries but clean specified patterns
            >>> my_unclean_file.clean_bibtex_file_and_output_cleaned_file(remove_unbalanced_entries=False,
            ...                                                           patterns_to_replace={'\{"\}': "'",
            ...                                                                '>': '',
            ...                                                                '<': ''})
            >>> # view results
            >>> my_cleaned_file = Text_File('test_data//problematic_characters_test_cleaned.bib')
            >>> my_cleaned_file.print_lines(46) # line 46 is still in same place because unbalanced entries not excluded
            title  = "Contribution to 'Multimedia as bridges for language and literacy for young children', SSSR:: Do multimedia in digital storybooks contribute to vocabulary development and which features are particularly supportive?",
            >>> my_cleaned_file.print_lines(32)  # line 32 is still in same plac because unbalanced entries not excluded
            title     = "Test of CP invariance in Z --- mu+ mu- gamma decay",

            ### BALANCING ##############################################################################################

            >>> my_file = Text_File('test_data//problematic_characters_test.bib')

            >>> # unbalanced curly bracket in 'title' field
            >>> my_file.print_lines(1,12)
            % UNCLOSED CURLY BRACKET
            % This entry will cause an EOF error due to the unclosed curly bracket in the title field values.
            @book{a82caf00e1a143759c7f5543b6c84ea5,
            title     = "{Knowledge Representation for Health Care (AIME 2015 International Joint Workshop, KR4HC/ProHealth 2015)",
            author    = "D Riano and R. Lenz and S Miksch and M Peleg and M. Reichert and {ten Teije}, A.C.M.",
            year      = "2015",
            doi       = "10.1007/978-3-319-26585-8",
            isbn      = "9783319265841",
            series    = "LNAI",
            publisher = "Springer",
            number    = "9485",
            }

            >>> # unbalanced > in 'title' field.
            >>> my_file.print_lines(31,41)
            @article{79948f66cc82409a8978d14c9131346a,
            title     = "Test of CP invariance in Z ---> mu+ mu- gamma decay",
            author    = "M. Acciarri and O. Adriani and M. Aguilar-Benitez and S.P. Ahlen and J. Alcaraz and G. Alemanni and J. Allaby and A. Aloisio and F.L. Linde",
            year      = "1998",
            doi       = "10.1016/S0370-2693(98)00965-4",
            volume    = "436",
            pages     = "428--436",
            journal   = "Physics Letters B",
            issn      = "0370-2693",
            publisher = "Elsevier",
            }

            >>> # faulty entry is not included in the cleaned file. Now there is another entry in its place.
            >>> my_file.clean_bibtex_file_and_output_cleaned_file()
            >>> my_cleaned_file = Text_File('test_data//problematic_characters_test_cleaned.bib')
            >>> my_cleaned_file.print_lines(1,7)
            @book{a350c3826d05484cb863e77166d6e17b,
            title     = "Proceedings of Console IX",
            keywords  = "international",
            author    = "C. Czinglar and K. K?hler and {van der Torre}, E.J. and K.E. Thrift and M. Zimmermann",
            year      = "2000",
            publisher = "Kluwer",
            }

            >>> # faulty entry is not included in the cleaned file. Now there is another entry in its place.
            >>> my_cleaned_file.print_lines(29,42)
            @article{96d9add3e2f44e8abbf030170689bc30,
            title     = "When and where did the great recession erode the support of democracy?{"}",
            abstract  = "It is likely that ten years of economic crisis have eroded the support of democracy in Europe. But how much? The existing research is divided on this issue. Some claim that the degree of satisfaction with democracy has declined across the whole of Europe during the Great Recession. Other researchers have found no empirical evidence that the support of democracy as a core value has declined across Europe. They claim that merely the specific support has decreased in some countries. This article will use the data from the European Social Survey to verify both claims. It shows that the Great Recession did not lead to a legitimacy crisis of European democracies and that the diffuse support of democracy remains high in most regions. The degree to which the specific support of democracy has been weakened is moderated by the type of welfare regime. In countries where the economic crisis did strike hard and the welfare state is weakly developed, the support of democracy has dropped dramatically. This outcome takes a middle position between two extremes in the ongoing academic debate on the support of democracy. Both positions regarding the increase or decrease of support of and satisfaction with democracy are in need of more nuance by taking into account the impact of welfare regimes. Existing research often assumes a uniform European context that shows either increasing or decreasing levels of satisfaction with democracy. Our research has shown that the response of citizens to the Great Recession has been influenced by the welfare regime.",
            keywords  = "Democracy, Economic crisis, Europe, Welfare state, Survey data, Quantitative methods",
            author    = "P.J.M. Pennings",
            year      = "2017",
            month     = "3",
            volume    = "17",
            pages     = "81--103",
            journal   = "Zeitschrift fur Vergleichende Politikwissenschaft",
            issn      = "1865-2646",
            publisher = "Springer Verlag",
            number    = "1",
            }


            ### ASCII CONVERSION #######################################################################################
            >>> my_file = Text_File('test_data//problematic_characters_test.bib')

            >>> # non-ascii characters in titles
            >>> my_file.print_lines(125)
            title     = "Networks of · / G/ ∞ queues with shot-noise-driven arrival intensities",
            >>> my_file.print_lines(142)
            title     = "Search for heavy resonances decaying to a $Z$ boson and a photon in $pp$ collisions at $\sqrt{s}=13$ TeV with the ATLAS detector",
            >>> my_file.print_lines(156)
            title    = "In pursuit of lepton flavour violation: A search for the τ-> μγγ decay with atlas at √s=8 TeV",
            >>> my_file.print_lines(166)
            title     = "Measurement of the CP-violating phase ϕsand the Bs0meson decay width difference with Bs0→ J/ψϕ decays in ATLAS",

            >>> my_file.clean_bibtex_file_and_output_cleaned_file(patterns_to_replace={'>': '', '<': ''})
            >>> my_cleaned_file = Text_File('test_data//problematic_characters_test_cleaned.bib')
            >>> my_cleaned_file.print_lines(95)
            title     = "Networks of * / G/ [?] queues with shot-noise-driven arrival intensities",
            >>> my_cleaned_file.print_lines(111)
            title     = "Search for heavy resonances decaying to a $Z$ boson and a photon in $pp$ collisions at $\sqrt{s}=13$ TeV with the ATLAS detector",
            >>> my_cleaned_file.print_lines(124)
            title    = "In pursuit of lepton flavour violation: A search for the t- mgg decay with atlas at [?]s=8 TeV",

        """
        # This command likely cannot read some files in which certain unicode characters exist due to an encoding bug.
        # See: http://www.i18nqa.com/debug/bug-double-conversion.html
        from preprocessor.string_tools import String
        from preprocessor.ListData import ListBuffer
        from unidecode import unidecode

        with open(self.input_file_path, encoding="utf8") as input_file:
            with open(self.output_file_path, mode='w', encoding="utf8") as output_file:

                buffer = ListBuffer()

                for current_line in input_file:
                    current_line = String(current_line).\
                        clean_from_newline_characters().\
                        replace_patterns(patterns_to_replace)

                    if convert_to_ascii:
                        current_line = String(unidecode(current_line.content))

                        # TODO: add character decode and perhaps also uridecode here

                    if remove_unbalanced_entries:
                        # new entry line
                        if current_line.is_line_type('bibtex', 'start of entry'):

                            # this is the first entry ever (just append to buffer)
                            if buffer.is_empty:
                                buffer.append_row(current_line.content)

                            # this is NOT the first entry ever (write buffer to output if balanced, then re-initiate)
                            else:
                                if buffer.is_each_row_balanced(exclude_special_rows_of_syntax='bibtex'):
                                    for each_buffer_line in buffer.dataset:
                                        print(each_buffer_line, file=output_file)
                                else:
                                    # currently, when an unbalanced row is detected, the entry it belongs to is simply
                                    # not written to the output file. If a more precise procedure (e.g., an unbalanced
                                    # character removal algorithm) is to be added, it should be added under this 'else'.
                                    pass
                                buffer.clear_all().\
                                    append_row(current_line.content)

                        # regular line (just append to buffer)
                        elif not current_line.is_line_type('bibtex', 'start of entry') \
                                and not current_line.is_line_type('bibtex', 'comment'):
                            buffer.append_row(current_line.content)

                    else:  # if no balancing is being done
                        print(current_line, file=output_file)

    # def clean(self, patterns_to_replace={'': ''}):
    #     """
    #
    #     Args:
    #         patterns_to_replace(dict): A dictionary of patterns that consists of entries in 'target: replacement'
    #             format.
    #
    #     Returns:
    #
    #     Examples:
    #         >>> my_unclean_file = Text_File('test_data//problematic_characters_test.bib')
    #         >>> my_unclean_file.print_lines(46)
    #         title  = "Contribution to {"}Multimedia as bridges for language and literacy for young children{"}, SSSR:: Do multimedia in digital storybooks contribute to vocabulary development and which features are particularly supportive?",
    #         >>> my_unclean_file.print_lines(32)
    #         title     = "Test of CP invariance in Z ---> mu+ mu- gamma decay",
    #
    #         >>> my_unclean_file.clean(patterns_to_replace={'\{"\}': "'",
    #         ...                                            '>': '',
    #         ...                                            '<': ''})
    #
    #         >>> my_cleaned_file = Text_File('test_data//problematic_characters_test_cleaned.bib')
    #         >>> my_cleaned_file.print_lines(46)
    #         title  = "Contribution to 'Multimedia as bridges for language and literacy for young children', SSSR:: Do multimedia in digital storybooks contribute to vocabulary development and which features are particularly supportive?",
    #         >>> my_cleaned_file.print_lines(32)
    #         title     = "Test of CP invariance in Z --- mu+ mu- gamma decay",
    #     """
    #     from preprocessor.string_tools import String
    #
    #     with open(self.input_file_path) as input_file:
    #         with open(self.output_file_path, mode='w') as output_file:
    #             for each_line in input_file:
    #                 each_line = String(each_line).\
    #                     clean_from_newline_characters().\
    #                     replace_patterns(patterns_to_replace)
    #
    #                     #each_line.split()
    #
    #                 # convert String object to str
    #                 print(each_line.content, file=output_file)
    #
    #