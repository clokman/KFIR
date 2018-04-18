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
