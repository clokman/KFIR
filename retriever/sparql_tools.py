from preprocessor.Text_File import Text_File

class Sparql_Query(Text_File):

    def __init__(self, input_file_path, endpoint_address):
        Text_File.__init__(self, input_file_path)

        self.query = self.return_content()
        self.endpoint_address = endpoint_address

    def run_query(self):
        """
        Examples:
            >>> my_query = Sparql_Query(input_file_path='test_data//simple_dbpedia_test.rq',
            ...                         endpoint_address="http://dbpedia.org/sparql")
            >>> my_query.run_query()
            أمثلة (توضيح)
            Example
            Example (Begriffsklärung)
            Example
        """
        from SPARQLWrapper import SPARQLWrapper, JSON

        sparql = SPARQLWrapper(self.endpoint_address)

        query = """
            %s
        """ % self.query

        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
            print(result["label"]["value"])
