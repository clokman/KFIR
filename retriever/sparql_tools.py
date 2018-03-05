class Sparql_Query():
    def __init__(self, input_query=''):
        """
        Examples:
            >>> #Initiation and initial values
            >>> my_query = Sparql_Query()
            >>> my_query.query
            ''
            >>> my_query.endpoint_address
            ''

            >>> # Take string as input
            >>> my_query_string = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\\n'\
                                  'SELECT ?label\\n'\
                                  'WHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }\\n'  # this
            >>>                   # notation (e.g., \\n at the end) is only necessary in docstrings, and actual
            >>>                   # string can be written inside ''' ''' marks in a Python script.
            >>> my_query.set_query(my_query_string)\
                        .print_query()
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

        self.results = {}
        self.number_of_lines_retrieved = 0


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


    def retrieve_results_from_endpoint(self, endpoint_address='', print_only=False):
        """
        Args:
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
            {1: {'journal_article': 'https://w3id.org/oc/corpus/br/362418', 'title': 'The DSM-5 diagnosis of nonsuicidal self-injury disorder: a review of the empirical literature', 'publication_year': '2015', 'journal_name': 'Child and Adolescent Psychiatry and Mental Health - Child Adolesc Psychiatry Ment Health', 'journal_issue_number': '1', 'journal_volume_number': '9', 'publisher_name': 'Springer Science + Business Media', 'doi': '10.1186/s13034-015-0062-7', 'pmid': '26417387', 'url': 'http://dx.doi.org/10.1186/s13034-015-0062-7', 'authors': 'Zetterqvist - Maria', 'cited_the_articles': 'https://w3id.org/oc/corpus/br/37961 | https://w3id.org/oc/corpus/br/38250 | https://w3id.org/oc/corpus/br/135448 | https://w3id.org/oc/corpus/br/135458 | https://w3id.org/oc/corpus/br/177639 | https://w3id.org/oc/corpus/br/177648 | https://w3id.org/oc/corpus/br/177653 | https://w3id.org/oc/corpus/br/177661 | https://w3id.org/oc/corpus/br/177774 | https://w3id.org/oc/corpus/br/362419 | https://w3id.org/oc/corpus/br/362426 | https://w3id.org/oc/corpus/br/362438 | https://w3id.org/oc/corpus/br/607811 | https://w3id.org/oc/corpus/br/1270766 | https://w3id.org/oc/corpus/br/1560911 | https://w3id.org/oc/corpus/br/1794850 | https://w3id.org/oc/corpus/br/1881397 | https://w3id.org/oc/corpus/br/2258672 | https://w3id.org/oc/corpus/br/2907029 | https://w3id.org/oc/corpus/br/2907034 | https://w3id.org/oc/corpus/br/2907035 | https://w3id.org/oc/corpus/br/2907042 | https://w3id.org/oc/corpus/br/2907056 | https://w3id.org/oc/corpus/br/3346205 | https://w3id.org/oc/corpus/br/3567493 | https://w3id.org/oc/corpus/br/3567495 | https://w3id.org/oc/corpus/br/3949890 | https://w3id.org/oc/corpus/br/5106137 | https://w3id.org/oc/corpus/br/5441063 | https://w3id.org/oc/corpus/br/5441066 | https://w3id.org/oc/corpus/br/5441085 | https://w3id.org/oc/corpus/br/5656230 | https://w3id.org/oc/corpus/br/6060536 | https://w3id.org/oc/corpus/br/6063037 | https://w3id.org/oc/corpus/br/6449521 | https://w3id.org/oc/corpus/br/6486152 | https://w3id.org/oc/corpus/br/6486162 | https://w3id.org/oc/corpus/br/6919305 | https://w3id.org/oc/corpus/br/6919323 | https://w3id.org/oc/corpus/br/7558746 | https://w3id.org/oc/corpus/br/7560541 | https://w3id.org/oc/corpus/br/7560644 | https://w3id.org/oc/corpus/br/7560645 | https://w3id.org/oc/corpus/br/7560646 | https://w3id.org/oc/corpus/br/7560647 | https://w3id.org/oc/corpus/br/7560648 | https://w3id.org/oc/corpus/br/7560651 | https://w3id.org/oc/corpus/br/7560652 | https://w3id.org/oc/corpus/br/7560653 | https://w3id.org/oc/corpus/br/7560654 | https://w3id.org/oc/corpus/br/7560655 | https://w3id.org/oc/corpus/br/7560656 | https://w3id.org/oc/corpus/br/7560657 | https://w3id.org/oc/corpus/br/7560658 | https://w3id.org/oc/corpus/br/7560659 | https://w3id.org/oc/corpus/br/7560660 | https://w3id.org/oc/corpus/br/7560661 | https://w3id.org/oc/corpus/br/7560662 | https://w3id.org/oc/corpus/br/7560663 | https://w3id.org/oc/corpus/br/7560664 | https://w3id.org/oc/corpus/br/7560665 | https://w3id.org/oc/corpus/br/7560666', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/362415'}, 2: {'journal_article': 'https://w3id.org/oc/corpus/br/384', 'title': 'Survival after relapse in patients with endometrial cancer: results from a randomized trial☆', 'publication_year': '2003', 'journal_name': 'Gynecologic Oncology', 'journal_issue_number': '2', 'journal_volume_number': '89', 'startEndPages': '201--209', 'publisher_name': 'Elsevier BV', 'doi': '10.1016/s0090-8258(03)00126-4', 'pmid': '12713981', 'url': 'http://dx.doi.org/10.1016/s0090-8258%2803%2900126-4', 'authors': 'Creutzberg - Carien L | van Putten - Wim L.J | Koper - Peter C | Lybeert - Marnix L.M | Jobsen - Jan J | Wárlám-Rodenhuis - Carla C | De Winter - Karin A.J | Lutgens - Ludy C.H.W | van den Bergh - Alfons C.M | van der Steen-Banasik - Elzbieta | Beerman - Henk | van Lent - Mat', 'cited_the_articles': '', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/1 | https://w3id.org/oc/corpus/br/1342763 | https://w3id.org/oc/corpus/br/1772164'}, 3: {'journal_article': 'https://w3id.org/oc/corpus/br/392', 'title': 'Stage IC adenocarcinoma of the endometrium: survival comparisons of surgically staged patients with and without adjuvant radiation therapyâ\x98\x86â\x98\x86Presented at the 33rd Annual Meeting of Gynecologic Oncologists, Miami, FL, March 2002.', 'publication_year': '2003', 'journal_name': 'Gynecologic Oncology', 'journal_issue_number': '2', 'journal_volume_number': '89', 'startEndPages': '295--300', 'publisher_name': 'Elsevier BV', 'doi': '10.1016/s0090-8258(03)00087-8', 'pmid': '12713994', 'url': 'http://dx.doi.org/10.1016/s0090-8258%2803%2900087-8', 'authors': 'Straughn - J.Michael | Huh - Warner K | Orr - James W | Kelly - F.Joseph | Roland - Phillip Y | Gold - Michael A | Powell - Matthew | Mutch - David G | Partridge - Edward E | Kilgore - Larry C | Barnes - Mack N | Austin - J.Maxwell | Alvarez - Ronald D', 'cited_the_articles': '', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/1'}}

            >>> my_oc_query.write_results_to_csv('test_data_and_queries//test_write_of_sparql_results.csv')
            The results were written to "test_data_and_queries//test_write_of_sparql_results.csv"
            >>> output_file = Text_File('test_data_and_queries//test_write_of_sparql_results.csv')
            >>> output_file.preview(4)
            "journal_article" , "title" , "publication_year" , "journal_name" , "journal_issue_number" , "journal_volume_number" , "publisher_name" , "doi" , "pmid" , "url" , "authors" , "cited_the_articles" , "cited_by_the_articles" , "startEndPages" ,
            "https://w3id.org/oc/corpus/br/362418" , "The DSM-5 diagnosis of nonsuicidal self-injury disorder: a review of the empirical literature" , "2015" , "Child and Adolescent Psychiatry and Mental Health - Child Adolesc Psychiatry Ment Health" , "1" , "9" , "Springer Science + Business Media" , "10.1186/s13034-015-0062-7" , "26417387" , "http://dx.doi.org/10.1186/s13034-015-0062-7" , "Zetterqvist - Maria" , "https://w3id.org/oc/corpus/br/37961 | https://w3id.org/oc/corpus/br/38250 | https://w3id.org/oc/corpus/br/135448 | https://w3id.org/oc/corpus/br/135458 | https://w3id.org/oc/corpus/br/177639 | https://w3id.org/oc/corpus/br/177648 | https://w3id.org/oc/corpus/br/177653 | https://w3id.org/oc/corpus/br/177661 | https://w3id.org/oc/corpus/br/177774 | https://w3id.org/oc/corpus/br/362419 | https://w3id.org/oc/corpus/br/362426 | https://w3id.org/oc/corpus/br/362438 | https://w3id.org/oc/corpus/br/607811 | https://w3id.org/oc/corpus/br/1270766 | https://w3id.org/oc/corpus/br/1560911 | https://w3id.org/oc/corpus/br/1794850 | https://w3id.org/oc/corpus/br/1881397 | https://w3id.org/oc/corpus/br/2258672 | https://w3id.org/oc/corpus/br/2907029 | https://w3id.org/oc/corpus/br/2907034 | https://w3id.org/oc/corpus/br/2907035 | https://w3id.org/oc/corpus/br/2907042 | https://w3id.org/oc/corpus/br/2907056 | https://w3id.org/oc/corpus/br/3346205 | https://w3id.org/oc/corpus/br/3567493 | https://w3id.org/oc/corpus/br/3567495 | https://w3id.org/oc/corpus/br/3949890 | https://w3id.org/oc/corpus/br/5106137 | https://w3id.org/oc/corpus/br/5441063 | https://w3id.org/oc/corpus/br/5441066 | https://w3id.org/oc/corpus/br/5441085 | https://w3id.org/oc/corpus/br/5656230 | https://w3id.org/oc/corpus/br/6060536 | https://w3id.org/oc/corpus/br/6063037 | https://w3id.org/oc/corpus/br/6449521 | https://w3id.org/oc/corpus/br/6486152 | https://w3id.org/oc/corpus/br/6486162 | https://w3id.org/oc/corpus/br/6919305 | https://w3id.org/oc/corpus/br/6919323 | https://w3id.org/oc/corpus/br/7558746 | https://w3id.org/oc/corpus/br/7560541 | https://w3id.org/oc/corpus/br/7560644 | https://w3id.org/oc/corpus/br/7560645 | https://w3id.org/oc/corpus/br/7560646 | https://w3id.org/oc/corpus/br/7560647 | https://w3id.org/oc/corpus/br/7560648 | https://w3id.org/oc/corpus/br/7560651 | https://w3id.org/oc/corpus/br/7560652 | https://w3id.org/oc/corpus/br/7560653 | https://w3id.org/oc/corpus/br/7560654 | https://w3id.org/oc/corpus/br/7560655 | https://w3id.org/oc/corpus/br/7560656 | https://w3id.org/oc/corpus/br/7560657 | https://w3id.org/oc/corpus/br/7560658 | https://w3id.org/oc/corpus/br/7560659 | https://w3id.org/oc/corpus/br/7560660 | https://w3id.org/oc/corpus/br/7560661 | https://w3id.org/oc/corpus/br/7560662 | https://w3id.org/oc/corpus/br/7560663 | https://w3id.org/oc/corpus/br/7560664 | https://w3id.org/oc/corpus/br/7560665 | https://w3id.org/oc/corpus/br/7560666" , "https://w3id.org/oc/corpus/br/362415" , " " ,
            "https://w3id.org/oc/corpus/br/384" , "Survival after relapse in patients with endometrial cancer: results from a randomized trial☆" , "2003" , "Gynecologic Oncology" , "2" , "89" , "Elsevier BV" , "10.1016/s0090-8258(03)00126-4" , "12713981" , "http://dx.doi.org/10.1016/s0090-8258%2803%2900126-4" , "Creutzberg - Carien L | van Putten - Wim L.J | Koper - Peter C | Lybeert - Marnix L.M | Jobsen - Jan J | Wárlám-Rodenhuis - Carla C | De Winter - Karin A.J | Lutgens - Ludy C.H.W | van den Bergh - Alfons C.M | van der Steen-Banasik - Elzbieta | Beerman - Henk | van Lent - Mat" , "" , "https://w3id.org/oc/corpus/br/1 | https://w3id.org/oc/corpus/br/1342763 | https://w3id.org/oc/corpus/br/1772164" , "201--209" ,
            "https://w3id.org/oc/corpus/br/392" , "Stage IC adenocarcinoma of the endometrium: survival comparisons of surgically staged patients with and without adjuvant radiation therapyââPresented at the 33rd Annual Meeting of Gynecologic Oncologists, Miami, FL, March 2002." , "2003" , "Gynecologic Oncology" , "2" , "89" , "Elsevier BV" , "10.1016/s0090-8258(03)00087-8" , "12713994" , "http://dx.doi.org/10.1016/s0090-8258%2803%2900087-8" , "Straughn - J.Michael | Huh - Warner K | Orr - James W | Kelly - F.Joseph | Roland - Phillip Y | Gold - Michael A | Powell - Matthew | Mutch - David G | Partridge - Edward E | Kilgore - Larry C | Barnes - Mack N | Austin - J.Maxwell | Alvarez - Ronald D" , "" , "https://w3id.org/oc/corpus/br/1" , "295--300" ,



        """
        from preprocessor.csv_tools import CSV_Line, CSV_Row, CSV_File
        from triplicator.bibTools import Bibliography
        from preprocessor.ListData import ListData

        list_data = ListData()
        list_data.import_json_object(self.results)

        all_formatted_lines = []
        for each_line in list_data.dataset:
            each_row = CSV_Row(each_line)
            formatted_csv_line = each_row.format_for_print_and_CONVERT_to_CSV_Line(
                column_separator=' , ',
                line_head='',
                line_tail=' ,',
                cell_wrapper='"')
            all_formatted_lines.append(formatted_csv_line)

        with open(output_file_path, mode='w', encoding='utf8') as output_file:
            for each_row in all_formatted_lines:
                print(each_row, file=output_file)
            print('The results were written to "%s"' % output_file_path)

        #bibliography = Bibliography()

        #headers = {}
        #for each_results_line_number, each_result in self.results.values():
        #    for each_field_name, each_field_values in each_result:
        #        headers.append(each_field_name)






class Open_Citations_Query(Sparql_Query):

    def __init__(self, input_query=''):
        Sparql_Query.__init__(self, input_query)


    def retrieve_article_by_doi(self, target_doi, print_only=False):
        """

        Args:
            target_doi(str)

        Returns:
            dict or nothing (if print_only is selected)

        Examples:
        >>> my_oc_query = Open_Citations_Query()
        >>> my_oc_query.retrieve_article_by_doi('10.1186/s13034-015-0062-7')
        {1: {'journal_article': 'https://w3id.org/oc/corpus/br/362418', 'title': 'The DSM-5 diagnosis of nonsuicidal self-injury disorder: a review of the empirical literature', 'publication_year': '2015', 'journal_name': 'Child and Adolescent Psychiatry and Mental Health - Child Adolesc Psychiatry Ment Health', 'journal_issue_number': '1', 'journal_volume_number': '9', 'publisher_name': 'Springer Science + Business Media', 'doi': '10.1186/s13034-015-0062-7', 'pmid': '26417387', 'url': 'http://dx.doi.org/10.1186/s13034-015-0062-7', 'authors': 'Zetterqvist - Maria', 'cited_the_articles': 'https://w3id.org/oc/corpus/br/37961 | https://w3id.org/oc/corpus/br/38250 | https://w3id.org/oc/corpus/br/135448 | https://w3id.org/oc/corpus/br/135458 | https://w3id.org/oc/corpus/br/177639 | https://w3id.org/oc/corpus/br/177648 | https://w3id.org/oc/corpus/br/177653 | https://w3id.org/oc/corpus/br/177661 | https://w3id.org/oc/corpus/br/177774 | https://w3id.org/oc/corpus/br/362419 | https://w3id.org/oc/corpus/br/362426 | https://w3id.org/oc/corpus/br/362438 | https://w3id.org/oc/corpus/br/607811 | https://w3id.org/oc/corpus/br/1270766 | https://w3id.org/oc/corpus/br/1560911 | https://w3id.org/oc/corpus/br/1794850 | https://w3id.org/oc/corpus/br/1881397 | https://w3id.org/oc/corpus/br/2258672 | https://w3id.org/oc/corpus/br/2907029 | https://w3id.org/oc/corpus/br/2907034 | https://w3id.org/oc/corpus/br/2907035 | https://w3id.org/oc/corpus/br/2907042 | https://w3id.org/oc/corpus/br/2907056 | https://w3id.org/oc/corpus/br/3346205 | https://w3id.org/oc/corpus/br/3567493 | https://w3id.org/oc/corpus/br/3567495 | https://w3id.org/oc/corpus/br/3949890 | https://w3id.org/oc/corpus/br/5106137 | https://w3id.org/oc/corpus/br/5441063 | https://w3id.org/oc/corpus/br/5441066 | https://w3id.org/oc/corpus/br/5441085 | https://w3id.org/oc/corpus/br/5656230 | https://w3id.org/oc/corpus/br/6060536 | https://w3id.org/oc/corpus/br/6063037 | https://w3id.org/oc/corpus/br/6449521 | https://w3id.org/oc/corpus/br/6486152 | https://w3id.org/oc/corpus/br/6486162 | https://w3id.org/oc/corpus/br/6919305 | https://w3id.org/oc/corpus/br/6919323 | https://w3id.org/oc/corpus/br/7558746 | https://w3id.org/oc/corpus/br/7560541 | https://w3id.org/oc/corpus/br/7560644 | https://w3id.org/oc/corpus/br/7560645 | https://w3id.org/oc/corpus/br/7560646 | https://w3id.org/oc/corpus/br/7560647 | https://w3id.org/oc/corpus/br/7560648 | https://w3id.org/oc/corpus/br/7560651 | https://w3id.org/oc/corpus/br/7560652 | https://w3id.org/oc/corpus/br/7560653 | https://w3id.org/oc/corpus/br/7560654 | https://w3id.org/oc/corpus/br/7560655 | https://w3id.org/oc/corpus/br/7560656 | https://w3id.org/oc/corpus/br/7560657 | https://w3id.org/oc/corpus/br/7560658 | https://w3id.org/oc/corpus/br/7560659 | https://w3id.org/oc/corpus/br/7560660 | https://w3id.org/oc/corpus/br/7560661 | https://w3id.org/oc/corpus/br/7560662 | https://w3id.org/oc/corpus/br/7560663 | https://w3id.org/oc/corpus/br/7560664 | https://w3id.org/oc/corpus/br/7560665 | https://w3id.org/oc/corpus/br/7560666', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/362415'}}
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
        {'journal_article': 'https://w3id.org/oc/corpus/br/362418', 'title': 'The DSM-5 diagnosis of nonsuicidal self-injury disorder: a review of the empirical literature', 'publication_year': '2015', 'journal_name': 'Child and Adolescent Psychiatry and Mental Health - Child Adolesc Psychiatry Ment Health', 'journal_issue_number': '1', 'journal_volume_number': '9', 'publisher_name': 'Springer Science + Business Media', 'doi': '10.1186/s13034-015-0062-7', 'pmid': '26417387', 'url': 'http://dx.doi.org/10.1186/s13034-015-0062-7', 'authors': 'Zetterqvist - Maria', 'cited_the_articles': 'https://w3id.org/oc/corpus/br/37961 | https://w3id.org/oc/corpus/br/38250 | https://w3id.org/oc/corpus/br/135448 | https://w3id.org/oc/corpus/br/135458 | https://w3id.org/oc/corpus/br/177639 | https://w3id.org/oc/corpus/br/177648 | https://w3id.org/oc/corpus/br/177653 | https://w3id.org/oc/corpus/br/177661 | https://w3id.org/oc/corpus/br/177774 | https://w3id.org/oc/corpus/br/362419 | https://w3id.org/oc/corpus/br/362426 | https://w3id.org/oc/corpus/br/362438 | https://w3id.org/oc/corpus/br/607811 | https://w3id.org/oc/corpus/br/1270766 | https://w3id.org/oc/corpus/br/1560911 | https://w3id.org/oc/corpus/br/1794850 | https://w3id.org/oc/corpus/br/1881397 | https://w3id.org/oc/corpus/br/2258672 | https://w3id.org/oc/corpus/br/2907029 | https://w3id.org/oc/corpus/br/2907034 | https://w3id.org/oc/corpus/br/2907035 | https://w3id.org/oc/corpus/br/2907042 | https://w3id.org/oc/corpus/br/2907056 | https://w3id.org/oc/corpus/br/3346205 | https://w3id.org/oc/corpus/br/3567493 | https://w3id.org/oc/corpus/br/3567495 | https://w3id.org/oc/corpus/br/3949890 | https://w3id.org/oc/corpus/br/5106137 | https://w3id.org/oc/corpus/br/5441063 | https://w3id.org/oc/corpus/br/5441066 | https://w3id.org/oc/corpus/br/5441085 | https://w3id.org/oc/corpus/br/5656230 | https://w3id.org/oc/corpus/br/6060536 | https://w3id.org/oc/corpus/br/6063037 | https://w3id.org/oc/corpus/br/6449521 | https://w3id.org/oc/corpus/br/6486152 | https://w3id.org/oc/corpus/br/6486162 | https://w3id.org/oc/corpus/br/6919305 | https://w3id.org/oc/corpus/br/6919323 | https://w3id.org/oc/corpus/br/7558746 | https://w3id.org/oc/corpus/br/7560541 | https://w3id.org/oc/corpus/br/7560644 | https://w3id.org/oc/corpus/br/7560645 | https://w3id.org/oc/corpus/br/7560646 | https://w3id.org/oc/corpus/br/7560647 | https://w3id.org/oc/corpus/br/7560648 | https://w3id.org/oc/corpus/br/7560651 | https://w3id.org/oc/corpus/br/7560652 | https://w3id.org/oc/corpus/br/7560653 | https://w3id.org/oc/corpus/br/7560654 | https://w3id.org/oc/corpus/br/7560655 | https://w3id.org/oc/corpus/br/7560656 | https://w3id.org/oc/corpus/br/7560657 | https://w3id.org/oc/corpus/br/7560658 | https://w3id.org/oc/corpus/br/7560659 | https://w3id.org/oc/corpus/br/7560660 | https://w3id.org/oc/corpus/br/7560661 | https://w3id.org/oc/corpus/br/7560662 | https://w3id.org/oc/corpus/br/7560663 | https://w3id.org/oc/corpus/br/7560664 | https://w3id.org/oc/corpus/br/7560665 | https://w3id.org/oc/corpus/br/7560666', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/362415'}
        """
        from retriever.query_templates import Query_Template

        query_string = Query_Template().get_oc_article_by_doi(target_doi)

        self.set_query(query_string)
        self.results = self.retrieve_results_from_endpoint(endpoint_address='http://opencitations.net/sparql')

        if print_only:
            self.print_results()
        else:
            return self.results


    def retrieve_articles_by_dois(self, target_dois_list, print_only=False):
        """
        Returns:
            dict or nothing (if print_only is selected)

        Examples:
            >>> my_oc_query = Open_Citations_Query()
            >>> target_dois_list = ['10.1186/s13034-015-0062-7', '10.1016/s0090-8258(03)00126-4',
            ...                     '10.1016/s0090-8258(03)00087-8']  # add '10.1016/s0020-7292(06)60031-3' to the list
            ...                     # to see a doi returning two results with a slight difference (different PMIDs in
            ...                     # two results)
            >>> my_oc_query.retrieve_articles_by_dois(target_dois_list)
            {1: {'journal_article': 'https://w3id.org/oc/corpus/br/362418', 'title': 'The DSM-5 diagnosis of nonsuicidal self-injury disorder: a review of the empirical literature', 'publication_year': '2015', 'journal_name': 'Child and Adolescent Psychiatry and Mental Health - Child Adolesc Psychiatry Ment Health', 'journal_issue_number': '1', 'journal_volume_number': '9', 'publisher_name': 'Springer Science + Business Media', 'doi': '10.1186/s13034-015-0062-7', 'pmid': '26417387', 'url': 'http://dx.doi.org/10.1186/s13034-015-0062-7', 'authors': 'Zetterqvist - Maria', 'cited_the_articles': 'https://w3id.org/oc/corpus/br/37961 | https://w3id.org/oc/corpus/br/38250 | https://w3id.org/oc/corpus/br/135448 | https://w3id.org/oc/corpus/br/135458 | https://w3id.org/oc/corpus/br/177639 | https://w3id.org/oc/corpus/br/177648 | https://w3id.org/oc/corpus/br/177653 | https://w3id.org/oc/corpus/br/177661 | https://w3id.org/oc/corpus/br/177774 | https://w3id.org/oc/corpus/br/362419 | https://w3id.org/oc/corpus/br/362426 | https://w3id.org/oc/corpus/br/362438 | https://w3id.org/oc/corpus/br/607811 | https://w3id.org/oc/corpus/br/1270766 | https://w3id.org/oc/corpus/br/1560911 | https://w3id.org/oc/corpus/br/1794850 | https://w3id.org/oc/corpus/br/1881397 | https://w3id.org/oc/corpus/br/2258672 | https://w3id.org/oc/corpus/br/2907029 | https://w3id.org/oc/corpus/br/2907034 | https://w3id.org/oc/corpus/br/2907035 | https://w3id.org/oc/corpus/br/2907042 | https://w3id.org/oc/corpus/br/2907056 | https://w3id.org/oc/corpus/br/3346205 | https://w3id.org/oc/corpus/br/3567493 | https://w3id.org/oc/corpus/br/3567495 | https://w3id.org/oc/corpus/br/3949890 | https://w3id.org/oc/corpus/br/5106137 | https://w3id.org/oc/corpus/br/5441063 | https://w3id.org/oc/corpus/br/5441066 | https://w3id.org/oc/corpus/br/5441085 | https://w3id.org/oc/corpus/br/5656230 | https://w3id.org/oc/corpus/br/6060536 | https://w3id.org/oc/corpus/br/6063037 | https://w3id.org/oc/corpus/br/6449521 | https://w3id.org/oc/corpus/br/6486152 | https://w3id.org/oc/corpus/br/6486162 | https://w3id.org/oc/corpus/br/6919305 | https://w3id.org/oc/corpus/br/6919323 | https://w3id.org/oc/corpus/br/7558746 | https://w3id.org/oc/corpus/br/7560541 | https://w3id.org/oc/corpus/br/7560644 | https://w3id.org/oc/corpus/br/7560645 | https://w3id.org/oc/corpus/br/7560646 | https://w3id.org/oc/corpus/br/7560647 | https://w3id.org/oc/corpus/br/7560648 | https://w3id.org/oc/corpus/br/7560651 | https://w3id.org/oc/corpus/br/7560652 | https://w3id.org/oc/corpus/br/7560653 | https://w3id.org/oc/corpus/br/7560654 | https://w3id.org/oc/corpus/br/7560655 | https://w3id.org/oc/corpus/br/7560656 | https://w3id.org/oc/corpus/br/7560657 | https://w3id.org/oc/corpus/br/7560658 | https://w3id.org/oc/corpus/br/7560659 | https://w3id.org/oc/corpus/br/7560660 | https://w3id.org/oc/corpus/br/7560661 | https://w3id.org/oc/corpus/br/7560662 | https://w3id.org/oc/corpus/br/7560663 | https://w3id.org/oc/corpus/br/7560664 | https://w3id.org/oc/corpus/br/7560665 | https://w3id.org/oc/corpus/br/7560666', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/362415'}, 2: {'journal_article': 'https://w3id.org/oc/corpus/br/384', 'title': 'Survival after relapse in patients with endometrial cancer: results from a randomized trial☆', 'publication_year': '2003', 'journal_name': 'Gynecologic Oncology', 'journal_issue_number': '2', 'journal_volume_number': '89', 'startEndPages': '201--209', 'publisher_name': 'Elsevier BV', 'doi': '10.1016/s0090-8258(03)00126-4', 'pmid': '12713981', 'url': 'http://dx.doi.org/10.1016/s0090-8258%2803%2900126-4', 'authors': 'Creutzberg - Carien L | van Putten - Wim L.J | Koper - Peter C | Lybeert - Marnix L.M | Jobsen - Jan J | Wárlám-Rodenhuis - Carla C | De Winter - Karin A.J | Lutgens - Ludy C.H.W | van den Bergh - Alfons C.M | van der Steen-Banasik - Elzbieta | Beerman - Henk | van Lent - Mat', 'cited_the_articles': '', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/1 | https://w3id.org/oc/corpus/br/1342763 | https://w3id.org/oc/corpus/br/1772164'}, 3: {'journal_article': 'https://w3id.org/oc/corpus/br/392', 'title': 'Stage IC adenocarcinoma of the endometrium: survival comparisons of surgically staged patients with and without adjuvant radiation therapyâ\x98\x86â\x98\x86Presented at the 33rd Annual Meeting of Gynecologic Oncologists, Miami, FL, March 2002.', 'publication_year': '2003', 'journal_name': 'Gynecologic Oncology', 'journal_issue_number': '2', 'journal_volume_number': '89', 'startEndPages': '295--300', 'publisher_name': 'Elsevier BV', 'doi': '10.1016/s0090-8258(03)00087-8', 'pmid': '12713994', 'url': 'http://dx.doi.org/10.1016/s0090-8258%2803%2900087-8', 'authors': 'Straughn - J.Michael | Huh - Warner K | Orr - James W | Kelly - F.Joseph | Roland - Phillip Y | Gold - Michael A | Powell - Matthew | Mutch - David G | Partridge - Edward E | Kilgore - Larry C | Barnes - Mack N | Austin - J.Maxwell | Alvarez - Ronald D', 'cited_the_articles': '', 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/1'}}
            >>> my_oc_query.retrieve_articles_by_dois(target_dois_list, print_only=True)
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
                 'publication_year': '2015',
                 'publisher_name': 'Springer Science + Business Media',
                 'title': 'The DSM-5 diagnosis of nonsuicidal self-injury disorder: a '
                          'review of the empirical literature',
                 'url': 'http://dx.doi.org/10.1186/s13034-015-0062-7'},
             2: {'authors': 'Creutzberg - Carien L | van Putten - Wim L.J | Koper - Peter '
                            'C | Lybeert - Marnix L.M | Jobsen - Jan J | Wárlám-Rodenhuis '
                            '- Carla C | De Winter - Karin A.J | Lutgens - Ludy C.H.W | '
                            'van den Bergh - Alfons C.M | van der Steen-Banasik - Elzbieta '
                            '| Beerman - Henk | van Lent - Mat',
                 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/1 | '
                                          'https://w3id.org/oc/corpus/br/1342763 | '
                                          'https://w3id.org/oc/corpus/br/1772164',
                 'cited_the_articles': '',
                 'doi': '10.1016/s0090-8258(03)00126-4',
                 'journal_article': 'https://w3id.org/oc/corpus/br/384',
                 'journal_issue_number': '2',
                 'journal_name': 'Gynecologic Oncology',
                 'journal_volume_number': '89',
                 'pmid': '12713981',
                 'publication_year': '2003',
                 'publisher_name': 'Elsevier BV',
                 'startEndPages': '201--209',
                 'title': 'Survival after relapse in patients with endometrial cancer: '
                          'results from a randomized trial☆',
                 'url': 'http://dx.doi.org/10.1016/s0090-8258%2803%2900126-4'},
             3: {'authors': 'Straughn - J.Michael | Huh - Warner K | Orr - James W | Kelly '
                            '- F.Joseph | Roland - Phillip Y | Gold - Michael A | Powell - '
                            'Matthew | Mutch - David G | Partridge - Edward E | Kilgore - '
                            'Larry C | Barnes - Mack N | Austin - J.Maxwell | Alvarez - '
                            'Ronald D',
                 'cited_by_the_articles': 'https://w3id.org/oc/corpus/br/1',
                 'cited_the_articles': '',
                 'doi': '10.1016/s0090-8258(03)00087-8',
                 'journal_article': 'https://w3id.org/oc/corpus/br/392',
                 'journal_issue_number': '2',
                 'journal_name': 'Gynecologic Oncology',
                 'journal_volume_number': '89',
                 'pmid': '12713994',
                 'publication_year': '2003',
                 'publisher_name': 'Elsevier BV',
                 'startEndPages': '295--300',
                 'title': 'Stage IC adenocarcinoma of the endometrium: survival '
                          'comparisons of surgically staged patients with and without '
                          'adjuvant radiation therapyâ\\x98\\x86â\\x98\\x86Presented at the '
                          '33rd Annual Meeting of Gynecologic Oncologists, Miami, FL, '
                          'March 2002.',
                 'url': 'http://dx.doi.org/10.1016/s0090-8258%2803%2900087-8'}}
        """

        no_of_results_returned_so_far = 0
        all_results = {}

        for each_target_doi in target_dois_list:
            current_result = self.retrieve_article_by_doi(each_target_doi)
            # aggregate returned results in all_results variable
            for each_key, each_value in current_result.items():  # keys represent row numbers of returned results table
                no_of_results_returned_so_far += 1               # ... and values represent fields and their values
                all_results[no_of_results_returned_so_far] = each_value

        self.results = all_results
        self.number_of_lines_retrieved = no_of_results_returned_so_far

        if print_only:
            self.print_results()
        else:
            return self.results