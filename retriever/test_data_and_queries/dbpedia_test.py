from retriever.sparql_tools import Sparql_Query

target_label = 'Example'

query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?label
    WHERE { <http://dbpedia.org/resource/%s> rdfs:label ?label }
""" % target_label

print(query)

sparql = Sparql_Query()
sparql.set_endpoint('http://dbpedia.org/sparql')
sparql.set_query(query)
sparql.retrieve_results_from_endpoint(print_only=True)

