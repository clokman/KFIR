class Test_Gastrodon(object):

    class Test_send_select_query(object):
        pass
        # def test_dbpedia_query(self):
        #     query = Gastrodon()
        #     query.set_prefixes('@prefix dbo: <http://dbpedia.org/ontology/> .')
        #     query.set_endpoint('http://dbpedia.org/sparql')
        #     result = query.send_select_query("SELECT ?s ?p ?o WHERE {?s ?p ?o .} LIMIT 2")
        #     assert result != None

    class Test_get_prefixes(object):

        def test_get_prefixes_object(self):
            import rdflib
            from retriever.sparql_tools import Gastrodon_Query

            query = Gastrodon_Query()
            query.set_prefixes("""
                @prefix dbo: <http://dbpedia.org/ontology/> .
                @prefix dbr: <http://dbpedia.org/resource/> .
            """)
            returned_prefixes = query.get_prefixes()
            assert (rdflib.term.URIRef('http://dbpedia.org/ontology/'), 'dbo') in returned_prefixes.items()
            assert (rdflib.term.URIRef('http://dbpedia.org/resource/'), 'dbr') in returned_prefixes.items()


    class Test_get_endpoint(object):

        def test_get_endpoint(self):
            from retriever.sparql_tools import Gastrodon_Query

            query = Gastrodon_Query()
            query.set_prefixes('@prefix dbo: <http://dbpedia.org/ontology/> .')
            query.set_endpoint('http://dbpedia.org/sparql')
            returned_endpoint = query.get_endpoint()
            assert returned_endpoint == 'http://dbpedia.org/sparql'


    class Test_errors(object):

        def test_prefix_cannot_be_empty_while_entering_endpoint(self):
            import pytest
            from retriever.sparql_tools import Gastrodon_Query

            query = Gastrodon_Query()
            with pytest.raises(ValueError):
                query.set_endpoint('http://dbpedia.org/sparql')

        def test_endpoint_cannot_be_empty_while_sending_query(self):
            import pytest
            from retriever.sparql_tools import Gastrodon_Query

            query = Gastrodon_Query()
            query.set_prefixes("""
                @prefix dbo: <http://dbpedia.org/ontology/> .
                @prefix dbr: <http://dbpedia.org/resource/> .
            """)

            with pytest.raises(ValueError):
                query.send_select_query("SELECT ?s ?p ?o WHERE {?s ?p ?o .} LIMIT 5")
