## TODO: Re-write rdfTools.py as an object oriented module

from __future__ import print_function
from preprocessor.Text_File import Text_File


class RDF_File(Text_File):
    def __init__(self, file_path):
        """
        Examples:
            >>> my_rdf_file = RDF_File('example_data//test.rdf')
            >>> my_rdf_file.clear_contents()  # in case file is used by another test before
            >>> my_rdf_file.append_line('first line string')
            >>> my_rdf_file.preview()
            first line string
        """
        Text_File.__init__(self, file_path)


    def write_triples_to_file(self, triples_object, show_progress_bar=True):
        """
        Args:
            triples_object(Triples)

        Returns:
            Nothing

        Examples:
            >>> # Prep
            >>> from meta.consoleOutput import ConsoleOutput
            >>> console = ConsoleOutput(log_file_path='log.txt')
            >>> console.clear_log_file()
            >>> my_triples = Triples()
            >>> my_triples.add_triple("<http://clokman.com/ontologies/scientific-research>", "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>", "<http://www.w3.org/2002/07/owl#Ontology>")\
                          .add_triple("<http://clokman.com/ontologies/scientific-research>", "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>", "<http://www.w3.org/2002/07/owl#Visualization>")\
                          .preview(2)
            Triple 1:
            ('<http://clokman.com/ontologies/scientific-research> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#Ontology> .')
            Triple 2:
            ('<http://clokman.com/ontologies/scientific-research> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#Visualization> .')
            >>> my_rdf_file = RDF_File('example_data//write_test.ttl')
            >>> my_rdf_file.clear_contents()  # in case file is used by another test before

            >>> # Write triples object
            >>> my_rdf_file.write_triples_to_file(my_triples, show_progress_bar=False)
            Calculating the length of the Triples object
            Writing of the triples to file "example_data//write_test.ttl" has started
            Success: 2 triples were written to "example_data//write_test.ttl"
            These items were skipped due to errors (0 items):
            <BLANKLINE>
            A log of the operation is kept in "log.txt"

            >>> my_rdf_file.preview(2)
            <http://clokman.com/ontologies/scientific-research> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Ontology> .
            <http://clokman.com/ontologies/scientific-research> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Visualization> .
        """
        from meta.consoleOutput import ConsoleOutput
        console = ConsoleOutput(log_file_path='log.txt')

        file_path = self.input_file_path

        console.log_message('Calculating the length of the Triples object', add_timestamp_in_file=True)
        maximum_progress = len(triples_object)  # for progress bar
        erroneous_triples = []  # for logging and reporting
        no_of_successfully_written_triples = 0

        # Write to file
        console.log_message('Writing of the triples to file "%s" has started' % file_path, add_timestamp_in_file=True)
        with open(file_path, mode="a", encoding='utf8') as file:
            for i, each_triple in enumerate(triples_object):
                try:
                    file.write(each_triple + '\n')
                    no_of_successfully_written_triples += 1
                except:
                    erroneous_triples.append(each_triple)
                finally:
                    if show_progress_bar:
                        console.print_current_progress(current_progress=i, maximum_progress=maximum_progress,
                                                       status_message='Writing triples to "%s"' % file_path)

        # Log
        # TODO: Include number of triples written to file in the log
        console.log_message('Success: %d triples were written to "%s"'
                            % (no_of_successfully_written_triples, file_path), add_timestamp_in_file=True)
        console.log_list_with_caption('These items were skipped due to errors', erroneous_triples)
        console.log_message('\nA log of the operation is kept in "%s"' % console.get_log_file_path())


class Triples():
    """
    Examples:
        >>> # prep
        >>> my_triples = Triples()
        >>> my_triples.add_triple("<http://clokman.com/ontologies/scientific-research>", "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>", "http://www.w3.org/2002/07/owl#Ontology")\
                      .add_triple("<http://clokman.com/ontologies/scientific-research>", "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>", "http://www.w3.org/2002/07/owl#Visualization")\
                      .preview()
        Triple 1:
        ('<http://clokman.com/ontologies/scientific-research> '
         '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
         'http://www.w3.org/2002/07/owl#Ontology .')

        >>> # repr
        >>> my_triples
        ['<http://clokman.com/ontologies/scientific-research> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> http://www.w3.org/2002/07/owl#Ontology .', '<http://clokman.com/ontologies/scientific-research> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> http://www.w3.org/2002/07/owl#Visualization .']
        >>> type(my_triples)
        <class 'rdfTools.Triples'>

        >>> # str
        >>> str(my_triples)
        "['<http://clokman.com/ontologies/scientific-research> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> http://www.w3.org/2002/07/owl#Ontology .', '<http://clokman.com/ontologies/scientific-research> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> http://www.w3.org/2002/07/owl#Visualization .']"
        >>> print(my_triples)
        ['<http://clokman.com/ontologies/scientific-research> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> http://www.w3.org/2002/07/owl#Ontology .', '<http://clokman.com/ontologies/scientific-research> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> http://www.w3.org/2002/07/owl#Visualization .']

        >>> # iter
        >>> for each_triple in my_triples:
        ...     print("triple: " + each_triple)
        triple: <http://clokman.com/ontologies/scientific-research> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> http://www.w3.org/2002/07/owl#Ontology .
        triple: <http://clokman.com/ontologies/scientific-research> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> http://www.w3.org/2002/07/owl#Visualization .

        >>> # getitem
        >>> my_triples[1]
        '<http://clokman.com/ontologies/scientific-research> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> http://www.w3.org/2002/07/owl#Visualization .'
        >>> my_triples[0:2]
        ['<http://clokman.com/ontologies/scientific-research> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> http://www.w3.org/2002/07/owl#Ontology .', '<http://clokman.com/ontologies/scientific-research> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> http://www.w3.org/2002/07/owl#Visualization .']

        >>> # setitem
        >>> my_triples[0] = 'test 1'
        >>> my_triples[0]
        'test 1'
        >>> my_triples[0:2]
        ['test 1', '<http://clokman.com/ontologies/scientific-research> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> http://www.w3.org/2002/07/owl#Visualization .']

        >>> # length
        >>> len(my_triples)
        2
    """
    def __init__(self):
        self.triples_list = []


    # Overrides #########################
    def __repr__(self):
        return repr(self.triples_list)

    def __str__(self):
        return str(self.triples_list)

    def __iter__(self):
        return iter(self.triples_list)

    def __getitem__(self, index):
        return self.triples_list[index]

    def __setitem__(self, index, value):
        self.triples_list[index] = value

    def __len__(self):
        return len(self.triples_list)
    #####################################


    def add_triple(self, sub, prop, obj):
        """
        Constructs a triple from three given parameters and adds it to self.triples_list.

        Args:
            sub(str): The subject; the 1st element of triple
            prop(str):  The property in triple; the predicate, the 2nd element of triple.
            obj(str): The object in triple; the 3rd element of triple.

        Raises:
            Exception: If no list variable is defined before the function is called, function will return error.

        Returns:
            - self

        Examples:
            >>> my_triples = Triples()
            >>> my_triples.add_triple("<http://clokman.com/ontologies/scientific-research>",
            ...             "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>",
            ...             "http://www.w3.org/2002/07/owl#Ontology")\
                          .preview()
            Triple 1:
            ('<http://clokman.com/ontologies/scientific-research> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             'http://www.w3.org/2002/07/owl#Ontology .')

            >>> #c_book      = <SOME_URI>
            >>> #p_rdf_type  = <SOME URI>
            >>> #c_class     = <SOME URI>
            >>> #add_triple(c_book, p_rdf_type, c_class)

        """
        triple = sub + " " + prop + " " + obj + " ."  # construct a triple in n3 format
        self.triples_list.append(triple)

        return self


    def add_prefix_triple(self, desired_prefix_name, prefix_uri_string):  # local function
        """
        Constructs a prefix assertion from given arguments and adds it to triples_list. Is a variant of add_triple function.
        Adds prefixes to triples_list in the following manner:
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

        Args:
            - desired_prefix_name(str): Enter empty string ('') to specify default prefix (i.e., ':')

        Returns:
            self

        See Also:
            add_triple

        Examples:
            >>> # add prefix triple
            >>> my_triples = Triples()
            >>> my_triples.add_prefix_triple('xsd',  'http://www.w3.org/2001/XMLSchema#xsd')\
                          .preview()
            Triple 1:
            '@prefix xsd: <http://www.w3.org/2001/XMLSchema#xsd> .'

            >>> # add default prefix triple
            >>> my_triples.clear_all()\
                          .add_prefix_triple('',  'http://www.w3.org/2001/XMLSchema#xsd')\
                          .preview()
            Triple 1:
            '@prefix : <http://www.w3.org/2001/XMLSchema#xsd> .'
        """
        # construct a prefix triple in n3 format
        prefix_triple = "@prefix " + desired_prefix_name + ": <" + prefix_uri_string + "> ."
        self.triples_list.append(prefix_triple)

        return self

    def preview(self, number_of_triples_to_preview=1):
        """

        Args:
            number_of_triples_to_preview:

        Returns:
            Nothing

        Examples:
            >>> # try to preview empty object
            >>> my_triples = Triples()
            >>> my_triples.preview()
            Instance does not have any triples to preview (empty instance).

            >>> # prep (add triples to object)
            >>> my_triples.add_triple("<http://clokman.com/ontologies/scientific-research>", "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>", "http://www.w3.org/2002/07/owl#Ontology")\
                          .add_triple("<http://clokman.com/ontologies/scientific-research>", "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>", "http://www.w3.org/2002/07/owl#Visualization")\
                          .preview()
            Triple 1:
            ('<http://clokman.com/ontologies/scientific-research> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             'http://www.w3.org/2002/07/owl#Ontology .')

            >>> # preview (custom parameters)
            >>> my_triples.preview(2)
            Triple 1:
            ('<http://clokman.com/ontologies/scientific-research> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             'http://www.w3.org/2002/07/owl#Ontology .')
            Triple 2:
            ('<http://clokman.com/ontologies/scientific-research> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             'http://www.w3.org/2002/07/owl#Visualization .')
        """
        from pprint import pprint

        if len(self.triples_list) == 0:
            print('Instance does not have any triples to preview (empty instance).')

        for i, each_triple in enumerate(self.triples_list):
            if i < number_of_triples_to_preview:
                print('Triple %s:' % str(i+1))
                pprint(each_triple)
            else:
                break

    def clear_all(self):
        """

        Returns:
            - self

        Examples:
            >>> # prep
            >>> my_triples = Triples()
            >>> my_triples.add_triple("<http://clokman.com/ontologies/scientific-research>", "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>", "http://www.w3.org/2002/07/owl#Ontology")\
                          .preview()
            Triple 1:
            ('<http://clokman.com/ontologies/scientific-research> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             'http://www.w3.org/2002/07/owl#Ontology .')

            >>> # clear_all
            >>> my_triples.clear_all()\
                          .preview()
            Instance does not have any triples to preview (empty instance).
        """
        self.triples_list = []

        return self

    def import_bibliography_object(self, source_bibliography, desired_source_bibliography_name, show_progress_bar=True):
        # TODO: This method is extracted as a method from the old source code and is not concise. It must be divided into many short methods.
        """
        Returns:
            - self

        Examples:
            >>> # prep
            >>> from triplicator.bibTools import Bibliography
            >>> my_bibliography_object = Bibliography()
            >>> my_bibliography_object.importBibtex('example_data//test_clean.bib')
            Parsing of example_data//test_clean.bib started
            pybtex package is parsing using bibtex.Parser()...
            pybtex package finished parsing
            Calculating file length...
            <BLANKLINE>
            <BLANKLINE>
            ---------------------------------------------------------------------------------------------------
            example_data//test_clean.bib parsed and imported as Bibliography object.
            <BLANKLINE>
            Fields added to the parsed the Bibliography object:
            {'b_abstract': 2,
             'b_author_labels': 3,
             'b_authors': 3,
             'b_document': 3,
             'b_document_label': 3,
             'b_doi': 1,
             'b_issn': 2,
             'b_journal': 2,
             'b_journal_label': 2,
             'b_pages': 2,
             'b_publication_month': 3,
             'b_publication_year': 3,
             'b_publisher': 3,
             'b_publisher_label': 3,
             'b_topic_labels': 1,
             'b_topics': 1,
             'b_type': 3,
             'b_volume': 2}
            <BLANKLINE>
            <BLANKLINE>

            >>> my_triples = Triples()
            >>> my_triples.import_bibliography_object(my_bibliography_object, desired_source_bibliography_name='some bibliography', show_progress_bar=False)\
                          .preview(1000)
            Triple 1:
            ('<http://www.w3.org/2000/01/rdf-schema#subClassOf> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 2:
            ('<http://clokman.com/kfir/ontology#isAuthorOf> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 3:
            ('<http://clokman.com/kfir/ontology#hasAuthor> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 4:
            ('<http://clokman.com/kfir/ontology#isPublishedOn> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 5:
            ('<http://clokman.com/kfir/ontology#isPublishedBy> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 6:
            ('<http://clokman.com/kfir/ontology#isPublishedOnYear> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 7:
            ('<http://clokman.com/kfir/ontology#isPublishedOnMonth> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 8:
            ('<http://clokman.com/kfir/ontology#isPublishedOnDate> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 9:
            ('<http://clokman.com/kfir/ontology#hasDOI> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 10:
            ('<http://clokman.com/kfir/ontology#hasISSN> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 11:
            ('<http://clokman.com/kfir/ontology#hasISBN> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 12:
            ('<http://clokman.com/kfir/ontology#isChapterOf> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 13:
            ('<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 14:
            ('<http://www.w3.org/2000/01/rdf-schema#label> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 15:
            ('<http://clokman.com/kfir/ontology#hasTopic> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 16:
            ('<http://clokman.com/kfir/ontology#hasAbstract> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 17:
            ('<http://clokman.com/kfir/ontology#hasCited> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 18:
            ('<http://clokman.com/kfir/ontology#isCitedBy> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 19:
            ('<http://www.w3.org/2002/07/owl#equivalentClass> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 20:
            ('<http://clokman.com/kfir/ontology#hasOriginBibliography> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#ObjectProperty> .')
            Triple 21:
            ('<http://clokman.com/kfir/ontology#Topic> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2000/01/rdf-schema#Class> .')
            Triple 22:
            ('<http://clokman.com/kfir/resource#some%20bibliography> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2000/01/rdf-schema#Class> .')
            Triple 23:
            ('<http://clokman.com/kfir/resource#some%20bibliography> '
             '<http://www.w3.org/2000/01/rdf-schema#subClassOf> '
             '<http://clokman.com/kfir/resource#Bibliography> .')
            Triple 24:
            ('<http://clokman.com/kfir/ontology#JournalArticle> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2000/01/rdf-schema#Class> .')
            Triple 25:
            ('<http://clokman.com/kfir/ontology#Book> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2000/01/rdf-schema#Class> .')
            Triple 26:
            ('<http://clokman.com/kfir/ontology#BookChapter> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2000/01/rdf-schema#Class> .')
            Triple 27:
            ('<http://clokman.com/kfir/ontology#Miscellaneous> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2000/01/rdf-schema#Class> .')
            Triple 28:
            ('<http://clokman.com/kfir/resource#Book_with_one_author> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#NamedIndividual> .')
            Triple 29:
            ('<http://clokman.com/kfir/resource#Book_with_one_author> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://clokman.com/kfir/ontology#Document> .')
            Triple 30:
            ('<http://clokman.com/kfir/resource#Book_with_one_author> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://clokman.com/kfir/ontology#Book> .')
            Triple 31:
            ('<http://clokman.com/kfir/ontology#Book> '
             '<http://www.w3.org/2000/01/rdf-schema#subClassOf> '
             '<http://clokman.com/kfir/ontology#Document> .')
            Triple 32:
            ('<http://clokman.com/kfir/resource#Book_with_one_author> '
             '<http://clokman.com/kfir/ontology#hasOriginBibliography> '
             '<http://clokman.com/kfir/resource#some%20bibliography> .')
            Triple 33:
            ('<http://clokman.com/kfir/resource#Book_with_one_author> '
             '<http://www.w3.org/2000/01/rdf-schema#label> "Book with one author"@en .')
            Triple 34:
            ('<http://clokman.com/kfir/resource#Jaschke_AC> '
             '<http://clokman.com/kfir/ontology#isAuthorOf> '
             '<http://clokman.com/kfir/resource#Book_with_one_author> .')
            Triple 35:
            ('<http://clokman.com/kfir/resource#Book_with_one_author> '
             '<http://clokman.com/kfir/ontology#hasAuthor> '
             '<http://clokman.com/kfir/resource#Jaschke_AC> .')
            Triple 36:
            ('<http://clokman.com/kfir/resource#Jaschke_AC> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#NamedIndividual> .')
            Triple 37:
            ('<http://clokman.com/kfir/resource#Jaschke_AC> '
             '<http://www.w3.org/2000/01/rdf-schema#label> "Jaschke, AC"@en .')
            Triple 38:
            ('<http://clokman.com/kfir/resource#Book_with_one_author> '
             '<http://clokman.com/kfir/ontology#isPublishedBy> '
             '<http://clokman.com/kfir/resource#Van_Gennep> .')
            Triple 39:
            ('<http://clokman.com/kfir/resource#Van_Gennep> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#NamedIndividual> .')
            Triple 40:
            ('<http://clokman.com/kfir/resource#Book_with_one_author> '
             '<http://clokman.com/kfir/ontology#isPublishedOnYear> "2017" .')
            Triple 41:
            ('<http://clokman.com/kfir/resource#Book_with_one_author> '
             '<http://clokman.com/kfir/ontology#isPublishedOnMonth> "10" .')
            Triple 42:
            ('<http://clokman.com/kfir/resource#Book_with_one_author> '
             '<http://clokman.com/kfir/ontology#isPublishedOnDate> "2017.10" .')
            Triple 43:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#NamedIndividual> .')
            Triple 44:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://clokman.com/kfir/ontology#Document> .')
            Triple 45:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://clokman.com/kfir/ontology#Article> .')
            Triple 46:
            ('<http://clokman.com/kfir/ontology#Article> '
             '<http://www.w3.org/2000/01/rdf-schema#subClassOf> '
             '<http://clokman.com/kfir/ontology#Document> .')
            Triple 47:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://clokman.com/kfir/ontology#hasOriginBibliography> '
             '<http://clokman.com/kfir/resource#some%20bibliography> .')
            Triple 48:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://www.w3.org/2000/01/rdf-schema#label> "Article with 5 authors with '
             '\\'and\\' notation"@en .')
            Triple 49:
            ('<http://clokman.com/kfir/resource#Lohr_A> '
             '<http://clokman.com/kfir/ontology#isAuthorOf> '
             '<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '.')
            Triple 50:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://clokman.com/kfir/ontology#hasAuthor> '
             '<http://clokman.com/kfir/resource#Lohr_A> .')
            Triple 51:
            ('<http://clokman.com/kfir/resource#Lohr_A> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#NamedIndividual> .')
            Triple 52:
            ('<http://clokman.com/kfir/resource#Lohr_A> '
             '<http://www.w3.org/2000/01/rdf-schema#label> "Lohr, A"@en .')
            Triple 53:
            ('<http://clokman.com/kfir/resource#Beunen_R> '
             '<http://clokman.com/kfir/ontology#isAuthorOf> '
             '<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '.')
            Triple 54:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://clokman.com/kfir/ontology#hasAuthor> '
             '<http://clokman.com/kfir/resource#Beunen_R> .')
            Triple 55:
            ('<http://clokman.com/kfir/resource#Beunen_R> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#NamedIndividual> .')
            Triple 56:
            ('<http://clokman.com/kfir/resource#Beunen_R> '
             '<http://www.w3.org/2000/01/rdf-schema#label> "Beunen, R"@en .')
            Triple 57:
            ('<http://clokman.com/kfir/resource#Savelli_H> '
             '<http://clokman.com/kfir/ontology#isAuthorOf> '
             '<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '.')
            Triple 58:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://clokman.com/kfir/ontology#hasAuthor> '
             '<http://clokman.com/kfir/resource#Savelli_H> .')
            Triple 59:
            ('<http://clokman.com/kfir/resource#Savelli_H> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#NamedIndividual> .')
            Triple 60:
            ('<http://clokman.com/kfir/resource#Savelli_H> '
             '<http://www.w3.org/2000/01/rdf-schema#label> "Savelli, H"@en .')
            Triple 61:
            ('<http://clokman.com/kfir/resource#Kalz_M> '
             '<http://clokman.com/kfir/ontology#isAuthorOf> '
             '<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '.')
            Triple 62:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://clokman.com/kfir/ontology#hasAuthor> '
             '<http://clokman.com/kfir/resource#Kalz_M> .')
            Triple 63:
            ('<http://clokman.com/kfir/resource#Kalz_M> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#NamedIndividual> .')
            Triple 64:
            ('<http://clokman.com/kfir/resource#Kalz_M> '
             '<http://www.w3.org/2000/01/rdf-schema#label> "Kalz, M"@en .')
            Triple 65:
            ('<http://clokman.com/kfir/resource#Ragas_A> '
             '<http://clokman.com/kfir/ontology#isAuthorOf> '
             '<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '.')
            Triple 66:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://clokman.com/kfir/ontology#hasAuthor> '
             '<http://clokman.com/kfir/resource#Ragas_A> .')
            Triple 67:
            ('<http://clokman.com/kfir/resource#Ragas_A> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#NamedIndividual> .')
            Triple 68:
            ('<http://clokman.com/kfir/resource#Ragas_A> '
             '<http://www.w3.org/2000/01/rdf-schema#label> "Ragas, A"@en .')
            Triple 69:
            ('<http://clokman.com/kfir/resource#Van_Belleghem_F> '
             '<http://clokman.com/kfir/ontology#isAuthorOf> '
             '<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '.')
            Triple 70:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://clokman.com/kfir/ontology#hasAuthor> '
             '<http://clokman.com/kfir/resource#Van_Belleghem_F> .')
            Triple 71:
            ('<http://clokman.com/kfir/resource#Van_Belleghem_F> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#NamedIndividual> .')
            Triple 72:
            ('<http://clokman.com/kfir/resource#Van_Belleghem_F> '
             '<http://www.w3.org/2000/01/rdf-schema#label> "Van_Belleghem, F"@en .')
            Triple 73:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://clokman.com/kfir/ontology#isPublishedOn> '
             '<http://clokman.com/kfir/resource#Current_Opinion_in_Environmental_Sustainability> '
             '.')
            Triple 74:
            ('<http://clokman.com/kfir/resource#Current_Opinion_in_Environmental_Sustainability> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#NamedIndividual> .')
            Triple 75:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://clokman.com/kfir/ontology#isPublishedBy> '
             '<http://clokman.com/kfir/resource#Elsevier> .')
            Triple 76:
            ('<http://clokman.com/kfir/resource#Elsevier> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#NamedIndividual> .')
            Triple 77:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://clokman.com/kfir/ontology#isPublishedOnYear> "2017" .')
            Triple 78:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://clokman.com/kfir/ontology#isPublishedOnMonth> "10" .')
            Triple 79:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://clokman.com/kfir/ontology#isPublishedOnDate> "2017.10" .')
            Triple 80:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://clokman.com/kfir/ontology#hasDOI> "10.1016/j.cosust.2017.08.009" .')
            Triple 81:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://clokman.com/kfir/ontology#hasISSN> "1877-3435" .')
            Triple 82:
            ('<http://clokman.com/kfir/resource#Article_with_5_authors_with_and_notation> '
             '<http://clokman.com/kfir/ontology#hasAbstract> "Since the 1950s the amount '
             'of plastics in the marine environment has increased dramatically. Worldwide '
             'there is a growing concern about the risks and possible adverse effects of '
             '(micro)plastics. This paper reflects on the sources and effects of marine '
             'litter and the effects of policies and other actions taken worldwide. '
             'Current knowledge offers a solid basis for effective action. Yet, so far the '
             'effects of policies and other initiatives are still largely insufficient. '
             'The search for appropriate responses could be based on possible '
             'interventions and profound understanding of the context specific factors for '
             'success. Moreover, the scope, timeframe and dynamics of all initiatives are '
             'distinctly different and orchestration at all levels, in close cooperation '
             'with one another, is currently lacking."@en .')
            Triple 83:
            ('<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#NamedIndividual> .')
            Triple 84:
            ('<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://clokman.com/kfir/ontology#Document> .')
            Triple 85:
            ('<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://clokman.com/kfir/ontology#Article> .')
            Triple 86:
            ('<http://clokman.com/kfir/ontology#Article> '
             '<http://www.w3.org/2000/01/rdf-schema#subClassOf> '
             '<http://clokman.com/kfir/ontology#Document> .')
            Triple 87:
            ('<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '<http://clokman.com/kfir/ontology#hasOriginBibliography> '
             '<http://clokman.com/kfir/resource#some%20bibliography> .')
            Triple 88:
            ('<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '<http://www.w3.org/2000/01/rdf-schema#label> "Article with 3 authors with '
             'mixed notation"@en .')
            Triple 89:
            ('<http://clokman.com/kfir/resource#Mendoza_Rodriguez_JP> '
             '<http://clokman.com/kfir/ontology#isAuthorOf> '
             '<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '.')
            Triple 90:
            ('<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '<http://clokman.com/kfir/ontology#hasAuthor> '
             '<http://clokman.com/kfir/resource#Mendoza_Rodriguez_JP> .')
            Triple 91:
            ('<http://clokman.com/kfir/resource#Mendoza_Rodriguez_JP> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#NamedIndividual> .')
            Triple 92:
            ('<http://clokman.com/kfir/resource#Mendoza_Rodriguez_JP> '
             '<http://www.w3.org/2000/01/rdf-schema#label> "Mendoza_Rodriguez, JP"@en .')
            Triple 93:
            ('<http://clokman.com/kfir/resource#Wielhouwer_JL> '
             '<http://clokman.com/kfir/ontology#isAuthorOf> '
             '<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '.')
            Triple 94:
            ('<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '<http://clokman.com/kfir/ontology#hasAuthor> '
             '<http://clokman.com/kfir/resource#Wielhouwer_JL> .')
            Triple 95:
            ('<http://clokman.com/kfir/resource#Wielhouwer_JL> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#NamedIndividual> .')
            Triple 96:
            ('<http://clokman.com/kfir/resource#Wielhouwer_JL> '
             '<http://www.w3.org/2000/01/rdf-schema#label> "Wielhouwer, JL"@en .')
            Triple 97:
            ('<http://clokman.com/kfir/resource#Kirchler_ESMN> '
             '<http://clokman.com/kfir/ontology#isAuthorOf> '
             '<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '.')
            Triple 98:
            ('<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '<http://clokman.com/kfir/ontology#hasAuthor> '
             '<http://clokman.com/kfir/resource#Kirchler_ESMN> .')
            Triple 99:
            ('<http://clokman.com/kfir/resource#Kirchler_ESMN> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#NamedIndividual> .')
            Triple 100:
            ('<http://clokman.com/kfir/resource#Kirchler_ESMN> '
             '<http://www.w3.org/2000/01/rdf-schema#label> "Kirchler, ESMN"@en .')
            Triple 101:
            ('<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '<http://clokman.com/kfir/ontology#isPublishedOn> '
             '<http://clokman.com/kfir/resource#Journal_of_Economic_Psychology> .')
            Triple 102:
            ('<http://clokman.com/kfir/resource#Journal_of_Economic_Psychology> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#NamedIndividual> .')
            Triple 103:
            ('<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '<http://clokman.com/kfir/ontology#isPublishedBy> '
             '<http://clokman.com/kfir/resource#Elsevier> .')
            Triple 104:
            ('<http://clokman.com/kfir/resource#Elsevier> '
             '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
             '<http://www.w3.org/2002/07/owl#NamedIndividual> .')
            Triple 105:
            ('<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '<http://clokman.com/kfir/ontology#isPublishedOnYear> "2017" .')
            Triple 106:
            ('<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '<http://clokman.com/kfir/ontology#isPublishedOnMonth> "10" .')
            Triple 107:
            ('<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '<http://clokman.com/kfir/ontology#isPublishedOnDate> "2017.10" .')
            Triple 108:
            ('<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '<http://clokman.com/kfir/ontology#hasISSN> "0167-4870" .')
            Triple 109:
            ('<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '<http://clokman.com/kfir/ontology#hasTopic> '
             '<http://clokman.com/kfir/resource#tax_compliance> .')
            Triple 110:
            ('<http://clokman.com/kfir/resource#tax_compliance> '
             '<http://www.w3.org/2000/01/rdf-schema#subClassOf> '
             '<http://clokman.com/kfir/ontology#Topic> .')
            Triple 111:
            ('<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '<http://clokman.com/kfir/ontology#hasTopic> '
             '<http://clokman.com/kfir/resource#auditing> .')
            Triple 112:
            ('<http://clokman.com/kfir/resource#auditing> '
             '<http://www.w3.org/2000/01/rdf-schema#subClassOf> '
             '<http://clokman.com/kfir/ontology#Topic> .')
            Triple 113:
            ('<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '<http://clokman.com/kfir/ontology#hasTopic> '
             '<http://clokman.com/kfir/resource#tax_enforcement> .')
            Triple 114:
            ('<http://clokman.com/kfir/resource#tax_enforcement> '
             '<http://www.w3.org/2000/01/rdf-schema#subClassOf> '
             '<http://clokman.com/kfir/ontology#Topic> .')
            Triple 115:
            ('<http://clokman.com/kfir/resource#Article_with_3_authors_with_mixed_notation> '
             '<http://clokman.com/kfir/ontology#hasAbstract> "Using country-level data '
             'from 2003–2014, we examine the association between auditing level (measured '
             'as number of verification actions taken by tax authorities per 100 taxpayers '
             'in each country) and tax compliance (measured as business executives’ '
             'perception of tax evasion). Our hypothesis is that compliance increases '
             'until a certain auditing level is reached, and decreases beyond that level '
             '(i.e., an elevated auditing level backfires). In line with our expectation, '
             'the results of a series of tests indicate that there is a U-shaped '
             'association between auditing and tax evasion. We discuss how a potential '
             'backfiring effect may depend on the extent to which compliance is '
             'voluntary."@en .')


            >>> # wrong type entered as source_bibliography parameter:
            >>> my_triples = Triples()
            >>> try:
            ...     #  source_bibliography parameter must be a Bibliography object, not a string
            ...     my_triples.import_bibliography_object('bad parameter', desired_source_bibliography_name='good parameter')
            ... except Exception as error_message:
            ...     print('Exception: ' + str(error_message))
            Exception: Parameter "bad parameter" must be of type <class 'triplicator.bibTools.Bibliography'>, but is currently of type <class 'str'>
        """
        ## TODO: Add basic class equivalencies (e.g., article = JournalArticle) to method

        # This method is formatted without line wrapping. Turn LINE WRAPPING OFF for optimal viewing.

        from preprocessor.string_tools import Parameter_Value
        from triplicator.bibTools import Bibliography
        from preprocessor.string_tools import String
        from preprocessor.Text_File import Log_File
        from meta.consoleOutput import ConsoleOutput
        from preprocessor.string_tools import Parameter_Value

        # Parameters
        Parameter_Value(source_bibliography).force_type(Bibliography)
        Parameter_Value(desired_source_bibliography_name).force_type(str)

        source_bibliography = source_bibliography
        origin_bibliography = desired_source_bibliography_name

        # for logging
        console = ConsoleOutput(log_file_path='log.txt')
        current_progress = 0
        maximum_progress = len(source_bibliography.entries.items())

        #################################################################################
        #                   STATIC DEFINITIONS: PROPERTIES, CLASSES                     #
        #################################################################################

        # Legend:
        # c_ = class
        # p_ = property
        # i_ = instance
        # b_ = Bibliography class object field/value


        ###### NAMESPACE PREFIX DEFINITIONS ######
        ont  = "http://clokman.com/kfir/ontology#"  # assign long domain  name to short variable.
        res  = "http://clokman.com/kfir/resource#"  # assign long domain  name to short variable.
        rdf  = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        rdfs = "http://www.w3.org/2000/01/rdf-schema#"
        owl  = "http://www.w3.org/2002/07/owl#"
        xsd  = "http://www.w3.org/2001/XMLSchema#"

        #self.add_prefix_triple("",    ont)
        #self.add_prefix_triple("res",  res)
        #self.add_prefix_triple("rdf",  rdf)
        #self.add_prefix_triple("rdfs", rdfs)
        #self.add_prefix_triple("owl",  owl)
        #self.add_prefix_triple("xsd",  xsd)


        ###### ONTOLOGY DEFINITIONS ######
        #self.add_triple()("<http://clokman.com/ontologies/scientific-research>",
        # "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>",
        # "http://www.w3.org/2002/07/owl#Ontology")
        #self.add_triple()("<http://clokman.com/ontologies/pure-vu>",
        # "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>",
        # "http://www.w3.org/2002/07/owl#Ontology")

        ###### A REQUIRED CLASS DEFINITION FOR PROPERTIES ######
        # Although class definitions and assertions will come later, this one is needed for property definitions.
        # ... so it is placed here as an exception.
        c_object_property = construct_uri(owl,  "ObjectProperty"    )


        ###### STATIC PROPERTY DEFINITIONS (p_) ######
        p_subclass_of             = construct_uri(rdfs, "subClassOf"           )  # assign URI to subclass of
        p_is_author_of            = construct_uri(ont,  "isAuthorOf"           )  # assign URI to is author of
        p_has_author              = construct_uri(ont,  "hasAuthor"            )  # ...
        p_is_published_on         = construct_uri(ont,  "isPublishedOn"        )
        p_is_published_by         = construct_uri(ont,  "isPublishedBy"        )
        p_is_published_on_year    = construct_uri(ont,  "isPublishedOnYear"    )
        p_is_published_on_month   = construct_uri(ont,  "isPublishedOnMonth"   )
        p_is_published_on_date    = construct_uri(ont,  "isPublishedOnDate"    )
        p_has_doi                 = construct_uri(ont,  "hasDOI"               )
        p_has_issn                = construct_uri(ont,  "hasISSN"              )
        p_has_isbn                = construct_uri(ont,  "hasISBN"              )
        p_is_chapter_of           = construct_uri(ont,  "isChapterOf"          )
        p_has_topic               = construct_uri(ont,  "hasTopic"             )
        p_has_abstract            = construct_uri(ont,  "hasAbstract"          )
        p_has_cited               = construct_uri(ont,  "hasCited"             )
        p_is_cited_by             = construct_uri(ont,  "isCitedBy"            )
        p_has_origin_bibliography = construct_uri(ont,  "hasOriginBibliography")
        p_rdf_type                = construct_uri(rdf,  "type"                 )
        p_label                   = construct_uri(rdfs, "label"                )
        p_equivalent_class        = construct_uri(owl,  "equivalentClass"      )

        # TODO: Add triple should add triple so self.some_object instead of a variable outside the instance
        self.add_triple(p_subclass_of,              p_rdf_type,     c_object_property)
        self.add_triple(p_is_author_of,             p_rdf_type,     c_object_property)
        self.add_triple(p_has_author,               p_rdf_type,     c_object_property)
        self.add_triple(p_is_published_on,          p_rdf_type,     c_object_property)
        self.add_triple(p_is_published_by,          p_rdf_type,     c_object_property)
        self.add_triple(p_is_published_on_year,     p_rdf_type,     c_object_property)
        self.add_triple(p_is_published_on_month,    p_rdf_type,     c_object_property)
        self.add_triple(p_is_published_on_date,     p_rdf_type,     c_object_property)
        self.add_triple(p_has_doi,                  p_rdf_type,     c_object_property)
        self.add_triple(p_has_issn,                 p_rdf_type,     c_object_property)
        self.add_triple(p_has_isbn,                 p_rdf_type,     c_object_property)
        self.add_triple(p_is_chapter_of,            p_rdf_type,     c_object_property)
        self.add_triple(p_rdf_type,                 p_rdf_type,     c_object_property)
        self.add_triple(p_label,                    p_rdf_type,     c_object_property)
        self.add_triple(p_has_topic,                p_rdf_type,     c_object_property)
        self.add_triple(p_has_abstract,             p_rdf_type,     c_object_property)
        self.add_triple(p_has_cited,                p_rdf_type,     c_object_property)
        self.add_triple(p_is_cited_by,              p_rdf_type,     c_object_property)
        self.add_triple(p_equivalent_class,         p_rdf_type,     c_object_property)
        self.add_triple(p_has_origin_bibliography,  p_rdf_type,     c_object_property)


        #################################################################################
        #       DOCUMENT CLASS DECLARATIONS AND CLASS EQUIVALENCY ASSERTIONS            #
        #################################################################################

        ###### STATIC CLASS DEFINITIONS (c_ )######
        c_document            = construct_uri(ont,  "Document"          )  # assign URI to document superclass
        c_journal             = construct_uri(ont,  "Journal"           )  # assign URI to Journal class
        c_topic               = construct_uri(ont,  "Topic"             )
        c_named_individual    = construct_uri(owl,  "NamedIndividual"   )
        #'c_object_property' is not defined here as is in other similar cases, but is defined previously,
        # before property definitions and assertions, as it is needed by them.
        c_class               = construct_uri(rdfs, "Class"             )
        c_bibliography        = construct_uri(res,  "Bibliography")
        c_origin_bibliography = construct_uri(res,  origin_bibliography)

        # TODO: TRY TO ADD THESE AND SEE WHAT HAPPENS IN PROTEGE:
        # self.add_triple()(c_document, p_rdf_type, c_class)
        # self.add_triple()(c_journal, p_rdf_type, c_class)
        self.add_triple(c_topic, p_rdf_type, c_class)
        # self.add_triple()(c_named_individual, p_rdf_type, c_class)
        # self.add_triple()(c_object_property, p_rdf_type, c_class)
        # self.add_triple()(c_class, p_rdf_type, c_class)

        # Bibliography origin class definitions
        self.add_triple(c_origin_bibliography,  p_rdf_type,    c_class)
        self.add_triple(c_origin_bibliography,  p_subclass_of, c_bibliography)

        # Static document type definitions
        # These are not used to categorize instances in the document directly, but necessary for the class
        # equivalencies with e.g., Pure-VU document types. As these are the document classes in the main ontology,
        # their variable names are not suffixed as in other cases (e.g., c_article_res).
        c_journal_article = construct_uri(ont, "JournalArticle")
        c_book            = construct_uri(ont, "Book")
        c_book_chapter    = construct_uri(ont, "BookChapter")
        c_miscellaneous   = construct_uri(ont, "Miscellaneous")

        self.add_triple(c_journal_article,  p_rdf_type, c_class)
        self.add_triple(c_book,             p_rdf_type, c_class)
        self.add_triple(c_book_chapter,     p_rdf_type, c_class)
        self.add_triple(c_miscellaneous,    p_rdf_type, c_class)

        ############################################################################################################
        # SECTION COMMENTED OUT (ON 14th OF FEB) TO PREVENT DUPLICATE CLASSES SUCH AS 'BOOK'(ont) and 'BOOK'(vu)
        # IF LEADS TO A PROBLEM WITH SR ONTOLOGY, IT SHOULD BE TURNED BACK ON OR ADAPTED IN A DIFFERENT WAY
        # # Pure-VU document type definitions
        # # These are necessary for class equivalency assertions between Pure-VU and SR document classes
        # # These pure VU class names (e.g., 'article', 'book', 'inbook') are not coded anywhere in these scripts, but
        # they are parsed with the below names by pybtex package.
        # # These classes are *automatically* (hence no explicit usage anywhere) used to assign types to instances in
        # the code below.
        # # As these are NOT the document classes in the main ontology, their variable names are suffixed
        # (e.g., c_article_res).
        # c_article_res = construct_uri(res, "article")
        # c_book_res    = construct_uri(res, "book")
        # c_inbook_res  = construct_uri(res, "inbook")
        # c_misc_res    = construct_uri(res, "misc")
        #
        # self.add_triple()(c_article_res,    p_rdf_type, c_class)
        # self.add_triple()(c_book_res,       p_rdf_type, c_class)
        # self.add_triple()(c_inbook_res,     p_rdf_type, c_class)
        # self.add_triple()(c_misc_res,       p_rdf_type, c_class)
        #
        #
        # # Class equivalency assertions
        # self.add_triple()(c_article_res, p_equivalent_class, c_journal_article)
        # self.add_triple()(c_book_res,    p_equivalent_class, c_book)
        # self.add_triple()(c_inbook_res,  p_equivalent_class, c_book_chapter)
        # self.add_triple()(c_misc_res,    p_equivalent_class, c_miscellaneous)
        ############################################################################################################

        #################################################################################
        #                     DYNAMIC TRIPLES: INSTANCES AND TYPES                      #
        #################################################################################

        for each_entry_id, each_entry in source_bibliography.entries.items():
            #TODO: this try-except block is a workaround [001]. remove it.
            try:
                #######  URIs  #######
                current_document_instance_name = each_entry["b_document"]  # document instance
                current_type = each_entry["b_type"]  # type
                current_type = String(current_type).capitalize_first_letter().content

            except:
                pass
            # NOTE: Do not move the lines below to category and instance definitions section in the beginning of the
            # script. c_document_type values need to be dynamically assigned within this for loop, as the document
            # classes (e.g., Article, Book) are extracted from the resource file.

            # extract the class of the current document (e.g., Article, Book) and assign it to the c_document_type
            c_document_type      = construct_uri(ont, current_type                  )
            # assign current document instance to an instance variable (denoted by i_), and give it an URI
            i_document_instance   = construct_uri(res, current_document_instance_name)


            #######  DOCUMENT INSTANCE + DOCUMENT TYPE + DOCUMENT #######
            self.add_triple(i_document_instance,  p_rdf_type,       c_named_individual) # named_indiviual means instance
            self.add_triple(i_document_instance,  p_rdf_type,       c_document)

            # bind the extracted document classes to the document instances (the latter was extracted previously)
            self.add_triple(i_document_instance,  p_rdf_type,       c_document_type   )
            self.add_triple(c_document_type,      p_subclass_of,    c_document        )

            ########  DOCUMENT ORIGIN BIBLIOGRAPHY  #######
            # the document comes from the given bibliography
            self.add_triple(i_document_instance, p_has_origin_bibliography, c_origin_bibliography)


            #######  DOCUMENT LABEL  #######
            #TODO: this try-except block is a workaround. remove it.
            try:
                self.add_triple(i_document_instance, p_label, construct_string_literal(each_entry["b_document_label"], "@en"))
            except:
                pass

            #######  HAS CITED  #######
            try:
                current_incoming_citations_list = each_entry["b_cited"]
                if current_incoming_citations_list != '':
                    current_incoming_citations_list = Parameter_Value(current_incoming_citations_list)\
                                                                     .convert_to_single_item_list_if_not_list()

                for each_incoming_citation in current_incoming_citations_list:
                    i_incoming_document_instance = construct_uri(res, each_incoming_citation)
                    # if i_incoming_document_instance corresponds to an existing document_instance,
                    # its uri would be exactly the same with that of document_instance
                    self.add_triple(i_incoming_document_instance, p_rdf_type, c_named_individual)
                    self.add_triple(i_document_instance, p_has_cited, i_incoming_document_instance)

            except:
                pass


            #######  IS CITED BY  #######
            try:
                current_outgoing_citations_list = each_entry["b_cited_by"]
                if current_outgoing_citations_list != '':
                    current_outgoing_citations_list = Parameter_Value(current_outgoing_citations_list)\
                                                                     .convert_to_single_item_list_if_not_list()

                for each_outgoing_citation in current_outgoing_citations_list:
                    i_outgoing_document_instance = construct_uri(res, each_outgoing_citation)
                    # if i_outgoing_document_instance corresponds to an existing document_instance,
                    # its uri would be exactly the same with that of document_instance
                    self.add_triple(i_outgoing_document_instance, p_rdf_type, c_named_individual)
                    self.add_triple(i_document_instance, p_is_cited_by, i_outgoing_document_instance)
            except:
                pass


            #######  AUTHOR  ########
            #TODO: this try-except block is a workaround. remove it.
            try:
                current_authors                = each_entry["b_authors"]
                current_author_labels          = each_entry["b_author_labels"]
            except:
                pass

            for each_current_author, each_current_author_label in zip(current_authors, current_author_labels):

                # Assign author to instance and give it an URI
                i_author = construct_uri(res, each_current_author)

                # Bind the instances to each other and define their types
                self.add_triple(i_author,             p_is_author_of,    i_document_instance)
                self.add_triple(i_document_instance,  p_has_author,      i_author)
                self.add_triple(i_author,             p_rdf_type,        c_named_individual)

                # Add author label
                self.add_triple(i_author, p_label,  construct_string_literal(each_current_author_label, "@en"))


            #######  PUBLICATION INSTANCE + PUBLISHED ON  #######
            # NOTE: Use this "try-except" structure except identifier, authors, document instance, type--all fields
            # except these ones may not always be present.
            # This property applies journal articles (but not to books and journals)
            try:
                current_journal = each_entry["b_journal"]         # extract current publication instance
                i_journal       = construct_uri(res, current_journal)  # create  URI from publication instance

                # Bind the instances to each other and define their types
                self.add_triple(i_document_instance,   p_is_published_on,  i_journal         )
                self.add_triple(i_journal,             p_rdf_type,         c_named_individual)

            except:
                pass


            #######  PUBLISHER  #######
            # NOTE: Use this "try-except" structure except identifier, authors, document instance, type--all fields
            # except these ones may not always be present.
            # This property applies to books and journals (but not to journal articles)
            try:
                current_publisher = each_entry["b_publisher"]
                i_publisher       = construct_uri(res, current_publisher)

                # Bind the instances to each other and define their types
                self.add_triple(i_document_instance,   p_is_published_by,  i_publisher       )
                self.add_triple(i_publisher,           p_rdf_type,         c_named_individual)

            except:
                pass


            #######  YEAR + MONTH + DATE #######
            # NOTE: Use this "try-except" structure except identifier, authors, document instance, type--all fields
            # except these ones may not always be present.
            try:
                # extract field values and combine them into a date
                current_year  = each_entry["b_publication_year"]
                current_month = each_entry["b_publication_month"]
                current_date  = current_year + "." + current_month

                # Bind the instances to each other and define their types
                # NOTE: Literals are constructed as strings instead of integers due to LD-R compatibility issues.
                # (LD-R had trouble querying years if they were integers.)
                # If these string years need to be turned into integers in future, though, use
                # 'construct_integer_literal()'.
                self.add_triple(i_document_instance,   p_is_published_on_year,  construct_string_literal(current_year))
                self.add_triple(i_document_instance,   p_is_published_on_month, construct_string_literal(current_month))
                self.add_triple(i_document_instance,   p_is_published_on_date,  construct_string_literal(current_date))

            except:
                try: # In case "month" is missing, just process "year".
                    current_year = each_entry["b_publication_year"]  # extract current publication year
                    self.add_triple(i_document_instance, p_is_published_on_year, construct_string_literal(current_year))

                except: # In case there is neither year or month
                    pass


            #######  DOI  #######
            # NOTE: Use this "try-except" structure except identifier, authors, document instance, type--all fields
            # except these ones may not always be present.
            try:

                # Extract current doi
                current_doi = each_entry["b_doi"]

                # Bind the values to instances, and define their types
                # (the current document is published by the current publisher)
                self.add_triple(i_document_instance,   p_has_doi,   construct_string_literal(current_doi))

            except:
                pass


            #######  ISSN  #######
            # NOTE: Use this "try-except" structure except identifier, authors, document instance, type--all fields
            # except these ones may not always be present.
            try:
                # Extract current issn
                current_issn = each_entry["b_issn"]

                # Bind the values to instances, and define their types
                self.add_triple(i_document_instance,   p_has_issn,  construct_string_literal(current_issn))  # the
                # current document is published by the current publisher

            except:
                pass


            #######  ISBN  #######
            # NOTE: Use this "try-except" structure except identifier, authors, document instance, type--all fields
            # except these ones may not always be present.
            try:
                # Extract current isbn
                current_isbn = each_entry["b_isbn"]

                # Bind the values to instances, and define their types
                self.add_triple(i_document_instance,   p_has_isbn,  construct_string_literal(current_isbn))

            except:
                pass


            #######  BOOK TITLE --> IS CHAPTER IN + PARENT BOOK INSTANCE #######
            # Assign parent book to the current document if available (i.e., if the current document is a book chapter).
            # Also infer parent book instance.
            # NOTE: Use this "try-except" structure except identifier, authors, document instance, type--all fields
            # except these ones may not always be present.
            try:
                # Extract current book title
                current_parent_book = each_entry["b_parent_book"]

                # Bind the values to instances, and define their types
                i_current_parent_book = construct_uri(res, current_parent_book)

                self.add_triple(i_document_instance,   p_is_chapter_of,  i_current_parent_book)
                self.add_triple(i_current_parent_book, p_rdf_type,       c_book)

            except:
                pass


            #######  KEYWORDS --> ABOUT  #######
            # Assign keywords to the current document if available and the keyword is not in ignore list.
            # NOTE: Use this "try-except" structure except identifier, authors, document instance, type--all fields
            # except these ones may not always be present.
            try:
                current_topics           = each_entry["b_topics"]
                list_of_topics_to_ignore = ["Journal_Article", "journal_article"]  # ignore these topics
                for each_topic in current_topics:
                    if each_topic not in list_of_topics_to_ignore:  # if the topic is not in the ignore list...
                        # Construct current topic uri dynamically for each topic
                        c_current_topic = construct_uri(res, each_topic)

                        # Connect document instance to each of these topics
                        self.add_triple(i_document_instance, p_has_topic, c_current_topic)

                        # And clarify that the 'current topic' is a subclass of 'topic'
                        self.add_triple(c_current_topic, p_subclass_of, c_topic)
            except:
                pass


            #######  ABSTRACT  #######
            # Assign abstract to the current document if available and the keyword is not in ignore list.
            # NOTE: Use this "try-except" structure except identifier, authors, document instance, type--all fields
            # except these ones may not always be present.
            try:
                current_abstract = each_entry["b_abstract"]
                list_of_values_to_ignore = []  # ignore these values if they are found in the abstract field

                if current_abstract not in list_of_values_to_ignore:  # if the abstract is not in the ignore list...
                    # Construct string literal for current abstract dynamically for each abstract
                    c_current_abstract = construct_string_literal(current_abstract, '@en')

                    # Connect document instance to each of the abstracts
                    self.add_triple(i_document_instance, p_has_abstract, c_current_abstract)
            except:
                pass


            # Progress bar update
            if show_progress_bar:
                console.print_current_progress(current_progress, maximum_progress, 'Converting Bibliography object to '
                                                                                   'Triples object.')
            current_progress += 1

        return self


###################################################################
#                      TRIPLE FUNCTIONS                           #
###################################################################
# TODO: Re-write as an OO module.

def construct_uri(prefix, name):
    """
    Returns:
        str

    Example:
        >>> sr = 'http://www.example.com/'
        >>> construct_uri(sr, "Document")
        '<http://www.example.com/Document>'

        >>> sr = 'http://www.example.com/'
        >>> construct_uri(sr, "Some Document")
        '<http://www.example.com/Some%20Document>'
    """
    from preprocessor.string_tools import String

    name = String(name).clean_from_non_uri_safe_characters()
    cleaned_name = str(name)

    uri = "<" + prefix + cleaned_name + ">"
    return uri


def construct_string_literal(input_string, language_tag=""):
    """
    Constructs an English (@en) string literal in turtle format.

    :param input_string: The string to be formatted as turtle sting literal.
    :return: English string literal in turtle format

    :example:
        construct_string_literal(current_fields["b_document_label"], "@en")

    :example:
        add_triple (i_document_instance, p_label,  construct_string_literal(current_fields["b_document_label"], "@en"))
    """

    new_string_literal = "\"" + input_string + "\"" + language_tag
    return new_string_literal


def construct_integer_literal(input_string):
    """
    Constructs an integer literal in turtle format. (Uses 'int' instead of 'integer').

    :param input_string: The string to be formatted as turtle integer literal.
    :return: Integer literal in turtle format

    :example:
    """

    new_integer_literal = "\"" + input_string + "\"" + "^^xsd:int"
    return new_integer_literal
