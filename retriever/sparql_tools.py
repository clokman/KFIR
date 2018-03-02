from preprocessor.string_tools import String

class Sparql_Query(String):
    def __init__(self):
        """
        Examples:
            >>> #Initiation and initial values
            >>> my_query = Sparql_Query()
            >>> my_query.content
            ''
            >>> my_query.endpoint_address
            ''

            >>> # Take string as input
            >>> my_query_string = 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\\n'\
                                  'SELECT ?label\\n'\
                                  'WHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }\\n'  # this
            >>>                   # notation (e.g., \\n at the end) is only necessary in docstrings, and actual
            >>>                   # string can be written inside ''' ''' marks in a Python script.
            >>> my_query.set_query(my_query_string)
            'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\\nSELECT ?label\\nWHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }\\n'

            >>> # Directly calling the object returns the query (newline characters may appear in terminal output)
            >>> my_query
            'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\\nSELECT ?label\\nWHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }\\n'
            >>> # Calling the object's conent variable is equivalent to calling the object directly
            >>> my_query.content
            'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\\nSELECT ?label\\nWHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }\\n'

            >>> # For prettier console output, print_query method can be used
            >>> my_query.print_query()
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?label
            WHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }
            <BLANKLINE>
        """
        String.__init__(self, '')  # passes on empty string as content

        self.endpoint_address = ''


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
        self.content = query_string
        return self


    def import_query_from_file(self, query_file_path):
        """
        Returns:
            self
        Examples:
            >>> # Take file as input
            >>> my_query = Sparql_Query()
            >>> my_query.import_query_from_file('test_data//simple_dbpedia_test.rq')
            '\\n            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\\nSELECT ?label\\nWHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }\\n        '
            >>> my_query.print_query()  # a slight, non-problematic misalignment due to extra spaces is visible in the
            ...                         # first line of query file
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


    def send_query(self):
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
                        .set_endpoint("http://dbpedia.org/sparql")\
                        .send_query()
            [{'label': {'type': 'literal', 'xml:lang': 'ar', 'value': 'أمثلة (توضيح)'}}, {'label': {'type': 'literal', 'xml:lang': 'en', 'value': 'Example'}}, {'label': {'type': 'literal', 'xml:lang': 'de', 'value': 'Example (Begriffsklärung)'}}, {'label': {'type': 'literal', 'xml:lang': 'fr', 'value': 'Example'}}]


            >>> my_query = Sparql_Query()
            >>> my_query.import_query_from_file('test_data//simple_dbpedia_test.rq')\
                        .set_endpoint("http://dbpedia.org/sparql")\
                        .send_query()
            [{'label': {'type': 'literal', 'xml:lang': 'ar', 'value': 'أمثلة (توضيح)'}}, {'label': {'type': 'literal', 'xml:lang': 'en', 'value': 'Example'}}, {'label': {'type': 'literal', 'xml:lang': 'de', 'value': 'Example (Begriffsklärung)'}}, {'label': {'type': 'literal', 'xml:lang': 'fr', 'value': 'Example'}}]

            >>> # A required parameter is not specified
            >>> my_query = Sparql_Query()
            >>> try:
            ...     my_query.send_query()
            ... except Exception as error_message:
            ...     print('Exception caught: ' + str(error_message))
            Exception caught: Parameters '['query', 'endpoint_address']' must be specified before this method is called. The current values of the parameters are ['', '']
            >>> my_query.set_endpoint('some endpoint')
            ''
            >>> try:
            ...     my_query.send_query()
            ... except Exception as error_message:
            ...     print('Exception caught: ' + str(error_message))
            Exception caught: Parameters '['query', 'endpoint_address']' must be specified before this method is called. The current values of the parameters are ['', 'some endpoint']


            >>> #my_query = Sparql_Query(query_file='queries//simplest.rq')
            >>> #my_query.send_query(endpoint_address="http://145.100.59.37:3500/blazegraph/sparql")
        """
        from preprocessor.string_tools import Parameter_Value
        # Required parameters cannot have the values of '' or None
        Parameter_Value.all_must_be_specified(parameters_list=[self.content, self.endpoint_address],
                                              parameter_names=['query', 'endpoint_address'])

        from SPARQLWrapper import SPARQLWrapper, JSON

        sparql_wrapper = SPARQLWrapper(self.endpoint_address)

        sparql_wrapper.setQuery(self.content)
        sparql_wrapper.setReturnFormat(JSON)

        results = sparql_wrapper.query().convert()

        results_list = []
        for each_result in results["results"]["bindings"]:
            results_list.append(each_result)

        return results_list



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
        print(self.content)