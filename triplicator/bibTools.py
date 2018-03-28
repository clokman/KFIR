from preprocessor.Text_File import Text_File, Log_File


class Bibtex_File(Text_File):
    """
    Examples:
        >>> # Instantiation
        >>> my_bibtex_file = Bibtex_File('example_data//vu_25_test.bib')

        >>> # Invalid formatting of input directory
        >>> try:
        ...     #  input directory path cannot contain single slashes
        ...     my_bibtex_file = Bibtex_File('example_data/vu_25_test.bib')
        ... except Exception as error_message:
        ...     print('Exception: ' + str(error_message))
        Exception: Invalid path: Path contains "/" as directory separator, and should be replaced with "//".
    """
    def __init__(self, input_file_path):
        Text_File.__init__(self, input_file_path)

        self.no_of_nonparsable_entries_due_to_unknown_reason = 0
        self.no_of_unbalanced_entries_skipped = 0


    def convert_to_ttl(self, desired_version_suffix, desired_source_bibliography_name, output_directory='',
                       show_progress_bar=True):
        """
        Takes a bib file and outputs a .ttl file.

        Args:
            desired_version: Version name to be added ttl file that will be outputted
                (e.g., my_bibliography.bib --> my_bibliography_2.1.ttl)
            desired_source_label: The bibliography source information that be attached to each entry
                (e.g., ex:my_article ==> ex:hasOriginBibliography ==> ex:opencitations)

        Returns:
            Nothing

        Also see:
            long_tests()

        Examples:
            >>> my_bibtex_file = Bibtex_File('example_data//vu_25_test.bib')
            >>> my_bibtex_file.convert_to_ttl(desired_version_suffix='0.0.test', desired_source_bibliography_name='arbitrary_label',
            ...                               output_directory='example_data//example_output_dir',
            ...                               show_progress_bar=False)
            Cleaning of "example_data//vu_25_test.bib" started
            Cleaning of "example_data//vu_25_test.bib" finished
            Parsing of example_data//vu_25_test_cleaned.bib started
            pybtex package is parsing using bibtex.Parser()...
            pybtex package finished parsing
            Calculating file length...
            <BLANKLINE>
            <BLANKLINE>
            ---------------------------------------------------------------------------------------------------
            example_data//vu_25_test_cleaned.bib parsed and imported as Bibliography object.
            <BLANKLINE>
            Fields added to the parsed the Bibliography object:
            {'b_author_labels': 2,
             'b_authors': 2,
             'b_document': 2,
             'b_document_label': 2,
             'b_note': 2,
             'b_publication_year': 2,
             'b_pure_bibliography_id': 2,
             'b_type': 2}
            <BLANKLINE>
            <BLANKLINE>
            Calculating the length of the Triples object
            Writing of the triples to file "example_data//example_output_dir//vu_25_test_0.0.test.ttl" has started
            Success: 53 triples were written to "example_data//example_output_dir//vu_25_test_0.0.test.ttl"
            These items were skipped due to errors (0 items):
            <BLANKLINE>
            A log of the operation is kept in "log.txt"

            >>> my_ttl_file = Text_File('example_data//example_output_dir//vu_25_test_0.0.test.ttl')
            >>> my_ttl_file.preview(50)
            <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#isAuthorOf> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#hasAuthor> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#isPublishedOn> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#isPublishedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#isPublishedOnYear> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#isPublishedOnMonth> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#isPublishedOnDate> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#hasDOI> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#hasISSN> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#hasISBN> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#isChapterOf> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://www.w3.org/2000/01/rdf-schema#label> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#hasTopic> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#hasAbstract> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://www.w3.org/2002/07/owl#equivalentClass> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#Topic> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> .
            <http://clokman.com/kfir/resource#arbitrary_label> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> .
            <http://clokman.com/kfir/resource#arbitrary_label> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/resource#Bibliography> .
            <http://clokman.com/kfir/ontology#JournalArticle> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> .
            <http://clokman.com/kfir/ontology#Book> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> .
            <http://clokman.com/kfir/ontology#BookChapter> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> .
            <http://clokman.com/kfir/ontology#Miscellaneous> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> .
            <http://clokman.com/kfir/resource#Geloof_en_rechtvaardiging> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
            <http://clokman.com/kfir/ontology#Misc> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
            <http://clokman.com/kfir/resource#Geloof_en_rechtvaardiging> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Misc> .
            <http://clokman.com/kfir/resource#Geloof_en_rechtvaardiging> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#arbitrary_label> .
            <http://clokman.com/kfir/resource#Geloof_en_rechtvaardiging> <http://www.w3.org/2000/01/rdf-schema#label> "Geloof en rechtvaardiging"@en .
            <http://clokman.com/kfir/resource#Agteresch_HJ> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#Geloof_en_rechtvaardiging> .
            <http://clokman.com/kfir/resource#Geloof_en_rechtvaardiging> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#Agteresch_HJ> .
            <http://clokman.com/kfir/resource#Agteresch_HJ> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
            <http://clokman.com/kfir/resource#Agteresch_HJ> <http://www.w3.org/2000/01/rdf-schema#label> "Agteresch, HJ"@en .
            <http://clokman.com/kfir/resource#Geloof_en_rechtvaardiging> <http://clokman.com/kfir/ontology#isPublishedOnYear> "2023" .
            <http://clokman.com/kfir/resource#Gereformeerde_katholiciteit_in_de_zeventiende_eeuw> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
            <http://clokman.com/kfir/ontology#Misc> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
            <http://clokman.com/kfir/resource#Gereformeerde_katholiciteit_in_de_zeventiende_eeuw> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Misc> .
            <http://clokman.com/kfir/resource#Gereformeerde_katholiciteit_in_de_zeventiende_eeuw> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#arbitrary_label> .
            <http://clokman.com/kfir/resource#Gereformeerde_katholiciteit_in_de_zeventiende_eeuw> <http://www.w3.org/2000/01/rdf-schema#label> "Gereformeerde katholiciteit in de zeventiende eeuw"@en .
            <http://clokman.com/kfir/resource#Hartevelt_LDA> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#Gereformeerde_katholiciteit_in_de_zeventiende_eeuw> .
            <http://clokman.com/kfir/resource#Gereformeerde_katholiciteit_in_de_zeventiende_eeuw> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#Hartevelt_LDA> .
            <http://clokman.com/kfir/resource#Hartevelt_LDA> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
            <http://clokman.com/kfir/resource#Hartevelt_LDA> <http://www.w3.org/2000/01/rdf-schema#label> "Hartevelt, LDA"@en .
            <http://clokman.com/kfir/resource#Gereformeerde_katholiciteit_in_de_zeventiende_eeuw> <http://clokman.com/kfir/ontology#isPublishedOnYear> "2021" .
            <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#isAuthorOf> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#hasAuthor> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#isPublishedOn> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
            <http://clokman.com/kfir/ontology#isPublishedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .

            >>> # Invalid formatting of output directory
            >>> my_bibtex_file = Bibtex_File('example_data//vu_25_test_0.0.test.bib')
            >>> try:
            ...     #  output directory path cannot contain single slashes
            ...     my_bibtex_file.convert_to_ttl(desired_version_suffix='0.0-test', desired_source_bibliography_name='vu',
            ...                                   output_directory='example_data/example_output_dir')
            ... except Exception as error_message:
            ...     print('Exception: ' + str(error_message))
            Exception: Invalid path: Path contains "/" as directory separator, and should be replaced with "//".

            >>> #  a string with spaces entered as value for desired_source_bibliography_name parameter
            >>> my_bibtex_file = Bibtex_File('example_data//vu_25_test.bib')
            >>> my_bibtex_file.convert_to_ttl(desired_version_suffix='v0.0.test2',
            ...                               desired_source_bibliography_name='bib name with spaces',
            ...                               output_directory='example_data//example_output_dir',
            ...                               show_progress_bar=False)
            Cleaning of "example_data//vu_25_test.bib" started
            Cleaning of "example_data//vu_25_test.bib" finished
            Parsing of example_data//vu_25_test_cleaned.bib started
            pybtex package is parsing using bibtex.Parser()...
            pybtex package finished parsing
            Calculating file length...
            <BLANKLINE>
            <BLANKLINE>
            ---------------------------------------------------------------------------------------------------
            example_data//vu_25_test_cleaned.bib parsed and imported as Bibliography object.
            <BLANKLINE>
            Fields added to the parsed the Bibliography object:
            {'b_author_labels': 2,
             'b_authors': 2,
             'b_document': 2,
             'b_document_label': 2,
             'b_note': 2,
             'b_publication_year': 2,
             'b_pure_bibliography_id': 2,
             'b_type': 2}
            <BLANKLINE>
            <BLANKLINE>
            Calculating the length of the Triples object
            Writing of the triples to file "example_data//example_output_dir//vu_25_test_v0.0.test2.ttl" has started
            Success: 53 triples were written to "example_data//example_output_dir//vu_25_test_v0.0.test2.ttl"
            These items were skipped due to errors (0 items):
            <BLANKLINE>
            A log of the operation is kept in "log.txt"
            >>> my_ttl_file = Text_File('example_data//example_output_dir//vu_25_test_v0.0.test2.ttl')
            >>> my_ttl_file.print_lines(29)
            <http://clokman.com/kfir/resource#Geloof_en_rechtvaardiging> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#bib_name_with_spaces> .

            >>> # see bottom of this file for longer tests

        """
        import os
        from unidecode import unidecode
        from preprocessor.string_tools import Parameter_Value, File_Path, String
        from triplicator.rdfTools import Triples, RDF_File
        from triplicator.bibTools import Bibliography  # refers to own module, but not redundant—required by force_type
                                                       # method used in Triples.import_bibliography_object()

        log_file = Log_File('log.txt')
        log_file.clear_contents()

        # Patterns to clean from bib files
        pattern_replacements_dictionary = {
            '<': '--',
            '>': '--',
            '\{"\}': "'",  # to replace {"} with '
            '\\\\': '--',  # to remove '\' in expressions such as '\sqrt{s}' and rogue '\'s.  unsure why '\\' does not work
            '“': "'",
            '”': "'",
            '’': "'"
        }

        # Error handling for output_directory and desired_version_suffix parameters
        Parameter_Value(output_directory).force_type(str)
        File_Path(output_directory).raise_error_if_single_slash()
        Parameter_Value(desired_version_suffix).force_type(str)

        # Error handling and cleaning of 'desired_source_bibliography_name' parameter
        Parameter_Value(desired_source_bibliography_name).force_type(str)
        # TODO: The following parameter cleaning procedure should be extracted as a method of String class.
        # the cleaning is done manually here as this item is injected by Triples() instance, and thus, is not
        # cleaned with bibliography cleaning process beforehand. As a result, if a parameter with illegal characters
        # is entered and had not been cleaned as below, this could lead to malformed URI's or unreadable ttl files.
        desired_source_bibliography_name = String(desired_source_bibliography_name). \
            clean_from_newline_characters(). \
            replace_patterns(pattern_replacements_dictionary).\
            replace_patterns({' ': "_"})  # spaces are not cleared by default for all bibliography entries such as labels,
                                          # so it must be taken care of individually here

        desired_source_bibliography_name.clean_from_non_ascii_characters()
        desired_source_bibliography_name.clean_from_non_uri_safe_characters()
        desired_source_bibliography_name = desired_source_bibliography_name.content  # convert String to str

        ### Clean the bib file ###
        self.clean_bibtex_file_and_write_output_to_another_file(patterns_to_replace=pattern_replacements_dictionary,
                                                                show_progress_bar=show_progress_bar)

        ### Parse the bib file ###
        bibliography = Bibliography()
        bibliography.importBibtex(self.cleaned_file_path, show_progress_bar=show_progress_bar)

        ### Convert to n3 format ###
        triples = Triples()
        triples.import_bibliography_object(bibliography,
                                           desired_source_bibliography_name=desired_source_bibliography_name,
                                           show_progress_bar=show_progress_bar)

        ### Write to .ttl file
        if output_directory and (not os.path.exists(output_directory)):
            os.makedirs(output_directory)

        if output_directory:
            output_directory_to_prepend = output_directory + '//'
        else:
            output_directory_to_prepend = ''

        ttl_file_path = output_directory_to_prepend + self.input_file_name + '_' + desired_version_suffix + '.ttl'
        ttl_file = RDF_File(ttl_file_path)
        ttl_file.write_triples_to_file(triples, show_progress_bar=show_progress_bar)


    def clean_bibtex_file_and_write_output_to_another_file(self, convert_to_ascii=True, patterns_to_replace={'': ''},
                                                           show_progress_bar=False):
        """

        Examples:
            ### CLEANING ###############################################################################################

            >>> # init and preview targets
            >>> my_unclean_file = Bibtex_File('example_data//problematic_characters_test.bib')
            >>> my_unclean_file.print_lines(46)
            title  = "Contribution to {"}Multimedia as bridges for language and literacy for young children{"}, SSSR:: Do multimedia in digital storybooks contribute to vocabulary development and which features are particularly supportive?",
            >>> my_unclean_file.print_lines(32)
            title     = "Test of CP invariance in Z ---> mu+ mu- gamma decay",
            >>> #remove unbalanced entries and clean specified patterns
            >>> my_unclean_file.clean_bibtex_file_and_write_output_to_another_file(patterns_to_replace={'\{"\}': "'",
            ...                                                                '>': '',
            ...                                                                '<': ''})
            Cleaning of "example_data//problematic_characters_test.bib" started
            Cleaning of "example_data//problematic_characters_test.bib" finished
            >>> # view results
            >>> my_cleaned_file = Bibtex_File('example_data//problematic_characters_test_cleaned.bib')
            >>> my_cleaned_file.print_lines(22) # line 46 is now line 22 because unbalanced entries excluded in output
            title  = "Contribution to 'Multimedia as bridges for language and literacy for young children', SSSR:: Do multimedia in digital storybooks contribute to vocabulary development and which features are particularly supportive?",

            >>> # init and preview targets
            >>> my_unclean_file = Bibtex_File('example_data//problematic_characters_test.bib')
            >>> my_unclean_file.print_lines(46)
            title  = "Contribution to {"}Multimedia as bridges for language and literacy for young children{"}, SSSR:: Do multimedia in digital storybooks contribute to vocabulary development and which features are particularly supportive?",
            >>> my_unclean_file.print_lines(32)
            title     = "Test of CP invariance in Z ---> mu+ mu- gamma decay",

            >>> # This test disabled because currently all unbalanced entries are being cleaned
            >>> ##do NOT remove unbalanced entries but clean specified patterns
            >>> #my_unclean_file.clean_bibtex_file_and_write_output_to_another_file(remove_unbalanced_entries=False,
            #...                                                           patterns_to_replace={'\{"\}': "'",
            #...                                                                '>': '',
            #...                                                                '<': ''})
            >>> # view results
            >>> #my_cleaned_file = Text_File('example_data//problematic_characters_test_cleaned.bib')
            >>> #my_cleaned_file.print_lines(46) # line 46 is still in same place because unbalanced entries not excluded
            title  = "Contribution to 'Multimedia as bridges for language and literacy for young children', SSSR:: Do multimedia in digital storybooks contribute to vocabulary development and which features are particularly supportive?",
            >>> #my_cleaned_file.print_lines(32)  # line 32 is still in same plac because unbalanced entries not excluded
            title     = "Test of CP invariance in Z --- mu+ mu- gamma decay",

            ### BALANCING ##############################################################################################

            >>> my_file = Bibtex_File('example_data//problematic_characters_test.bib')

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
            >>> my_file.clean_bibtex_file_and_write_output_to_another_file()
            Cleaning of "example_data//problematic_characters_test.bib" started
            Cleaning of "example_data//problematic_characters_test.bib" finished
            >>> my_cleaned_file = Bibtex_File('example_data//problematic_characters_test_cleaned.bib')
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
            >>> my_file = Bibtex_File('example_data//problematic_characters_test.bib')

            >>> # non-ascii characters in titles
            >>> my_file.print_lines(125)
            title     = "Networks of · / G/ ∞ queues with shot-noise-driven arrival intensities",
            >>> my_file.print_lines(142)
            title     = "Search for heavy resonances decaying to a $Z$ boson and a photon in $pp$ collisions at $\sqrt{s}=13$ TeV with the ATLAS detector",
            >>> my_file.print_lines(156)
            title    = "In pursuit of lepton flavour violation: A search for the τ-> μγγ decay with atlas at √s=8 TeV",
            >>> my_file.print_lines(166)
            title     = "Measurement of the CP-violating phase ϕsand the Bs0meson decay width difference with Bs0→ J/ψϕ decays in ATLAS",

            >>> my_file.clean_bibtex_file_and_write_output_to_another_file(patterns_to_replace={'>': '', '<': ''})
            Cleaning of "example_data//problematic_characters_test.bib" started
            Cleaning of "example_data//problematic_characters_test.bib" finished
            >>> my_cleaned_file = Bibtex_File('example_data//problematic_characters_test_cleaned.bib')
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
        from meta.consoleOutput import ConsoleOutput

        current_progress = 0
        maximum_progress = self.get_no_of_lines_in_file()

        console = ConsoleOutput(log_file_path='log.txt')
        console.log_message(('Cleaning of "%s" started' % self.input_file_path),
                            add_timestamp_in_file=True)


        with open(self.input_file_path, encoding="utf8") as input_file:
            with open(self.cleaned_file_path, mode='w', encoding="utf8") as output_file:

                buffer = ListBuffer()

                for current_line in input_file:
                    current_line = String(current_line).\
                        clean_from_newline_characters().\
                        replace_patterns(patterns_to_replace)

                    if convert_to_ascii:
                        current_line.clean_from_non_ascii_characters()

                    # new entry line
                    if current_line.is_line_type('bibtex', 'start of entry'):

                        # this is the first entry ever (just append to buffer)
                        if buffer.is_empty:
                            buffer.append_row(current_line.content)

                        # this is NOT the first entry ever (write buffer to output if balanced, then re-initiate)
                        else:
                            if buffer.is_each_row_balanced(exclude_special_rows_of_syntax='bibtex'):
                                if buffer.is_parsable('bibtex'):
                                    for each_buffer_line in buffer.dataset:
                                        print(each_buffer_line, file=output_file)
                                else:
                                    self.no_of_nonparsable_entries_due_to_unknown_reason += 1
                            else:
                                # currently, when an unbalanced row is detected, the entry it belongs to is simply
                                # not written to the output file. If a more precise procedure (e.g., an unbalanced
                                # character removal algorithm) is to be added, it should be added under this 'else'.
                                self.no_of_unbalanced_entries_skipped += 1

                            buffer.clear_all().\
                                append_row(current_line.content)

                    # regular line (just append to buffer)
                    elif not current_line.is_line_type('bibtex', 'start of entry') \
                            and not current_line.is_line_type('bibtex', 'comment'):
                        buffer.append_row(current_line.content)

                    # reporting
                    if show_progress_bar:  # show_progress_bar is False by default to prevent overly long test outputs
                        console.print_current_progress(current_progress, maximum_progress,
                                                          'Cleaning %s' % self.input_file_path)
                        current_progress += 1

        console.log_message(('Cleaning of "%s" finished' % self.input_file_path), add_timestamp_in_file=True)


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

        instance.no_of_existing_fields_enriched_in_last_operation = 0
        instance.no_of_fields_added_in_last_operation = 0
        instance.no_of_entries_enriched_in_last_operation = 0
        instance.no_of_entries_added_in_last_operation = 0

        instance.log_file_path = 'log.txt'

    ###################################################################################################################
    ############################################### IMPORT FUNCTIONS ##################################################
    ###################################################################################################################

    def importBibtex(instance, path_of_file_to_import, conversion_arguments_list='bib_default', show_progress_bar=False):
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


        Returns:
            Nothing; modifies the object it is called from.

        Examples:
            >>> # Import a .bib object as Bibliography object
            >>> my_bib = Bibliography()
            >>> my_bib.importBibtex('example_data//test.bib')
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
             'b_pure_bibliography_id': 4,
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
                # CAUTION: If any changes are made to 'desired_field_name's, the same changes should be made to
                # Bibliography.importCsv() > conversion_arguments_list > 'open citations' > 'desired_field_name' column
                # [target_field_value in existing data,     formatting_algorithm,               desired_field_name in new object]
                ['each_pybtex_entry.type',                  'capitalize_first_letter',          'b_type'],
                ['each_pybtex_entry_id',                    'none',                             'b_pure_bibliography_id'],
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
                  show_progress_bar=False
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
                CSV_Bibliography class in csvImporter module.

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
            >>> # import a csv file
            >>> oc_bibliography = Bibliography()
            >>> oc_bibliography.importCsv(path_of_file_to_import='example_data//oc_query_2.2_results_short_sample.csv',
            ...                           csv_delimiter_character=',',
            ...                           field_value_list_separator=' | ',
            ...                           id_column_header='journal_article',
            ...                           conversion_arguments_list='open citations',
            ...                           cleaning_algorithm='default')
            Parsing of "example_data//oc_query_2.2_results_short_sample.csv" started
            Conversion from ListData to Bibliography object started
            Conversion completed. 3 out of 3 ListData rows converted to Bibliography object entries
            <BLANKLINE>
            Formatting of Bibliography entries started
            "example_data//oc_query_2.2_results_short_sample.csv" parsed and imported into Bibliography object in memory
            <BLANKLINE>
            Number of fields in the parsed bibliography:
            {'b_author_labels': 3,
             'b_authors': 3,
             'b_cited': 3,
             'b_cited_by': 3,
             'b_document': 3,
             'b_document_label': 3,
             'b_doi': 3,
             'b_issue_number': 3,
             'b_journal': 3,
             'b_journal_label': 3,
             'b_open_citations_id': 3,
             'b_pages': 2,
             'b_pmid': 3,
             'b_publication_year': 3,
             'b_publisher': 3,
             'b_publisher_label': 3,
             'b_type': 3,
             'b_url': 3,
             'b_volume': 3}

            >>> oc_bibliography.preview(2)
            <BLANKLINE>
            ----------------------------------ENTRY 1----------------------------------
            ('https://w3id.org/oc/corpus/br/362418',
             {'b_author_labels': ['Zetterqvist, M'],
              'b_authors': ['Zetterqvist_M'],
              'b_cited': ['https://w3id.org/oc/corpus/br/37961',
                          'https://w3id.org/oc/corpus/br/38250',
                          'https://w3id.org/oc/corpus/br/135448',
                          'https://w3id.org/oc/corpus/br/135458',
                          'https://w3id.org/oc/corpus/br/177639',
                          'https://w3id.org/oc/corpus/br/177648',
                          'https://w3id.org/oc/corpus/br/177653',
                          'https://w3id.org/oc/corpus/br/177661',
                          'https://w3id.org/oc/corpus/br/177774',
                          'https://w3id.org/oc/corpus/br/362419',
                          'https://w3id.org/oc/corpus/br/362426',
                          'https://w3id.org/oc/corpus/br/362438',
                          'https://w3id.org/oc/corpus/br/607811',
                          'https://w3id.org/oc/corpus/br/1270766',
                          'https://w3id.org/oc/corpus/br/1560911',
                          'https://w3id.org/oc/corpus/br/1794850',
                          'https://w3id.org/oc/corpus/br/1881397',
                          'https://w3id.org/oc/corpus/br/2258672',
                          'https://w3id.org/oc/corpus/br/2907029',
                          'https://w3id.org/oc/corpus/br/2907034',
                          'https://w3id.org/oc/corpus/br/2907035',
                          'https://w3id.org/oc/corpus/br/2907042',
                          'https://w3id.org/oc/corpus/br/2907056',
                          'https://w3id.org/oc/corpus/br/3346205',
                          'https://w3id.org/oc/corpus/br/3567493',
                          'https://w3id.org/oc/corpus/br/3567495',
                          'https://w3id.org/oc/corpus/br/3949890',
                          'https://w3id.org/oc/corpus/br/5106137',
                          'https://w3id.org/oc/corpus/br/5441063',
                          'https://w3id.org/oc/corpus/br/5441066',
                          'https://w3id.org/oc/corpus/br/5441085',
                          'https://w3id.org/oc/corpus/br/5656230',
                          'https://w3id.org/oc/corpus/br/6060536',
                          'https://w3id.org/oc/corpus/br/6063037',
                          'https://w3id.org/oc/corpus/br/6449521',
                          'https://w3id.org/oc/corpus/br/6486152',
                          'https://w3id.org/oc/corpus/br/6486162',
                          'https://w3id.org/oc/corpus/br/6919305',
                          'https://w3id.org/oc/corpus/br/6919323',
                          'https://w3id.org/oc/corpus/br/7558746',
                          'https://w3id.org/oc/corpus/br/7560541',
                          'https://w3id.org/oc/corpus/br/7560644',
                          'https://w3id.org/oc/corpus/br/7560645',
                          'https://w3id.org/oc/corpus/br/7560646',
                          'https://w3id.org/oc/corpus/br/7560647',
                          'https://w3id.org/oc/corpus/br/7560648',
                          'https://w3id.org/oc/corpus/br/7560651',
                          'https://w3id.org/oc/corpus/br/7560652',
                          'https://w3id.org/oc/corpus/br/7560653',
                          'https://w3id.org/oc/corpus/br/7560654',
                          'https://w3id.org/oc/corpus/br/7560655',
                          'https://w3id.org/oc/corpus/br/7560656',
                          'https://w3id.org/oc/corpus/br/7560657',
                          'https://w3id.org/oc/corpus/br/7560658',
                          'https://w3id.org/oc/corpus/br/7560659',
                          'https://w3id.org/oc/corpus/br/7560660',
                          'https://w3id.org/oc/corpus/br/7560661',
                          'https://w3id.org/oc/corpus/br/7560662',
                          'https://w3id.org/oc/corpus/br/7560663',
                          'https://w3id.org/oc/corpus/br/7560664',
                          'https://w3id.org/oc/corpus/br/7560665',
                          'https://w3id.org/oc/corpus/br/7560666'],
              'b_cited_by': 'https://w3id.org/oc/corpus/br/362415',
              'b_document': 'The_DSM-5_diagnosis_of_nonsuicidal_self-injury_disorder-a_review_of_the_empirical_literature',
              'b_document_label': 'The DSM-5 diagnosis of nonsuicidal self-injury '
                                  'disorder-a review of the empirical literature',
              'b_doi': '10.1186/s13034-015-0062-7',
              'b_issue_number': '1',
              'b_journal': 'Child_and_Adolescent_Psychiatry_and_Mental_Health-Child_Adolesc_Psychiatry_Ment_Health',
              'b_journal_label': 'Child and Adolescent Psychiatry and Mental Health-Child '
                                 'Adolesc Psychiatry Ment Health',
              'b_open_citations_id': 'https://w3id.org/oc/corpus/br/362418',
              'b_pages': ' ',
              'b_pmid': '26417387',
              'b_publication_year': '2015',
              'b_publisher': 'Springer_Science_%2B_Business_Media',
              'b_publisher_label': 'Springer Science + Business Media',
              'b_type': 'Journal Article',
              'b_url': 'http://dx.doi.org/10.1186/s13034-015-0062-7',
              'b_volume': '9'})
            <BLANKLINE>
            ----------------------------------ENTRY 2----------------------------------
            ('https://w3id.org/oc/corpus/br/384',
             {'b_author_labels': ['Creutzberg, CL', 'van_Putten, WLJ', 'Koper, PC',
                                  'Lybeert, MLM', 'Jobsen, JJ', 'Warlam-Rodenhuis, CC',
                                  'De_Winter, KAJ', 'Lutgens, LCHW', 'van_den_Bergh, ACM',
                                  'van_der_Steen-Banasik, E', 'Beerman, H', 'van_Lent, M'],
              'b_authors': ['Creutzberg_CL', 'van_Putten_WLJ', 'Koper_PC', 'Lybeert_MLM',
                            'Jobsen_JJ', 'Warlam-Rodenhuis_CC', 'De_Winter_KAJ',
                            'Lutgens_LCHW', 'van_den_Bergh_ACM', 'van_der_Steen-Banasik_E',
                            'Beerman_H', 'van_Lent_M'],
              'b_cited': '',
              'b_cited_by': ['https://w3id.org/oc/corpus/br/1',
                             'https://w3id.org/oc/corpus/br/1342763',
                             'https://w3id.org/oc/corpus/br/1772164'],
              'b_document': 'Survival_after_relapse_in_patients_with_endometrial_cancer-results_from_a_randomized_trial',
              'b_document_label': 'Survival after relapse in patients with endometrial '
                                  'cancer-results from a randomized trial',
              'b_doi': '10.1016/s0090-8258(03)00126-4',
              'b_issue_number': '2',
              'b_journal': 'Gynecologic_Oncology',
              'b_journal_label': 'Gynecologic Oncology',
              'b_open_citations_id': 'https://w3id.org/oc/corpus/br/384',
              'b_pages': '201--209',
              'b_pmid': '12713981',
              'b_publication_year': '2003',
              'b_publisher': 'Elsevier_BV',
              'b_publisher_label': 'Elsevier BV',
              'b_type': 'Journal Article',
              'b_url': 'http://dx.doi.org/10.1016/s0090-8258%2803%2900126-4',
              'b_volume': '89'})
            <BLANKLINE>




            >>> # create a Bibliography instance by using custom conversion_arguments_list
            >>> custom_arguments_list = [
            ...     ['each_entry_data["titles"]', 'pybtex_document_instance_name', 'x_document'],
            ...     ['each_entry_data["titles"]', 'pybtex_document_label',         'x_document_label']
            ... ]
            >>> my_custom_bibliography = Bibliography()
            >>> my_custom_bibliography.importCsv(path_of_file_to_import='example_data//test.csv',
            ...                                    conversion_arguments_list=custom_arguments_list,
            ...                                    cleaning_algorithm="default",
            ...                                    csv_delimiter_character=',',
            ...                                    field_value_list_separator=' | ',
            ...                                    id_column_header='referenceEntry')
            Parsing of "example_data//test.csv" started
            Conversion from ListData to Bibliography object started
            Conversion completed. 7 out of 7 ListData rows converted to Bibliography object entries
            <BLANKLINE>
            Formatting of Bibliography entries started
            "example_data//test.csv" parsed and imported into Bibliography object in memory
            <BLANKLINE>
            Number of fields in the parsed bibliography:
            {'x_document': 7, 'x_document_label': 7}
            >>> my_custom_bibliography.preview(1)
            <BLANKLINE>
            ----------------------------------ENTRY 1----------------------------------
            ('https://w3id.org/oc/corpus/br/44493',
             {'x_document': 'Midwife-led_continuity_models_versus_other_models_of_care_for_childbearing_women',
              'x_document_label': 'Midwife-led continuity models versus other models of '
                                  'care for childbearing women'})
            <BLANKLINE>

            >>>

            >>> # import a csv file
            >>> old_oc_conversion_arguments_list = [ # this is the old open citations conversion arguments list (was a keyword argument)
            ...     # [target_field_value in existing data,  formatting_algorithm,                                       desired_field_name in new object]
            ...     ['each_entry_data["titles"]',            'pybtex_document_instance_name',                            'b_document'],
            ...     ['each_entry_data["titles"]',            'pybtex_document_label',                                    'b_document_label'],
            ...     ['each_entry_data["dois"]',              'oc_select_first_item_if_list',                             'b_doi'],
            ...     ['each_entry_data["authors"]',           'open_citations_author_instance_name',                      'b_authors'],
            ...     ['each_entry_data["authors"]',           'open_citations_author_label',                              'b_author_labels'],
            ...     ['each_entry_data["publications"]',      'pybtex_document_instance_name',                            'b_publication'],
            ...     ['each_entry_data["publications"]',      'pybtex_document_label',                                    'b_publication_label'],
            ...     ['each_entry_data["publication_types"]', 'oc_select_last_item_if_list',                              'b_publication_type'],
            ...     ['each_entry_data["types"]',             'oc_select_last_item_if_list',                              'b_type'],
            ...     ['each_entry_data["years"]',             'oc_select_first_item_if_list',                             'b_publication_year'],
            ...     ['each_entry_data["publishers"]',        'pybtex_document_instance_name',                            'b_publisher'],
            ...     ['each_entry_data["publishers"]',        'pybtex_document_label',                                    'b_publisher_label']
            ... ]
            >>> my_csv_bibliography = Bibliography()
            >>> my_csv_bibliography.importCsv(path_of_file_to_import='example_data//test.csv',
            ...                                conversion_arguments_list=old_oc_conversion_arguments_list,
            ...                                cleaning_algorithm="default",
            ...                                csv_delimiter_character=',',
            ...                                field_value_list_separator=' | ',
            ...                                id_column_header='referenceEntry')
            Parsing of "example_data//test.csv" started
            Conversion from ListData to Bibliography object started
            Conversion completed. 7 out of 7 ListData rows converted to Bibliography object entries
            <BLANKLINE>
            Formatting of Bibliography entries started
            "example_data//test.csv" parsed and imported into Bibliography object in memory
            <BLANKLINE>
            Number of fields in the parsed bibliography:
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
             >>> my_csv_bibliography.preview(1)
             <BLANKLINE>
             ----------------------------------ENTRY 1----------------------------------
             ('https://w3id.org/oc/corpus/br/44493',
              {'b_author_labels': ['Sandall, J', 'Soltani, H', 'Gates, S', 'Shennan, A',
                                   'Devane, D'],
               'b_authors': ['Sandall_J', 'Soltani_H', 'Gates_S', 'Shennan_A', 'Devane_D'],
               'b_document': 'Midwife-led_continuity_models_versus_other_models_of_care_for_childbearing_women',
               'b_document_label': 'Midwife-led continuity models versus other models of '
                                   'care for childbearing women',
               'b_doi': '10.1002/14651858.cd004667.pub3',
               'b_publication': 'Cochrane_Database_of_Systematic_Reviews-Reviews',
               'b_publication_label': 'Cochrane Database of Systematic Reviews-Reviews',
               'b_publication_type': 'http://purl.org/spar/fabio/ExpressionCollection',
               'b_publication_year': '2013',
               'b_publisher': 'Wiley-Blackwell',
               'b_publisher_label': 'Wiley-Blackwell',
               'b_type': 'http://purl.org/spar/fabio/ReferenceEntry'})
             <BLANKLINE>

        """
        from triplicator.csvImporter import CSV_Bibliography
        from meta.consoleOutput import ConsoleOutput

        console = ConsoleOutput('log.txt')
        console.log_message('Parsing of "%s" started' % path_of_file_to_import, add_timestamp_in_file=True)

        # pass functions to CSV container and create an instance of CSV_Bibliography class
        csv_bibliography = CSV_Bibliography(csv_file_path=path_of_file_to_import,
                                            id_column_header=id_column_header,
                                            field_value_list_separator=field_value_list_separator,
                                            csv_delimiter_character=csv_delimiter_character,
                                            cleaning_algorithm=cleaning_algorithm,
                                            show_progress_bar=show_progress_bar
                                            )

        if conversion_arguments_list == 'open citations':
        # "publication_type" , "journal_article" , "journal_issue_number" , "journal_volume_number" , "startEndPages" , "publisher_name" , "cited_by_article"
            conversion_arguments_list = [
                # CAUTION: If there would be any merge operation would be made with other bib files (e.g.,
                # using 'enrich_with' method), the 'desired_field_name's should be the same with those in
                # Bibliography.importBibtex() > conversion_arguments_list > 'bib_default' > 'desired_field_name' column
                # If a field name differs from its counterpart in the bib conversion algorithm, then during the merge
                # operation it will likely be added as a separate field under this differing name
                # [target_field_value in existing data,      formatting_algorithm,                                          desired_field_name in new object]
                ['each_entry_data["publication_type"]',      'oc_select_last_item_if_list_and_capitalize_first_letter',     'b_type'],
                # even though the field name below is "journal_article" and it refers to the column with the same header
                # in the source csv file, this is the name of the column that contains OpenCitations IDs of documents
                ['each_entry_data["journal_article"]',       'oc_select_first_item_if_list',                                'b_open_citations_id'],
                ['each_entry_data["title"]',                 'pybtex_document_instance_name',                               'b_document'],
                ['each_entry_data["title"]',                 'pybtex_document_label',                                       'b_document_label'],
                ['each_entry_data["authors"]',               'open_citations_author_instance_name',                         'b_authors'],
                ['each_entry_data["authors"]',               'open_citations_author_label',                                 'b_author_labels'],
                ['each_entry_data["journal_name"]',          'pybtex_document_instance_name',                               'b_journal'],
                ['each_entry_data["journal_name"]',          'pybtex_document_label',                                       'b_journal_label'],
                ['each_entry_data["publisher_name"]',        'pybtex_document_instance_name',                               'b_publisher'],
                ['each_entry_data["publisher_name"]',        'pybtex_document_label',                                       'b_publisher_label'],
                ['each_entry_data["publication_year"]',      'oc_select_first_item_if_list',                                'b_publication_year'],
                ['each_entry_data["journal_issue_number"]',  'oc_select_first_item_if_list',                                'b_issue_number'],
                ['each_entry_data["journal_volume_number"]', 'oc_select_first_item_if_list',                                'b_volume'],
                ['each_entry_data["startEndPages"]',         'oc_select_first_item_if_list',                                'b_pages'],
                ['each_entry_data["doi"]',                   'oc_select_first_item_if_list',                                'b_doi'],
                ['each_entry_data["pmid"]',                  'oc_select_first_item_if_list',                                'b_pmid'],
                ['each_entry_data["url"]',                   'oc_select_first_item_if_list',                                'b_url'],
                ['each_entry_data["cited_by_the_articles"]', 'none',                                                        'b_cited_by'],
                ['each_entry_data["cited_the_articles"]',    'none',                                                        'b_cited']
            ]

        # if a custom conversion_arguments_list is provided, proceed without modifying the provided list
        elif type(conversion_arguments_list) is list:
            pass

        else:
            raise ValueError("Conversion_arguments_list parameter should be either left blank or be a list that "
                             "contains sublists of arguments.")


        # For logging
        console.log_message("\nFormatting of Bibliography entries started", add_timestamp_in_file=True)
        maximum_progress = len(csv_bibliography.entries.keys())

        failed_conversion_arguments = []

        # loop through individual reference entries in the parsed pybtex bib file
        for i, (each_entry_id, each_entry_data) in enumerate(csv_bibliography.entries.items()):
            if show_progress_bar:
                console.print_current_progress(i, maximum_progress, 'Formatting Bibliography object entries')

            # loop through each line in the conversion_arguments_list
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


        ###############################
        #  OVERALL OPERATION SUMMARY   #
        ###############################

        console.log_message('"%s" parsed and imported into Bibliography object in memory' % path_of_file_to_import,
                            add_timestamp_in_file=True)

        console.log_message("\nNumber of fields in the parsed bibliography:", print_to_file=False)  # because...
                                                                    #  ... '.summarize()' does not print to file
        instance.summarize()


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


    def enrich_with(instance, target_bibliography_object, field_to_match_in_bibliographies, method='left join'):
        """
        Left joins or merges two bibliographies.

        Args:
            target_bibliography_object(Bibliography): The target bibliography that will be used to enrich the current
                bibliography.
            field_to_match_in_bibliographies(str): The field name that will be used to match entries between bibliographies
                (e.g., doi)
            method(str): Method to use when combining bibliographies

        Keyword Args:
            'left join' (method): Add new fields and values from the target_bibliography_object only if the record they
                belong to exists in the instance bibliography (i.e., to self)
            'merge' (method): Left joins when possible, add if not, adds new entries from other_bibliography to the
                instance bibliography (i.e., to self)

        Returns:
            Nothing

        Examples:
            >>> #=================================================
            >>> # EXAMPLE: CREATE AND COMBINE BIBLIOGRAPHY OBJECTS
            >>> #=================================================

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
            >>> bib_one.enrich_with(target_bibliography_object=bib_two, field_to_match_in_bibliographies='doi')
            <BLANKLINE>
            Enrichment completed successfully.
            Existing entries enriched: 1
            Fields added to existing entries: 1
            New entries added: 0
            >>> bib_one.preview()
            <BLANKLINE>
            ----------------------------------ENTRY 1----------------------------------
            ('01', {'author': 'John Doe', 'doi': '6226', 'title': 'This is a title'})
            <BLANKLINE>

            >>> # no entries appended in 'left join' mode
            >>> bib_two.setEntry(entry_id='100', field_name='doi', field_value='5000')  # doi 500 not in bib_one
            >>> bib_two.setEntry(entry_id='100', field_name='note', field_value='This is a note')
            >>> bib_one.enrich_with(target_bibliography_object=bib_two, field_to_match_in_bibliographies='doi')
            <BLANKLINE>
            Enrichment completed successfully.
            Existing entries enriched: 0
            Fields added to existing entries: 0
            New entries added: 0
            >>> bib_one.preview(10)
            <BLANKLINE>
            ----------------------------------ENTRY 1----------------------------------
            ('01', {'author': 'John Doe', 'doi': '6226', 'title': 'This is a title'})
            <BLANKLINE>

            >>> # entries enriched and appended in 'merge' mode
            >>> bib_two.setEntry(entry_id='41124', field_name='doi', field_value='6226')  # doi 6226 is in bib_one too
            >>> bib_two.setEntry(entry_id='41124', field_name='publisher', field_value='Some publisher')
            >>> bib_two.setEntry(entry_id='100', field_name='doi', field_value='5000')  # doi 500 not in bib_one
            >>> bib_two.setEntry(entry_id='100', field_name='note', field_value='This is a note')
            >>> bib_one.enrich_with(target_bibliography_object=bib_two, field_to_match_in_bibliographies='doi'
            ...         , method='merge')
            <BLANKLINE>
            Enrichment completed successfully.
            Existing entries enriched: 1
            Fields added to existing entries: 1
            New entries added: 1

            >>> bib_one.preview(10)
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


            >>> #=============================================
            >>> # EXAMPLE: IMPORT AND COMBINE TWO BIBTEX FILES
            >>> #=============================================

            >>> # bib file import and merge
            >>> bib_poor = Bibliography()
            >>> bib_poor.importBibtex('example_data//merge_test_file_poor.bib')
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
             'b_pure_bibliography_id': 2,
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
              'b_pure_bibliography_id': 'b56e503067994b389d4eced98fae2206',
              'b_type': 'Article'})
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
              'b_pure_bibliography_id': 'd0e972a611e44a80b8014f1069bfad88',
              'b_type': 'Book'})
            <BLANKLINE>

            >>> bib_rich = Bibliography()
            >>> bib_rich.importBibtex('example_data//merge_test_file_rich.bib')
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
             'b_pure_bibliography_id': 2,
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
              'b_pure_bibliography_id': 'b56e503067994b389d4eced98fae2206',
              'b_type': 'Article',
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
              'b_pure_bibliography_id': 'd0e972a611e44a80b8014f1069bfad88',
              'b_type': 'Book'})
            <BLANKLINE>

            >>> bib_poor.enrich_with(target_bibliography_object=bib_rich, field_to_match_in_bibliographies='b_doi')
            <BLANKLINE>
            Enrichment completed successfully.
            Existing entries enriched: 2
            Fields added to existing entries: 12
            New entries added: 0

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
              'b_pure_bibliography_id': 'b56e503067994b389d4eced98fae2206',
              'b_type': 'Article',
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
              'b_pure_bibliography_id': 'd0e972a611e44a80b8014f1069bfad88',
              'b_type': 'Book'})
            <BLANKLINE>


            >>> #===========================================
            >>> # EXAMPLE: MERGE BIB AND CSV(Open Citations)
            >>> #===========================================

            >>> vu_bibliography = Bibliography()
            >>> vu_bibliography.importBibtex('example_data//oc_query_complementary_bibtex_for_merging.bib')
            Parsing of example_data//oc_query_complementary_bibtex_for_merging.bib started
            pybtex package is parsing using bibtex.Parser()...
            pybtex package finished parsing
            Calculating file length...
            <BLANKLINE>
            <BLANKLINE>
            ---------------------------------------------------------------------------------------------------
            example_data//oc_query_complementary_bibtex_for_merging.bib parsed and imported as Bibliography object.
            <BLANKLINE>
            Fields added to the parsed the Bibliography object:
            {'b_abstract': 1,
             'b_author_labels': 2,
             'b_authors': 2,
             'b_document': 2,
             'b_document_label': 2,
             'b_doi': 2,
             'b_publication_year': 1,
             'b_publisher': 1,
             'b_publisher_label': 1,
             'b_pure_bibliography_id': 2,
             'b_type': 2}
            <BLANKLINE>
            <BLANKLINE>

            >>> oc_bibliography = Bibliography()
            >>> oc_bibliography.importCsv(path_of_file_to_import='example_data/oc_query_2.2_results_short_sample_for_merging.csv',
            ...                           csv_delimiter_character=',',
            ...                           field_value_list_separator=' | ',
            ...                           id_column_header='journal_article',
            ...                           conversion_arguments_list='open citations',
            ...                           cleaning_algorithm='default')
            Parsing of "example_data/oc_query_2.2_results_short_sample_for_merging.csv" started
            Conversion from ListData to Bibliography object started
            Conversion completed. 3 out of 3 ListData rows converted to Bibliography object entries
            <BLANKLINE>
            Formatting of Bibliography entries started
            "example_data/oc_query_2.2_results_short_sample_for_merging.csv" parsed and imported into Bibliography object in memory
            <BLANKLINE>
            Number of fields in the parsed bibliography:
            {'b_author_labels': 3,
             'b_authors': 3,
             'b_cited': 3,
             'b_cited_by': 3,
             'b_document': 3,
             'b_document_label': 3,
             'b_doi': 3,
             'b_issue_number': 3,
             'b_journal': 3,
             'b_journal_label': 3,
             'b_open_citations_id': 3,
             'b_pages': 2,
             'b_pmid': 3,
             'b_publication_year': 3,
             'b_publisher': 3,
             'b_publisher_label': 3,
             'b_type': 3,
             'b_url': 3,
             'b_volume': 3}
            >>> # compare entries in two bibliographies
            >>> from pprint import pprint
            >>> # entry in the the poorer bibliography
            >>> pprint(vu_bibliography.getEntriesByField('b_doi', '10.1186/s13034-015-0062-7'), compact=True)
            [{'b_abstract': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed '
                            'do eiusmod tempor incididunt ut labore et dolore magna '
                            'aliqua. Ut enim ad minim veniam, quis nostrud exercitation '
                            'ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis '
                            'aute irure dolor in reprehenderit in voluptate velit esse '
                            'cillum dolore eu fugiat nulla pariatur. Excepteur sint '
                            'occaecat cupidatat non proident, sunt in culpa qui officia '
                            'deserunt mollit anim id est laborum.',
              'b_author_labels': ['Maria, Z'],
              'b_authors': ['Maria_Z'],
              'b_document': 'The_DSM-5_diagnosis_of_nonsuicidal_self-injury_disorder-a_review_of_the_empirical_literature',
              'b_document_label': 'The_DSM-5_diagnosis_of_nonsuicidal_self-injury_disorder-a_review_of_the_empirical_literature',
              'b_doi': '10.1186/s13034-015-0062-7',
              'b_pure_bibliography_id': 'b466af64b57f4089b0596f133f4862d2',
              'b_type': 'Article'}]
             >>> # entry in the the richer bibliography
             >>> pprint(oc_bibliography.getEntriesByField('b_doi', '10.1186/s13034-015-0062-7'), compact=True)
             [{'b_author_labels': ['Zetterqvist, M'],
               'b_authors': ['Zetterqvist_M'],
               'b_cited': ['https://w3id.org/oc/corpus/br/37961',
                           'https://w3id.org/oc/corpus/br/38250',
                           'https://w3id.org/oc/corpus/br/135448',
                           'https://w3id.org/oc/corpus/br/135458',
                           'https://w3id.org/oc/corpus/br/177639',
                           'https://w3id.org/oc/corpus/br/177648',
                           'https://w3id.org/oc/corpus/br/177653',
                           'https://w3id.org/oc/corpus/br/177661',
                           'https://w3id.org/oc/corpus/br/177774',
                           'https://w3id.org/oc/corpus/br/362419',
                           'https://w3id.org/oc/corpus/br/362426',
                           'https://w3id.org/oc/corpus/br/362438',
                           'https://w3id.org/oc/corpus/br/607811',
                           'https://w3id.org/oc/corpus/br/1270766',
                           'https://w3id.org/oc/corpus/br/1560911',
                           'https://w3id.org/oc/corpus/br/1794850',
                           'https://w3id.org/oc/corpus/br/1881397',
                           'https://w3id.org/oc/corpus/br/2258672',
                           'https://w3id.org/oc/corpus/br/2907029',
                           'https://w3id.org/oc/corpus/br/2907034',
                           'https://w3id.org/oc/corpus/br/2907035',
                           'https://w3id.org/oc/corpus/br/2907042',
                           'https://w3id.org/oc/corpus/br/2907056',
                           'https://w3id.org/oc/corpus/br/3346205',
                           'https://w3id.org/oc/corpus/br/3567493',
                           'https://w3id.org/oc/corpus/br/3567495',
                           'https://w3id.org/oc/corpus/br/3949890',
                           'https://w3id.org/oc/corpus/br/5106137',
                           'https://w3id.org/oc/corpus/br/5441063',
                           'https://w3id.org/oc/corpus/br/5441066',
                           'https://w3id.org/oc/corpus/br/5441085',
                           'https://w3id.org/oc/corpus/br/5656230',
                           'https://w3id.org/oc/corpus/br/6060536',
                           'https://w3id.org/oc/corpus/br/6063037',
                           'https://w3id.org/oc/corpus/br/6449521',
                           'https://w3id.org/oc/corpus/br/6486152',
                           'https://w3id.org/oc/corpus/br/6486162',
                           'https://w3id.org/oc/corpus/br/6919305',
                           'https://w3id.org/oc/corpus/br/6919323',
                           'https://w3id.org/oc/corpus/br/7558746',
                           'https://w3id.org/oc/corpus/br/7560541',
                           'https://w3id.org/oc/corpus/br/7560644',
                           'https://w3id.org/oc/corpus/br/7560645',
                           'https://w3id.org/oc/corpus/br/7560646',
                           'https://w3id.org/oc/corpus/br/7560647',
                           'https://w3id.org/oc/corpus/br/7560648',
                           'https://w3id.org/oc/corpus/br/7560651',
                           'https://w3id.org/oc/corpus/br/7560652',
                           'https://w3id.org/oc/corpus/br/7560653',
                           'https://w3id.org/oc/corpus/br/7560654',
                           'https://w3id.org/oc/corpus/br/7560655',
                           'https://w3id.org/oc/corpus/br/7560656',
                           'https://w3id.org/oc/corpus/br/7560657',
                           'https://w3id.org/oc/corpus/br/7560658',
                           'https://w3id.org/oc/corpus/br/7560659',
                           'https://w3id.org/oc/corpus/br/7560660',
                           'https://w3id.org/oc/corpus/br/7560661',
                           'https://w3id.org/oc/corpus/br/7560662',
                           'https://w3id.org/oc/corpus/br/7560663',
                           'https://w3id.org/oc/corpus/br/7560664',
                           'https://w3id.org/oc/corpus/br/7560665',
                           'https://w3id.org/oc/corpus/br/7560666'],
               'b_cited_by': 'https://w3id.org/oc/corpus/br/362415',
               'b_document': 'The_DSM-5_diagnosis_of_nonsuicidal_self-injury_disorder-a_review_of_the_empirical_literature',
               'b_document_label': 'The DSM-5 diagnosis of nonsuicidal self-injury '
                                   'disorder-a review of the empirical literature',
               'b_doi': '10.1186/s13034-015-0062-7',
               'b_issue_number': '1',
               'b_journal': 'Child_and_Adolescent_Psychiatry_and_Mental_Health-Child_Adolesc_Psychiatry_Ment_Health',
               'b_journal_label': 'Child and Adolescent Psychiatry and Mental Health-Child '
                                  'Adolesc Psychiatry Ment Health',
               'b_open_citations_id': 'https://w3id.org/oc/corpus/br/362418',
               'b_pages': ' ',
               'b_pmid': '26417387',
               'b_publication_year': '2015',
               'b_publisher': 'Springer_Science_%2B_Business_Media',
               'b_publisher_label': 'Springer Science + Business Media',
               'b_type': 'Journal Article',
               'b_url': 'http://dx.doi.org/10.1186/s13034-015-0062-7',
               'b_volume': '9'}]

            >>> # another entry in the the poorer bibliography
            >>> pprint(vu_bibliography.getEntriesByField('b_doi', '10.1016/s0090-8258(03)00087-8'), compact=True)
            [{'b_author_labels': ['Straughn, MJ', 'Huh, WK'],
              'b_authors': ['Straughn_MJ', 'Huh_WK'],
              'b_document': 'Stage_IC_adenocarcinoma_of_the_endometrium-survival_comparisons_of_surgically_staged_patients_with_and_without_adjuvant_radiation_therapy%C3%A2%C2%98%C2%86%C3%A2%C2%98%C2%86Presented_at_the_33rd_Annual_Meeting_of_Gynecologic_Oncologists_Miami_FL_March_2002',
              'b_document_label': 'Stage IC adenocarcinoma of the endometrium-survival '
                                  'comparisons of surgically staged patients with and '
                                  'without adjuvant radiation '
                                  'therapyâ\x98\x86â\x98\x86Presented at the 33rd Annual '
                                  'Meeting of Gynecologic Oncologists, Miami, FL, March '
                                  '2002.',
              'b_doi': '10.1016/s0090-8258(03)00087-8',
              'b_publication_year': '2003',
              'b_publisher': 'Elsevier_BV',
              'b_publisher_label': 'Elsevier B.V.',
              'b_pure_bibliography_id': 'b3cd7336ed9a48bfaed37af3a2e593c6',
              'b_type': 'Article'}]
            >>> # another entry in the the richer bibliography
            >>> pprint(oc_bibliography.getEntriesByField('b_doi', '10.1016/s0090-8258(03)00087-8'), compact=True)
            [{'b_author_labels': ['Straughn, JM', 'Huh, WK', 'Orr, JW', 'Kelly, FJ',
                                  'Roland, PY', 'Gold, MA', 'Powell, M', 'Mutch, DG',
                                  'Partridge, EE', 'Kilgore, LC', 'Barnes, MN',
                                  'Austin, JM', 'Alvarez, RD'],
              'b_authors': ['Straughn_JM', 'Huh_WK', 'Orr_JW', 'Kelly_FJ', 'Roland_PY',
                            'Gold_MA', 'Powell_M', 'Mutch_DG', 'Partridge_EE', 'Kilgore_LC',
                            'Barnes_MN', 'Austin_JM', 'Alvarez_RD'],
              'b_cited': '',
              'b_cited_by': 'https://w3id.org/oc/corpus/br/1',
              'b_document': 'Stage_IC_adenocarcinoma_of_the_endometrium-survival_comparisons_of_surgically_staged_patients_with_and_without_adjuvant_radiation_therapyaaPresented_at_the_33rd_Annual_Meeting_of_Gynecologic_Oncologists-Miami-FL-March_2002',
              'b_document_label': 'Stage IC adenocarcinoma of the endometrium-survival '
                                  'comparisons of surgically staged patients with and '
                                  'without adjuvant radiation therapyaaPresented at the '
                                  '33rd Annual Meeting of Gynecologic '
                                  'Oncologists-Miami-FL-March 2002.',
              'b_doi': '10.1016/s0090-8258(03)00087-8',
              'b_issue_number': '2',
              'b_journal': 'Gynecologic_Oncology',
              'b_journal_label': 'Gynecologic Oncology',
              'b_open_citations_id': 'https://w3id.org/oc/corpus/br/392',
              'b_pages': '295--300',
              'b_pmid': '12713994',
              'b_publication_year': '2003',
              'b_publisher': 'Elsevier_BV',
              'b_publisher_label': 'Elsevier BV',
              'b_type': 'Journal Article',
              'b_url': 'http://dx.doi.org/10.1016/s0090-8258%2803%2900087-8',
              'b_volume': '89'}]


            >>> # merge poorer and richer bibliographies
            >>> vu_bibliography.enrich_with(oc_bibliography, field_to_match_in_bibliographies='b_doi')
            <BLANKLINE>
            Enrichment completed successfully.
            Existing entries enriched: 2
            Fields added to existing entries: 23
            New entries added: 0


            >>> vu_bibliography.preview(100)
            <BLANKLINE>
            ----------------------------------ENTRY 1----------------------------------
            ('b466af64b57f4089b0596f133f4862d2',
             {'b_abstract': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed '
                            'do eiusmod tempor incididunt ut labore et dolore magna '
                            'aliqua. Ut enim ad minim veniam, quis nostrud exercitation '
                            'ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis '
                            'aute irure dolor in reprehenderit in voluptate velit esse '
                            'cillum dolore eu fugiat nulla pariatur. Excepteur sint '
                            'occaecat cupidatat non proident, sunt in culpa qui officia '
                            'deserunt mollit anim id est laborum.',
              'b_author_labels': ['Maria, Z'],
              'b_authors': ['Maria_Z'],
              'b_cited': ['https://w3id.org/oc/corpus/br/37961',
                          'https://w3id.org/oc/corpus/br/38250',
                          'https://w3id.org/oc/corpus/br/135448',
                          'https://w3id.org/oc/corpus/br/135458',
                          'https://w3id.org/oc/corpus/br/177639',
                          'https://w3id.org/oc/corpus/br/177648',
                          'https://w3id.org/oc/corpus/br/177653',
                          'https://w3id.org/oc/corpus/br/177661',
                          'https://w3id.org/oc/corpus/br/177774',
                          'https://w3id.org/oc/corpus/br/362419',
                          'https://w3id.org/oc/corpus/br/362426',
                          'https://w3id.org/oc/corpus/br/362438',
                          'https://w3id.org/oc/corpus/br/607811',
                          'https://w3id.org/oc/corpus/br/1270766',
                          'https://w3id.org/oc/corpus/br/1560911',
                          'https://w3id.org/oc/corpus/br/1794850',
                          'https://w3id.org/oc/corpus/br/1881397',
                          'https://w3id.org/oc/corpus/br/2258672',
                          'https://w3id.org/oc/corpus/br/2907029',
                          'https://w3id.org/oc/corpus/br/2907034',
                          'https://w3id.org/oc/corpus/br/2907035',
                          'https://w3id.org/oc/corpus/br/2907042',
                          'https://w3id.org/oc/corpus/br/2907056',
                          'https://w3id.org/oc/corpus/br/3346205',
                          'https://w3id.org/oc/corpus/br/3567493',
                          'https://w3id.org/oc/corpus/br/3567495',
                          'https://w3id.org/oc/corpus/br/3949890',
                          'https://w3id.org/oc/corpus/br/5106137',
                          'https://w3id.org/oc/corpus/br/5441063',
                          'https://w3id.org/oc/corpus/br/5441066',
                          'https://w3id.org/oc/corpus/br/5441085',
                          'https://w3id.org/oc/corpus/br/5656230',
                          'https://w3id.org/oc/corpus/br/6060536',
                          'https://w3id.org/oc/corpus/br/6063037',
                          'https://w3id.org/oc/corpus/br/6449521',
                          'https://w3id.org/oc/corpus/br/6486152',
                          'https://w3id.org/oc/corpus/br/6486162',
                          'https://w3id.org/oc/corpus/br/6919305',
                          'https://w3id.org/oc/corpus/br/6919323',
                          'https://w3id.org/oc/corpus/br/7558746',
                          'https://w3id.org/oc/corpus/br/7560541',
                          'https://w3id.org/oc/corpus/br/7560644',
                          'https://w3id.org/oc/corpus/br/7560645',
                          'https://w3id.org/oc/corpus/br/7560646',
                          'https://w3id.org/oc/corpus/br/7560647',
                          'https://w3id.org/oc/corpus/br/7560648',
                          'https://w3id.org/oc/corpus/br/7560651',
                          'https://w3id.org/oc/corpus/br/7560652',
                          'https://w3id.org/oc/corpus/br/7560653',
                          'https://w3id.org/oc/corpus/br/7560654',
                          'https://w3id.org/oc/corpus/br/7560655',
                          'https://w3id.org/oc/corpus/br/7560656',
                          'https://w3id.org/oc/corpus/br/7560657',
                          'https://w3id.org/oc/corpus/br/7560658',
                          'https://w3id.org/oc/corpus/br/7560659',
                          'https://w3id.org/oc/corpus/br/7560660',
                          'https://w3id.org/oc/corpus/br/7560661',
                          'https://w3id.org/oc/corpus/br/7560662',
                          'https://w3id.org/oc/corpus/br/7560663',
                          'https://w3id.org/oc/corpus/br/7560664',
                          'https://w3id.org/oc/corpus/br/7560665',
                          'https://w3id.org/oc/corpus/br/7560666'],
              'b_cited_by': 'https://w3id.org/oc/corpus/br/362415',
              'b_document': 'The_DSM-5_diagnosis_of_nonsuicidal_self-injury_disorder-a_review_of_the_empirical_literature',
              'b_document_label': 'The_DSM-5_diagnosis_of_nonsuicidal_self-injury_disorder-a_review_of_the_empirical_literature',
              'b_doi': '10.1186/s13034-015-0062-7',
              'b_issue_number': '1',
              'b_journal': 'Child_and_Adolescent_Psychiatry_and_Mental_Health-Child_Adolesc_Psychiatry_Ment_Health',
              'b_journal_label': 'Child and Adolescent Psychiatry and Mental Health-Child '
                                 'Adolesc Psychiatry Ment Health',
              'b_open_citations_id': 'https://w3id.org/oc/corpus/br/362418',
              'b_pages': ' ',
              'b_pmid': '26417387',
              'b_publication_year': '2015',
              'b_publisher': 'Springer_Science_%2B_Business_Media',
              'b_publisher_label': 'Springer Science + Business Media',
              'b_pure_bibliography_id': 'b466af64b57f4089b0596f133f4862d2',
              'b_type': 'Article',
              'b_url': 'http://dx.doi.org/10.1186/s13034-015-0062-7',
              'b_volume': '9'})
            <BLANKLINE>
            ----------------------------------ENTRY 2----------------------------------
            ('b3cd7336ed9a48bfaed37af3a2e593c6',
             {'b_author_labels': ['Straughn, MJ', 'Huh, WK'],
              'b_authors': ['Straughn_MJ', 'Huh_WK'],
              'b_cited': '',
              'b_cited_by': 'https://w3id.org/oc/corpus/br/1',
              'b_document': 'Stage_IC_adenocarcinoma_of_the_endometrium-survival_comparisons_of_surgically_staged_patients_with_and_without_adjuvant_radiation_therapy%C3%A2%C2%98%C2%86%C3%A2%C2%98%C2%86Presented_at_the_33rd_Annual_Meeting_of_Gynecologic_Oncologists_Miami_FL_March_2002',
              'b_document_label': 'Stage IC adenocarcinoma of the endometrium-survival '
                                  'comparisons of surgically staged patients with and '
                                  'without adjuvant radiation '
                                  'therapyâ\x98\x86â\x98\x86Presented at the 33rd Annual '
                                  'Meeting of Gynecologic Oncologists, Miami, FL, March '
                                  '2002.',
              'b_doi': '10.1016/s0090-8258(03)00087-8',
              'b_issue_number': '2',
              'b_journal': 'Gynecologic_Oncology',
              'b_journal_label': 'Gynecologic Oncology',
              'b_open_citations_id': 'https://w3id.org/oc/corpus/br/392',
              'b_pages': '295--300',
              'b_pmid': '12713994',
              'b_publication_year': '2003',
              'b_publisher': 'Elsevier_BV',
              'b_publisher_label': 'Elsevier B.V.',
              'b_pure_bibliography_id': 'b3cd7336ed9a48bfaed37af3a2e593c6',
              'b_type': 'Article',
              'b_url': 'http://dx.doi.org/10.1016/s0090-8258%2803%2900087-8',
              'b_volume': '89'})
            <BLANKLINE>
        """
        # reset instance counters (in case this is not the first merge operation on the instance, this is necessary)
        instance.no_of_entries_enriched_in_last_operation = 0
        instance.no_of_existing_fields_enriched_in_last_operation = 0
        instance.no_of_entries_added_in_last_operation = 0
        instance.no_of_fields_added_in_last_operation = 0

        other_bibliography = target_bibliography_object
        target_field_name = field_to_match_in_bibliographies

        for each_entry_id_in_other_bibliography, each_entry_data_in_other_bibliography in other_bibliography.entries.items():

            # for logging
            last_entry_is_enriched = False
            last_entry_is_added = False

            # if a field name and value(e.g., doi) from other bibliography is found in the current one, enrich
            # the corresponding entry in the current dataset with this field name and its value
            # TODO: This try-except block should either be made more specific or replaced with an if-else block
            try:
                each_target_value_in_other_bibliography = each_entry_data_in_other_bibliography[target_field_name]

                # Make sure that only one entry in self matches the target value (e.g., doi)
                matching_entry_in_this_bibliography = instance.getEntriesByField(field_name=target_field_name, field_value=each_target_value_in_other_bibliography)
                matching_entry_ids_in_this_bibliography = instance._field_values_registry[target_field_name][each_target_value_in_other_bibliography]

                if len(matching_entry_ids_in_this_bibliography) > 1:

                    # TODO: If a DOI (or another target value) appears in multiple entries, only the first entry is
                    # TODO: ... enriched, and the other occurrences is simply left alone.
                    # TODO: ... A 'merge_duplicate_entries' function should be implemented and used during cleaning for
                    # TODO: ... cleaner behavior
                    # If multiple matches is the case (e.g., a DOI appears in multiple entries in self bibliography)
                    # only set the first occurrence for enrichment
                    matching_entry_id_in_this_bibliography = matching_entry_ids_in_this_bibliography[0]

                    # the old error in case there is more than one matching (e.g.) DOI:
                    #raise ValueError("More than one ID (%s) in the source bibliography returned with the field name '%s' and value '%s'."
                    #                % (matching_entry_ids_in_this_bibliography, target_field_name, each_target_value_in_other_bibliography))
                else:
                    matching_entry_id_in_this_bibliography = matching_entry_ids_in_this_bibliography[0]

                # Enrich fields of matching entries
                existing_field_names_in_matching_entry_of_this_bibliography = list(matching_entry_in_this_bibliography[0].keys())
                for each_field_name_in_entry_from_other_bibliography, each_field_value_in_entry_from_other_bibliography in each_entry_data_in_other_bibliography.items():

                    if each_field_name_in_entry_from_other_bibliography not in existing_field_names_in_matching_entry_of_this_bibliography:
                        instance.entries[matching_entry_id_in_this_bibliography][each_field_name_in_entry_from_other_bibliography] \
                            = each_field_value_in_entry_from_other_bibliography

                        # Logging
                        instance.no_of_existing_fields_enriched_in_last_operation += 1
                        last_entry_is_enriched = True

                    else:  # if field already exists in self bibliography, do nothing
                        pass
            # TODO: Merge function is not thoroughly tested and it should be
            except:  # if the field name and value from the other bib is not found
               if method == 'merge':  # add field name and value to a new entry (if in merge mode)
                   for each_field_name_in_entry_from_other_bibliography, each_field_value_in_entry_from_other_bibliography in each_entry_data_in_other_bibliography.items():
                       instance.setEntry(each_entry_id_in_other_bibliography, each_field_name_in_entry_from_other_bibliography, each_field_value_in_entry_from_other_bibliography)

   ###### Logging ######################################################################################################
                       instance.no_of_fields_added_in_last_operation += 1

                   last_entry_is_added = True
               else:  # not in merge mode, do nothing
                   pass

            if last_entry_is_enriched:
                instance.no_of_entries_enriched_in_last_operation += 1
            elif last_entry_is_added:
                instance.no_of_entries_added_in_last_operation += 1

        lines_of_console_message = [
            'Existing entries enriched: %d' % instance.no_of_entries_enriched_in_last_operation,
            'Fields added to existing entries: %d' % instance.no_of_existing_fields_enriched_in_last_operation,
            'New entries added: %d' % instance.no_of_entries_added_in_last_operation
            #'New fields added with new entries: %d' % instance.no_of_fields_added_in_last_operation #  currently
                                                                                        # ... unnecessary  to report
        ]
        from meta.consoleOutput import ConsoleOutput
        console = ConsoleOutput('log.txt')
        console.log_list_with_caption('\nEnrichment completed successfully.', lines_of_console_message,
                                      print_list_length_with_caption=False, add_timestamp_in_file=True)
    ###### Logging END #################################################################################################

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

        field_value_is_empty = False
        if field_value == None or field_value == ' ' or field_value == '_':
            field_value_is_empty = True

        field_name_already_in_registry = False
        if field_name in instance._field_type_registry:
            field_name_already_in_registry = True


        if not field_value_is_empty:
            if not field_name_already_in_registry:
                instance._field_type_registry[field_name] = 1
            else:
                instance._field_type_registry[field_name] += 1


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
        list_data_bibliography.import_bibliography_object(instance)
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

        "oc_select_first_item_if_list" (algorithm): 'oc' prefix stands for 'OpenCitations' and these cleaning procedures
            are made for OpenCitations data.

        "oc_select_last_item_if_list_and_capitalize_first_letter" (algorithm)

        "oc_select_last_item_if_list" (algorithm)

        "capitalize_first_letter" (algorithm)

        "none" (algorithm)

    Raises:
        Keyword Error: Keyword for 'algorithm' parameter does not exist.

    Returns:
        A version of the inputted values that is formatted according the specified algorithm.
        Some algorithms and their corresponding outputs:

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
                               "open_citations_author_label",
                               "oc_select_first_item_if_list",
                               "oc_select_last_item_if_list_and_capitalize_first_letter",
                               "oc_select_last_item_if_list",
                               "capitalize_first_letter",
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
        from preprocessor.string_tools import Parameter_Value
        target_field = Parameter_Value(target_field).convert_to_single_item_list_if_not_list()
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
    #                           MINIMIZE LISTS                                   #
    # ---------------------------------------------------------------------------#
    # TODO: These list minimization/selection functions should be replaced with more graceful equivalents.
    elif algorithm is "oc_select_first_item_if_list":
        if type(target_field) is list:
            inputted_list = target_field
            return inputted_list[0]
        else:
            return target_field

    elif algorithm is "oc_select_last_item_if_list_and_capitalize_first_letter":
        from preprocessor.string_tools import String

        if type(target_field) is list:
            selected_element = target_field[-1]
        else:
            selected_element = target_field

        formatted_element = String(selected_element).capitalize_first_letter().content
        return formatted_element


    elif algorithm is "oc_select_last_item_if_list":
        from preprocessor.string_tools import String

        if type(target_field) is list:
            selected_element = target_field[-1]
        else:
            selected_element = target_field

        return selected_element


    elif algorithm is "capitalize_first_letter":
        from preprocessor.string_tools import String
        from preprocessor.string_tools import Parameter_Value
        inputted_list = Parameter_Value(target_field).convert_to_single_item_list_if_not_list()
        formatted_list = []

        for each_element in inputted_list:
            each_element = String(each_element).capitalize_first_letter().content
            formatted_list.append(each_element)

        return formatted_list[0]


    # ---------------------------------------------------------------------------#
    #               NO FORMATTING: MINIMIZE LISTS (FOR NOW)                      #
    # ---------------------------------------------------------------------------#
    elif algorithm is "none":
        # if no formatting is wanted, the target field values are returned as they are.
        return target_field


def long_tests():
    """
    Tests with long outputs are being run under this function

    Additional tests for .convert_to_ttl():
        >>> my_bibtex_file = Bibtex_File('example_data//vu_1k_test.bib')
        >>> my_bibtex_file.convert_to_ttl(desired_version_suffix='0.0_test', desired_source_bibliography_name='vu')
        Cleaning of "example_data//vu_1k_test.bib" started
        [------------------------------------------------------------] 0% ...Cleaning example_data//vu_1k_test.bib
        [=-----------------------------------------------------------] 0% ...Cleaning example_data//vu_1k_test.bib
        [=-----------------------------------------------------------] 1% ...Cleaning example_data//vu_1k_test.bib
        [=-----------------------------------------------------------] 2% ...Cleaning example_data//vu_1k_test.bib
        [==----------------------------------------------------------] 2% ...Cleaning example_data//vu_1k_test.bib
        [==----------------------------------------------------------] 3% ...Cleaning example_data//vu_1k_test.bib
        [==----------------------------------------------------------] 4% ...Cleaning example_data//vu_1k_test.bib
        [===---------------------------------------------------------] 4% ...Cleaning example_data//vu_1k_test.bib
        [===---------------------------------------------------------] 5% ...Cleaning example_data//vu_1k_test.bib
        [====--------------------------------------------------------] 5% ...Cleaning example_data//vu_1k_test.bib
        [====--------------------------------------------------------] 6% ...Cleaning example_data//vu_1k_test.bib
        [====--------------------------------------------------------] 7% ...Cleaning example_data//vu_1k_test.bib
        [=====-------------------------------------------------------] 7% ...Cleaning example_data//vu_1k_test.bib
        [=====-------------------------------------------------------] 8% ...Cleaning example_data//vu_1k_test.bib
        [=====-------------------------------------------------------] 9% ...Cleaning example_data//vu_1k_test.bib
        [======------------------------------------------------------] 9% ...Cleaning example_data//vu_1k_test.bib
        [======------------------------------------------------------] 10% ...Cleaning example_data//vu_1k_test.bib
        [=======-----------------------------------------------------] 10% ...Cleaning example_data//vu_1k_test.bib
        [=======-----------------------------------------------------] 11% ...Cleaning example_data//vu_1k_test.bib
        [=======-----------------------------------------------------] 12% ...Cleaning example_data//vu_1k_test.bib
        [========----------------------------------------------------] 12% ...Cleaning example_data//vu_1k_test.bib
        [========----------------------------------------------------] 13% ...Cleaning example_data//vu_1k_test.bib
        [========----------------------------------------------------] 14% ...Cleaning example_data//vu_1k_test.bib
        [=========---------------------------------------------------] 14% ...Cleaning example_data//vu_1k_test.bib
        [=========---------------------------------------------------] 15% ...Cleaning example_data//vu_1k_test.bib
        [==========--------------------------------------------------] 15% ...Cleaning example_data//vu_1k_test.bib
        [==========--------------------------------------------------] 16% ...Cleaning example_data//vu_1k_test.bib
        [==========--------------------------------------------------] 17% ...Cleaning example_data//vu_1k_test.bib
        [===========-------------------------------------------------] 17% ...Cleaning example_data//vu_1k_test.bib
        [===========-------------------------------------------------] 18% ...Cleaning example_data//vu_1k_test.bib
        [===========-------------------------------------------------] 19% ...Cleaning example_data//vu_1k_test.bib
        [============------------------------------------------------] 19% ...Cleaning example_data//vu_1k_test.bib
        [============------------------------------------------------] 20% ...Cleaning example_data//vu_1k_test.bib
        [=============-----------------------------------------------] 20% ...Cleaning example_data//vu_1k_test.bib
        [=============-----------------------------------------------] 21% ...Cleaning example_data//vu_1k_test.bib
        [=============-----------------------------------------------] 22% ...Cleaning example_data//vu_1k_test.bib
        [==============----------------------------------------------] 22% ...Cleaning example_data//vu_1k_test.bib
        [==============----------------------------------------------] 23% ...Cleaning example_data//vu_1k_test.bib
        [==============----------------------------------------------] 24% ...Cleaning example_data//vu_1k_test.bib
        [===============---------------------------------------------] 24% ...Cleaning example_data//vu_1k_test.bib
        [===============---------------------------------------------] 25% ...Cleaning example_data//vu_1k_test.bib
        [================--------------------------------------------] 25% ...Cleaning example_data//vu_1k_test.bib
        [================--------------------------------------------] 26% ...Cleaning example_data//vu_1k_test.bib
        [================--------------------------------------------] 27% ...Cleaning example_data//vu_1k_test.bib
        [=================-------------------------------------------] 27% ...Cleaning example_data//vu_1k_test.bib
        [=================-------------------------------------------] 28% ...Cleaning example_data//vu_1k_test.bib
        [=================-------------------------------------------] 29% ...Cleaning example_data//vu_1k_test.bib
        [==================------------------------------------------] 29% ...Cleaning example_data//vu_1k_test.bib
        [==================------------------------------------------] 30% ...Cleaning example_data//vu_1k_test.bib
        [===================-----------------------------------------] 30% ...Cleaning example_data//vu_1k_test.bib
        [===================-----------------------------------------] 31% ...Cleaning example_data//vu_1k_test.bib
        [===================-----------------------------------------] 32% ...Cleaning example_data//vu_1k_test.bib
        [====================----------------------------------------] 32% ...Cleaning example_data//vu_1k_test.bib
        [====================----------------------------------------] 33% ...Cleaning example_data//vu_1k_test.bib
        [====================----------------------------------------] 34% ...Cleaning example_data//vu_1k_test.bib
        [=====================---------------------------------------] 34% ...Cleaning example_data//vu_1k_test.bib
        [=====================---------------------------------------] 35% ...Cleaning example_data//vu_1k_test.bib
        [======================--------------------------------------] 35% ...Cleaning example_data//vu_1k_test.bib
        [======================--------------------------------------] 36% ...Cleaning example_data//vu_1k_test.bib
        [======================--------------------------------------] 37% ...Cleaning example_data//vu_1k_test.bib
        [=======================-------------------------------------] 37% ...Cleaning example_data//vu_1k_test.bib
        [=======================-------------------------------------] 38% ...Cleaning example_data//vu_1k_test.bib
        [=======================-------------------------------------] 39% ...Cleaning example_data//vu_1k_test.bib
        [========================------------------------------------] 39% ...Cleaning example_data//vu_1k_test.bib
        [========================------------------------------------] 40% ...Cleaning example_data//vu_1k_test.bib
        [=========================-----------------------------------] 40% ...Cleaning example_data//vu_1k_test.bib
        [=========================-----------------------------------] 41% ...Cleaning example_data//vu_1k_test.bib
        [=========================-----------------------------------] 42% ...Cleaning example_data//vu_1k_test.bib
        [==========================----------------------------------] 42% ...Cleaning example_data//vu_1k_test.bib
        [==========================----------------------------------] 43% ...Cleaning example_data//vu_1k_test.bib
        [==========================----------------------------------] 44% ...Cleaning example_data//vu_1k_test.bib
        [===========================---------------------------------] 44% ...Cleaning example_data//vu_1k_test.bib
        [===========================---------------------------------] 45% ...Cleaning example_data//vu_1k_test.bib
        [============================--------------------------------] 45% ...Cleaning example_data//vu_1k_test.bib
        [============================--------------------------------] 46% ...Cleaning example_data//vu_1k_test.bib
        [============================--------------------------------] 47% ...Cleaning example_data//vu_1k_test.bib
        [=============================-------------------------------] 47% ...Cleaning example_data//vu_1k_test.bib
        [=============================-------------------------------] 48% ...Cleaning example_data//vu_1k_test.bib
        [=============================-------------------------------] 49% ...Cleaning example_data//vu_1k_test.bib
        [==============================------------------------------] 49% ...Cleaning example_data//vu_1k_test.bib
        [==============================------------------------------] 50% ...Cleaning example_data//vu_1k_test.bib
        [===============================-----------------------------] 50% ...Cleaning example_data//vu_1k_test.bib
        [===============================-----------------------------] 51% ...Cleaning example_data//vu_1k_test.bib
        [===============================-----------------------------] 52% ...Cleaning example_data//vu_1k_test.bib
        [================================----------------------------] 52% ...Cleaning example_data//vu_1k_test.bib
        [================================----------------------------] 53% ...Cleaning example_data//vu_1k_test.bib
        [================================----------------------------] 54% ...Cleaning example_data//vu_1k_test.bib
        [=================================---------------------------] 54% ...Cleaning example_data//vu_1k_test.bib
        [=================================---------------------------] 55% ...Cleaning example_data//vu_1k_test.bib
        [==================================--------------------------] 55% ...Cleaning example_data//vu_1k_test.bib
        [==================================--------------------------] 56% ...Cleaning example_data//vu_1k_test.bib
        [==================================--------------------------] 57% ...Cleaning example_data//vu_1k_test.bib
        [===================================-------------------------] 57% ...Cleaning example_data//vu_1k_test.bib
        [===================================-------------------------] 58% ...Cleaning example_data//vu_1k_test.bib
        [===================================-------------------------] 59% ...Cleaning example_data//vu_1k_test.bib
        [====================================------------------------] 59% ...Cleaning example_data//vu_1k_test.bib
        [====================================------------------------] 60% ...Cleaning example_data//vu_1k_test.bib
        [=====================================-----------------------] 60% ...Cleaning example_data//vu_1k_test.bib
        [=====================================-----------------------] 61% ...Cleaning example_data//vu_1k_test.bib
        [=====================================-----------------------] 62% ...Cleaning example_data//vu_1k_test.bib
        [======================================----------------------] 62% ...Cleaning example_data//vu_1k_test.bib
        [======================================----------------------] 63% ...Cleaning example_data//vu_1k_test.bib
        [======================================----------------------] 64% ...Cleaning example_data//vu_1k_test.bib
        [=======================================---------------------] 64% ...Cleaning example_data//vu_1k_test.bib
        [=======================================---------------------] 65% ...Cleaning example_data//vu_1k_test.bib
        [========================================--------------------] 65% ...Cleaning example_data//vu_1k_test.bib
        [========================================--------------------] 66% ...Cleaning example_data//vu_1k_test.bib
        [========================================--------------------] 67% ...Cleaning example_data//vu_1k_test.bib
        [=========================================-------------------] 67% ...Cleaning example_data//vu_1k_test.bib
        [=========================================-------------------] 68% ...Cleaning example_data//vu_1k_test.bib
        [=========================================-------------------] 69% ...Cleaning example_data//vu_1k_test.bib
        [==========================================------------------] 69% ...Cleaning example_data//vu_1k_test.bib
        [==========================================------------------] 70% ...Cleaning example_data//vu_1k_test.bib
        [===========================================-----------------] 70% ...Cleaning example_data//vu_1k_test.bib
        [===========================================-----------------] 71% ...Cleaning example_data//vu_1k_test.bib
        [===========================================-----------------] 72% ...Cleaning example_data//vu_1k_test.bib
        [============================================----------------] 72% ...Cleaning example_data//vu_1k_test.bib
        [============================================----------------] 73% ...Cleaning example_data//vu_1k_test.bib
        [============================================----------------] 74% ...Cleaning example_data//vu_1k_test.bib
        [=============================================---------------] 74% ...Cleaning example_data//vu_1k_test.bib
        [=============================================---------------] 75% ...Cleaning example_data//vu_1k_test.bib
        [==============================================--------------] 75% ...Cleaning example_data//vu_1k_test.bib
        [==============================================--------------] 76% ...Cleaning example_data//vu_1k_test.bib
        [==============================================--------------] 77% ...Cleaning example_data//vu_1k_test.bib
        [===============================================-------------] 77% ...Cleaning example_data//vu_1k_test.bib
        [===============================================-------------] 78% ...Cleaning example_data//vu_1k_test.bib
        [===============================================-------------] 79% ...Cleaning example_data//vu_1k_test.bib
        [================================================------------] 79% ...Cleaning example_data//vu_1k_test.bib
        [================================================------------] 80% ...Cleaning example_data//vu_1k_test.bib
        [=================================================-----------] 80% ...Cleaning example_data//vu_1k_test.bib
        [=================================================-----------] 81% ...Cleaning example_data//vu_1k_test.bib
        [=================================================-----------] 82% ...Cleaning example_data//vu_1k_test.bib
        [==================================================----------] 82% ...Cleaning example_data//vu_1k_test.bib
        [==================================================----------] 83% ...Cleaning example_data//vu_1k_test.bib
        [==================================================----------] 84% ...Cleaning example_data//vu_1k_test.bib
        [===================================================---------] 84% ...Cleaning example_data//vu_1k_test.bib
        [===================================================---------] 85% ...Cleaning example_data//vu_1k_test.bib
        [====================================================--------] 85% ...Cleaning example_data//vu_1k_test.bib
        [====================================================--------] 86% ...Cleaning example_data//vu_1k_test.bib
        [====================================================--------] 87% ...Cleaning example_data//vu_1k_test.bib
        [=====================================================-------] 87% ...Cleaning example_data//vu_1k_test.bib
        [=====================================================-------] 88% ...Cleaning example_data//vu_1k_test.bib
        [=====================================================-------] 89% ...Cleaning example_data//vu_1k_test.bib
        [======================================================------] 89% ...Cleaning example_data//vu_1k_test.bib
        [======================================================------] 90% ...Cleaning example_data//vu_1k_test.bib
        [=======================================================-----] 90% ...Cleaning example_data//vu_1k_test.bib
        [=======================================================-----] 91% ...Cleaning example_data//vu_1k_test.bib
        [=======================================================-----] 92% ...Cleaning example_data//vu_1k_test.bib
        [========================================================----] 92% ...Cleaning example_data//vu_1k_test.bib
        [========================================================----] 93% ...Cleaning example_data//vu_1k_test.bib
        [========================================================----] 94% ...Cleaning example_data//vu_1k_test.bib
        [=========================================================---] 94% ...Cleaning example_data//vu_1k_test.bib
        [=========================================================---] 95% ...Cleaning example_data//vu_1k_test.bib
        [==========================================================--] 95% ...Cleaning example_data//vu_1k_test.bib
        [==========================================================--] 96% ...Cleaning example_data//vu_1k_test.bib
        [==========================================================--] 97% ...Cleaning example_data//vu_1k_test.bib
        [===========================================================-] 97% ...Cleaning example_data//vu_1k_test.bib
        [===========================================================-] 98% ...Cleaning example_data//vu_1k_test.bib
        [===========================================================-] 99% ...Cleaning example_data//vu_1k_test.bib
        [============================================================] 99% ...Cleaning example_data//vu_1k_test.bib
        Cleaning of "example_data//vu_1k_test.bib" finished
        Parsing of example_data//vu_1k_test_cleaned.bib started
        pybtex package is parsing using bibtex.Parser()...
        pybtex package finished parsing
        Calculating file length...
        [------------------------------------------------------------] 0% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=-----------------------------------------------------------] 1% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=-----------------------------------------------------------] 2% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [==----------------------------------------------------------] 3% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [===---------------------------------------------------------] 4% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [===---------------------------------------------------------] 5% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [====--------------------------------------------------------] 6% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=====-------------------------------------------------------] 7% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=====-------------------------------------------------------] 8% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [======------------------------------------------------------] 9% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=======-----------------------------------------------------] 11% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=======-----------------------------------------------------] 12% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [========----------------------------------------------------] 13% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=========---------------------------------------------------] 14% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=========---------------------------------------------------] 15% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [==========--------------------------------------------------] 16% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [===========-------------------------------------------------] 17% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [===========-------------------------------------------------] 18% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [============------------------------------------------------] 19% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=============-----------------------------------------------] 20% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=============-----------------------------------------------] 22% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [==============----------------------------------------------] 23% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [===============---------------------------------------------] 24% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [===============---------------------------------------------] 25% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [================--------------------------------------------] 26% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [================--------------------------------------------] 27% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=================-------------------------------------------] 28% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [==================------------------------------------------] 29% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [==================------------------------------------------] 30% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [===================-----------------------------------------] 31% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [====================----------------------------------------] 33% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [====================----------------------------------------] 34% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=====================---------------------------------------] 35% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [======================--------------------------------------] 36% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [======================--------------------------------------] 37% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=======================-------------------------------------] 38% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [========================------------------------------------] 39% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [========================------------------------------------] 40% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=========================-----------------------------------] 41% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [==========================----------------------------------] 42% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [==========================----------------------------------] 44% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [===========================---------------------------------] 45% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [============================--------------------------------] 46% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [============================--------------------------------] 47% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=============================-------------------------------] 48% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [==============================------------------------------] 49% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [==============================------------------------------] 50% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [===============================-----------------------------] 51% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [================================----------------------------] 52% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [================================----------------------------] 53% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=================================---------------------------] 54% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [==================================--------------------------] 56% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [==================================--------------------------] 57% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [===================================-------------------------] 58% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [====================================------------------------] 59% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [====================================------------------------] 60% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=====================================-----------------------] 61% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [======================================----------------------] 62% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [======================================----------------------] 63% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=======================================---------------------] 64% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [========================================--------------------] 65% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [========================================--------------------] 67% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=========================================-------------------] 68% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [==========================================------------------] 69% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [==========================================------------------] 70% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [===========================================-----------------] 71% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [============================================----------------] 72% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [============================================----------------] 73% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=============================================---------------] 74% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=============================================---------------] 75% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [==============================================--------------] 76% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [===============================================-------------] 78% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [===============================================-------------] 79% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [================================================------------] 80% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=================================================-----------] 81% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=================================================-----------] 82% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [==================================================----------] 83% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [===================================================---------] 84% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [===================================================---------] 85% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [====================================================--------] 86% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=====================================================-------] 87% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=====================================================-------] 89% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [======================================================------] 90% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=======================================================-----] 91% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=======================================================-----] 92% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [========================================================----] 93% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=========================================================---] 94% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [=========================================================---] 95% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [==========================================================--] 96% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [===========================================================-] 97% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        [===========================================================-] 98% ...Parsing file "example_data//vu_1k_test_cleaned.bib"
        <BLANKLINE>
        <BLANKLINE>
        ---------------------------------------------------------------------------------------------------
        example_data//vu_1k_test_cleaned.bib parsed and imported as Bibliography object.
        <BLANKLINE>
        Fields added to the parsed the Bibliography object:
        {'b_abstract': 20,
         'b_author_labels': 91,
         'b_authors': 91,
         'b_document': 91,
         'b_document_label': 91,
         'b_doi': 18,
         'b_edition': 3,
         'b_isbn': 7,
         'b_issn': 20,
         'b_issue_number': 5,
         'b_journal': 21,
         'b_journal_label': 21,
         'b_note': 28,
         'b_pages': 17,
         'b_parent_book': 34,
         'b_parent_book_label': 34,
         'b_publication_month': 32,
         'b_publication_year': 91,
         'b_publisher': 56,
         'b_publisher_label': 56,
         'b_pure_bibliography_id': 91,
         'b_topic_labels': 14,
         'b_topics': 14,
         'b_type': 91,
         'b_volume': 18}
        <BLANKLINE>
        <BLANKLINE>
        [------------------------------------------------------------] 0% ...Converting Bibliography object to Triples object.
        [=-----------------------------------------------------------] 1% ...Converting Bibliography object to Triples object.
        [=-----------------------------------------------------------] 2% ...Converting Bibliography object to Triples object.
        [==----------------------------------------------------------] 3% ...Converting Bibliography object to Triples object.
        [===---------------------------------------------------------] 4% ...Converting Bibliography object to Triples object.
        [===---------------------------------------------------------] 5% ...Converting Bibliography object to Triples object.
        [====--------------------------------------------------------] 6% ...Converting Bibliography object to Triples object.
        [=====-------------------------------------------------------] 7% ...Converting Bibliography object to Triples object.
        [=====-------------------------------------------------------] 8% ...Converting Bibliography object to Triples object.
        [======------------------------------------------------------] 9% ...Converting Bibliography object to Triples object.
        [=======-----------------------------------------------------] 11% ...Converting Bibliography object to Triples object.
        [=======-----------------------------------------------------] 12% ...Converting Bibliography object to Triples object.
        [========----------------------------------------------------] 13% ...Converting Bibliography object to Triples object.
        [=========---------------------------------------------------] 14% ...Converting Bibliography object to Triples object.
        [=========---------------------------------------------------] 15% ...Converting Bibliography object to Triples object.
        [==========--------------------------------------------------] 16% ...Converting Bibliography object to Triples object.
        [===========-------------------------------------------------] 17% ...Converting Bibliography object to Triples object.
        [===========-------------------------------------------------] 18% ...Converting Bibliography object to Triples object.
        [============------------------------------------------------] 19% ...Converting Bibliography object to Triples object.
        [=============-----------------------------------------------] 20% ...Converting Bibliography object to Triples object.
        [=============-----------------------------------------------] 22% ...Converting Bibliography object to Triples object.
        [==============----------------------------------------------] 23% ...Converting Bibliography object to Triples object.
        [===============---------------------------------------------] 24% ...Converting Bibliography object to Triples object.
        [===============---------------------------------------------] 25% ...Converting Bibliography object to Triples object.
        [================--------------------------------------------] 26% ...Converting Bibliography object to Triples object.
        [================--------------------------------------------] 27% ...Converting Bibliography object to Triples object.
        [=================-------------------------------------------] 28% ...Converting Bibliography object to Triples object.
        [==================------------------------------------------] 29% ...Converting Bibliography object to Triples object.
        [==================------------------------------------------] 30% ...Converting Bibliography object to Triples object.
        [===================-----------------------------------------] 31% ...Converting Bibliography object to Triples object.
        [====================----------------------------------------] 33% ...Converting Bibliography object to Triples object.
        [====================----------------------------------------] 34% ...Converting Bibliography object to Triples object.
        [=====================---------------------------------------] 35% ...Converting Bibliography object to Triples object.
        [======================--------------------------------------] 36% ...Converting Bibliography object to Triples object.
        [======================--------------------------------------] 37% ...Converting Bibliography object to Triples object.
        [=======================-------------------------------------] 38% ...Converting Bibliography object to Triples object.
        [========================------------------------------------] 39% ...Converting Bibliography object to Triples object.
        [========================------------------------------------] 40% ...Converting Bibliography object to Triples object.
        [=========================-----------------------------------] 41% ...Converting Bibliography object to Triples object.
        [==========================----------------------------------] 42% ...Converting Bibliography object to Triples object.
        [==========================----------------------------------] 44% ...Converting Bibliography object to Triples object.
        [===========================---------------------------------] 45% ...Converting Bibliography object to Triples object.
        [============================--------------------------------] 46% ...Converting Bibliography object to Triples object.
        [============================--------------------------------] 47% ...Converting Bibliography object to Triples object.
        [=============================-------------------------------] 48% ...Converting Bibliography object to Triples object.
        [==============================------------------------------] 49% ...Converting Bibliography object to Triples object.
        [==============================------------------------------] 50% ...Converting Bibliography object to Triples object.
        [===============================-----------------------------] 51% ...Converting Bibliography object to Triples object.
        [================================----------------------------] 52% ...Converting Bibliography object to Triples object.
        [================================----------------------------] 53% ...Converting Bibliography object to Triples object.
        [=================================---------------------------] 54% ...Converting Bibliography object to Triples object.
        [==================================--------------------------] 56% ...Converting Bibliography object to Triples object.
        [==================================--------------------------] 57% ...Converting Bibliography object to Triples object.
        [===================================-------------------------] 58% ...Converting Bibliography object to Triples object.
        [====================================------------------------] 59% ...Converting Bibliography object to Triples object.
        [====================================------------------------] 60% ...Converting Bibliography object to Triples object.
        [=====================================-----------------------] 61% ...Converting Bibliography object to Triples object.
        [======================================----------------------] 62% ...Converting Bibliography object to Triples object.
        [======================================----------------------] 63% ...Converting Bibliography object to Triples object.
        [=======================================---------------------] 64% ...Converting Bibliography object to Triples object.
        [========================================--------------------] 65% ...Converting Bibliography object to Triples object.
        [========================================--------------------] 67% ...Converting Bibliography object to Triples object.
        [=========================================-------------------] 68% ...Converting Bibliography object to Triples object.
        [==========================================------------------] 69% ...Converting Bibliography object to Triples object.
        [==========================================------------------] 70% ...Converting Bibliography object to Triples object.
        [===========================================-----------------] 71% ...Converting Bibliography object to Triples object.
        [============================================----------------] 72% ...Converting Bibliography object to Triples object.
        [============================================----------------] 73% ...Converting Bibliography object to Triples object.
        [=============================================---------------] 74% ...Converting Bibliography object to Triples object.
        [=============================================---------------] 75% ...Converting Bibliography object to Triples object.
        [==============================================--------------] 76% ...Converting Bibliography object to Triples object.
        [===============================================-------------] 78% ...Converting Bibliography object to Triples object.
        [===============================================-------------] 79% ...Converting Bibliography object to Triples object.
        [================================================------------] 80% ...Converting Bibliography object to Triples object.
        [=================================================-----------] 81% ...Converting Bibliography object to Triples object.
        [=================================================-----------] 82% ...Converting Bibliography object to Triples object.
        [==================================================----------] 83% ...Converting Bibliography object to Triples object.
        [===================================================---------] 84% ...Converting Bibliography object to Triples object.
        [===================================================---------] 85% ...Converting Bibliography object to Triples object.
        [====================================================--------] 86% ...Converting Bibliography object to Triples object.
        [=====================================================-------] 87% ...Converting Bibliography object to Triples object.
        [=====================================================-------] 89% ...Converting Bibliography object to Triples object.
        [======================================================------] 90% ...Converting Bibliography object to Triples object.
        [=======================================================-----] 91% ...Converting Bibliography object to Triples object.
        [=======================================================-----] 92% ...Converting Bibliography object to Triples object.
        [========================================================----] 93% ...Converting Bibliography object to Triples object.
        [=========================================================---] 94% ...Converting Bibliography object to Triples object.
        [=========================================================---] 95% ...Converting Bibliography object to Triples object.
        [==========================================================--] 96% ...Converting Bibliography object to Triples object.
        [===========================================================-] 97% ...Converting Bibliography object to Triples object.
        [===========================================================-] 98% ...Converting Bibliography object to Triples object.
        Calculating the length of the Triples object
        Writing of the triples to file "vu_1k_test_0.0_test.ttl" has started
        [------------------------------------------------------------] 0% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=-----------------------------------------------------------] 0% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=-----------------------------------------------------------] 1% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=-----------------------------------------------------------] 2% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==----------------------------------------------------------] 2% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==----------------------------------------------------------] 3% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==----------------------------------------------------------] 4% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===---------------------------------------------------------] 4% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===---------------------------------------------------------] 5% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [====--------------------------------------------------------] 5% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [====--------------------------------------------------------] 6% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [====--------------------------------------------------------] 7% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=====-------------------------------------------------------] 7% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=====-------------------------------------------------------] 8% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=====-------------------------------------------------------] 9% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [======------------------------------------------------------] 9% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [======------------------------------------------------------] 10% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=======-----------------------------------------------------] 10% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=======-----------------------------------------------------] 11% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=======-----------------------------------------------------] 12% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [========----------------------------------------------------] 12% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [========----------------------------------------------------] 13% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [========----------------------------------------------------] 14% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=========---------------------------------------------------] 14% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=========---------------------------------------------------] 15% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==========--------------------------------------------------] 15% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==========--------------------------------------------------] 16% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==========--------------------------------------------------] 17% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===========-------------------------------------------------] 17% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===========-------------------------------------------------] 18% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===========-------------------------------------------------] 19% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [============------------------------------------------------] 19% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [============------------------------------------------------] 20% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=============-----------------------------------------------] 20% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=============-----------------------------------------------] 21% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=============-----------------------------------------------] 22% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==============----------------------------------------------] 22% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==============----------------------------------------------] 23% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==============----------------------------------------------] 24% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===============---------------------------------------------] 24% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===============---------------------------------------------] 25% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [================--------------------------------------------] 25% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [================--------------------------------------------] 26% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [================--------------------------------------------] 27% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=================-------------------------------------------] 27% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=================-------------------------------------------] 28% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=================-------------------------------------------] 29% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==================------------------------------------------] 29% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==================------------------------------------------] 30% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===================-----------------------------------------] 30% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===================-----------------------------------------] 31% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===================-----------------------------------------] 32% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [====================----------------------------------------] 32% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [====================----------------------------------------] 33% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [====================----------------------------------------] 34% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=====================---------------------------------------] 34% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=====================---------------------------------------] 35% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [======================--------------------------------------] 35% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [======================--------------------------------------] 36% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [======================--------------------------------------] 37% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=======================-------------------------------------] 37% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=======================-------------------------------------] 38% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=======================-------------------------------------] 39% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [========================------------------------------------] 39% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [========================------------------------------------] 40% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=========================-----------------------------------] 40% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=========================-----------------------------------] 41% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=========================-----------------------------------] 42% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==========================----------------------------------] 42% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==========================----------------------------------] 43% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==========================----------------------------------] 44% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===========================---------------------------------] 44% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===========================---------------------------------] 45% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [============================--------------------------------] 45% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [============================--------------------------------] 46% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [============================--------------------------------] 47% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=============================-------------------------------] 47% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=============================-------------------------------] 48% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=============================-------------------------------] 49% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==============================------------------------------] 49% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==============================------------------------------] 50% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===============================-----------------------------] 50% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===============================-----------------------------] 51% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===============================-----------------------------] 52% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [================================----------------------------] 52% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [================================----------------------------] 53% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [================================----------------------------] 54% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=================================---------------------------] 54% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=================================---------------------------] 55% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==================================--------------------------] 55% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==================================--------------------------] 56% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==================================--------------------------] 57% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===================================-------------------------] 57% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===================================-------------------------] 58% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===================================-------------------------] 59% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [====================================------------------------] 59% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [====================================------------------------] 60% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=====================================-----------------------] 60% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=====================================-----------------------] 61% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=====================================-----------------------] 62% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [======================================----------------------] 62% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [======================================----------------------] 63% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [======================================----------------------] 64% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=======================================---------------------] 64% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=======================================---------------------] 65% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [========================================--------------------] 65% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [========================================--------------------] 66% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [========================================--------------------] 67% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=========================================-------------------] 67% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=========================================-------------------] 68% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=========================================-------------------] 69% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==========================================------------------] 69% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==========================================------------------] 70% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===========================================-----------------] 70% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===========================================-----------------] 71% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===========================================-----------------] 72% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [============================================----------------] 72% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [============================================----------------] 73% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [============================================----------------] 74% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=============================================---------------] 74% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=============================================---------------] 75% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==============================================--------------] 75% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==============================================--------------] 76% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==============================================--------------] 77% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===============================================-------------] 77% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===============================================-------------] 78% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===============================================-------------] 79% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [================================================------------] 79% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [================================================------------] 80% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=================================================-----------] 80% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=================================================-----------] 81% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=================================================-----------] 82% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==================================================----------] 82% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==================================================----------] 83% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==================================================----------] 84% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===================================================---------] 84% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===================================================---------] 85% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [====================================================--------] 85% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [====================================================--------] 86% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [====================================================--------] 87% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=====================================================-------] 87% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=====================================================-------] 88% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=====================================================-------] 89% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [======================================================------] 89% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [======================================================------] 90% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=======================================================-----] 90% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=======================================================-----] 91% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=======================================================-----] 92% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [========================================================----] 92% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [========================================================----] 93% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [========================================================----] 94% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=========================================================---] 94% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [=========================================================---] 95% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==========================================================--] 95% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==========================================================--] 96% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [==========================================================--] 97% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===========================================================-] 97% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===========================================================-] 98% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [===========================================================-] 99% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [============================================================] 99% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        [============================================================] 100% ...Writing triples to "vu_1k_test_0.0_test.ttl"
        Success: 2088 triples were written to "vu_1k_test_0.0_test.ttl"
        These items were skipped due to errors (0 items):
        <BLANKLINE>
        A log of the operation is kept in "log.txt"

        >>> from preprocessor.Text_File import Text_File
        >>> my_ttl_file = Text_File('vu_1k_test_0.0_test.ttl')
        >>> my_ttl_file.preview(250)
        <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#isAuthorOf> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#hasAuthor> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#isPublishedOn> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#isPublishedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#isPublishedOnYear> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#isPublishedOnMonth> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#isPublishedOnDate> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#hasDOI> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#hasISSN> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#hasISBN> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#hasPureBibliographyID> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#hasOpenCitationsID> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#isChapterOf> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://www.w3.org/2000/01/rdf-schema#label> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#hasTopic> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#hasAbstract> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#hasCited> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#isCitedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://www.w3.org/2002/07/owl#equivalentClass> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#ObjectProperty> .
        <http://clokman.com/kfir/ontology#Topic> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> .
        <http://clokman.com/kfir/resource#vu> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> .
        <http://clokman.com/kfir/resource#vu> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/resource#Bibliography> .
        <http://clokman.com/kfir/ontology#JournalArticle> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> .
        <http://clokman.com/kfir/ontology#Book> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> .
        <http://clokman.com/kfir/ontology#BookChapter> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> .
        <http://clokman.com/kfir/ontology#Miscellaneous> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> .
        <http://clokman.com/kfir/resource#a1f8850ca82a4fb89aab8db2a49f8fa1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#a1f8850ca82a4fb89aab8db2a49f8fa1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#a1f8850ca82a4fb89aab8db2a49f8fa1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Misc> .
        <http://clokman.com/kfir/ontology#Misc> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#a1f8850ca82a4fb89aab8db2a49f8fa1> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#vu> .
        <http://clokman.com/kfir/resource#a1f8850ca82a4fb89aab8db2a49f8fa1> <http://www.w3.org/2000/01/rdf-schema#label> "Geloof en rechtvaardiging"@en .
        <http://clokman.com/kfir/resource#Agteresch_HJ> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#a1f8850ca82a4fb89aab8db2a49f8fa1> .
        <http://clokman.com/kfir/resource#a1f8850ca82a4fb89aab8db2a49f8fa1> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#Agteresch_HJ> .
        <http://clokman.com/kfir/resource#Agteresch_HJ> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#Agteresch_HJ> <http://www.w3.org/2000/01/rdf-schema#label> "Agteresch, HJ"@en .
        <http://clokman.com/kfir/resource#a1f8850ca82a4fb89aab8db2a49f8fa1> <http://clokman.com/kfir/ontology#isPublishedOnYear> "2023" .
        <http://clokman.com/kfir/resource#a1f8850ca82a4fb89aab8db2a49f8fa1> <http://clokman.com/kfir/ontology#hasPureBibliographyID> "a1f8850ca82a4fb89aab8db2a49f8fa1" .
        <http://clokman.com/kfir/resource#61d5cb748d514012b7ecba7bfd6dd745> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#61d5cb748d514012b7ecba7bfd6dd745> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#61d5cb748d514012b7ecba7bfd6dd745> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Misc> .
        <http://clokman.com/kfir/ontology#Misc> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#61d5cb748d514012b7ecba7bfd6dd745> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#vu> .
        <http://clokman.com/kfir/resource#61d5cb748d514012b7ecba7bfd6dd745> <http://www.w3.org/2000/01/rdf-schema#label> "Gereformeerde katholiciteit in de zeventiende eeuw"@en .
        <http://clokman.com/kfir/resource#Hartevelt_LDA> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#61d5cb748d514012b7ecba7bfd6dd745> .
        <http://clokman.com/kfir/resource#61d5cb748d514012b7ecba7bfd6dd745> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#Hartevelt_LDA> .
        <http://clokman.com/kfir/resource#Hartevelt_LDA> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#Hartevelt_LDA> <http://www.w3.org/2000/01/rdf-schema#label> "Hartevelt, LDA"@en .
        <http://clokman.com/kfir/resource#61d5cb748d514012b7ecba7bfd6dd745> <http://clokman.com/kfir/ontology#isPublishedOnYear> "2021" .
        <http://clokman.com/kfir/resource#61d5cb748d514012b7ecba7bfd6dd745> <http://clokman.com/kfir/ontology#hasPureBibliographyID> "61d5cb748d514012b7ecba7bfd6dd745" .
        <http://clokman.com/kfir/resource#5f2ab8884cf8455cac67c15632bbc6a0> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#5f2ab8884cf8455cac67c15632bbc6a0> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#5f2ab8884cf8455cac67c15632bbc6a0> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Misc> .
        <http://clokman.com/kfir/ontology#Misc> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#5f2ab8884cf8455cac67c15632bbc6a0> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#vu> .
        <http://clokman.com/kfir/resource#5f2ab8884cf8455cac67c15632bbc6a0> <http://www.w3.org/2000/01/rdf-schema#label> "Johann Friedrich Stapfer (1708-1775)-Theology, Orthodoxy and Polemics in the Late Orthodoxy Period"@en .
        <http://clokman.com/kfir/resource#Blauw_C> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#5f2ab8884cf8455cac67c15632bbc6a0> .
        <http://clokman.com/kfir/resource#5f2ab8884cf8455cac67c15632bbc6a0> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#Blauw_C> .
        <http://clokman.com/kfir/resource#Blauw_C> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#Blauw_C> <http://www.w3.org/2000/01/rdf-schema#label> "Blauw, C"@en .
        <http://clokman.com/kfir/resource#5f2ab8884cf8455cac67c15632bbc6a0> <http://clokman.com/kfir/ontology#isPublishedOnYear> "2021" .
        <http://clokman.com/kfir/resource#5f2ab8884cf8455cac67c15632bbc6a0> <http://clokman.com/kfir/ontology#hasPureBibliographyID> "5f2ab8884cf8455cac67c15632bbc6a0" .
        <http://clokman.com/kfir/resource#351ffad9f38f44368f9808595d5537bf> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#351ffad9f38f44368f9808595d5537bf> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#351ffad9f38f44368f9808595d5537bf> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Misc> .
        <http://clokman.com/kfir/ontology#Misc> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#351ffad9f38f44368f9808595d5537bf> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#vu> .
        <http://clokman.com/kfir/resource#351ffad9f38f44368f9808595d5537bf> <http://www.w3.org/2000/01/rdf-schema#label> "Liturgy John Owen"@en .
        <http://clokman.com/kfir/resource#Hyde_D> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#351ffad9f38f44368f9808595d5537bf> .
        <http://clokman.com/kfir/resource#351ffad9f38f44368f9808595d5537bf> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#Hyde_D> .
        <http://clokman.com/kfir/resource#Hyde_D> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#Hyde_D> <http://www.w3.org/2000/01/rdf-schema#label> "Hyde, D"@en .
        <http://clokman.com/kfir/resource#351ffad9f38f44368f9808595d5537bf> <http://clokman.com/kfir/ontology#isPublishedOnYear> "2021" .
        <http://clokman.com/kfir/resource#351ffad9f38f44368f9808595d5537bf> <http://clokman.com/kfir/ontology#hasPureBibliographyID> "351ffad9f38f44368f9808595d5537bf" .
        <http://clokman.com/kfir/resource#f1a6e4c09d174631ba2bc5839ce037ea> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#f1a6e4c09d174631ba2bc5839ce037ea> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#f1a6e4c09d174631ba2bc5839ce037ea> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Misc> .
        <http://clokman.com/kfir/ontology#Misc> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#f1a6e4c09d174631ba2bc5839ce037ea> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#vu> .
        <http://clokman.com/kfir/resource#f1a6e4c09d174631ba2bc5839ce037ea> <http://www.w3.org/2000/01/rdf-schema#label> "It Seems Good to the Holy Spirit and Us-How Reformed Churches in America May Move Past Binary and Beyond Opaque into Missional Decision Making"@en .
        <http://clokman.com/kfir/resource#Wilson_M> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#f1a6e4c09d174631ba2bc5839ce037ea> .
        <http://clokman.com/kfir/resource#f1a6e4c09d174631ba2bc5839ce037ea> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#Wilson_M> .
        <http://clokman.com/kfir/resource#Wilson_M> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#Wilson_M> <http://www.w3.org/2000/01/rdf-schema#label> "Wilson, M"@en .
        <http://clokman.com/kfir/resource#f1a6e4c09d174631ba2bc5839ce037ea> <http://clokman.com/kfir/ontology#isPublishedOnYear> "2020" .
        <http://clokman.com/kfir/resource#f1a6e4c09d174631ba2bc5839ce037ea> <http://clokman.com/kfir/ontology#hasPureBibliographyID> "f1a6e4c09d174631ba2bc5839ce037ea" .
        <http://clokman.com/kfir/resource#3bfe0162a51646b48679ebf8ecfa224a> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#3bfe0162a51646b48679ebf8ecfa224a> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#3bfe0162a51646b48679ebf8ecfa224a> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Misc> .
        <http://clokman.com/kfir/ontology#Misc> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#3bfe0162a51646b48679ebf8ecfa224a> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#vu> .
        <http://clokman.com/kfir/resource#3bfe0162a51646b48679ebf8ecfa224a> <http://www.w3.org/2000/01/rdf-schema#label> "N.T. Wright and Missional Hermeneutics"@en .
        <http://clokman.com/kfir/resource#Gonzalez_CJ> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#3bfe0162a51646b48679ebf8ecfa224a> .
        <http://clokman.com/kfir/resource#3bfe0162a51646b48679ebf8ecfa224a> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#Gonzalez_CJ> .
        <http://clokman.com/kfir/resource#Gonzalez_CJ> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#Gonzalez_CJ> <http://www.w3.org/2000/01/rdf-schema#label> "Gonzalez, CJ"@en .
        <http://clokman.com/kfir/resource#3bfe0162a51646b48679ebf8ecfa224a> <http://clokman.com/kfir/ontology#isPublishedOnYear> "2020" .
        <http://clokman.com/kfir/resource#3bfe0162a51646b48679ebf8ecfa224a> <http://clokman.com/kfir/ontology#hasPureBibliographyID> "3bfe0162a51646b48679ebf8ecfa224a" .
        <http://clokman.com/kfir/resource#8c4e14adf9174238be2598a06a4c9525> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#8c4e14adf9174238be2598a06a4c9525> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#8c4e14adf9174238be2598a06a4c9525> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Misc> .
        <http://clokman.com/kfir/ontology#Misc> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#8c4e14adf9174238be2598a06a4c9525> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#vu> .
        <http://clokman.com/kfir/resource#8c4e14adf9174238be2598a06a4c9525> <http://www.w3.org/2000/01/rdf-schema#label> "The Mission of North American Church Planting in Europe-Motivations and effectiveness of North American church planting in continental Europe"@en .
        <http://clokman.com/kfir/resource#Rossi_S> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#8c4e14adf9174238be2598a06a4c9525> .
        <http://clokman.com/kfir/resource#8c4e14adf9174238be2598a06a4c9525> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#Rossi_S> .
        <http://clokman.com/kfir/resource#Rossi_S> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#Rossi_S> <http://www.w3.org/2000/01/rdf-schema#label> "Rossi, S"@en .
        <http://clokman.com/kfir/resource#8c4e14adf9174238be2598a06a4c9525> <http://clokman.com/kfir/ontology#isPublishedOnYear> "2020" .
        <http://clokman.com/kfir/resource#8c4e14adf9174238be2598a06a4c9525> <http://clokman.com/kfir/ontology#hasPureBibliographyID> "8c4e14adf9174238be2598a06a4c9525" .
        <http://clokman.com/kfir/resource#82971e5f9f2d40f0ab69296d2af28c21> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#82971e5f9f2d40f0ab69296d2af28c21> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#82971e5f9f2d40f0ab69296d2af28c21> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Misc> .
        <http://clokman.com/kfir/ontology#Misc> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#82971e5f9f2d40f0ab69296d2af28c21> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#vu> .
        <http://clokman.com/kfir/resource#82971e5f9f2d40f0ab69296d2af28c21> <http://www.w3.org/2000/01/rdf-schema#label> "Typologisch preken"@en .
        <http://clokman.com/kfir/resource#vd_Weg_AAF> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#82971e5f9f2d40f0ab69296d2af28c21> .
        <http://clokman.com/kfir/resource#82971e5f9f2d40f0ab69296d2af28c21> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#vd_Weg_AAF> .
        <http://clokman.com/kfir/resource#vd_Weg_AAF> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#vd_Weg_AAF> <http://www.w3.org/2000/01/rdf-schema#label> "vd_Weg, AAF"@en .
        <http://clokman.com/kfir/resource#82971e5f9f2d40f0ab69296d2af28c21> <http://clokman.com/kfir/ontology#isPublishedOnYear> "2020" .
        <http://clokman.com/kfir/resource#82971e5f9f2d40f0ab69296d2af28c21> <http://clokman.com/kfir/ontology#hasPureBibliographyID> "82971e5f9f2d40f0ab69296d2af28c21" .
        <http://clokman.com/kfir/resource#f9f67ac5cf52469c92c8120aba31e1a4> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#f9f67ac5cf52469c92c8120aba31e1a4> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#f9f67ac5cf52469c92c8120aba31e1a4> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Misc> .
        <http://clokman.com/kfir/ontology#Misc> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#f9f67ac5cf52469c92c8120aba31e1a4> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#vu> .
        <http://clokman.com/kfir/resource#f9f67ac5cf52469c92c8120aba31e1a4> <http://www.w3.org/2000/01/rdf-schema#label> "Ministry and Mission-an investigation of the missional challenges for the Reformed Presbyterian theology of ministry in a post-Christendom age"@en .
        <http://clokman.com/kfir/resource#den_Hertog_RG> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#f9f67ac5cf52469c92c8120aba31e1a4> .
        <http://clokman.com/kfir/resource#f9f67ac5cf52469c92c8120aba31e1a4> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#den_Hertog_RG> .
        <http://clokman.com/kfir/resource#den_Hertog_RG> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#den_Hertog_RG> <http://www.w3.org/2000/01/rdf-schema#label> "den_Hertog, RG"@en .
        <http://clokman.com/kfir/resource#f9f67ac5cf52469c92c8120aba31e1a4> <http://clokman.com/kfir/ontology#isPublishedOnYear> "2019" .
        <http://clokman.com/kfir/resource#f9f67ac5cf52469c92c8120aba31e1a4> <http://clokman.com/kfir/ontology#hasPureBibliographyID> "f9f67ac5cf52469c92c8120aba31e1a4" .
        <http://clokman.com/kfir/resource#d0d9e402bf5d4c90b9f9aa7e31f236d2> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#d0d9e402bf5d4c90b9f9aa7e31f236d2> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#d0d9e402bf5d4c90b9f9aa7e31f236d2> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Misc> .
        <http://clokman.com/kfir/ontology#Misc> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#d0d9e402bf5d4c90b9f9aa7e31f236d2> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#vu> .
        <http://clokman.com/kfir/resource#d0d9e402bf5d4c90b9f9aa7e31f236d2> <http://www.w3.org/2000/01/rdf-schema#label> "PhD begeleiding Sien de Groot, Universiteit Gent, promotor Marc de Groote"@en .
        <http://clokman.com/kfir/resource#van_Opstall_EM> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#d0d9e402bf5d4c90b9f9aa7e31f236d2> .
        <http://clokman.com/kfir/resource#d0d9e402bf5d4c90b9f9aa7e31f236d2> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#van_Opstall_EM> .
        <http://clokman.com/kfir/resource#van_Opstall_EM> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#van_Opstall_EM> <http://www.w3.org/2000/01/rdf-schema#label> "van_Opstall, EM"@en .
        <http://clokman.com/kfir/resource#d0d9e402bf5d4c90b9f9aa7e31f236d2> <http://clokman.com/kfir/ontology#isPublishedOnYear> "2019" .
        <http://clokman.com/kfir/resource#d0d9e402bf5d4c90b9f9aa7e31f236d2> <http://clokman.com/kfir/ontology#hasPureBibliographyID> "d0d9e402bf5d4c90b9f9aa7e31f236d2" .
        <http://clokman.com/kfir/resource#e883e940a6fc42109164e4fd60249f03> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#e883e940a6fc42109164e4fd60249f03> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#e883e940a6fc42109164e4fd60249f03> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Misc> .
        <http://clokman.com/kfir/ontology#Misc> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#e883e940a6fc42109164e4fd60249f03> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#vu> .
        <http://clokman.com/kfir/resource#e883e940a6fc42109164e4fd60249f03> <http://www.w3.org/2000/01/rdf-schema#label> "Reasonableness and Pleasantness of christianity in Matthew Henry"@en .
        <http://clokman.com/kfir/resource#Murray_DP> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#e883e940a6fc42109164e4fd60249f03> .
        <http://clokman.com/kfir/resource#e883e940a6fc42109164e4fd60249f03> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#Murray_DP> .
        <http://clokman.com/kfir/resource#Murray_DP> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#Murray_DP> <http://www.w3.org/2000/01/rdf-schema#label> "Murray, DP"@en .
        <http://clokman.com/kfir/resource#e883e940a6fc42109164e4fd60249f03> <http://clokman.com/kfir/ontology#isPublishedOnYear> "2019" .
        <http://clokman.com/kfir/resource#e883e940a6fc42109164e4fd60249f03> <http://clokman.com/kfir/ontology#hasPureBibliographyID> "e883e940a6fc42109164e4fd60249f03" .
        <http://clokman.com/kfir/resource#445d259ad2454906960165a6bbae883c> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#445d259ad2454906960165a6bbae883c> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#445d259ad2454906960165a6bbae883c> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Misc> .
        <http://clokman.com/kfir/ontology#Misc> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#445d259ad2454906960165a6bbae883c> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#vu> .
        <http://clokman.com/kfir/resource#445d259ad2454906960165a6bbae883c> <http://www.w3.org/2000/01/rdf-schema#label> "Reward captures attention independent of the current focus of attention"@en .
        <http://clokman.com/kfir/resource#Xue_X> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#445d259ad2454906960165a6bbae883c> .
        <http://clokman.com/kfir/resource#445d259ad2454906960165a6bbae883c> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#Xue_X> .
        <http://clokman.com/kfir/resource#Xue_X> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#Xue_X> <http://www.w3.org/2000/01/rdf-schema#label> "Xue, X"@en .
        <http://clokman.com/kfir/resource#Li_S> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#445d259ad2454906960165a6bbae883c> .
        <http://clokman.com/kfir/resource#445d259ad2454906960165a6bbae883c> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#Li_S> .
        <http://clokman.com/kfir/resource#Li_S> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#Li_S> <http://www.w3.org/2000/01/rdf-schema#label> "Li, S"@en .
        <http://clokman.com/kfir/resource#Theeuwes_JL> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#445d259ad2454906960165a6bbae883c> .
        <http://clokman.com/kfir/resource#445d259ad2454906960165a6bbae883c> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#Theeuwes_JL> .
        <http://clokman.com/kfir/resource#Theeuwes_JL> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#Theeuwes_JL> <http://www.w3.org/2000/01/rdf-schema#label> "Theeuwes, JL"@en .
        <http://clokman.com/kfir/resource#445d259ad2454906960165a6bbae883c> <http://clokman.com/kfir/ontology#isPublishedOnYear> "2019" .
        <http://clokman.com/kfir/resource#445d259ad2454906960165a6bbae883c> <http://clokman.com/kfir/ontology#hasDOI> "10.1167/16.12.84" .
        <http://clokman.com/kfir/resource#445d259ad2454906960165a6bbae883c> <http://clokman.com/kfir/ontology#hasPureBibliographyID> "445d259ad2454906960165a6bbae883c" .
        <http://clokman.com/kfir/resource#8c769226a4fb44daa0cd2f8dc74136d3> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#8c769226a4fb44daa0cd2f8dc74136d3> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#8c769226a4fb44daa0cd2f8dc74136d3> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Misc> .
        <http://clokman.com/kfir/ontology#Misc> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#8c769226a4fb44daa0cd2f8dc74136d3> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#vu> .
        <http://clokman.com/kfir/resource#8c769226a4fb44daa0cd2f8dc74136d3> <http://www.w3.org/2000/01/rdf-schema#label> "Truth and Truth-Telling-Engaging South Africa's Post-Apartheid Public Religious Discourse"@en .
        <http://clokman.com/kfir/resource#van_der_Riet_RL> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#8c769226a4fb44daa0cd2f8dc74136d3> .
        <http://clokman.com/kfir/resource#8c769226a4fb44daa0cd2f8dc74136d3> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#van_der_Riet_RL> .
        <http://clokman.com/kfir/resource#van_der_Riet_RL> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#van_der_Riet_RL> <http://www.w3.org/2000/01/rdf-schema#label> "van_der_Riet, RL"@en .
        <http://clokman.com/kfir/resource#8c769226a4fb44daa0cd2f8dc74136d3> <http://clokman.com/kfir/ontology#isPublishedOnYear> "2019" .
        <http://clokman.com/kfir/resource#8c769226a4fb44daa0cd2f8dc74136d3> <http://clokman.com/kfir/ontology#hasPureBibliographyID> "8c769226a4fb44daa0cd2f8dc74136d3" .
        <http://clokman.com/kfir/resource#f067bb9b678546da89b80ddc45b50291> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#f067bb9b678546da89b80ddc45b50291> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#f067bb9b678546da89b80ddc45b50291> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Misc> .
        <http://clokman.com/kfir/ontology#Misc> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#f067bb9b678546da89b80ddc45b50291> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#vu> .
        <http://clokman.com/kfir/resource#f067bb9b678546da89b80ddc45b50291> <http://www.w3.org/2000/01/rdf-schema#label> "Una Sancta-Towards a Contextualised Ecclesiology for the Korean Churches"@en .
        <http://clokman.com/kfir/resource#Park_S> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#f067bb9b678546da89b80ddc45b50291> .
        <http://clokman.com/kfir/resource#f067bb9b678546da89b80ddc45b50291> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#Park_S> .
        <http://clokman.com/kfir/resource#Park_S> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#Park_S> <http://www.w3.org/2000/01/rdf-schema#label> "Park, S"@en .
        <http://clokman.com/kfir/resource#f067bb9b678546da89b80ddc45b50291> <http://clokman.com/kfir/ontology#isPublishedOnYear> "2019" .
        <http://clokman.com/kfir/resource#f067bb9b678546da89b80ddc45b50291> <http://clokman.com/kfir/ontology#hasPureBibliographyID> "f067bb9b678546da89b80ddc45b50291" .
        <http://clokman.com/kfir/resource#cd51779243fb4c228d8313b89b8746e4> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#cd51779243fb4c228d8313b89b8746e4> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#cd51779243fb4c228d8313b89b8746e4> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Misc> .
        <http://clokman.com/kfir/ontology#Misc> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#cd51779243fb4c228d8313b89b8746e4> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#vu> .
        <http://clokman.com/kfir/resource#cd51779243fb4c228d8313b89b8746e4> <http://www.w3.org/2000/01/rdf-schema#label> "White anti-apartheid theologies as resource for a theological response to whiteness in post-apartheid South Africa"@en .
        <http://clokman.com/kfir/resource#van_Wyngaard_GJ> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#cd51779243fb4c228d8313b89b8746e4> .
        <http://clokman.com/kfir/resource#cd51779243fb4c228d8313b89b8746e4> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#van_Wyngaard_GJ> .
        <http://clokman.com/kfir/resource#van_Wyngaard_GJ> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#van_Wyngaard_GJ> <http://www.w3.org/2000/01/rdf-schema#label> "van_Wyngaard, GJ"@en .
        <http://clokman.com/kfir/resource#cd51779243fb4c228d8313b89b8746e4> <http://clokman.com/kfir/ontology#isPublishedOnYear> "2019" .
        <http://clokman.com/kfir/resource#cd51779243fb4c228d8313b89b8746e4> <http://clokman.com/kfir/ontology#hasPureBibliographyID> "cd51779243fb4c228d8313b89b8746e4" .
        <http://clokman.com/kfir/resource#1a2e1f3f51644da0929d49e8299f7532> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#1a2e1f3f51644da0929d49e8299f7532> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#1a2e1f3f51644da0929d49e8299f7532> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Inbook> .
        <http://clokman.com/kfir/ontology#Inbook> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#1a2e1f3f51644da0929d49e8299f7532> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#vu> .
        <http://clokman.com/kfir/resource#1a2e1f3f51644da0929d49e8299f7532> <http://www.w3.org/2000/01/rdf-schema#label> "A Future for Cultural History of the Dutch Wadden Region-Challenges and Policies in a Maritime Agricultural Landscape"@en .
        <http://clokman.com/kfir/resource#Egberts_LR> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#1a2e1f3f51644da0929d49e8299f7532> .
        <http://clokman.com/kfir/resource#1a2e1f3f51644da0929d49e8299f7532> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#Egberts_LR> .
        <http://clokman.com/kfir/resource#Egberts_LR> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#Egberts_LR> <http://www.w3.org/2000/01/rdf-schema#label> "Egberts, LR"@en .
        <http://clokman.com/kfir/resource#1a2e1f3f51644da0929d49e8299f7532> <http://clokman.com/kfir/ontology#isPublishedBy> <http://clokman.com/kfir/resource#Amsterdam_University_Press> .
        <http://clokman.com/kfir/resource#Amsterdam_University_Press> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#1a2e1f3f51644da0929d49e8299f7532> <http://clokman.com/kfir/ontology#isPublishedOnYear> "2018" .
        <http://clokman.com/kfir/resource#1a2e1f3f51644da0929d49e8299f7532> <http://clokman.com/kfir/ontology#isPublishedOnMonth> "10" .
        <http://clokman.com/kfir/resource#1a2e1f3f51644da0929d49e8299f7532> <http://clokman.com/kfir/ontology#isPublishedOnDate> "2018.10" .
        <http://clokman.com/kfir/resource#1a2e1f3f51644da0929d49e8299f7532> <http://clokman.com/kfir/ontology#hasPureBibliographyID> "1a2e1f3f51644da0929d49e8299f7532" .
        <http://clokman.com/kfir/resource#1a2e1f3f51644da0929d49e8299f7532> <http://clokman.com/kfir/ontology#isChapterOf> <http://clokman.com/kfir/resource#Waddenland_Outstanding> .
        <http://clokman.com/kfir/resource#Waddenland_Outstanding> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Book> .
        <http://clokman.com/kfir/resource#fc77697ea6da4af396d009f8871dcea5> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#fc77697ea6da4af396d009f8871dcea5> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#fc77697ea6da4af396d009f8871dcea5> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://clokman.com/kfir/ontology#Article> .
        <http://clokman.com/kfir/ontology#Article> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://clokman.com/kfir/ontology#Document> .
        <http://clokman.com/kfir/resource#fc77697ea6da4af396d009f8871dcea5> <http://clokman.com/kfir/ontology#hasOriginBibliography> <http://clokman.com/kfir/resource#vu> .
        <http://clokman.com/kfir/resource#fc77697ea6da4af396d009f8871dcea5> <http://www.w3.org/2000/01/rdf-schema#label> "Climate, aggression, and violence (CLASH)-a cultural-evolutionary approach"@en .
        <http://clokman.com/kfir/resource#Rinderu_MI> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#fc77697ea6da4af396d009f8871dcea5> .
        <http://clokman.com/kfir/resource#fc77697ea6da4af396d009f8871dcea5> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#Rinderu_MI> .
        <http://clokman.com/kfir/resource#Rinderu_MI> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#Rinderu_MI> <http://www.w3.org/2000/01/rdf-schema#label> "Rinderu, MI"@en .
        <http://clokman.com/kfir/resource#Bushman_BJ> <http://clokman.com/kfir/ontology#isAuthorOf> <http://clokman.com/kfir/resource#fc77697ea6da4af396d009f8871dcea5> .
        <http://clokman.com/kfir/resource#fc77697ea6da4af396d009f8871dcea5> <http://clokman.com/kfir/ontology#hasAuthor> <http://clokman.com/kfir/resource#Bushman_BJ> .
        <http://clokman.com/kfir/resource#Bushman_BJ> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#NamedIndividual> .
        <http://clokman.com/kfir/resource#Bushman_BJ> <http://www.w3.org/2000/01/rdf-schema#label> "Bushman, BJ"@en .


        >>> import os
        >>> os.remove('vu_1k_test_0.0_test.ttl')
    """