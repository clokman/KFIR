from preprocessor.string_tools import String

class Sparql_Query():
    def __init__(self, input_query=''):
        """
        Examples:
            >>> ### QUICKSTART ###
            >>> # Initiation and setting parameters
            >>> my_query = Sparql_Query()
            >>> my_query_string = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\\n'\
                                  'SELECT ?label\\n'\
                                  'WHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }\\n'
            >>>                   # this notation (i.e., \\n at the end and quotes encapsulating each line) is only
            >>>                   # necessary in docstrings, and actual string can be entirely written inside
            >>>                   #''' ''' symbols (as ''' QUERY ''') in a Python script.
            >>> my_query.set_query(my_query_string)\
                        .print_query() # print_query added to supress returning self; not necessary in an actual script
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?label
            WHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }
            <BLANKLINE>
            >>> # Send and print query
            >>> my_query.retrieve_results_from_endpoint('http://dbpedia.org/sparql')
            {1: {'label': 'أمثلة (توضيح)'}, 2: {'label': 'Example'}, 3: {'label': 'Example (Begriffsklärung)'}, 4: {'label': 'Example'}}
            >>> my_query.print_results()
            {1: {'label': 'أمثلة (توضيح)'},
             2: {'label': 'Example'},
             3: {'label': 'Example (Begriffsklärung)'},
             4: {'label': 'Example'}}


            >>> ### MORE EXAMPLES ###

            >>> #Initiation and initial values
            >>> my_query = Sparql_Query()
            >>> my_query.query
            ''
            >>> my_query.endpoint_address
            ''

            >>> # Take string as input
            >>> my_query_string = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\\n'\
                                  'SELECT ?label\\n'\
                                  'WHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }\\n'
            >>>                   # this notation (i.e., \\n at the end and quotes encapsulating each line) is only
            >>>                   # necessary in docstrings, and actual string can be entirely written inside
            >>>                   #''' ''' symbols (as ''' QUERY ''') in a Python script.
            >>> my_query.set_query(my_query_string)\
                        .print_query() # print_query added to supress returning self; not necessary in an actual script
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?label
            WHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }
            <BLANKLINE>

            >>> # Directly calling the object's content returns the query (newline characters may appear in terminal output)
            >>> my_query.query
            'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\\nSELECT ?label\\nWHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }\\n'

            >>> # For prettier console output, print_query method can be used
            >>> my_query.print_query()
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?label
            WHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }
            <BLANKLINE>
        """
        self.query = input_query
        self.endpoint_address = ''

        self.query_parameters_registry = {}  # main query parameters. Can contain multiple search criteria such as multiple DOIs.

        self.valid_search_criteria_registry = []  # valid components of main query parameters. Each is a single item, like a DOI.
        self.invalid_search_criteria_registry = []  # thus, query_parameter and search_criteria do not refer to the same concept

        self.number_of_lines_retrieved = 0
        self.results = {}


    def set_query(self, query_string):
        """
        Returns:
            self

        Examples:
            >>> # Take string as input
            >>> my_query_string = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\\n'\
                                  'SELECT ?label\\n'\
                                  'WHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }\\n'  # this
            >>>                   # notation (e.g., \\n at the end) is only necessary in docstrings, and actual
            >>>                   # string can be written inside ''' ''' marks in a Python script.

            >>> my_query = Sparql_Query()
            >>> my_query.set_query(my_query_string)\
                        .print_query()  # self.conent is not directly called, as it returns the query with newline chars
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?label
            WHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }
            <BLANKLINE>
        """
        self.query = query_string
        return self


    def import_query_from_file(self, query_file_path):
        """
        Returns:
            self
        Examples:
            >>> # Take file as input
            >>> my_query = Sparql_Query()
            >>> my_query.import_query_from_file('test_data_and_queries//simple_dbpedia_test.rq')\
                        .print_query()  # a slight, non-problematic misalignment due to extra spaces is visible in the\
                                        # first line of query file
            <BLANKLINE>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?label
            WHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }
            <BLANKLINE>
        """
        from preprocessor.Text_File import Text_File
        query_file = Text_File(query_file_path)

        query = """
            %s
        """ % query_file.return_content()

        self.set_query(query)

        return self


    def set_endpoint(self, endpoint_address):
        """
        Returns:
            self

        Examples:
            >>> my_query = Sparql_Query()
            >>> my_query.set_endpoint('http://opencitations.net/sparql')\
                        .endpoint_address
            'http://opencitations.net/sparql'
        """
        self.endpoint_address = endpoint_address
        return self


    def import_endpoint_from_file(self, file_path):
        """
        Reads and parses an enpoint address from a file. Useful in cases where the endpoint address needs to be stored
        locally (i.e., neither in code nor on Git) for privacy purposes.

        Args:
            file_path(str)

        Returns:
            self

        Examples:
            # Import endpoint from file and check if endpoint is correctly updated
            >>> my_query = Sparql_Query()
            >>> my_query.import_endpoint_from_file('test_data_and_queries//endpoint_address_valid.txt').endpoint_address
            'http://dbpedia.org/sparql'

            >>> # File has two lines (error)
            >>> my_query.import_endpoint_from_file('test_data_and_queries//endpoint_address_invalid.txt')
            ValueError('The file that contains the endpoint address should have only one line, but the inputted file contains more lines.',)
        """
        from preprocessor.Text_File import Text_File
        file = Text_File(file_path)
        endpoint_address_in_file = file.return_content()

        if '\n' in endpoint_address_in_file:
            return ValueError('The file that contains the endpoint address should have only one line, but the inputted '
                              'file contains more lines.')

        self.endpoint_address = endpoint_address_in_file

        return self


    def retrieve_results_from_endpoint(self, endpoint_address='', print_only=False):
        """
        Args:
            endpoint_address(str): A URL string. If not specified, sets the endpoint to the self.endpoint.
            print_results(bool): If False, returns the results but does not print them to console

        Returns:
            self

        See Also:
            https://github.com/RDFLib/sparqlwrapper/blob/master/scripts/example.py

        Examples:
            >>> # Take string as input
            >>> my_query_string = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\\n'\
                                  'SELECT ?label\\n'\
                                  'WHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }\\n'  # this
            >>>                   # notation (e.g., \\n at the end) is only necessary in docstrings, and actual
            >>>                   # string can be written inside ''' ''' marks in a Python script.
            >>> my_query = Sparql_Query()
            >>> my_query.set_query(my_query_string)\
                        .set_endpoint("http://dbpedia.org/sparql")\
                        .retrieve_results_from_endpoint()
            {1: {'label': 'أمثلة (توضيح)'}, 2: {'label': 'Example'}, 3: {'label': 'Example (Begriffsklärung)'}, 4: {'label': 'Example'}}


            >>> my_query = Sparql_Query()
            >>> my_query.import_query_from_file('test_data_and_queries//simple_dbpedia_test.rq')\
                        .set_endpoint("http://dbpedia.org/sparql")\
                        .retrieve_results_from_endpoint()
            {1: {'label': 'أمثلة (توضيح)'}, 2: {'label': 'Example'}, 3: {'label': 'Example (Begriffsklärung)'}, 4: {'label': 'Example'}}

            >>> # A shorter expression without using set_query and set_endpoint
            >>> my_query = Sparql_Query(my_query_string)
            >>> my_query.retrieve_results_from_endpoint('http://dbpedia.org/sparql')
            {1: {'label': 'أمثلة (توضيح)'}, 2: {'label': 'Example'}, 3: {'label': 'Example (Begriffsklärung)'}, 4: {'label': 'Example'}}

            # print only (returns nothing, but prints results to console)
            >>> my_query.retrieve_results_from_endpoint('http://dbpedia.org/sparql', print_only=True)
            {1: {'label': 'أمثلة (توضيح)'},
             2: {'label': 'Example'},
             3: {'label': 'Example (Begriffsklärung)'},
             4: {'label': 'Example'}}

            >>> # A required parameter is not specified
            >>> my_query = Sparql_Query()
            >>> try:
            ...     my_query.retrieve_results_from_endpoint()
            ... except Exception as error_message:
            ...     print('Exception caught: ' + str(error_message))
            Exception caught: Parameters '['query', 'endpoint_address']' must be specified before this method is called. The current values of the parameters are ['', '']
            >>> my_query.set_endpoint('some endpoint').endpoint_address
            'some endpoint'

            >>> try:
            ...     my_query.retrieve_results_from_endpoint()
            ... except Exception as error_message:
            ...     print('Exception caught: ' + str(error_message))
            Exception caught: Parameters '['query', 'endpoint_address']' must be specified before this method is called. The current values of the parameters are ['', 'some endpoint']


            >>> #my_query = Sparql_Query(query_file='queries//simplest.rq')
            >>> #my_query.get_results(endpoint_address="http://145.100.59.37:3500/blazegraph/sparql")
        """
        if endpoint_address == '':
            endpoint_address = self.endpoint_address
        self.endpoint_address = endpoint_address

        from preprocessor.string_tools import Parameter_Value
        # Required parameters cannot have the values of '' or None
        Parameter_Value.require_parameters(parameters_list=[self.query, self.endpoint_address],
                                           parameter_names=['query', 'endpoint_address'])

        from SPARQLWrapper import SPARQLWrapper, JSON

        sparql_wrapper = SPARQLWrapper(self.endpoint_address)

        sparql_wrapper.setQuery(self.query)
        sparql_wrapper.setReturnFormat(JSON)

        results = sparql_wrapper.query().convert()

        results_dictionary = {}
        for i, each_result in enumerate(results["results"]["bindings"]):

            iteraton_no = i + 1  # to start counting entries from 1 instead of 0
            results_dictionary[iteraton_no] = {}

            for each_field_name, each_field_values_dictionary in each_result.items():
                results_dictionary[iteraton_no][each_field_name] = each_field_values_dictionary['value']

            self.number_of_lines_retrieved = iteraton_no

        self.results = results_dictionary

        if print_only:
            self.print_results()
        else:
            return self.results


    def print_query(self):
        """
        For prettier console output, as calling the object or 'self.conent' instead returns the query with newline chars
        visible (i.e., '\\n's appearing in string)

        Returns:
            nothing

        Examples:
            >>> my_query_string = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\\n'\
                                  'SELECT ?label\\n'\
                                  'WHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }\\n'  # this
            >>>                   # notation (e.g., \\n at the end) is only necessary in docstrings, and actual
            >>>                   # string can be written inside ''' ''' marks in a Python script.


            >>> my_query = Sparql_Query().set_query(my_query_string)
            >>> my_query.print_query()
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?label
            WHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }
            <BLANKLINE>
        """
        print(self.query)


    def print_results(self):
        """
        For prettier console output, as calling the object or 'self.results' instead returns the query as one line

        Returns:
            nothing

        Examples:
            >>> my_query_string = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\\n'\
                                  'SELECT ?label\\n'\
                                  'WHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }\\n'  # this
            >>>                   # notation (e.g., \\n at the end) is only necessary in docstrings, and actual
            >>>                   # string can be written inside ''' ''' marks in a Python script.


            >>> my_query = Sparql_Query().set_query(my_query_string)
            >>> my_query.print_query()
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?label
            WHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }
            <BLANKLINE>

            >>> my_query.set_endpoint('http://dbpedia.org/sparql')\
                        .endpoint_address
            'http://dbpedia.org/sparql'

            >>> my_query.retrieve_results_from_endpoint(print_only=False)
            {1: {'label': 'أمثلة (توضيح)'}, 2: {'label': 'Example'}, 3: {'label': 'Example (Begriffsklärung)'}, 4: {'label': 'Example'}}
            >>> my_query.print_results()
            {1: {'label': 'أمثلة (توضيح)'},
             2: {'label': 'Example'},
             3: {'label': 'Example (Begriffsklärung)'},
             4: {'label': 'Example'}}
        """
        from pprint import pprint
        pprint(self.results)


    def write_results_to_csv(self, output_file_path):
        """
        Returns:
            nothing

        Examples:
            >>> my_query = Sparql_Query().import_query_from_file('test_data_and_queries//simple_dbpedia_test.rq')
            >>> my_query.retrieve_results_from_endpoint('http://dbpedia.org/sparql')
            {1: {'label': 'أمثلة (توضيح)'}, 2: {'label': 'Example'}, 3: {'label': 'Example (Begriffsklärung)'}, 4: {'label': 'Example'}}
            >>> my_query.print_results()
            {1: {'label': 'أمثلة (توضيح)'},
             2: {'label': 'Example'},
             3: {'label': 'Example (Begriffsklärung)'},
             4: {'label': 'Example'}}
            >>> my_query.write_results_to_csv('test_data_and_queries//test_write_of_sparql_results.csv')
            The results were written to "test_data_and_queries//test_write_of_sparql_results.csv"

            >>> from preprocessor.Text_File import Text_File
            >>> output_file = Text_File('test_data_and_queries//test_write_of_sparql_results.csv')
            >>> output_file.preview(5)
            "label" ,
            "أمثلة (توضيح)" ,
            "Example" ,
            "Example (Begriffsklärung)" ,
            "Example" ,

            >>> from retriever.sparql_tools import Open_Citations_Query
            >>> my_oc_query = Open_Citations_Query()
            >>> my_oc_query.retrieve_articles_by_dois(['10.1186/s13034-015-0062-7',
            ...                                                    '10.1016/s0090-8258(03)00126-4',
            ...                                                    '10.1016/s0090-8258(03)00087-8'])
            DOI validation completed
            Number of valid DOIs: 3
            Number of invalid DOIs: 0
            Valid and invalid query criteria in parameter "doi_list" were recorded in instance variables
            <BLANKLINE>
            All queries were completed successfully (3 results retrieved out of 3 queries)
            {1: {'journal_article': 'https://w3id.org/oc/corpus/br/362418', 'publication_type': 'Article', 'title': 'The DSM-5 diagnosis of nonsuicidal self-injury disorder: a review of the empirical literature', 'publication_year': '2015', 'journal_name': 'Child and Adolescent Psychiatry and Mental Health - Child Adolesc Psychiatry Ment Health', 'journal_issue_number': '1', 'journal_volume_number': '9', 'publisher_name': 'Springer Science + Business Media', 'doi': '10.1186/s13034-015-0062-7', 'pmid': '26417387', 'url': 'http://dx.doi.org/10.1186/s13034-015-0062-7', 'authors': 'Zetterqvist - Maria', 'cited_the_articles': 'https://w3id.org/oc/corpus/br/37961 | https://w3id.org/oc/corpus/br/38250 | https://w3id.org/oc/corpus/br/135448 | https://w3id.org/oc/corpus/br/135458 | https://w3id.org/oc/corpus/br/177639 | https://w3id.org/oc/corpus/br/177648 | https://w3id.org/oc/corpus/br/177653 | https://w3id.org/oc/corpus/br/177661 | https://w3id.org/oc/corpus/br/177774 | https://w3id.org/oc/corpus/br/362419 | https://w3id.org/oc/corpus/br/362426 | https://w3id.org/oc/corpus/br/362438 | https://w3id.org/oc/corpus/br/607811 | https://w3id.org/oc/corpus/br/1270766 | https://w3id.org/oc/corpus/br/1560911 | https://w3id.org/oc/corpus/br/1794850 | https://w3id.org/oc/corpus/br/1881397 | https://w3id.org/oc/corpus/br/2258672 | https://w3id.org/oc/corpus/br/2907029 | https://w3id.org/oc/corpus/br/2907034 | https://w3id.org/oc/corpus/br/2907035 | https://w3id.org/oc/corpus/br/2907042 | https://w3id.org/oc/corpus/br/2907056 | https://w3id.org/oc/corpus/br/3346205 | https://w3id.org/oc/corpus/br/3567493 | https://w3id.org/oc/corpus/br/3567495 | https://w3id.org/oc/corpus/br/3949890 | https://w3id.org/oc/corpus/br/5106137 | https://w3id.org/oc/corpus/br/5441063 | https://w3id.org/oc/corpus/br/5441066 | https://w3id.org/oc/corpus/br/5441085 | https://w3id.org/oc/corpus/br/5656230 | https://w3id.org/oc/corpus/br/6060536 | https://w3id.org/oc/corpus/br/6063037 | https://w3id.org/oc/corpus/br/6449521 | https://w3id.org/oc/corpus/br/6486152 | https://w3id.org/oc/corpus/br/6486162 | https://w3id.org/oc/corpus/br/6919305 | https://w3id.org/oc/corpus/br/6919323 | https://w3id.org/oc/corpus/br/7558746 | https://w3id.org/oc/corpus/br/7560541 | https://w3id.org/oc/corpus/br/7560644 | https://w3id.org/oc/corpus/br/7560645 | https://w3id.org/oc/corpus/br/7560646 | https://w3id.org/oc/corpus/br/7560647 | https://w3id.org/oc/corpus/br/7560648 | https://w3id.org/oc/corpus/br/7560651 | https://w3id.org/oc/corpus/br/7560652 | https://w3id.org/oc/corpus/br/7560653 | https://w3id.org/oc/corpus/br/7560654 | https://w3id.org/oc/corpus/br/7560655 | https://w3id.org/oc/corpus/br/7560656 | https://w3id.org/oc/corpus/br/7560657 | https://w3id.org/oc/corpus/br/7560658 | https://w3id.org/oc/corpus/br/7560659 | https://w3id.org/oc/corpus/br/7560660 | https://w3id.org/oc/corpus/br/7560661 | https://w3id.org/oc/corpus/br/7560662 | https://w3id.org/oc/corpus/br/7560663 | https://w3id.org/oc/corpus/br/7560664 | https://w3id.org/oc/corpus/br/7560665 | https://w3id.org/oc/corpus/br/7560666', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/362415'}, 2: {'journal_article': 'https://w3id.org/oc/corpus/br/384', 'publication_type': 'Article', 'title': 'Survival after relapse in patients with endometrial cancer: results from a randomized trial☆', 'publication_year': '2003', 'journal_name': 'Gynecologic Oncology', 'journal_issue_number': '2', 'journal_volume_number': '89', 'publisher_name': 'Elsevier BV', 'doi': '10.1016/s0090-8258(03)00126-4', 'pmid': '12713981', 'url': 'http://dx.doi.org/10.1016/s0090-8258%2803%2900126-4', 'authors': 'Creutzberg - Carien L | van Putten - Wim L.J | Koper - Peter C | Lybeert - Marnix L.M | Jobsen - Jan J | Wárlám-Rodenhuis - Carla C | De Winter - Karin A.J | Lutgens - Ludy C.H.W | van den Bergh - Alfons C.M | van der Steen-Banasik - Elzbieta | Beerman - Henk | van Lent - Mat', 'cited_the_articles': '', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/1 | https://w3id.org/oc/corpus/br/1342763 | https://w3id.org/oc/corpus/br/1772164'}, 3: {'journal_article': 'https://w3id.org/oc/corpus/br/392', 'publication_type': 'Article', 'title': 'Stage IC adenocarcinoma of the endometrium: survival comparisons of surgically staged patients with and without adjuvant radiation therapyâ\x98\x86â\x98\x86Presented at the 33rd Annual Meeting of Gynecologic Oncologists, Miami, FL, March 2002.', 'publication_year': '2003', 'journal_name': 'Gynecologic Oncology', 'journal_issue_number': '2', 'journal_volume_number': '89', 'publisher_name': 'Elsevier BV', 'doi': '10.1016/s0090-8258(03)00087-8', 'pmid': '12713994', 'url': 'http://dx.doi.org/10.1016/s0090-8258%2803%2900087-8', 'authors': 'Straughn - J.Michael | Huh - Warner K | Orr - James W | Kelly - F.Joseph | Roland - Phillip Y | Gold - Michael A | Powell - Matthew | Mutch - David G | Partridge - Edward E | Kilgore - Larry C | Barnes - Mack N | Austin - J.Maxwell | Alvarez - Ronald D', 'cited_the_articles': '', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/1'}}

            >>> my_oc_query.write_results_to_csv('test_data_and_queries//test_write_of_sparql_results.csv')
            The results were written to "test_data_and_queries//test_write_of_sparql_results.csv"
            >>> output_file = Text_File('test_data_and_queries//test_write_of_sparql_results.csv')
            >>> output_file.preview(4)
            "journal_article" , "publication_type" , "title" , "publication_year" , "journal_name" , "journal_issue_number" , "journal_volume_number" , "publisher_name" , "doi" , "pmid" , "url" , "authors" , "cited_the_articles" , "cited_by_the_articles" ,
            "https://w3id.org/oc/corpus/br/362418" , "Article" , "The DSM-5 diagnosis of nonsuicidal self-injury disorder: a review of the empirical literature" , "2015" , "Child and Adolescent Psychiatry and Mental Health - Child Adolesc Psychiatry Ment Health" , "1" , "9" , "Springer Science + Business Media" , "10.1186/s13034-015-0062-7" , "26417387" , "http://dx.doi.org/10.1186/s13034-015-0062-7" , "Zetterqvist - Maria" , "https://w3id.org/oc/corpus/br/37961 | https://w3id.org/oc/corpus/br/38250 | https://w3id.org/oc/corpus/br/135448 | https://w3id.org/oc/corpus/br/135458 | https://w3id.org/oc/corpus/br/177639 | https://w3id.org/oc/corpus/br/177648 | https://w3id.org/oc/corpus/br/177653 | https://w3id.org/oc/corpus/br/177661 | https://w3id.org/oc/corpus/br/177774 | https://w3id.org/oc/corpus/br/362419 | https://w3id.org/oc/corpus/br/362426 | https://w3id.org/oc/corpus/br/362438 | https://w3id.org/oc/corpus/br/607811 | https://w3id.org/oc/corpus/br/1270766 | https://w3id.org/oc/corpus/br/1560911 | https://w3id.org/oc/corpus/br/1794850 | https://w3id.org/oc/corpus/br/1881397 | https://w3id.org/oc/corpus/br/2258672 | https://w3id.org/oc/corpus/br/2907029 | https://w3id.org/oc/corpus/br/2907034 | https://w3id.org/oc/corpus/br/2907035 | https://w3id.org/oc/corpus/br/2907042 | https://w3id.org/oc/corpus/br/2907056 | https://w3id.org/oc/corpus/br/3346205 | https://w3id.org/oc/corpus/br/3567493 | https://w3id.org/oc/corpus/br/3567495 | https://w3id.org/oc/corpus/br/3949890 | https://w3id.org/oc/corpus/br/5106137 | https://w3id.org/oc/corpus/br/5441063 | https://w3id.org/oc/corpus/br/5441066 | https://w3id.org/oc/corpus/br/5441085 | https://w3id.org/oc/corpus/br/5656230 | https://w3id.org/oc/corpus/br/6060536 | https://w3id.org/oc/corpus/br/6063037 | https://w3id.org/oc/corpus/br/6449521 | https://w3id.org/oc/corpus/br/6486152 | https://w3id.org/oc/corpus/br/6486162 | https://w3id.org/oc/corpus/br/6919305 | https://w3id.org/oc/corpus/br/6919323 | https://w3id.org/oc/corpus/br/7558746 | https://w3id.org/oc/corpus/br/7560541 | https://w3id.org/oc/corpus/br/7560644 | https://w3id.org/oc/corpus/br/7560645 | https://w3id.org/oc/corpus/br/7560646 | https://w3id.org/oc/corpus/br/7560647 | https://w3id.org/oc/corpus/br/7560648 | https://w3id.org/oc/corpus/br/7560651 | https://w3id.org/oc/corpus/br/7560652 | https://w3id.org/oc/corpus/br/7560653 | https://w3id.org/oc/corpus/br/7560654 | https://w3id.org/oc/corpus/br/7560655 | https://w3id.org/oc/corpus/br/7560656 | https://w3id.org/oc/corpus/br/7560657 | https://w3id.org/oc/corpus/br/7560658 | https://w3id.org/oc/corpus/br/7560659 | https://w3id.org/oc/corpus/br/7560660 | https://w3id.org/oc/corpus/br/7560661 | https://w3id.org/oc/corpus/br/7560662 | https://w3id.org/oc/corpus/br/7560663 | https://w3id.org/oc/corpus/br/7560664 | https://w3id.org/oc/corpus/br/7560665 | https://w3id.org/oc/corpus/br/7560666" , "https://w3id.org/oc/corpus/br/362415" ,
            "https://w3id.org/oc/corpus/br/384" , "Article" , "Survival after relapse in patients with endometrial cancer: results from a randomized trial☆" , "2003" , "Gynecologic Oncology" , "2" , "89" , "Elsevier BV" , "10.1016/s0090-8258(03)00126-4" , "12713981" , "http://dx.doi.org/10.1016/s0090-8258%2803%2900126-4" , "Creutzberg - Carien L | van Putten - Wim L.J | Koper - Peter C | Lybeert - Marnix L.M | Jobsen - Jan J | Wárlám-Rodenhuis - Carla C | De Winter - Karin A.J | Lutgens - Ludy C.H.W | van den Bergh - Alfons C.M | van der Steen-Banasik - Elzbieta | Beerman - Henk | van Lent - Mat" , "" , "https://w3id.org/oc/corpus/br/1 | https://w3id.org/oc/corpus/br/1342763 | https://w3id.org/oc/corpus/br/1772164" ,
            "https://w3id.org/oc/corpus/br/392" , "Article" , "Stage IC adenocarcinoma of the endometrium: survival comparisons of surgically staged patients with and without adjuvant radiation therapyââPresented at the 33rd Annual Meeting of Gynecologic Oncologists, Miami, FL, March 2002." , "2003" , "Gynecologic Oncology" , "2" , "89" , "Elsevier BV" , "10.1016/s0090-8258(03)00087-8" , "12713994" , "http://dx.doi.org/10.1016/s0090-8258%2803%2900087-8" , "Straughn - J.Michael | Huh - Warner K | Orr - James W | Kelly - F.Joseph | Roland - Phillip Y | Gold - Michael A | Powell - Matthew | Mutch - David G | Partridge - Edward E | Kilgore - Larry C | Barnes - Mack N | Austin - J.Maxwell | Alvarez - Ronald D" , "" , "https://w3id.org/oc/corpus/br/1" ,


        """
        from preprocessor.csv_tools import CSV_Line, CSV_Row, CSV_File
        from triplicator.bibTools import Bibliography
        from preprocessor.ListData import ListData
        from meta.consoleOutput import ConsoleOutput

        console = ConsoleOutput(log_file_path='log.txt')

        list_data = ListData()
        list_data.import_json_object(self.results)

        all_formatted_lines = []
        for each_line in list_data.dataset:
            each_row = CSV_Row(each_line)
            formatted_csv_line = each_row.format_for_print_and_CONVERT_to_CSV_Line(
                column_separator=' , ',
                line_head=' ',
                line_tail=' ,',
                cell_wrapper='"')
            all_formatted_lines.append(formatted_csv_line)

        with open(output_file_path, mode='w', encoding='utf8') as output_file:
            for each_row in all_formatted_lines:
                print(each_row, file=output_file)

            message = 'The results were written to "%s"' % output_file_path
            console.log_message(message, add_timestamp_in_file=True)


    def update_query_parameters_registry(self, parameter_name, parameter_value):
        """
        Updates query parameters for later retrieval. Intended for logging.
        WARNING: Could results in significant memory consumption in large queries. Could be used for diagnostic purposes but it is probably not a good idea to make this method a part of a regular algorithm.

        Returns:
            nothing

        Examples:
            >>> my_query = Sparql_Query()
            >>> my_query.update_query_parameters_registry(parameter_name = 'authors', parameter_value='Jane Doe')
            >>> my_query.query_parameters_registry
            {'authors': ['Jane Doe']}
            >>> my_query.update_query_parameters_registry(parameter_name = 'authors', parameter_value=['April Smith', 'June Doe'])
            >>> my_query.query_parameters_registry
            {'authors': ['Jane Doe', ['April Smith', 'June Doe']]}
            >>> my_query.update_query_parameters_registry(parameter_name = 'issn', parameter_value=['572652267325756'])
            >>> my_query.query_parameters_registry
            {'authors': ['Jane Doe', ['April Smith', 'June Doe']], 'issn': [['572652267325756']]}
        """
        try:
            self.query_parameters_registry[parameter_name].append(parameter_value)
        except KeyError:
            self.query_parameters_registry[parameter_name] = [parameter_value]


        #self.query_parameters_registry = {parameter_name: parameter_value}



class Gastrodon_Query():

    def __init__(self):

        import pandas
        pandas.options.display.width = 120
        pandas.options.display.max_colwidth = 100

        self.endpoint_object = None
        self.prefixes_object = None


    def send_select_query(self, query):
        """
        Args:
            query(str)

        Returns:
           pandas DataFrame

        Notes:
            Gastrodon_Query modules are also tested using unit tests.

        Examples:
            >>> query = Gastrodon_Query()
            >>> results = query.set_prefixes('@prefix dbo: <http://dbpedia.org/ontology/> .')\
                     .set_endpoint('http://dbpedia.org/sparql')\
                     .send_select_query("SELECT ?s ?p ?o WHERE {?s ?p ?o .} LIMIT 2")
            >>> results['s'][1]
            rdflib.term.URIRef('http://www.openlinksw.com/virtrdf-data-formats#default-iid-nullable')
            >>> results['p'][1]
            'rdf:type'
            >>> results['o'][1]
            rdflib.term.URIRef('http://www.openlinksw.com/schemas/virtrdf#QuadMapFormat')
        """
        self._check_if_minimum_query_parameters_specified()

        result = self.endpoint_object.select(query)
        return result


    def send_construct_query(self, query):
        """

        Args:
            query(str)

        Returns:
            pandas.DataFrame


        Examples:
            >>> # Init and send simple query
            >>> query = Gastrodon_Query()
            >>> query.set_prefixes('@prefix dbo: <http://dbpedia.org/ontology/> .\\n @prefix cc: <http://creativecommons.org/ns#> .')\
                     .set_endpoint('http://dbpedia.org/sparql')\
                     .send_construct_query('CONSTRUCT {<a> <b> <c> . } WHERE {?s ?p ?o} LIMIT 10')
              Subject Predicate Object
            0       a         b      c

            >>> # Send a slightly more complex query (only one result is being requested due to results being returned
            >>> # with random order)
            >>> query.send_construct_query('CONSTRUCT {?s <has_license> <http://www.gnu.org/copyleft/fdl.html> . } WHERE {?s cc:license <http://www.gnu.org/copyleft/fdl.html> .}')
              Subject    Predicate                                Object
            0    dbo:  has_license  http://www.gnu.org/copyleft/fdl.html

        """
        import pandas, numpy
        from preprocessor.data_tools import Pandas_Dataframe

        self._check_if_minimum_query_parameters_specified()

        result_as_graph = self.endpoint_object.construct(query)

        result_as_dataframe = pandas.DataFrame(columns=['Subject', 'Predicate', 'Object'])
        result_as_dataframe = Pandas_Dataframe(result_as_dataframe)  # Pandas_Dataframe is a class that extends the
                                                                     #  functionality of pandas.DataFrame

        for (s, p, o) in result_as_graph.triples((None, None, None)):  # None acts as the wildcard '*'

            s = self._shorten_uri_using_prefixes_if_possible(s)
            p = self._shorten_uri_using_prefixes_if_possible(p)
            o = self._shorten_uri_using_prefixes_if_possible(o)

            each_row_dataframe = pandas.DataFrame(numpy.array([[s, p, o]]), columns=['Subject', 'Predicate', 'Object'])
            result_as_dataframe.insert_dataframe_at_index(len(result_as_dataframe.dataframe), each_row_dataframe)

        return result_as_dataframe.dataframe


    def send_update_query(self, query):
        """

        Args:
            query(str)

        """

        self._check_if_minimum_query_parameters_specified()

        self.endpoint_object.update(query)



    def send_count_query(self, query_variable_that_holds_count_results, query):
        """
        Args:
            query(str)
            query_variable_that_holds_count_results(str)

        Returns:
           int

        Notes:
            Gastrodon_Query modules are also tested using unit tests.

        Examples:
            >>> query = Gastrodon_Query()
            >>> query.set_prefixes('@prefix dbo: <http://dbpedia.org/ontology/> .\\n @prefix cc: <http://creativecommons.org/ns#> .')\
                     .set_endpoint('http://dbpedia.org/sparql')\
                     .send_count_query('licenses', 'SELECT (COUNT(?s) AS ?licenses) {?s cc:license ?o .}')
            4
        """
        result = self.send_select_query(query=query).at[0, query_variable_that_holds_count_results]
        return result


    def set_prefixes(self, prefixes):
        """
        Args:
            prefixes(str)

        Returns:
            Gastrodon_Query

        Notes:
            Gastrodon_Query modules are also also tested using unit tests.

        Examples:
            >>> gastrodon_query = Gastrodon_Query()
            >>> gastrodon_query.set_prefixes('@prefix dbo: <http://dbpedia.org/ontology/> .')\
                               ._get_prefixes()
            {rdflib.term.URIRef('http://www.w3.org/XML/1998/namespace'): 'xml', rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'): 'rdf', rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#'): 'rdfs', rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#'): 'xsd', rdflib.term.URIRef('http://dbpedia.org/ontology/'): 'dbo'}

            >>> gastrodon_query.set_prefixes('@prefix dbo: <http://dbpedia.org/ontology/> .\\n'\
                                             '@prefix dbr: <http://dbpedia.org/resource/> .')\
                               ._get_prefixes()
            ... # The prefixes above can also be surrounded with three double quotes when ran form script or terminal.
            ... # This current notation is only for testing, as docstring environment prevents usage of three double
            ... # quotes within tests.
            {rdflib.term.URIRef('http://www.w3.org/XML/1998/namespace'): 'xml', rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'): 'rdf', rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#'): 'rdfs', rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#'): 'xsd', rdflib.term.URIRef('http://dbpedia.org/ontology/'): 'dbo', rdflib.term.URIRef('http://dbpedia.org/resource/'): 'dbr'}
        """
        import gastrodon
        prefixes_object = gastrodon.inline("""
                    %s
                """ % prefixes).graph
        self.prefixes_object = prefixes_object
        return self


    def set_endpoint(self, endpoint_url):
        """
        Args:
            endpoint_url(str)

        Returns:
            Gastrodon_Query

        Examples:
            >>> # Set and get endpoint
            >>> gastrodon_query = Gastrodon_Query()
            >>> gastrodon_query.set_prefixes('@prefix dbo: <http://dbpedia.org/ontology/> .')\
                               .set_endpoint('http://dbpedia.org/sparql')\
                               ._get_endpoint()
            'http://dbpedia.org/sparql'

            >>> # Prefixes must be set before the end point (exception)
            >>> gastrodon_query_two = Gastrodon_Query()
            >>> try:
            ...     gastrodon_query_two.set_endpoint('http://dbpedia.org/sparql')
            ... except Exception as error_message:
            ...     print('Exception caught:', error_message)
            Exception caught: Parameters '['prefixes']' must be specified before this method is called. The current values of the parameters are [None]

        Notes:
            Gastrodon_Query modules are also tested using unit tests.
        """
        import gastrodon
        from preprocessor.string_tools import Parameter_Value
        Parameter_Value().require_parameters([self.prefixes_object], ['prefixes'])

        endpoint_object = gastrodon.RemoteEndpoint(
            url=endpoint_url,
            default_graph=None,
            prefixes=self.prefixes_object
        )

        self.endpoint_object = endpoint_object
        return self


    def _get_endpoint(self):
        """
        Returns:
            str

        Examples:
            >>> gastrodon_query = Gastrodon_Query()
            >>> gastrodon_query.set_prefixes('@prefix dbo: <http://dbpedia.org/ontology/> .')\
                               .set_endpoint('http://dbpedia.org/sparql')\
                               ._get_endpoint()
            'http://dbpedia.org/sparql'

            >>> gastrodon_query.endpoint_object = None
            >>> gastrodon_query._get_endpoint()

        Notes:
            Gastrodon_Query modules are also tested using unit tests.
        """
        if self.endpoint_object != None:
            return self.endpoint_object.url
        else:
            return self.endpoint_object


    def _get_prefixes(self, convert_to_dictionary_of_strings=False):
        """
        Returns a dictionary of namespace uris and their corresponding prefixes (i.e., their abbreviations).

        Args:
            convert_to_dictionary_of_strings(bool): If True, returns the dictionary in {str1: str2, str3: str4} format. If False, returns the dictionary in {rdflib.term.URIRef1: str1, rdflib.term.URIRef2: str2} format.

        Returns:
            dict of rdflib.term.URIRef objects vs strings, dict of strins, or nothing (see Args)

        Examples:
            >>> gastrodon_query = Gastrodon_Query()
            >>> gastrodon_query.set_prefixes('@prefix dbo: <http://dbpedia.org/ontology/> .')\
                               ._get_prefixes()
            {rdflib.term.URIRef('http://www.w3.org/XML/1998/namespace'): 'xml', rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'): 'rdf', rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#'): 'rdfs', rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#'): 'xsd', rdflib.term.URIRef('http://dbpedia.org/ontology/'): 'dbo'}

            >>> gastrodon_query.set_prefixes('@prefix dbo: <http://dbpedia.org/ontology/> .\\n'\
                                             '@prefix dbr: <http://dbpedia.org/resource/> .')\
                                ._get_prefixes()
            ... # The prefixes above can also be surrounded with three double quotes when ran form script or terminal.
            ... # This current notation is only for testing, as docstring environment prevents usage of three double
            ... # quotes within tests.
            {rdflib.term.URIRef('http://www.w3.org/XML/1998/namespace'): 'xml', rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'): 'rdf', rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#'): 'rdfs', rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#'): 'xsd', rdflib.term.URIRef('http://dbpedia.org/ontology/'): 'dbo', rdflib.term.URIRef('http://dbpedia.org/resource/'): 'dbr'}

            >>> # return prefixes and uris as a dictionary of strings:
            >>> gastrodon_query._get_prefixes(convert_to_dictionary_of_strings=True)
            {'http://www.w3.org/XML/1998/namespace': 'xml', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#': 'rdf', 'http://www.w3.org/2000/01/rdf-schema#': 'rdfs', 'http://www.w3.org/2001/XMLSchema#': 'xsd', 'http://dbpedia.org/ontology/': 'dbo', 'http://dbpedia.org/resource/': 'dbr'}
            >>> # empty_prefix (returns no output)
            >>> gastrodon_query = Gastrodon_Query()
            >>> gastrodon_query._get_prefixes()
        """
        import gastrodon
        if self.prefixes_object == None:
            return self.prefixes_object

        else:
            if convert_to_dictionary_of_strings:
                stringified_uris_and_prefixes = {}
                for each_uri, each_prefix in self.prefixes_object.store._IOMemory__prefix.items():
                    each_uri_as_string = str(each_uri)
                    stringified_uris_and_prefixes[each_uri_as_string] = each_prefix
                return stringified_uris_and_prefixes

            else:
                return self.prefixes_object.store._IOMemory__prefix


    def _shorten_uri_using_prefixes_if_possible(self, uri):
        """
        Shortens a specified URI using the prefixes attribute of the Gastrodon_Query instance.

        Args:
            uri(str or rdflib.term.URIRef): A long uri such as 'http://www.w3.org/XML/1998/namespace' or rdflib.term.URIRef('http://www.w3.org/XML/1998/namespace')
                or

        Returns:
            str

        Examples:
            >>> # Shorten a string URI
            >>> query = Gastrodon_Query()
            >>> query.set_prefixes('@prefix dbo: <http://dbpedia.org/ontology/> .\\n @prefix cc: <http://creativecommons.org/ns#> .')\
                     ._shorten_uri_using_prefixes_if_possible('http://dbpedia.org/ontology/test')
            'dbo:test'

            >>> # Shorten a rdflib.term.URIRef URI
            >>> import rdflib
            >>> query = Gastrodon_Query()
            >>> query.set_prefixes('@prefix dbo: <http://dbpedia.org/ontology/> .\\n @prefix cc: <http://creativecommons.org/ns#> .')\
                     ._shorten_uri_using_prefixes_if_possible(rdflib.term.URIRef('http://dbpedia.org/ontology/test'))
            'dbo:test'

            >>> # URI does not have a prefix specified in the instance prefixes (returns uri as is [and as a string]):
            >>> import rdflib
            >>> query = Gastrodon_Query()
            >>> query.set_prefixes('@prefix dbo: <http://dbpedia.org/ontology/> .\\n @prefix cc: <http://creativecommons.org/ns#> .')\
                     ._shorten_uri_using_prefixes_if_possible('http://example.org/test')
            'http://example.org/test'
        """
        uris_and_prefixes_dictionary = self._get_prefixes(convert_to_dictionary_of_strings=True)
        for each_namespace_uri, each_namespace_prefix in uris_and_prefixes_dictionary.items():

            if each_namespace_uri in uri:
                uri_tail = str(uri).split(sep=each_namespace_uri)[1]
                uri = (each_namespace_prefix + ':' + uri_tail)

        return uri

    @staticmethod
    def _is_graph_prefix(graph_prefix):
        """
        Checks if the given string's formatting indicates that it is a graph name prefix or not

        Args:
            graph_prefix(str)

        Returns:
            bool

        Examples:
            >>> Gastrodon_Query._is_graph_prefix('kfir:')
            True

            >>> Gastrodon_Query._is_graph_prefix('kfir')
            False

            >>> Gastrodon_Query._is_graph_prefix('<http://example.com>')
            False

            >>> Gastrodon_Query._is_graph_prefix('<https://example.com>')
            False

            >>> Gastrodon_Query._is_graph_prefix('https://example.com')
            False

            >>> Gastrodon_Query._is_graph_prefix('https://example.com')
            False
        """

        from preprocessor.string_tools import String

        graph_prefix_String = String(graph_prefix)

        is_full_uri_string = graph_prefix_String.is_any_of_the_patterns_there(['>', '<', 'http://', 'https://'])
        is_graph_prefix = graph_prefix[-1] == ':'

        if is_graph_prefix and not is_full_uri_string:
            return True
        else:
            return False


    def _force_recognition_if_graph_prefix(self, graph_prefix):
        """
        Checks if the specified graph_prefix is indeed a graph prefix, and if it is, checks whether it exists in 
        self.prefixes_object. 
        Does nothing if a full graph uri is provided.

        Args:
            graph_prefix(str)

        Returns:
            ValueError (if graph_prefix is not recongized) or nothing (if it is recognized)

        Examples:
            >>> # Initiate instance
            >>> my_query = Gastrodon_Query()

            >>> # Set query parameters and send a count query
            >>> my_query.set_prefixes('''\
                @prefix wos: <http://wos.risis.eu/vocabulary/> .\
                @prefix wosres: <http://wos.risis.eu/resource/> .\
                @prefix wosGraph: <http://clokman.com/wos> .\
            ''')._get_prefixes(convert_to_dictionary_of_strings=True)
            {'http://www.w3.org/XML/1998/namespace': 'xml', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#': 'rdf', 'http://www.w3.org/2000/01/rdf-schema#': 'rdfs', 'http://www.w3.org/2001/XMLSchema#': 'xsd', 'http://wos.risis.eu/vocabulary/': 'wos', 'http://wos.risis.eu/resource/': 'wosres', 'http://clokman.com/wos': 'wosGraph'}

            >>> # Unrecognized graph prefix
            >>> try:
            ...     my_query._force_recognition_if_graph_prefix('kfir:')
            ... except ValueError as error_message:
            ...     print('Caught error: %s.' % error_message)
            Caught error: The graph prefix "kfir:" is not in known prefixes; consider adding it as a prefix. The current pefixes are: "dict_values(['xml', 'rdf', 'rdfs', 'xsd', 'wos', 'wosres', 'wosGraph']).".

            >>> # Recognized graph prefix
            >>> my_query._force_recognition_if_graph_prefix('wosGraph:')  # returns nothing

            >>> # Not a graph prefix (do nothing)
            >>> my_query._force_recognition_if_graph_prefix('http://example.com')  # returns nothing
        """
        if Gastrodon_Query._is_graph_prefix(graph_prefix):
            current_prefixes = self._get_prefixes(convert_to_dictionary_of_strings=True).values()

            graph_prefix_without_colon = graph_prefix[:-1]

            if graph_prefix_without_colon not in current_prefixes:
                raise ValueError('The graph prefix "{graph_prefix}" is not in known prefixes; consider adding it as a prefix. The current pefixes are: "{current_prefixes}."'.format(graph_prefix=graph_prefix, current_prefixes=current_prefixes))




    def _check_if_minimum_query_parameters_specified(self):
        from preprocessor.string_tools import Parameter_Value
        Parameter_Value().require_parameters([self.prefixes_object, self.endpoint_object],
                                             ['prefixes', 'endpoint'])


class WebOfScienceQuery(Gastrodon_Query):
    def __init__(self, gastrodon_query=None):
        """
        Examples:
            >>> # INITIALIZE FROM EXISTING GASTRODON QUERY =============================================================
            >>> # Initiate Gastrodon_Query object ----------------------------------------------------------------------
            >>> my_gastodon_query = Gastrodon_Query()

            >>> # Set and check prefixes
            >>> my_gastodon_query.set_prefixes('''\
                @prefix wosGraph: <http://clokman.com/wos> .\
                @prefix kfirGraph: <http://clokman.com/kfir> .\
                @prefix testGraph: <http://clokman.com/test> .\
            ''')._get_prefixes()
            {rdflib.term.URIRef('http://www.w3.org/XML/1998/namespace'): 'xml', rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'): 'rdf', rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#'): 'rdfs', rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#'): 'xsd', rdflib.term.URIRef('http://clokman.com/wos'): 'wosGraph', rdflib.term.URIRef('http://clokman.com/kfir'): 'kfirGraph', rdflib.term.URIRef('http://clokman.com/test'): 'testGraph'}

            >>> # Get endpoint address from file, set it, and check
            >>> from preprocessor.Text_File import Text_File
            >>> eculture_endpoint_url_file = Text_File('..//private//eculture_virtuoso_endpoint_address')
            >>> eculture_endpoint_url = eculture_endpoint_url_file.return_content()
            >>> url = my_gastodon_query.set_endpoint(eculture_endpoint_url)\
                              .endpoint_object.url
            >>> print(type(url), len(url))  # for checking the endpoint url without revealing it
            <class 'str'> 50
            >>> #-------------------------------------------------------------------------------------------------------

            >>> # Import to WebOfScienceQuery and test functionality ---------------------------------------------------
            >>> my_wos_query = WebOfScienceQuery(my_gastodon_query)
            >>> my_wos_query._get_prefixes()
            {rdflib.term.URIRef('http://www.w3.org/XML/1998/namespace'): 'xml', rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'): 'rdf', rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#'): 'rdfs', rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#'): 'xsd', rdflib.term.URIRef('http://clokman.com/wos'): 'wosGraph', rdflib.term.URIRef('http://clokman.com/kfir'): 'kfirGraph', rdflib.term.URIRef('http://clokman.com/test'): 'testGraph'}

            >>> private_endpoint_url = my_wos_query.endpoint_object.url
            >>> print(type(url), len(url))  # for checking the endpoint url without revealing it
            <class 'str'> 50

            >>> # Run queries
            >>> results = my_wos_query.send_select_query("SELECT ?s ?p ?o WHERE {?s ?p ?o .} LIMIT 2")
            >>> results['s'][0]
            rdflib.term.URIRef('http://www.openlinksw.com/virtrdf-data-formats#default-iid')
            >>> results['p'][0]
            'rdf:type'
            >>> results['o'][0]
            rdflib.term.URIRef('http://www.openlinksw.com/schemas/virtrdf#QuadMapFormat')

            >>> #-------------------------------------------------------------------------------------------------------
            >>> #=======================================================================================================


            >>> # INITIALIZE FROM SCRATCH ==============================================================================
            >>> # Initiate object
            >>> eculture_query = WebOfScienceQuery()

            >>> # Set and check prefixes
            >>> eculture_query.set_prefixes('''\
                @prefix wosGraph: <http://clokman.com/wos> .\
                @prefix kfirGraph: <http://clokman.com/kfir> .\
                @prefix testGraph: <http://clokman.com/test> .\
            ''')._get_prefixes()
            {rdflib.term.URIRef('http://www.w3.org/XML/1998/namespace'): 'xml', rdflib.term.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'): 'rdf', rdflib.term.URIRef('http://www.w3.org/2000/01/rdf-schema#'): 'rdfs', rdflib.term.URIRef('http://www.w3.org/2001/XMLSchema#'): 'xsd', rdflib.term.URIRef('http://clokman.com/wos'): 'wosGraph', rdflib.term.URIRef('http://clokman.com/kfir'): 'kfirGraph', rdflib.term.URIRef('http://clokman.com/test'): 'testGraph'}

            >>> # Get endpoint address from file, set it, and check
            >>> from preprocessor.Text_File import Text_File
            >>> eculture_endpoint_url_file = Text_File('..//private//eculture_virtuoso_endpoint_address')
            >>> eculture_endpoint_url = eculture_endpoint_url_file.return_content()
            >>> url = eculture_query.set_endpoint(eculture_endpoint_url)\
                              .endpoint_object.url
            >>> print(type(url), len(url))  # for checking the endpoint url without revealing it
            <class 'str'> 50
            >>> #=======================================================================================================
        """
        Gastrodon_Query.__init__(self)

        if gastrodon_query:
            self.__dict__.update(gastrodon_query.__dict__)  # copy all attributes from Gastrodon instance to self
        else:
            pass

        self._last_query_results = None


    def tokenize_process_and_update_string_literals(self, target_property_uri,
                                                   uri_of_source_graph='wosGraph:',
                                                   uri_of_graph_to_write_the_output='kfirGraph:',
                                                   new_property_uri='same as target',
                                                   delimiter_pattern_in_literal_cells='; ',
                                                   query_volume=0, batch_size=10,
                                                   purify=True,
                                                   defragment_strings_using_list=[],
                                                   fragmentation_signalling_character='&',
                                                   fragmentation_signalling_character_index=-1,
                                                   show_progress=False):
        """
        Args:
            target_property_uri(str): The uri of the property that points to literals of interest
            uri_of_graph_to_write_the_output(str): Can be the same or different from the original graph.
            query_volume(int): Works as a global LIMIT keyword put on the query. '0' means maximum possible. The maximum
                possible value is automatically calculated.
            batch_size(int): The number of retrieved results from the triple store to be processed per iteration
                (i.e., in each purification-update cycle). Works as a local LIMIT keyword for each iteration of the
                loop.
            new_property_uri(str): Used for renaming the target_property_uri in the new graph
            show_progress(bool): Shows progress bar during operation

        Returns:
            nothing

        Examples:
            >>> # INIT =================================================================================================
            >>> # Import endpoint address from private file
            >>> from preprocessor.Text_File import Text_File
            >>> eculture_endpoint_url_file = Text_File('..//private//eculture_virtuoso_endpoint_address')
            >>> eculture_endpoint_url = eculture_endpoint_url_file.return_content()

            >>> # Initiate instance
            >>> eculture_query = WebOfScienceQuery()

            >>> # Set query parameters and clear docTestsGraph
            >>> eculture_query.set_prefixes('''\
                @prefix wos: <http://wos.risis.eu/vocabulary/> .\
                @prefix wosres: <http://wos.risis.eu/resource/> .\
                @prefix wosGraph: <http://clokman.com/wos> .\
                @prefix docTestsGraph: <http://clokman.com/doctestsgraph> .\
                @prefix kfir: <http://clokman.com/kfir/ontology#> .\
            ''').set_endpoint(eculture_endpoint_url).send_update_query('CLEAR GRAPH docTestsGraph:')

            >>> # Confirm that the doctest graph is empty
            >>> eculture_query.send_select_query('SELECT * {GRAPH docTestsGraph: {?s ?p ?o}} LIMIT 2')
            Empty DataFrame
            Columns: [s, p, o]
            Index: []
            >>> #=======================================================================================================


            >>> # USAGE WITH DEFAULT PARAMETERS ========================================================================
            >>> # View the literals to be cleaned (Web of Science Categories (wos:WC))
            >>> eculture_query.send_select_query("SELECT DISTINCT ?o {GRAPH wosGraph: {?s a wos:Article; wos:WC ?o}} LIMIT 10")
                                               o
            0            Film, Radio, Television
            1  Clinical Neurology; Neurosciences
            2                      Asian Studies
            3                 Clinical Neurology
            4                     Sport Sciences
            5             Environmental Sciences
            6                     Anesthesiology
            7                         Microscopy
            8       Medicine, General & Internal
            9  Economics; Planning & Development

            >>> # Use the method to purify and tokenize Web of Science categories
            >>> eculture_query.tokenize_process_and_update_string_literals(target_property_uri='wos:WC',
            ...                                                        uri_of_graph_to_write_the_output = 'docTestsGraph:',
            ...                                                        query_volume=50)
            Operation completed without errors.

            >>> eculture_query.send_select_query('SELECT * {GRAPH docTestsGraph: {?s ?p ?o}} LIMIT 15')
                                         s       p                               o
            0   wosres:WOS_000060208200006  wos:WC         Film, Radio, Television
            1   wosres:WOS_000070935900005  wos:WC              Clinical Neurology
            2   wosres:WOS_000070935900005  wos:WC                   Neurosciences
            3   wosres:WOS_000070948900005  wos:WC                   Asian Studies
            4   wosres:WOS_000070961600011  wos:WC              Clinical Neurology
            5   wosres:WOS_000070961600033  wos:WC              Clinical Neurology
            6   wosres:WOS_000070969600003  wos:WC                  Sport Sciences
            7   wosres:WOS_000070970500011  wos:WC          Environmental Sciences
            8   wosres:WOS_000070998100010  wos:WC                  Anesthesiology
            9   wosres:WOS_000070998900007  wos:WC                      Microscopy
            10  wosres:WOS_000071006900008  wos:WC  Medicine, General and Internal
            11  wosres:WOS_000071013000007  wos:WC                       Economics
            12  wosres:WOS_000071013000007  wos:WC        Planning and Development
            13  wosres:WOS_000071018600001  wos:WC                        Oncology
            14  wosres:WOS_000071021600006  wos:WC       Pharmacology and Pharmacy
            >>> #=======================================================================================================


            >>> # USAGE WITH CUSTOM PARAMETERS =========================================================================
            >>> # Clean doctest graph and confirm cleaning
            >>> eculture_query.send_update_query('CLEAR GRAPH docTestsGraph:')
            >>> eculture_query.send_select_query('SELECT * {GRAPH docTestsGraph: {?s ?p ?o}} LIMIT 2')
            Empty DataFrame
            Columns: [s, p, o]
            Index: []

            >>> # View the literals to be cleaned (Author keywords (wos:DE))
            >>> eculture_query.send_select_query("SELECT DISTINCT ?o {GRAPH wosGraph: {?s a wos:Article; wos:DE ?o}} LIMIT 10")
                                                                                      o
            0           Elymus athericus; growth; photosynthesis; ozone; UV-B radiation
            1                              pain, postoperative; analgesics, prescribing
            2           DIC; Nomarski; interference; microscopy; CCD; image processing;
            3  analysis; reconstruction; optical pathlength; phase; transparent; living
            4                    atherosclerosis; homocysteine; metformin; vitamin B-12
            5                                               policy; household economics
            6      sub-Saharan Africa; Swaziland; labor migration; food security; labor
            7                nitric oxide radical; NO scavenging; thiol; S-nitrosothiol
            8                                             (electrochemical); NO sensing
            9      lumbar spine; vertebra; trabecular bone; Wolff's Law; intervertebral

            >>> # Use the method on author keywords (wos:DE)
            >>> eculture_query.tokenize_process_and_update_string_literals(target_property_uri='wos:DE',
            ...                                                        new_property_uri = 'kfir:hasAuthorKeyword',
            ...                                                        uri_of_graph_to_write_the_output = 'docTestsGraph:',
            ...                                                        query_volume=50, batch_size=10)
            Operation completed without errors.

            >>> eculture_query.send_select_query('SELECT * {GRAPH docTestsGraph: {?s ?p ?o}} LIMIT 1000')
                                          s                      p                                                  o
            0    wosres:WOS_000070970500011  kfir:hasAuthorKeyword                                     photosynthesis
            1    wosres:WOS_000070970500011  kfir:hasAuthorKeyword                                              ozone
            2    wosres:WOS_000070970500011  kfir:hasAuthorKeyword                                     UV-B radiation
            3    wosres:WOS_000070970500011  kfir:hasAuthorKeyword                                             growth
            4    wosres:WOS_000070970500011  kfir:hasAuthorKeyword                                   Elymus athericus
            5    wosres:WOS_000070998100010  kfir:hasAuthorKeyword                                pain, postoperative
            6    wosres:WOS_000070998100010  kfir:hasAuthorKeyword                            analgesics, prescribing
            7    wosres:WOS_000070998900007  kfir:hasAuthorKeyword                                                CCD
            8    wosres:WOS_000070998900007  kfir:hasAuthorKeyword                                   image processing
            9    wosres:WOS_000070998900007  kfir:hasAuthorKeyword                                         microscopy
            10   wosres:WOS_000070998900007  kfir:hasAuthorKeyword                                           analysis
            11   wosres:WOS_000070998900007  kfir:hasAuthorKeyword                                             living
            12   wosres:WOS_000070998900007  kfir:hasAuthorKeyword                                     reconstruction
            13   wosres:WOS_000070998900007  kfir:hasAuthorKeyword                                              phase
            14   wosres:WOS_000070998900007  kfir:hasAuthorKeyword                                       interference
            15   wosres:WOS_000070998900007  kfir:hasAuthorKeyword                                 optical pathlength
            16   wosres:WOS_000070998900007  kfir:hasAuthorKeyword                                        transparent
            17   wosres:WOS_000070998900007  kfir:hasAuthorKeyword                                                DIC
            18   wosres:WOS_000070998900007  kfir:hasAuthorKeyword                                           Nomarski
            19   wosres:WOS_000071006900008  kfir:hasAuthorKeyword                                    atherosclerosis
            20   wosres:WOS_000071006900008  kfir:hasAuthorKeyword                                       homocysteine
            21   wosres:WOS_000071006900008  kfir:hasAuthorKeyword                                          metformin
            22   wosres:WOS_000071006900008  kfir:hasAuthorKeyword                                       vitamin B-12
            23   wosres:WOS_000071013000007  kfir:hasAuthorKeyword                                          Swaziland
            24   wosres:WOS_000071013000007  kfir:hasAuthorKeyword                                      food security
            25   wosres:WOS_000071013000007  kfir:hasAuthorKeyword                                 sub-Saharan Africa
            26   wosres:WOS_000071013000007  kfir:hasAuthorKeyword                                             policy
            27   wosres:WOS_000071013000007  kfir:hasAuthorKeyword                                              labor
            28   wosres:WOS_000071013000007  kfir:hasAuthorKeyword                                    labor migration
            29   wosres:WOS_000071013000007  kfir:hasAuthorKeyword                                household economics
            ..                          ...                    ...                                                ...
            122  wosres:WOS_000071166300006  kfir:hasAuthorKeyword                    trigonal-bipyramidal structures
            123  wosres:WOS_000071166300006  kfir:hasAuthorKeyword                                     stereomutation
            124  wosres:WOS_000071166300006  kfir:hasAuthorKeyword                                          Si-29-NMR
            125  wosres:WOS_000071166300006  kfir:hasAuthorKeyword                      lithium pentaorganylsilicates
            126  wosres:WOS_000071166300006  kfir:hasAuthorKeyword                                tetraorganylsilanes
            127  wosres:WOS_000071178700002  kfir:hasAuthorKeyword                                       malnutrition
            128  wosres:WOS_000071178700002  kfir:hasAuthorKeyword                                          lactation
            129  wosres:WOS_000071178700002  kfir:hasAuthorKeyword                                            puberty
            130  wosres:WOS_000071178700002  kfir:hasAuthorKeyword                      hypogonadotropic hypogonadism
            131  wosres:WOS_000071178700002  kfir:hasAuthorKeyword                       Follicle Stimulating Hormone
            132  wosres:WOS_000071178700002  kfir:hasAuthorKeyword                             lactational amenorrhea
            133  wosres:WOS_000071178700002  kfir:hasAuthorKeyword                                           twinning
            134  wosres:WOS_000071178700002  kfir:hasAuthorKeyword                                      twin research
            135  wosres:WOS_000071178700002  kfir:hasAuthorKeyword                                oral contraceptives
            136  wosres:WOS_000071178700002  kfir:hasAuthorKeyword                             weight loss amenorrhea
            137  wosres:WOS_000071178700006  kfir:hasAuthorKeyword                                 prenatal diagnosis
            138  wosres:WOS_000071178700006  kfir:hasAuthorKeyword                                           placenta
            139  wosres:WOS_000071178700006  kfir:hasAuthorKeyword                                 genomic imprinting
            140  wosres:WOS_000071178700006  kfir:hasAuthorKeyword                                        trophoblast
            141  wosres:WOS_000071178700006  kfir:hasAuthorKeyword                                    molar pregnancy
            142  wosres:WOS_000071178700006  kfir:hasAuthorKeyword                                              HASH2
            143  wosres:WOS_000071178700006  kfir:hasAuthorKeyword                  DNA binding transcription factors
            144  wosres:WOS_000071179700013  kfir:hasAuthorKeyword                                        macrophages
            145  wosres:WOS_000071179700013  kfir:hasAuthorKeyword                         retinal pigment epithelium
            146  wosres:WOS_000071179700013  kfir:hasAuthorKeyword                                   membrane protein
            147  wosres:WOS_000071179700013  kfir:hasAuthorKeyword                                               uvea
            148  wosres:WOS_000071179700013  kfir:hasAuthorKeyword             dichloromethylene diphosphonate Cl2MDP
            149  wosres:WOS_000071179700013  kfir:hasAuthorKeyword  experimental melanin-protein induced uveitis EMIU
            150  wosres:WOS_000071179700013  kfir:hasAuthorKeyword                                 pigment epithelial
            151  wosres:WOS_000071179700013  kfir:hasAuthorKeyword                                       uveitis EAPU
            <BLANKLINE>
            [152 rows x 3 columns]
            >>> #=======================================================================================================


            >>> # USAGE ON DIFFERENT DATA THAT REQUIRES DEFRAGMENTATION BUT NO PURIFICATION ============================
            >>> # Clean doctest graph and confirm cleaning
            >>> eculture_query.send_update_query('CLEAR GRAPH docTestsGraph:')
            >>> eculture_query.send_select_query('SELECT * {GRAPH docTestsGraph: {?s ?p ?o}} LIMIT 2')
            Empty DataFrame
            Columns: [s, p, o]
            Index: []

            # >>> eculture_query.send_update_query("INSERT DATA {GRAPH docTestsGraph: {<ab> <b> <c> .}}")
            # >>> eculture_query.send_select_query('SELECT * {GRAPH docTestsGraph: {?s ?p ?o}} LIMIT 2')

            >>> eculture_query.send_update_query('''
            ...     INSERT DATA {
            ...            GRAPH docTestsGraph: {
            ...                wosres:WOS_000080363400002 a wos:Article;
            ...                                           wos:fragmented_WC "Computational Biology; Statistics & Probability",
            ...                                                             "Computer Science, Interdisciplinary Applications; Mathematical &"
            ...            }
            ... }''')
            >>> eculture_query.send_select_query('SELECT * {GRAPH docTestsGraph: {?s ?p ?o}}')
                                        s                  p                                                                 o
            0  wosres:WOS_000080363400002           rdf:type                                                       wos:Article
            1  wosres:WOS_000080363400002  wos:fragmented_WC                   Computational Biology; Statistics & Probability
            2  wosres:WOS_000080363400002  wos:fragmented_WC  Computer Science, Interdisciplinary Applications; Mathematical &

            >>> from preprocessor.string_tools import String
            >>> list_of_wos_categories = []
            >>>
            >>> with open('..//ontologies//complete_list_of_wos_categories.txt') as wos_categories_file:
            ...     for each_line in wos_categories_file:
            ...         each_line = String(each_line)
            ...         each_line = each_line.clean_from_newline_characters()
            ...         list_of_wos_categories.append(each_line.content)
            >>> print(list_of_wos_categories[145:150])
            ['Mathematical & Computational Biology', 'Mathematics', 'Mathematics, Applied', 'Mathematics, Interdisciplinary Applications', 'Mechanics']


            >>> # Use the method to tokenize, defragment, and upload the results as new data
            >>> eculture_query.tokenize_process_and_update_string_literals(target_property_uri='wos:fragmented_WC',
            ...                                                        uri_of_source_graph='docTestsGraph:',
            ...                                                        new_property_uri = 'kfir:fixed_WC',
            ...                                                        uri_of_graph_to_write_the_output = 'docTestsGraph:',
            ...                                                        purify=False,
            ...                                                        defragment_strings_using_list=list_of_wos_categories,
            ...                                                        query_volume=10, batch_size=10)
            Operation completed without errors.

            >>> # View the result of the tokenization & preprocessing operation:
            >>> # Note that the items 'Mathematical &' and 'Computational Biology' has been merged into one item as a
            >>> # result of the operation.
            >>> eculture_query.send_select_query('SELECT * {GRAPH docTestsGraph: {?s ?p ?o}} LIMIT 1000')
                                        s                  p                                                                 o
            0  wosres:WOS_000080363400002           rdf:type                                                       wos:Article
            1  wosres:WOS_000080363400002  wos:fragmented_WC                   Computational Biology; Statistics & Probability
            2  wosres:WOS_000080363400002  wos:fragmented_WC  Computer Science, Interdisciplinary Applications; Mathematical &
            3  wosres:WOS_000080363400002      kfir:fixed_WC                              Mathematical & Computational Biology
            4  wosres:WOS_000080363400002      kfir:fixed_WC                                          Statistics & Probability
            5  wosres:WOS_000080363400002      kfir:fixed_WC                  Computer Science, Interdisciplinary Applications
            >>> #=======================================================================================================
        """
        from retriever.sparql_tools import Sparql_Parameter
        from preprocessor.dataframe_tools import Data_Frame
        from meta.consoleOutput import ConsoleOutput
        console = ConsoleOutput()
        error_log = []

        # make sure that any graph prefixes used as parameter values are recognized
        self._force_recognition_if_graph_prefix(uri_of_source_graph)
        self._force_recognition_if_graph_prefix(uri_of_graph_to_write_the_output)

        # if no new_property_uri is specified, use the uri of the target property
        if new_property_uri == 'same as target':
            new_property_uri = target_property_uri

        # if query size is zero, assign maximum possible size to it
        if query_volume == 0:
            query_volume = self.count_number_of_instances_of_property(target_property_uri)

        # the main loop of the method
        for current_offset in range(0, query_volume, batch_size):
            if show_progress:
                console.print_current_progress(current_progress=current_offset, maximum_progress=query_volume,
                                               status_message='Processing strings and updating specified graph')

            # Retrieve a subset of the dataset that contains the article ids and associated objects (e.g., keywords)
            ids_vs_target_object = self.retrieve_subjects_and_objects_of_property(target_property_uri, graph=uri_of_source_graph,
                                                                                  desired_column_name_for_literal='targetLiteral',
                                                                                  desired_column_name_for_identifier='wosArticleUri',
                                                                                  limit=batch_size,
                                                                                  offset=current_offset)

            # Because the retrieved keywords are in a semicolon-separated list, they need to be tokenized:
            ids_vs_target_object = Data_Frame(ids_vs_target_object)  # this is not 'pandas.DataFrame' class
            ids_vs_target_object.tokenize_string_column(string_column_name='targetLiteral',
                                                   id_column_name='wosArticleUri',
                                                   delimiter_pattern_in_literal_cells=delimiter_pattern_in_literal_cells)

            # Tokenized keywords may contain items such as "Wolff's Law" and "(electrochemical)".
            # They need to be cleaned from special characters:
            if purify:
                ids_vs_target_object.purify_column(target_column_name='targetLiteral')

            # Collapse the keywords onto article uris as lists
            ids_vs_target_object = ids_vs_target_object.collapse_dataframe_on_column(values_column_name='targetLiteral',
                                                                           identifier_column_name='wosArticleUri')

            if defragment_strings_using_list:
                checklist = defragment_strings_using_list

                ids_vs_target_object.combine_items_within_each_row_if_combination_exists_in_external_list(
                                    target_column_name='targetLiteral',
                                    external_list_to_compare_with=checklist,
                                    fragmentation_signalling_character=fragmentation_signalling_character,
                                    fragmentation_signalling_character_index=fragmentation_signalling_character_index)


            # Extract the author keywords column
            author_keywords_column = ids_vs_target_object.dataframe['targetLiteral']

            # Convert lists on each cell of author keywords column to parameter strings (to be used in VALUES
            # keyword of SPARQL)
            parameterized_keywords = Sparql_Parameter.Values_Parameter_Series()
            parameterized_keywords.import_and_convert_pandas_series(author_keywords_column)

            # Replace the author keywords column of the dataframe with the parameterized version
            ids_vs_target_object.dataframe['targetLiteral'] = parameterized_keywords.series
            ids_vs_target_object.dataframe

            # Update the database
            for index, each_row in ids_vs_target_object.dataframe.iterrows():
                each_article_id = each_row.values[0]
                each_parameter_string = each_row.values[1]
                try:
                    self.send_update_query(
                        """
                        INSERT {
                            GRAPH %s {
                                %s %s ?keyword
                            }
                        }
                        WHERE{
                            VALUES ?keyword {%s}
                        }
                        """ % (uri_of_graph_to_write_the_output, each_article_id, new_property_uri, each_parameter_string)
                    )
                except Exception as error_message:
                    error_log.append(str(error_message))

        # Error logging
        if error_log != []:
            print('Operation completed.')
            print('These %d errors were logged during the operation:') % len(error_log)
            for each_item in error_log:
                print(each_item, '\n')
        else:
            print('Operation completed without errors.')


    def retrieve_subjects_and_objects_of_property(self, property,
                                                  graph='wosGraph:',
                                                  restrict_subjects_to_type='wos:Article',
                                                  desired_column_name_for_literal='targetLiteral',
                                                  desired_column_name_for_identifier='wosArticleUri',
                                                  limit=0, offset=0):
        """
        Retrieves the two sides of a property (i.e., the subject and the object around the property)

        Args:
            property(str): The uri of the property that connects the article to literal.
                (e.g., 'wos:DE' connects Web of Science articles to the literals that are author keywords).
                prefixes if they are defined in Gastrodon Query.
            desired_column_name_for_literal(str)
            offset(int): Value to pass on to SPARQL OFFSET statement
            limit(int): Value to pass on to SPARQL LIMIT statement

        Returns:
            pandas.DataFrame

        Examples:
            >>> # Import endpoint address from private file
            >>> from preprocessor.Text_File import Text_File
            >>> eculture_endpoint_url_file = Text_File('..//private//eculture_virtuoso_endpoint_address')
            >>> eculture_endpoint_url = eculture_endpoint_url_file.return_content()

            >>> # Initiate instance
            >>> eculture_query = WebOfScienceQuery()

            >>> # Set query parameters and send a query
            >>> eculture_query.set_prefixes('''\
                @prefix wos: <http://wos.risis.eu/vocabulary/> .\
                @prefix wosres: <http://wos.risis.eu/resource/> .\
                @prefix wosGraph: <http://clokman.com/wos> .\
            ''').set_endpoint(eculture_endpoint_url)\
                .retrieve_subjects_and_objects_of_property(property='wos:DE', limit=10)
                            wosArticleUri                                                             targetLiteral
            0  wosres:WOS_000070970500011           Elymus athericus; growth; photosynthesis; ozone; UV-B radiation
            1  wosres:WOS_000070998100010                              pain, postoperative; analgesics, prescribing
            2  wosres:WOS_000070998900007           DIC; Nomarski; interference; microscopy; CCD; image processing;
            3  wosres:WOS_000070998900007  analysis; reconstruction; optical pathlength; phase; transparent; living
            4  wosres:WOS_000071006900008                    atherosclerosis; homocysteine; metformin; vitamin B-12
            5  wosres:WOS_000071013000007                                               policy; household economics
            6  wosres:WOS_000071013000007      sub-Saharan Africa; Swaziland; labor migration; food security; labor
            7  wosres:WOS_000071021600006                nitric oxide radical; NO scavenging; thiol; S-nitrosothiol
            8  wosres:WOS_000071021600006                                             (electrochemical); NO sensing
            9  wosres:WOS_000071040300005      lumbar spine; vertebra; trabecular bone; Wolff's Law; intervertebral


            >>> # Send another query that has a different contector_property, offset, and column names
            >>> eculture_query.retrieve_subjects_and_objects_of_property(property='wos:WC',
            ...                                                   desired_column_name_for_literal='myKeywords',
            ...                                                   desired_column_name_for_identifier='myIdentifier',
            ...                                                   limit=10, offset=10)
                             myIdentifier                                                          myKeywords
            0  wosres:WOS_000071013000007                                   Economics; Planning & Development
            1  wosres:WOS_000071018600001                                                            Oncology
            2  wosres:WOS_000071021600006                                             Pharmacology & Pharmacy
            3  wosres:WOS_000071040300005                                     Clinical Neurology; Orthopedics
            4  wosres:WOS_000071040500044                                                      Plant Sciences
            5  wosres:WOS_000071044500005                          Agricultural Economics & Policy; Economics
            6  wosres:WOS_000071047000001                       Biology; Mathematical & Computational Biology
            7  wosres:WOS_000071052500006                                                             Imaging
            8  wosres:WOS_000071052500006  Neurosciences; Neuroimaging; Radiology, Nuclear Medicine & Medical
            9  wosres:WOS_000071053800004                                                    Physics, Nuclear

            >>> # Error: Offset parameter cannot be specified without also specifying the limit parameter
            >>> try:
            ...     eculture_query.retrieve_subjects_and_objects_of_property(property='wos:WC',
            ...                                                   desired_column_name_for_literal='myKeywords',
            ...                                                   desired_column_name_for_identifier='myIdentifier',
            ...                                                   offset=10)
            ... except ValueError as error_message:
            ...     print('Caught error: %s' % error_message)
            Caught error: 'offset' parameter cannot be specified without providing also the 'limit' parameter. The current offset value is '10', and current limit value is '0'.

        """
        # TODO: Other graphs, and possibly more flexible query overall
        # Prepare LIMIT statement (if it exists) for SPARQL query
        if limit == 0:
            limit_statement_in_query = ''

            if offset != 0:
                raise ValueError("'offset' parameter cannot be specified without providing also the 'limit' parameter. "
                                 "The current offset value is '{offset}', and current limit value is '{limit}'."
                                 .format(offset=offset, limit=limit))

        else:
            limit_statement_in_query = 'LIMIT %d' % limit

        article_ids_vs_literals_dataframe = self.send_select_query("""
        
            SELECT DISTINCT (?subject AS ?%(desired_column_name_for_identifier)s) ?%(desired_column_name_for_literal)s
            WHERE{
                GRAPH %(graph)s {
                    ?subject a %(subject_type)s .
                    ?subject %(property)s ?%(desired_column_name_for_literal)s .
                }
            }
            %(limit_statement_in_query)s
            OFFSET %(offset)d
    
            """ % {'desired_column_name_for_identifier': desired_column_name_for_identifier,
                   'desired_column_name_for_literal':desired_column_name_for_literal,
                   'graph': graph,
                   'subject_type': restrict_subjects_to_type,
                   'property':property,
                   'limit_statement_in_query':limit_statement_in_query,
                   'offset':offset}
        )
        self._last_query_results = article_ids_vs_literals_dataframe
        return self._last_query_results


    def count_number_of_instances_of_property(self, property, graph='wosGraph:', restrict_subjects_to_type='wos:Article'):
        """
        Retrieves the two sides of a property (i.e., the subject and the object around the property)

        Args:
            property(str): URI of the property that connects the article to literal.
                (e.g., 'wos:DE' connects Web of Science articles to the literals that are author keywords).
                Can take prefixed URIs if the related prefixes are defined for the query instance.
            graph(str): URI of the graph. Can be prefixes if defined earlier (e.g., wosGraph:) instead of full URIs
            restrict_subjects_to_type(str): URI of the type to be used to limit selection. Can take prefixed URIs.

        Returns:
            int

        Examples:
            >>> # INIT =================================================================================================
            >>> # Import endpoint address from private file
            >>> from preprocessor.Text_File import Text_File
            >>> eculture_endpoint_url_file = Text_File('..//private//eculture_virtuoso_endpoint_address')
            >>> eculture_endpoint_url = eculture_endpoint_url_file.return_content()

            >>> # Initiate instance
            >>> eculture_query = WebOfScienceQuery()

            >>> # Set query parameters and clear docTestsGraph
            >>> eculture_query.set_prefixes('''\
                @prefix wos: <http://wos.risis.eu/vocabulary/> .\
                @prefix wosres: <http://wos.risis.eu/resource/> .\
                @prefix wosGraph: <http://clokman.com/wos> .\
                @prefix docTestsGraph: <http://clokman.com/doctestsgraph> .\
                @prefix kfir: <http://clokman.com/kfir/ontology#> .\
            ''').set_endpoint(eculture_endpoint_url).send_update_query('CLEAR GRAPH docTestsGraph:')

            >>> # Confirm that the doctest graph is empty
            >>> eculture_query.send_select_query('SELECT * {GRAPH docTestsGraph: {?s ?p ?o}} LIMIT 2')
            Empty DataFrame
            Columns: [s, p, o]
            Index: []
            
            >>> eculture_query.send_update_query('''
            ...     INSERT DATA {
            ...            GRAPH docTestsGraph: {
            ...                wosres:WOS_000080363400002 a wos:Article;
            ...                                           wos:WC "Statistics & Probability"
            ...            }
            ... }''')
            >>> eculture_query.send_select_query('SELECT * {GRAPH docTestsGraph: {?s ?p ?o}}')
                                        s         p                         o
            0  wosres:WOS_000080363400002  rdf:type               wos:Article
            1  wosres:WOS_000080363400002    wos:WC  Statistics & Probability

            >>> #=======================================================================================================

            # Send a count quety with defauly parameters
            >>> eculture_query.count_number_of_instances_of_property(property='wos:DE')
            134254

            >>> # Send another query that has a different subject restriction
            >>> eculture_query.count_number_of_instances_of_property(property='wos:DE', restrict_subjects_to_type='wos:Publication')
            157861

            >>> # Send another query that has a different connector_property
            >>> eculture_query.count_number_of_instances_of_property(property='wos:WC')
            145145

            >>> # Send a query for a different graph
            >>> eculture_query.count_number_of_instances_of_property(property='wos:WC', graph='docTestsGraph:')
            1

            >>> # Send a query for a different graph and different property
            >>> eculture_query.count_number_of_instances_of_property(property='a', graph='docTestsGraph:')
            1

            >>> # Send a query for a graph with an unknown uri prefix:
            >>> try:
            ...     eculture_query.count_number_of_instances_of_property(property='wos:WC', graph='kfirGraph:')
            ... except ValueError as error_message:
            ...     print('Caught error: "%s".' % error_message)
            Caught error: "The graph prefix "kfirGraph:" is not in known prefixes; consider adding it as a prefix. The current pefixes are: "dict_values(['xml', 'rdf', 'rdfs', 'xsd', 'wos', 'wosres', 'wosGraph', 'docTestsGraph', 'kfir'])."".

        """
        self._force_recognition_if_graph_prefix(graph_prefix=graph)  # will do nothing if a full graph uri is provided

        count = self.send_count_query(
            query="""

                          SELECT (COUNT (?literal) AS ?literals) 
                          WHERE{
                              GRAPH %(graph)s {
                                  ?article a %(allowed_subject_type)s;
                                           %(property)s ?literal .
                              }
                          }
                      """ % {'graph': graph, 'allowed_subject_type': restrict_subjects_to_type, 'property': property},
            query_variable_that_holds_count_results='literals'
        )

        return count



    # def convert_articles_vs_keywords_dataframe_to_dictionary(articles_vs_keywords_dataframe):
    #     """
    #     Args:
    #         articles_vs_keywords_dataframe(pandas.dataframe)
    #     Returns:
    #         dict
    #
    #     Examples:
    #     """
    #
    #     raw_articles_vs_keywords_dictionary = articles_vs_keywords_dataframe.to_dict('split')
    #
    #     indexed_dictionary = {}
    #     for each_entry in raw_articles_vs_keywords_dictionary['data']:
    #         each_article_id = each_entry[0]
    #         each_keywords_string = each_entry[1]
    #
    #         each_keywords_list = each_keywords_string.split('; ')
    #
    #         indexed_dictionary[each_article_id] = each_keywords_list
    #     return indexed_dictionary
    #
    # id_vs_keyword_dictionary = convert_articles_vs_keywords_dataframe_to_dictionary(articles_vs_keywords_dataframe)
    #
    # from pprint import pprint
    # pprint(id_vs_keyword_dictionary)



class Open_Citations_Query(Sparql_Query):

    def __init__(self, input_query=''):
        Sparql_Query.__init__(self, input_query)


    def retrieve_article_by_doi(self, target_doi,
                                also_query_for_different_versions_of_doi=False,
                                print_only=False,
                                log_query_parameters_to_registry=False):
        """
        Args:
            target_doi(str)
            also_query_for_different_versions_of_doi(bool): If True, generates possible versions of the inputted
                DOI. These alernative versions (e.g., 'http://dx.doi.org/10.1038/modpathol.3800620'), along with the
                kernel of the DOI (e.g., '10.1038/modpathol.3800620') are used in the same SPARQL query (and NOT
                queried using different queries). Generating alternative versions and using them in a single query
                this way (with SPARQL's VALUES keyword) is dramatically more time-efficient than using REGEX
                STRENDS keywords in SPARQL.
            print_only(bool): If True, Prints the results to console and returns nothing. If False, only returns
                the result.
            log_query_parameters(bool): If True, logs parameters used in queries (i.e., dois, and if enabled, their
                alternative versions) in an instance variable. WARNING: Could results in significant memory
                consumption in large queries. Could be used for diagnostic purposes but it is probably not a good
                idea to make this method a part of a regular algorithm.

        Returns:
            dict or nothing (if print_only is selected)

        Examples:
            >>> my_oc_query = Open_Citations_Query()
            >>> my_oc_query.retrieve_article_by_doi('10.1186/s13034-015-0062-7')
            {1: {'journal_article': 'https://w3id.org/oc/corpus/br/362418', 'publication_type': 'Article', 'title': 'The DSM-5 diagnosis of nonsuicidal self-injury disorder: a review of the empirical literature', 'publication_year': '2015', 'journal_name': 'Child and Adolescent Psychiatry and Mental Health - Child Adolesc Psychiatry Ment Health', 'journal_issue_number': '1', 'journal_volume_number': '9', 'publisher_name': 'Springer Science + Business Media', 'doi': '10.1186/s13034-015-0062-7', 'pmid': '26417387', 'url': 'http://dx.doi.org/10.1186/s13034-015-0062-7', 'authors': 'Zetterqvist - Maria', 'cited_the_articles': 'https://w3id.org/oc/corpus/br/37961 | https://w3id.org/oc/corpus/br/38250 | https://w3id.org/oc/corpus/br/135448 | https://w3id.org/oc/corpus/br/135458 | https://w3id.org/oc/corpus/br/177639 | https://w3id.org/oc/corpus/br/177648 | https://w3id.org/oc/corpus/br/177653 | https://w3id.org/oc/corpus/br/177661 | https://w3id.org/oc/corpus/br/177774 | https://w3id.org/oc/corpus/br/362419 | https://w3id.org/oc/corpus/br/362426 | https://w3id.org/oc/corpus/br/362438 | https://w3id.org/oc/corpus/br/607811 | https://w3id.org/oc/corpus/br/1270766 | https://w3id.org/oc/corpus/br/1560911 | https://w3id.org/oc/corpus/br/1794850 | https://w3id.org/oc/corpus/br/1881397 | https://w3id.org/oc/corpus/br/2258672 | https://w3id.org/oc/corpus/br/2907029 | https://w3id.org/oc/corpus/br/2907034 | https://w3id.org/oc/corpus/br/2907035 | https://w3id.org/oc/corpus/br/2907042 | https://w3id.org/oc/corpus/br/2907056 | https://w3id.org/oc/corpus/br/3346205 | https://w3id.org/oc/corpus/br/3567493 | https://w3id.org/oc/corpus/br/3567495 | https://w3id.org/oc/corpus/br/3949890 | https://w3id.org/oc/corpus/br/5106137 | https://w3id.org/oc/corpus/br/5441063 | https://w3id.org/oc/corpus/br/5441066 | https://w3id.org/oc/corpus/br/5441085 | https://w3id.org/oc/corpus/br/5656230 | https://w3id.org/oc/corpus/br/6060536 | https://w3id.org/oc/corpus/br/6063037 | https://w3id.org/oc/corpus/br/6449521 | https://w3id.org/oc/corpus/br/6486152 | https://w3id.org/oc/corpus/br/6486162 | https://w3id.org/oc/corpus/br/6919305 | https://w3id.org/oc/corpus/br/6919323 | https://w3id.org/oc/corpus/br/7558746 | https://w3id.org/oc/corpus/br/7560541 | https://w3id.org/oc/corpus/br/7560644 | https://w3id.org/oc/corpus/br/7560645 | https://w3id.org/oc/corpus/br/7560646 | https://w3id.org/oc/corpus/br/7560647 | https://w3id.org/oc/corpus/br/7560648 | https://w3id.org/oc/corpus/br/7560651 | https://w3id.org/oc/corpus/br/7560652 | https://w3id.org/oc/corpus/br/7560653 | https://w3id.org/oc/corpus/br/7560654 | https://w3id.org/oc/corpus/br/7560655 | https://w3id.org/oc/corpus/br/7560656 | https://w3id.org/oc/corpus/br/7560657 | https://w3id.org/oc/corpus/br/7560658 | https://w3id.org/oc/corpus/br/7560659 | https://w3id.org/oc/corpus/br/7560660 | https://w3id.org/oc/corpus/br/7560661 | https://w3id.org/oc/corpus/br/7560662 | https://w3id.org/oc/corpus/br/7560663 | https://w3id.org/oc/corpus/br/7560664 | https://w3id.org/oc/corpus/br/7560665 | https://w3id.org/oc/corpus/br/7560666', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/362415'}}

            >>> my_oc_query.retrieve_article_by_doi('10.1186/s13034-015-0062-7', print_only=True)
            {1: {'authors': 'Zetterqvist - Maria',
                 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/362415',
                 'cited_the_articles': 'https://w3id.org/oc/corpus/br/37961 | '
                                       'https://w3id.org/oc/corpus/br/38250 | '
                                       'https://w3id.org/oc/corpus/br/135448 | '
                                       'https://w3id.org/oc/corpus/br/135458 | '
                                       'https://w3id.org/oc/corpus/br/177639 | '
                                       'https://w3id.org/oc/corpus/br/177648 | '
                                       'https://w3id.org/oc/corpus/br/177653 | '
                                       'https://w3id.org/oc/corpus/br/177661 | '
                                       'https://w3id.org/oc/corpus/br/177774 | '
                                       'https://w3id.org/oc/corpus/br/362419 | '
                                       'https://w3id.org/oc/corpus/br/362426 | '
                                       'https://w3id.org/oc/corpus/br/362438 | '
                                       'https://w3id.org/oc/corpus/br/607811 | '
                                       'https://w3id.org/oc/corpus/br/1270766 | '
                                       'https://w3id.org/oc/corpus/br/1560911 | '
                                       'https://w3id.org/oc/corpus/br/1794850 | '
                                       'https://w3id.org/oc/corpus/br/1881397 | '
                                       'https://w3id.org/oc/corpus/br/2258672 | '
                                       'https://w3id.org/oc/corpus/br/2907029 | '
                                       'https://w3id.org/oc/corpus/br/2907034 | '
                                       'https://w3id.org/oc/corpus/br/2907035 | '
                                       'https://w3id.org/oc/corpus/br/2907042 | '
                                       'https://w3id.org/oc/corpus/br/2907056 | '
                                       'https://w3id.org/oc/corpus/br/3346205 | '
                                       'https://w3id.org/oc/corpus/br/3567493 | '
                                       'https://w3id.org/oc/corpus/br/3567495 | '
                                       'https://w3id.org/oc/corpus/br/3949890 | '
                                       'https://w3id.org/oc/corpus/br/5106137 | '
                                       'https://w3id.org/oc/corpus/br/5441063 | '
                                       'https://w3id.org/oc/corpus/br/5441066 | '
                                       'https://w3id.org/oc/corpus/br/5441085 | '
                                       'https://w3id.org/oc/corpus/br/5656230 | '
                                       'https://w3id.org/oc/corpus/br/6060536 | '
                                       'https://w3id.org/oc/corpus/br/6063037 | '
                                       'https://w3id.org/oc/corpus/br/6449521 | '
                                       'https://w3id.org/oc/corpus/br/6486152 | '
                                       'https://w3id.org/oc/corpus/br/6486162 | '
                                       'https://w3id.org/oc/corpus/br/6919305 | '
                                       'https://w3id.org/oc/corpus/br/6919323 | '
                                       'https://w3id.org/oc/corpus/br/7558746 | '
                                       'https://w3id.org/oc/corpus/br/7560541 | '
                                       'https://w3id.org/oc/corpus/br/7560644 | '
                                       'https://w3id.org/oc/corpus/br/7560645 | '
                                       'https://w3id.org/oc/corpus/br/7560646 | '
                                       'https://w3id.org/oc/corpus/br/7560647 | '
                                       'https://w3id.org/oc/corpus/br/7560648 | '
                                       'https://w3id.org/oc/corpus/br/7560651 | '
                                       'https://w3id.org/oc/corpus/br/7560652 | '
                                       'https://w3id.org/oc/corpus/br/7560653 | '
                                       'https://w3id.org/oc/corpus/br/7560654 | '
                                       'https://w3id.org/oc/corpus/br/7560655 | '
                                       'https://w3id.org/oc/corpus/br/7560656 | '
                                       'https://w3id.org/oc/corpus/br/7560657 | '
                                       'https://w3id.org/oc/corpus/br/7560658 | '
                                       'https://w3id.org/oc/corpus/br/7560659 | '
                                       'https://w3id.org/oc/corpus/br/7560660 | '
                                       'https://w3id.org/oc/corpus/br/7560661 | '
                                       'https://w3id.org/oc/corpus/br/7560662 | '
                                       'https://w3id.org/oc/corpus/br/7560663 | '
                                       'https://w3id.org/oc/corpus/br/7560664 | '
                                       'https://w3id.org/oc/corpus/br/7560665 | '
                                       'https://w3id.org/oc/corpus/br/7560666',
                 'doi': '10.1186/s13034-015-0062-7',
                 'journal_article': 'https://w3id.org/oc/corpus/br/362418',
                 'journal_issue_number': '1',
                 'journal_name': 'Child and Adolescent Psychiatry and Mental Health - '
                                 'Child Adolesc Psychiatry Ment Health',
                 'journal_volume_number': '9',
                 'pmid': '26417387',
                 'publication_type': 'Article',
                 'publication_year': '2015',
                 'publisher_name': 'Springer Science + Business Media',
                 'title': 'The DSM-5 diagnosis of nonsuicidal self-injury disorder: a '
                          'review of the empirical literature',
                 'url': 'http://dx.doi.org/10.1186/s13034-015-0062-7'}}

            >>> # Queries over returned results
            >>> # print DOI of first result
            >>> print(my_oc_query.results[1]['doi'])
            10.1186/s13034-015-0062-7

            >>> # print first result
            >>> print(my_oc_query.results[1])
            {'journal_article': 'https://w3id.org/oc/corpus/br/362418', 'publication_type': 'Article', 'title': 'The DSM-5 diagnosis of nonsuicidal self-injury disorder: a review of the empirical literature', 'publication_year': '2015', 'journal_name': 'Child and Adolescent Psychiatry and Mental Health - Child Adolesc Psychiatry Ment Health', 'journal_issue_number': '1', 'journal_volume_number': '9', 'publisher_name': 'Springer Science + Business Media', 'doi': '10.1186/s13034-015-0062-7', 'pmid': '26417387', 'url': 'http://dx.doi.org/10.1186/s13034-015-0062-7', 'authors': 'Zetterqvist - Maria', 'cited_the_articles': 'https://w3id.org/oc/corpus/br/37961 | https://w3id.org/oc/corpus/br/38250 | https://w3id.org/oc/corpus/br/135448 | https://w3id.org/oc/corpus/br/135458 | https://w3id.org/oc/corpus/br/177639 | https://w3id.org/oc/corpus/br/177648 | https://w3id.org/oc/corpus/br/177653 | https://w3id.org/oc/corpus/br/177661 | https://w3id.org/oc/corpus/br/177774 | https://w3id.org/oc/corpus/br/362419 | https://w3id.org/oc/corpus/br/362426 | https://w3id.org/oc/corpus/br/362438 | https://w3id.org/oc/corpus/br/607811 | https://w3id.org/oc/corpus/br/1270766 | https://w3id.org/oc/corpus/br/1560911 | https://w3id.org/oc/corpus/br/1794850 | https://w3id.org/oc/corpus/br/1881397 | https://w3id.org/oc/corpus/br/2258672 | https://w3id.org/oc/corpus/br/2907029 | https://w3id.org/oc/corpus/br/2907034 | https://w3id.org/oc/corpus/br/2907035 | https://w3id.org/oc/corpus/br/2907042 | https://w3id.org/oc/corpus/br/2907056 | https://w3id.org/oc/corpus/br/3346205 | https://w3id.org/oc/corpus/br/3567493 | https://w3id.org/oc/corpus/br/3567495 | https://w3id.org/oc/corpus/br/3949890 | https://w3id.org/oc/corpus/br/5106137 | https://w3id.org/oc/corpus/br/5441063 | https://w3id.org/oc/corpus/br/5441066 | https://w3id.org/oc/corpus/br/5441085 | https://w3id.org/oc/corpus/br/5656230 | https://w3id.org/oc/corpus/br/6060536 | https://w3id.org/oc/corpus/br/6063037 | https://w3id.org/oc/corpus/br/6449521 | https://w3id.org/oc/corpus/br/6486152 | https://w3id.org/oc/corpus/br/6486162 | https://w3id.org/oc/corpus/br/6919305 | https://w3id.org/oc/corpus/br/6919323 | https://w3id.org/oc/corpus/br/7558746 | https://w3id.org/oc/corpus/br/7560541 | https://w3id.org/oc/corpus/br/7560644 | https://w3id.org/oc/corpus/br/7560645 | https://w3id.org/oc/corpus/br/7560646 | https://w3id.org/oc/corpus/br/7560647 | https://w3id.org/oc/corpus/br/7560648 | https://w3id.org/oc/corpus/br/7560651 | https://w3id.org/oc/corpus/br/7560652 | https://w3id.org/oc/corpus/br/7560653 | https://w3id.org/oc/corpus/br/7560654 | https://w3id.org/oc/corpus/br/7560655 | https://w3id.org/oc/corpus/br/7560656 | https://w3id.org/oc/corpus/br/7560657 | https://w3id.org/oc/corpus/br/7560658 | https://w3id.org/oc/corpus/br/7560659 | https://w3id.org/oc/corpus/br/7560660 | https://w3id.org/oc/corpus/br/7560661 | https://w3id.org/oc/corpus/br/7560662 | https://w3id.org/oc/corpus/br/7560663 | https://w3id.org/oc/corpus/br/7560664 | https://w3id.org/oc/corpus/br/7560665 | https://w3id.org/oc/corpus/br/7560666', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/362415'}

        >>> my_oc_query.retrieve_article_by_doi('10.1186/s13034-015-0062-7',
        ...                                     also_query_for_different_versions_of_doi=True,
        ...                                     log_query_parameters_to_registry=True)
        {1: {'journal_article': 'https://w3id.org/oc/corpus/br/362418', 'publication_type': 'Article', 'title': 'The DSM-5 diagnosis of nonsuicidal self-injury disorder: a review of the empirical literature', 'publication_year': '2015', 'journal_name': 'Child and Adolescent Psychiatry and Mental Health - Child Adolesc Psychiatry Ment Health', 'journal_issue_number': '1', 'journal_volume_number': '9', 'publisher_name': 'Springer Science + Business Media', 'doi': '10.1186/s13034-015-0062-7', 'pmid': '26417387', 'url': 'http://dx.doi.org/10.1186/s13034-015-0062-7', 'authors': 'Zetterqvist - Maria', 'cited_the_articles': 'https://w3id.org/oc/corpus/br/37961 | https://w3id.org/oc/corpus/br/38250 | https://w3id.org/oc/corpus/br/135448 | https://w3id.org/oc/corpus/br/135458 | https://w3id.org/oc/corpus/br/177639 | https://w3id.org/oc/corpus/br/177648 | https://w3id.org/oc/corpus/br/177653 | https://w3id.org/oc/corpus/br/177661 | https://w3id.org/oc/corpus/br/177774 | https://w3id.org/oc/corpus/br/362419 | https://w3id.org/oc/corpus/br/362426 | https://w3id.org/oc/corpus/br/362438 | https://w3id.org/oc/corpus/br/607811 | https://w3id.org/oc/corpus/br/1270766 | https://w3id.org/oc/corpus/br/1560911 | https://w3id.org/oc/corpus/br/1794850 | https://w3id.org/oc/corpus/br/1881397 | https://w3id.org/oc/corpus/br/2258672 | https://w3id.org/oc/corpus/br/2907029 | https://w3id.org/oc/corpus/br/2907034 | https://w3id.org/oc/corpus/br/2907035 | https://w3id.org/oc/corpus/br/2907042 | https://w3id.org/oc/corpus/br/2907056 | https://w3id.org/oc/corpus/br/3346205 | https://w3id.org/oc/corpus/br/3567493 | https://w3id.org/oc/corpus/br/3567495 | https://w3id.org/oc/corpus/br/3949890 | https://w3id.org/oc/corpus/br/5106137 | https://w3id.org/oc/corpus/br/5441063 | https://w3id.org/oc/corpus/br/5441066 | https://w3id.org/oc/corpus/br/5441085 | https://w3id.org/oc/corpus/br/5656230 | https://w3id.org/oc/corpus/br/6060536 | https://w3id.org/oc/corpus/br/6063037 | https://w3id.org/oc/corpus/br/6449521 | https://w3id.org/oc/corpus/br/6486152 | https://w3id.org/oc/corpus/br/6486162 | https://w3id.org/oc/corpus/br/6919305 | https://w3id.org/oc/corpus/br/6919323 | https://w3id.org/oc/corpus/br/7558746 | https://w3id.org/oc/corpus/br/7560541 | https://w3id.org/oc/corpus/br/7560644 | https://w3id.org/oc/corpus/br/7560645 | https://w3id.org/oc/corpus/br/7560646 | https://w3id.org/oc/corpus/br/7560647 | https://w3id.org/oc/corpus/br/7560648 | https://w3id.org/oc/corpus/br/7560651 | https://w3id.org/oc/corpus/br/7560652 | https://w3id.org/oc/corpus/br/7560653 | https://w3id.org/oc/corpus/br/7560654 | https://w3id.org/oc/corpus/br/7560655 | https://w3id.org/oc/corpus/br/7560656 | https://w3id.org/oc/corpus/br/7560657 | https://w3id.org/oc/corpus/br/7560658 | https://w3id.org/oc/corpus/br/7560659 | https://w3id.org/oc/corpus/br/7560660 | https://w3id.org/oc/corpus/br/7560661 | https://w3id.org/oc/corpus/br/7560662 | https://w3id.org/oc/corpus/br/7560663 | https://w3id.org/oc/corpus/br/7560664 | https://w3id.org/oc/corpus/br/7560665 | https://w3id.org/oc/corpus/br/7560666', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/362415'}}
        >>> my_oc_query.query_parameters_registry
        {'doi': [['10.1186/s13034-015-0062-7', 'https://doi.org/10.1186/s13034-015-0062-7', 'http://doi.org/10.1186/s13034-015-0062-7', 'http://dx.doi.org/10.1186/s13034-015-0062-7', 'https://dx.doi.org/10.1186/s13034-015-0062-7', 'DOI 10.1186/s13034-015-0062-7', 'doi 10.1186/s13034-015-0062-7', 'DOI: 10.1186/s13034-015-0062-7', 'doi: 10.1186/s13034-015-0062-7', 'DOI:10.1186/s13034-015-0062-7', 'doi:10.1186/s13034-015-0062-7', 'doi.org/10.1186/s13034-015-0062-7']]}
        """
        from retriever.query_templates import Query_Template

        if also_query_for_different_versions_of_doi:
             target_doi = DOI_String(target_doi)
             target_dois = target_doi.generate_alternative_versions_if_doi()  # generated DOIs are to be used
                                                                              # instead of regex or 'strEnds' methods
                                                                              # in SPARQL (querying this way is
                                                                              # dramatically faster)
        else:
            target_dois = target_doi
        if log_query_parameters_to_registry:
            self.update_query_parameters_registry('doi', target_dois)  # could increase memory consumption significantly

        query_string = Query_Template().retrieve_oc_articles_by_dois(target_dois=target_dois)

        self.set_query(query_string)
        self.results = self.retrieve_results_from_endpoint(endpoint_address='http://opencitations.net/sparql')

        if print_only:
            self.print_results()
        else:
            return self.results


    def retrieve_articles_by_dois(self, target_dois_list, print_only=False, show_progress_bar=False):
        """
        Args:
            target_dois_list(list)
            print_only(bool): If true, prints the result to console and returns nothing. If false, only returns the result.
            show_progress_bar(bool)

        Returns:
            dict or nothing (if print_only is selected)

        Examples:
            >>> my_oc_query = Open_Citations_Query()
            >>> target_dois_list = ['10.1186/s13034-015-0062-7', '10.1016/s0090-8258(03)00126-4',
            ...                     '10.1016/s0090-8258(03)00087-8']  # add '10.1016/s0020-7292(06)60031-3' to the list
            ...                     # to see a doi returning two results with a slight difference (different PMIDs in
            ...                     # two results)
            >>> my_oc_query.retrieve_articles_by_dois(target_dois_list)
            DOI validation completed
            Number of valid DOIs: 3
            Number of invalid DOIs: 0
            Valid and invalid query criteria in parameter "doi_list" were recorded in instance variables
            <BLANKLINE>
            All queries were completed successfully (3 results retrieved out of 3 queries)
            {1: {'journal_article': 'https://w3id.org/oc/corpus/br/362418', 'publication_type': 'Article', 'title': 'The DSM-5 diagnosis of nonsuicidal self-injury disorder: a review of the empirical literature', 'publication_year': '2015', 'journal_name': 'Child and Adolescent Psychiatry and Mental Health - Child Adolesc Psychiatry Ment Health', 'journal_issue_number': '1', 'journal_volume_number': '9', 'publisher_name': 'Springer Science + Business Media', 'doi': '10.1186/s13034-015-0062-7', 'pmid': '26417387', 'url': 'http://dx.doi.org/10.1186/s13034-015-0062-7', 'authors': 'Zetterqvist - Maria', 'cited_the_articles': 'https://w3id.org/oc/corpus/br/37961 | https://w3id.org/oc/corpus/br/38250 | https://w3id.org/oc/corpus/br/135448 | https://w3id.org/oc/corpus/br/135458 | https://w3id.org/oc/corpus/br/177639 | https://w3id.org/oc/corpus/br/177648 | https://w3id.org/oc/corpus/br/177653 | https://w3id.org/oc/corpus/br/177661 | https://w3id.org/oc/corpus/br/177774 | https://w3id.org/oc/corpus/br/362419 | https://w3id.org/oc/corpus/br/362426 | https://w3id.org/oc/corpus/br/362438 | https://w3id.org/oc/corpus/br/607811 | https://w3id.org/oc/corpus/br/1270766 | https://w3id.org/oc/corpus/br/1560911 | https://w3id.org/oc/corpus/br/1794850 | https://w3id.org/oc/corpus/br/1881397 | https://w3id.org/oc/corpus/br/2258672 | https://w3id.org/oc/corpus/br/2907029 | https://w3id.org/oc/corpus/br/2907034 | https://w3id.org/oc/corpus/br/2907035 | https://w3id.org/oc/corpus/br/2907042 | https://w3id.org/oc/corpus/br/2907056 | https://w3id.org/oc/corpus/br/3346205 | https://w3id.org/oc/corpus/br/3567493 | https://w3id.org/oc/corpus/br/3567495 | https://w3id.org/oc/corpus/br/3949890 | https://w3id.org/oc/corpus/br/5106137 | https://w3id.org/oc/corpus/br/5441063 | https://w3id.org/oc/corpus/br/5441066 | https://w3id.org/oc/corpus/br/5441085 | https://w3id.org/oc/corpus/br/5656230 | https://w3id.org/oc/corpus/br/6060536 | https://w3id.org/oc/corpus/br/6063037 | https://w3id.org/oc/corpus/br/6449521 | https://w3id.org/oc/corpus/br/6486152 | https://w3id.org/oc/corpus/br/6486162 | https://w3id.org/oc/corpus/br/6919305 | https://w3id.org/oc/corpus/br/6919323 | https://w3id.org/oc/corpus/br/7558746 | https://w3id.org/oc/corpus/br/7560541 | https://w3id.org/oc/corpus/br/7560644 | https://w3id.org/oc/corpus/br/7560645 | https://w3id.org/oc/corpus/br/7560646 | https://w3id.org/oc/corpus/br/7560647 | https://w3id.org/oc/corpus/br/7560648 | https://w3id.org/oc/corpus/br/7560651 | https://w3id.org/oc/corpus/br/7560652 | https://w3id.org/oc/corpus/br/7560653 | https://w3id.org/oc/corpus/br/7560654 | https://w3id.org/oc/corpus/br/7560655 | https://w3id.org/oc/corpus/br/7560656 | https://w3id.org/oc/corpus/br/7560657 | https://w3id.org/oc/corpus/br/7560658 | https://w3id.org/oc/corpus/br/7560659 | https://w3id.org/oc/corpus/br/7560660 | https://w3id.org/oc/corpus/br/7560661 | https://w3id.org/oc/corpus/br/7560662 | https://w3id.org/oc/corpus/br/7560663 | https://w3id.org/oc/corpus/br/7560664 | https://w3id.org/oc/corpus/br/7560665 | https://w3id.org/oc/corpus/br/7560666', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/362415'}, 2: {'journal_article': 'https://w3id.org/oc/corpus/br/384', 'publication_type': 'Article', 'title': 'Survival after relapse in patients with endometrial cancer: results from a randomized trial☆', 'publication_year': '2003', 'journal_name': 'Gynecologic Oncology', 'journal_issue_number': '2', 'journal_volume_number': '89', 'publisher_name': 'Elsevier BV', 'doi': '10.1016/s0090-8258(03)00126-4', 'pmid': '12713981', 'url': 'http://dx.doi.org/10.1016/s0090-8258%2803%2900126-4', 'authors': 'Creutzberg - Carien L | van Putten - Wim L.J | Koper - Peter C | Lybeert - Marnix L.M | Jobsen - Jan J | Wárlám-Rodenhuis - Carla C | De Winter - Karin A.J | Lutgens - Ludy C.H.W | van den Bergh - Alfons C.M | van der Steen-Banasik - Elzbieta | Beerman - Henk | van Lent - Mat', 'cited_the_articles': '', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/1 | https://w3id.org/oc/corpus/br/1342763 | https://w3id.org/oc/corpus/br/1772164'}, 3: {'journal_article': 'https://w3id.org/oc/corpus/br/392', 'publication_type': 'Article', 'title': 'Stage IC adenocarcinoma of the endometrium: survival comparisons of surgically staged patients with and without adjuvant radiation therapyâ\x98\x86â\x98\x86Presented at the 33rd Annual Meeting of Gynecologic Oncologists, Miami, FL, March 2002.', 'publication_year': '2003', 'journal_name': 'Gynecologic Oncology', 'journal_issue_number': '2', 'journal_volume_number': '89', 'publisher_name': 'Elsevier BV', 'doi': '10.1016/s0090-8258(03)00087-8', 'pmid': '12713994', 'url': 'http://dx.doi.org/10.1016/s0090-8258%2803%2900087-8', 'authors': 'Straughn - J.Michael | Huh - Warner K | Orr - James W | Kelly - F.Joseph | Roland - Phillip Y | Gold - Michael A | Powell - Matthew | Mutch - David G | Partridge - Edward E | Kilgore - Larry C | Barnes - Mack N | Austin - J.Maxwell | Alvarez - Ronald D', 'cited_the_articles': '', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/1'}}


            >>> my_oc_query.retrieve_articles_by_dois(target_dois_list)
            DOI validation completed
            Number of valid DOIs: 6
            Number of invalid DOIs: 0
            Valid and invalid query criteria in parameter "doi_list" were recorded in instance variables
            <BLANKLINE>
            All queries were completed successfully (6 results retrieved out of 6 queries)
            {1: {'journal_article': 'https://w3id.org/oc/corpus/br/362418', 'publication_type': 'Article', 'title': 'The DSM-5 diagnosis of nonsuicidal self-injury disorder: a review of the empirical literature', 'publication_year': '2015', 'journal_name': 'Child and Adolescent Psychiatry and Mental Health - Child Adolesc Psychiatry Ment Health', 'journal_issue_number': '1', 'journal_volume_number': '9', 'publisher_name': 'Springer Science + Business Media', 'doi': '10.1186/s13034-015-0062-7', 'pmid': '26417387', 'url': 'http://dx.doi.org/10.1186/s13034-015-0062-7', 'authors': 'Zetterqvist - Maria', 'cited_the_articles': 'https://w3id.org/oc/corpus/br/37961 | https://w3id.org/oc/corpus/br/38250 | https://w3id.org/oc/corpus/br/135448 | https://w3id.org/oc/corpus/br/135458 | https://w3id.org/oc/corpus/br/177639 | https://w3id.org/oc/corpus/br/177648 | https://w3id.org/oc/corpus/br/177653 | https://w3id.org/oc/corpus/br/177661 | https://w3id.org/oc/corpus/br/177774 | https://w3id.org/oc/corpus/br/362419 | https://w3id.org/oc/corpus/br/362426 | https://w3id.org/oc/corpus/br/362438 | https://w3id.org/oc/corpus/br/607811 | https://w3id.org/oc/corpus/br/1270766 | https://w3id.org/oc/corpus/br/1560911 | https://w3id.org/oc/corpus/br/1794850 | https://w3id.org/oc/corpus/br/1881397 | https://w3id.org/oc/corpus/br/2258672 | https://w3id.org/oc/corpus/br/2907029 | https://w3id.org/oc/corpus/br/2907034 | https://w3id.org/oc/corpus/br/2907035 | https://w3id.org/oc/corpus/br/2907042 | https://w3id.org/oc/corpus/br/2907056 | https://w3id.org/oc/corpus/br/3346205 | https://w3id.org/oc/corpus/br/3567493 | https://w3id.org/oc/corpus/br/3567495 | https://w3id.org/oc/corpus/br/3949890 | https://w3id.org/oc/corpus/br/5106137 | https://w3id.org/oc/corpus/br/5441063 | https://w3id.org/oc/corpus/br/5441066 | https://w3id.org/oc/corpus/br/5441085 | https://w3id.org/oc/corpus/br/5656230 | https://w3id.org/oc/corpus/br/6060536 | https://w3id.org/oc/corpus/br/6063037 | https://w3id.org/oc/corpus/br/6449521 | https://w3id.org/oc/corpus/br/6486152 | https://w3id.org/oc/corpus/br/6486162 | https://w3id.org/oc/corpus/br/6919305 | https://w3id.org/oc/corpus/br/6919323 | https://w3id.org/oc/corpus/br/7558746 | https://w3id.org/oc/corpus/br/7560541 | https://w3id.org/oc/corpus/br/7560644 | https://w3id.org/oc/corpus/br/7560645 | https://w3id.org/oc/corpus/br/7560646 | https://w3id.org/oc/corpus/br/7560647 | https://w3id.org/oc/corpus/br/7560648 | https://w3id.org/oc/corpus/br/7560651 | https://w3id.org/oc/corpus/br/7560652 | https://w3id.org/oc/corpus/br/7560653 | https://w3id.org/oc/corpus/br/7560654 | https://w3id.org/oc/corpus/br/7560655 | https://w3id.org/oc/corpus/br/7560656 | https://w3id.org/oc/corpus/br/7560657 | https://w3id.org/oc/corpus/br/7560658 | https://w3id.org/oc/corpus/br/7560659 | https://w3id.org/oc/corpus/br/7560660 | https://w3id.org/oc/corpus/br/7560661 | https://w3id.org/oc/corpus/br/7560662 | https://w3id.org/oc/corpus/br/7560663 | https://w3id.org/oc/corpus/br/7560664 | https://w3id.org/oc/corpus/br/7560665 | https://w3id.org/oc/corpus/br/7560666', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/362415'}, 2: {'journal_article': 'https://w3id.org/oc/corpus/br/384', 'publication_type': 'Article', 'title': 'Survival after relapse in patients with endometrial cancer: results from a randomized trial☆', 'publication_year': '2003', 'journal_name': 'Gynecologic Oncology', 'journal_issue_number': '2', 'journal_volume_number': '89', 'publisher_name': 'Elsevier BV', 'doi': '10.1016/s0090-8258(03)00126-4', 'pmid': '12713981', 'url': 'http://dx.doi.org/10.1016/s0090-8258%2803%2900126-4', 'authors': 'Creutzberg - Carien L | van Putten - Wim L.J | Koper - Peter C | Lybeert - Marnix L.M | Jobsen - Jan J | Wárlám-Rodenhuis - Carla C | De Winter - Karin A.J | Lutgens - Ludy C.H.W | van den Bergh - Alfons C.M | van der Steen-Banasik - Elzbieta | Beerman - Henk | van Lent - Mat', 'cited_the_articles': '', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/1 | https://w3id.org/oc/corpus/br/1342763 | https://w3id.org/oc/corpus/br/1772164'}, 3: {'journal_article': 'https://w3id.org/oc/corpus/br/392', 'publication_type': 'Article', 'title': 'Stage IC adenocarcinoma of the endometrium: survival comparisons of surgically staged patients with and without adjuvant radiation therapyâ\x98\x86â\x98\x86Presented at the 33rd Annual Meeting of Gynecologic Oncologists, Miami, FL, March 2002.', 'publication_year': '2003', 'journal_name': 'Gynecologic Oncology', 'journal_issue_number': '2', 'journal_volume_number': '89', 'publisher_name': 'Elsevier BV', 'doi': '10.1016/s0090-8258(03)00087-8', 'pmid': '12713994', 'url': 'http://dx.doi.org/10.1016/s0090-8258%2803%2900087-8', 'authors': 'Straughn - J.Michael | Huh - Warner K | Orr - James W | Kelly - F.Joseph | Roland - Phillip Y | Gold - Michael A | Powell - Matthew | Mutch - David G | Partridge - Edward E | Kilgore - Larry C | Barnes - Mack N | Austin - J.Maxwell | Alvarez - Ronald D', 'cited_the_articles': '', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/1'}, 4: {'journal_article': 'https://w3id.org/oc/corpus/br/362418', 'publication_type': 'Article', 'title': 'The DSM-5 diagnosis of nonsuicidal self-injury disorder: a review of the empirical literature', 'publication_year': '2015', 'journal_name': 'Child and Adolescent Psychiatry and Mental Health - Child Adolesc Psychiatry Ment Health', 'journal_issue_number': '1', 'journal_volume_number': '9', 'publisher_name': 'Springer Science + Business Media', 'doi': '10.1186/s13034-015-0062-7', 'pmid': '26417387', 'url': 'http://dx.doi.org/10.1186/s13034-015-0062-7', 'authors': 'Zetterqvist - Maria', 'cited_the_articles': 'https://w3id.org/oc/corpus/br/37961 | https://w3id.org/oc/corpus/br/38250 | https://w3id.org/oc/corpus/br/135448 | https://w3id.org/oc/corpus/br/135458 | https://w3id.org/oc/corpus/br/177639 | https://w3id.org/oc/corpus/br/177648 | https://w3id.org/oc/corpus/br/177653 | https://w3id.org/oc/corpus/br/177661 | https://w3id.org/oc/corpus/br/177774 | https://w3id.org/oc/corpus/br/362419 | https://w3id.org/oc/corpus/br/362426 | https://w3id.org/oc/corpus/br/362438 | https://w3id.org/oc/corpus/br/607811 | https://w3id.org/oc/corpus/br/1270766 | https://w3id.org/oc/corpus/br/1560911 | https://w3id.org/oc/corpus/br/1794850 | https://w3id.org/oc/corpus/br/1881397 | https://w3id.org/oc/corpus/br/2258672 | https://w3id.org/oc/corpus/br/2907029 | https://w3id.org/oc/corpus/br/2907034 | https://w3id.org/oc/corpus/br/2907035 | https://w3id.org/oc/corpus/br/2907042 | https://w3id.org/oc/corpus/br/2907056 | https://w3id.org/oc/corpus/br/3346205 | https://w3id.org/oc/corpus/br/3567493 | https://w3id.org/oc/corpus/br/3567495 | https://w3id.org/oc/corpus/br/3949890 | https://w3id.org/oc/corpus/br/5106137 | https://w3id.org/oc/corpus/br/5441063 | https://w3id.org/oc/corpus/br/5441066 | https://w3id.org/oc/corpus/br/5441085 | https://w3id.org/oc/corpus/br/5656230 | https://w3id.org/oc/corpus/br/6060536 | https://w3id.org/oc/corpus/br/6063037 | https://w3id.org/oc/corpus/br/6449521 | https://w3id.org/oc/corpus/br/6486152 | https://w3id.org/oc/corpus/br/6486162 | https://w3id.org/oc/corpus/br/6919305 | https://w3id.org/oc/corpus/br/6919323 | https://w3id.org/oc/corpus/br/7558746 | https://w3id.org/oc/corpus/br/7560541 | https://w3id.org/oc/corpus/br/7560644 | https://w3id.org/oc/corpus/br/7560645 | https://w3id.org/oc/corpus/br/7560646 | https://w3id.org/oc/corpus/br/7560647 | https://w3id.org/oc/corpus/br/7560648 | https://w3id.org/oc/corpus/br/7560651 | https://w3id.org/oc/corpus/br/7560652 | https://w3id.org/oc/corpus/br/7560653 | https://w3id.org/oc/corpus/br/7560654 | https://w3id.org/oc/corpus/br/7560655 | https://w3id.org/oc/corpus/br/7560656 | https://w3id.org/oc/corpus/br/7560657 | https://w3id.org/oc/corpus/br/7560658 | https://w3id.org/oc/corpus/br/7560659 | https://w3id.org/oc/corpus/br/7560660 | https://w3id.org/oc/corpus/br/7560661 | https://w3id.org/oc/corpus/br/7560662 | https://w3id.org/oc/corpus/br/7560663 | https://w3id.org/oc/corpus/br/7560664 | https://w3id.org/oc/corpus/br/7560665 | https://w3id.org/oc/corpus/br/7560666', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/362415'}, 5: {'journal_article': 'https://w3id.org/oc/corpus/br/384', 'publication_type': 'Article', 'title': 'Survival after relapse in patients with endometrial cancer: results from a randomized trial☆', 'publication_year': '2003', 'journal_name': 'Gynecologic Oncology', 'journal_issue_number': '2', 'journal_volume_number': '89', 'publisher_name': 'Elsevier BV', 'doi': '10.1016/s0090-8258(03)00126-4', 'pmid': '12713981', 'url': 'http://dx.doi.org/10.1016/s0090-8258%2803%2900126-4', 'authors': 'Creutzberg - Carien L | van Putten - Wim L.J | Koper - Peter C | Lybeert - Marnix L.M | Jobsen - Jan J | Wárlám-Rodenhuis - Carla C | De Winter - Karin A.J | Lutgens - Ludy C.H.W | van den Bergh - Alfons C.M | van der Steen-Banasik - Elzbieta | Beerman - Henk | van Lent - Mat', 'cited_the_articles': '', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/1 | https://w3id.org/oc/corpus/br/1342763 | https://w3id.org/oc/corpus/br/1772164'}, 6: {'journal_article': 'https://w3id.org/oc/corpus/br/392', 'publication_type': 'Article', 'title': 'Stage IC adenocarcinoma of the endometrium: survival comparisons of surgically staged patients with and without adjuvant radiation therapyâ\x98\x86â\x98\x86Presented at the 33rd Annual Meeting of Gynecologic Oncologists, Miami, FL, March 2002.', 'publication_year': '2003', 'journal_name': 'Gynecologic Oncology', 'journal_issue_number': '2', 'journal_volume_number': '89', 'publisher_name': 'Elsevier BV', 'doi': '10.1016/s0090-8258(03)00087-8', 'pmid': '12713994', 'url': 'http://dx.doi.org/10.1016/s0090-8258%2803%2900087-8', 'authors': 'Straughn - J.Michael | Huh - Warner K | Orr - James W | Kelly - F.Joseph | Roland - Phillip Y | Gold - Michael A | Powell - Matthew | Mutch - David G | Partridge - Edward E | Kilgore - Larry C | Barnes - Mack N | Austin - J.Maxwell | Alvarez - Ronald D', 'cited_the_articles': '', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/1'}}

        """
        from meta.consoleOutput import ConsoleOutput
        console = ConsoleOutput('log.txt')

        target_dois_list = self.validate_dois(target_dois_list)

        no_of_results_returned_so_far = 0
        no_of_queries_made_so_far = 0
        all_results = {}
        failed_queries = []

        maximum_progress = len(target_dois_list)

        for i, each_target_doi in enumerate(target_dois_list):
            try:
                current_result = self.retrieve_article_by_doi(each_target_doi)
                # aggregate returned results in all_results variable
                for each_key, each_value in current_result.items():  # keys represent row numbers of returned results table
                    no_of_results_returned_so_far += 1               # ... and values represent fields and their values
                    all_results[no_of_results_returned_so_far] = each_value

                if show_progress_bar:
                    console.print_current_progress(i, maximum_progress, 'Querying SPARQL endpoint at %s '
                                                                        '(%d/%d queries made and %d results retrieved)'
                                                   % (self.endpoint_address,
                                                      no_of_queries_made_so_far, maximum_progress,
                                                      no_of_results_returned_so_far))
            except:
                failed_queries.append(each_target_doi)
            finally:
                no_of_queries_made_so_far += 1

        self.results = all_results
        self.number_of_lines_retrieved = no_of_results_returned_so_far

        # Logging
        if failed_queries:
            message = 'Query completed (%d results retrieved). Queries with these DOIs failed' % no_of_results_returned_so_far
            console.log_list_with_caption(message, failed_queries, add_timestamp_in_file=True)
            console.log_message(' ')  # empty line between failed items and printed/returned results
        else:
            message = '\nAll queries were completed successfully (%d results retrieved out of %d queries)' \
                      % (no_of_results_returned_so_far, no_of_queries_made_so_far)
            console.log_message(message, add_timestamp_in_file=True)

        if print_only:
            self.print_results()
        else:
            return self.results


    def validate_dois(self, doi_list):
        """
        Validates DOIs and returns valid DOIs. Also records valid and invalid DOIs found to as instance variables.

        Args:
            doi_list(list)

        Returns:
            list

        Examples:
            >>> ### Import and filter all dois in UvA and VU Pure files ###

            >>> #Prep
            >>> from preprocessor.string_tools import String
            >>> from pprint import pprint
            >>> doi_list = []
            >>> with open('test_data_and_queries/all_dois_in_uva_and_vu_bibliographies_identical_test_copy.csv',
            ...           encoding='utf8') as doi_file:
            ...     for each_line in doi_file:
            ...         cleaned_line = String(each_line)
            ...         cleaned_line = cleaned_line.clean_from_newline_characters()
            ...         doi_list.append(str(cleaned_line))

            >>> # Filtering
            >>> my_query = Open_Citations_Query()
            >>> valid_dois = my_query.validate_dois(doi_list)  # variable assignment made to prevent long output
            DOI validation completed
            Number of valid DOIs: 91591
            Number of invalid DOIs: 189
            Valid and invalid query criteria in parameter "doi_list" were recorded in instance variables
            >>> # preview valid DOIs
            >>> pprint(my_query.valid_search_criteria_registry[:15])
            ['10.1163/187607508X384689',
             '10.1017/S0954579416000572',
             '10.1007/s11562-016-0353-7',
             '10.1016/j.adolescence.2016.09.008',
             '10.1186/s13561-016-0122-6',
             '10.1007/s00799-016-0182-6',
             '10.5194/gmd-2016-266',
             '10.1007/s00737-015-0531-2',
             '10.1103/RevModPhys.88.021003',
             'https://doi.org/10.1101/167171',
             'https://doi.org/10.1016/j.chb.2017.04.047',
             '10.1016/j.trb.2016.09.005',
             '10.1016/j.ancene.2016.01.001',
             '10.1111/adb.12322',
             '10.1017/njg.2016.45']
            >>> # preview invalid DOIs
            >>> pprint(my_query.invalid_search_criteria_registry[:15])
            ['(DOI) - 10.1111/cch.12521',
             'http://www.socialevraagstukken.nl/veiligheid-creeer-je-met-geborgenheid/',
             'http://www.metajournal.org//articles_pdf/02--krijnen-meta-techno-final.pdf',
             'http://global-sport.eu/beyond-colonialism-contemporary-cricket-narratives-in-the-caribbean',
             'http://www.mdpi.com/2075-471X/5/1/10/htm',
             'http://ntvmr.uni-muenster.de/nt-conjectures',
             'http://vis4dh.com/papers/GlamMap%20Geovisualization%20for%20e-Humanities.pdf',
             'http://onlinelibrary.wiley.com/doi/10.1002/pon.4302/full',
             'http://cadmus.eui.eu/handle/1814/41508',
             'http://www.vala.org.au/direct-download/vala2016-proceedings/vala2016-papers/590-vala2016-session-8-betti-paper/file',
             'http://link.springer.com/article/10.1007/s12508-017-0047-4',
             'http://booksandjournals.brillonline.com/content/journals/1572543x/46/3',
             '1609.00544',
             'http://hdl.handle.net/11370/500ac271-aa39-49f7-9ec5-891c2b3c622f',
             'http://www.envirobiotechjournals.com/article_abstract.php?aid=6963&iid=212&jid=1']
        """
        import re
        from meta.consoleOutput import ConsoleOutput
        console = ConsoleOutput('log.txt')

        for item in doi_list:
            if re.search('^10\.|'
                         '^https://doi\.org/10\.|'
                         '^http://doi\.org/10\.|'
                         '^http://dx\.doi\.org/10\.|'
                         '^https://dx\.doi\.org/10\.|'
                         '^DOI 10\.|'
                         '^DOI: 10\.|'
                         '^DOI:10\.|'
                         '^doi:|'
                         '^doi\.org/|'
                         '^URN:|'
                         '^urn:', item) \
                    and len(item) < 80 \
                    and not re.search('^http://www\.|'  # DOI links does not contain 'www.'
                                      '^https://www\.', item):
                self.valid_search_criteria_registry.append(item)
            else:
                self.invalid_search_criteria_registry.append(item)

        caption = "DOI validation completed"
        console.log_message(caption, add_timestamp_in_file=True)
        summary = 'Number of valid DOIs: %d\n' \
                  'Number of invalid DOIs: %d\n' \
                  'Valid and invalid query criteria in parameter "doi_list" were recorded in instance variables' \
                  % (len(self.valid_search_criteria_registry), len(self.invalid_search_criteria_registry))
        console.log_message(summary)
        return self.valid_search_criteria_registry


class DOI_String(String):

    def __init__(self, content):
        String.__init__(self, content=content)


    def reduce_to_kernel(self):
        """
        Removes all characters except the core DOI from the DOI_String (e.g.,
        'http://doi.org/10.1016/j.adolescence.2016.09.008' becomes '10.1016/j.adolescence.2016.09.008').
        If DOI_String is not detected as a DOI (e.g., 'URN-5235-KLFGA-533'), it is returned without change.

        Returns:
            DOI_String (self)

        Examples:
            >>> # Single DOI conversion
            >>> my_doi = DOI_String('10.1016/j.adolescence.2016.09.008')
            >>> my_doi.reduce_to_kernel()
            '10.1016/j.adolescence.2016.09.008'

            >>> my_doi = DOI_String('http://doi.org/10.1016/j.adolescence.2016.09.008')
            >>> my_doi.reduce_to_kernel()
            '10.1016/j.adolescence.2016.09.008'

            >>> my_doi = DOI_String('https://doi.org/10.1016/j.adolescence.2016.09.008')
            >>> my_doi.reduce_to_kernel()
            '10.1016/j.adolescence.2016.09.008'

            >>> my_doi = DOI_String('http://dx.doi.org/10.1016/j.adolescence.2016.09.008')
            >>> my_doi.reduce_to_kernel()
            '10.1016/j.adolescence.2016.09.008'

            >>> my_doi = DOI_String('https://dx.doi.org/10.1016/j.adolescence.2016.09.008')
            >>> my_doi.reduce_to_kernel()
            '10.1016/j.adolescence.2016.09.008'

            >>> my_doi = DOI_String('DOI 10.1016/j.adolescence.2016.09.008')
            >>> my_doi.reduce_to_kernel()
            '10.1016/j.adolescence.2016.09.008'

            >>> my_doi = DOI_String('DOI: 10.1016/j.adolescence.2016.09.008')
            >>> my_doi.reduce_to_kernel()
            '10.1016/j.adolescence.2016.09.008'

            >>> my_doi = DOI_String('DOI:10.1016/j.adolescence.2016.09.008')
            >>> my_doi.reduce_to_kernel()
            '10.1016/j.adolescence.2016.09.008'

            >>> my_doi = DOI_String('doi:10.1016/j.adolescence.2016.09.008')
            >>> my_doi.reduce_to_kernel()
            '10.1016/j.adolescence.2016.09.008'

            >>> my_doi = DOI_String('doi.org/10.1016/j.adolescence.2016.09.008')
            >>> my_doi.reduce_to_kernel()
            '10.1016/j.adolescence.2016.09.008'

            >>> # Non-DOI input
            >>> my_doi = DOI_String('URN-3242340-ATJJK-3466')
            >>> my_doi.reduce_to_kernel()
            'URN-3242340-ATJJK-3466'

            >>> # Non-DOI input
            >>> my_doi = DOI_String('http://jena.apache.org/tutorials/sparql_filters.html')
            >>> my_doi.reduce_to_kernel()
            'http://jena.apache.org/tutorials/sparql_filters.html'
        """
        import re
        # if input is a DOI, extract and return its kernel
        if self.is_doi():
           position_of_the_doi_substring = re.search('10\.', self.content)
           doi_kernel = position_of_the_doi_substring.string[position_of_the_doi_substring.span()[0]:]
           self.content = doi_kernel

        # otherwise, return the input as string
        else:
           pass

        return self


    def generate_alternative_versions_if_doi(self):
        """
        Generates alternative versions of the DOI_String (e.g., 'http://doi.org/10.1016/j.adolescence.2016.09.008'
        is an alternative version of '10.1016/j.adolescence.2016.09.008'). If DOI_String is not detected as a
        DOI (e.g., 'URN-5235-KLFGA-533'), it is returned as a single-item list, without any other change to
        original string.

        Returns:
            list

        Examples:
            >>> # Single DOI conversion
            >>> my_doi = DOI_String('10.1016/j.adolescence.2016.09.008')
            >>> my_oc_query = Open_Citations_Query()
            >>> my_doi.generate_alternative_versions_if_doi()
            ['10.1016/j.adolescence.2016.09.008', 'https://doi.org/10.1016/j.adolescence.2016.09.008', 'http://doi.org/10.1016/j.adolescence.2016.09.008', 'http://dx.doi.org/10.1016/j.adolescence.2016.09.008', 'https://dx.doi.org/10.1016/j.adolescence.2016.09.008', 'DOI 10.1016/j.adolescence.2016.09.008', 'doi 10.1016/j.adolescence.2016.09.008', 'DOI: 10.1016/j.adolescence.2016.09.008', 'doi: 10.1016/j.adolescence.2016.09.008', 'DOI:10.1016/j.adolescence.2016.09.008', 'doi:10.1016/j.adolescence.2016.09.008', 'doi.org/10.1016/j.adolescence.2016.09.008']


            >>> # Non-DOI input
            >>> my_doi = DOI_String('URN-3242340-ATJJK-3466')
            >>> my_doi.generate_alternative_versions_if_doi()
            ['URN-3242340-ATJJK-3466']

        """
        if self.is_doi():
            pass
        else:
            return [self.content]

        prepend_strings = ['https://doi.org/',
                           'http://doi.org/',
                           'http://dx.doi.org/',
                           'https://dx.doi.org/',
                           'DOI ',
                           'doi ',
                           'DOI: ',
                           'doi: ',
                           'DOI:',
                           'doi:',
                           'doi.org/']

        doi_kernel = self.reduce_to_kernel().content
        alternative_versions = [doi_kernel]  # start with list with the the kernel
        for each_item in prepend_strings:
            extended_doi = String(doi_kernel)
            extended_doi.prepend(each_item)
            alternative_versions.append(extended_doi)

        return alternative_versions


    def is_doi(self):
        """
        Checks if DOI_String matches a DOI pattern (e.g., 'http://doi.org/10.1016/j.adolescence.2016.09.008').
        If DOI_String is not detected as a DOI (e.g., 'URN-5235-KLFGA-533'), it is returns False.

        Returns:
            bool

        Examples:
            >>> # Single DOI conversion
            >>> my_doi = DOI_String('10.1016/j.adolescence.2016.09.008')
            >>> my_doi.is_doi()
            True

            >>> my_doi = DOI_String('http://doi.org/10.1016/j.adolescence.2016.09.008')
            >>> my_doi.is_doi()
            True

            >>> my_doi = DOI_String('https://doi.org/10.1016/j.adolescence.2016.09.008')
            >>> my_doi.is_doi()
            True

            >>> my_doi = DOI_String('http://dx.doi.org/10.1016/j.adolescence.2016.09.008')
            >>> my_doi.is_doi()
            True

            >>> my_doi = DOI_String('https://dx.doi.org/10.1016/j.adolescence.2016.09.008')
            >>> my_doi.is_doi()
            True

            >>> my_doi = DOI_String('DOI 10.1016/j.adolescence.2016.09.008')
            >>> my_doi.is_doi()
            True

            >>> my_doi = DOI_String('DOI: 10.1016/j.adolescence.2016.09.008')
            >>> my_doi.is_doi()
            True

            >>> my_doi = DOI_String('DOI:10.1016/j.adolescence.2016.09.008')
            >>> my_doi.is_doi()
            True

            >>> my_doi = DOI_String('doi:10.1016/j.adolescence.2016.09.008')
            >>> my_doi.is_doi()
            True

            >>> my_doi = DOI_String('doi.org/10.1016/j.adolescence.2016.09.008')
            >>> my_doi.is_doi()
            True

            >>> # Non-DOI input
            >>> my_doi = DOI_String('URN-3242340-ATJJK-3466')
            >>> my_doi.is_doi()
            False

            >>> # Non-DOI input
            >>> my_doi = DOI_String('http://jena.apache.org/tutorials/sparql_filters.html')
            >>> my_doi.is_doi()
            False
        """
        import re

        doi_check = re.search('^10\.|'
                              '^https://doi\.org/10\.|'
                              '^http://doi\.org/10\.|'
                              '^http://dx\.doi\.org/10\.|'
                              '^https://dx\.doi\.org/10\.|'
                              '^DOI 10\.|'
                              '^doi 10\.|'
                              '^DOI: 10\.|'
                              '^doi: 10\.|'
                              '^DOI:10\.|'
                              '^doi:10\.|'
                              '^doi\.org/10\.|', self.content)

        if doi_check.span() != (0, 0):
            return True
        else:
           return False


class Sparql_Parameter:

    class Values_Parameter_String:
        def __init__(self, formatted_parameter_string=None):
            """
            Args:
                formatted_parameter_string(str): And already formatted parameter string for SPARQL VALUES keyword

            Examples:
                >>> # Initiate empty
                >>> my_parameter = Sparql_Parameter.Values_Parameter_String()

                >>> # Initiate with a string that contains parameters
                >>> my_parameter = Sparql_Parameter.Values_Parameter_String('a b c')

                >>> # Exception: Cannot initiate with a non-string
                >>> try:
                ...     my_parameter = Sparql_Parameter.Values_Parameter_String([1, 2 ,3])
                ... except Exception as exception:  # catch exception
                ...     print (exception)
                Parameter "[1, 2, 3]" must be of type <class 'str'>, but is currently of type <class 'list'>
            """
            from preprocessor.string_tools import Parameter_Value

            if formatted_parameter_string:
                Parameter_Value(formatted_parameter_string).force_type(str)
                content = formatted_parameter_string
            else:
                content = None


        def import_list_and_convert_to_parameter(self, list):
            """

            Args:
                list(list)

            Returns:
                Values_Parameter_String (updated self)

            Examples:
                >>> # Convert list of strings
                >>> my_list = ['a', 'b', 'c']
                >>> my_parameter = Sparql_Parameter.Values_Parameter_String()
                >>> my_parameter.import_list_and_convert_to_parameter(my_list).content
                '"a" "b" "c"'

                >>> # Convert list of non-strings
                >>> my_list = [1, 2, 3]
                >>> my_parameter = Sparql_Parameter.Values_Parameter_String()
                >>> my_parameter.import_list_and_convert_to_parameter(my_list).content
                '"1" "2" "3"'
            """
            parameter_string = ''
            for each_item in list:
                each_item = str(each_item)
                parameter_string = parameter_string + '"' + each_item + '"' + ' '

            # Remove the extra space at the end
            parameter_string = parameter_string[:-1]

            self.content = parameter_string
            return self


    class Values_Parameter_Series:

        def __init__(self):
            self.series = None

        def import_and_convert_pandas_series(self, series_object):
            """

            Args:
                series_object(pandas.Series):

            Returns:
                Values_Parameter_Series  (updated self)

            Examples:
                >>> import pandas
                >>> my_pandas_series = pandas.Series([['a', 'b', 'c' ],
                ...                                   [1, 2, 3],
                ...                                   [True, False, True]
                ... ])
                >>> my_pandas_series
                0              [a, b, c]
                1              [1, 2, 3]
                2    [True, False, True]
                dtype: object

                >>> my_parameter_series = Sparql_Parameter.Values_Parameter_Series()
                >>> my_parameter_series.import_and_convert_pandas_series(my_pandas_series)\
                                       .series
                0              "a" "b" "c"
                1              "1" "2" "3"
                2    "True" "False" "True"
                dtype: object

            """
            import pandas
            from preprocessor.string_tools import Parameter_Value

            Parameter_Value(series_object).force_type(pandas.Series)

            transformed_series = pandas.Series()

            for each_index, each_keywords_list in series_object.iteritems():

                parameterized_keyword_list = Sparql_Parameter.Values_Parameter_String()
                parameterized_keyword_list.import_list_and_convert_to_parameter(each_keywords_list)

                parameterized_keyword_series = pandas.Series(parameterized_keyword_list.content)

                transformed_series = transformed_series.append(parameterized_keyword_series, ignore_index=True)

            self.series = transformed_series

            return self
