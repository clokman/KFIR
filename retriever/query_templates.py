
class Query_Template():
    """
    Builds queries by inserting any given parameters into query templates.
    """

    def retrieve_dbpedia_entry_label(self, target_label):
        """
        Returns:
            str

        Examples:
            >>> my_query = Query_Template().retrieve_dbpedia_entry_label('Amsterdam')
            >>> print(my_query)
            <BLANKLINE>
                        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                        SELECT ?label
                        WHERE { <http://dbpedia.org/resource/Example> rdfs:label ?label }
            <BLANKLINE>

            >>> print(type(my_query))
            <class 'str'>
        """
        target_label = 'Example'

        query = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?label
            WHERE { <http://dbpedia.org/resource/%s> rdfs:label ?label }
        """ % target_label

        return query


    def retrieve_oc_articles_by_dois(self, target_dois):
        """
        Examples:
            >>> my_query = Query_Template().retrieve_oc_articles_by_dois("10.1038/modpathol.3800620")
            >>> print(my_query[0:25])        # preview
            <BLANKLINE>
                        # v2.6
            <BLANKLINE>

            >>> print(my_query[1530:1950])  # preview
             WHERE{
            <BLANKLINE>
                          VALUES ?target_doi_literal{"10.1038/modpathol.3800620" }
            <BLANKLINE>
                          # select journal articles
                          ?journal_article rdf:type fabio:JournalArticle .
                          ?journal_article datacite:hasIdentifier ?doiUri .
                          ?doiUri datacite:usesIdentifierScheme datacite:doi .
                          ?doiUri literal:hasLiteralValue ?target_doi_literal .
            <BLANKLINE>
        """
        # Make a query suitable for SPARQL expresion such as:
        # VALUES ?target_doi_literal{'10.1038/modpathol.3800620'  '10.1186/s40104-016-0099-3' }
        from preprocessor.string_tools import Parameter_Value
        target_doi_list = Parameter_Value(target_dois).convert_to_single_item_list_if_not_list()

        query_parameter = ''
        for each_doi in target_doi_list:
            query_parameter = query_parameter + '"%s" ' % each_doi

        query = """
            # v2.6
            PREFIX cito: <http://purl.org/spar/cito/>
            PREFIX dcterm: <http://purl.org/dc/terms/>
            PREFIX datacite: <http://purl.org/spar/datacite/>
            PREFIX literal: <http://www.essepuntato.it/2010/06/literalreification/>
            PREFIX biro: <http://purl.org/spar/biro/>
            PREFIX frbr: <http://purl.org/vocab/frbr/core#>
            PREFIX c4o: <http://purl.org/spar/c4o/>
            PREFIX pro: <http://purl.org/spar/pro/>
            PREFIX fabio: <http://purl.org/spar/fabio/>
            PREFIX prism: <http://prismstandard.org/namespaces/basic/2.0/>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            
            PREFIX bibResource: <https://w3id.org/oc/corpus/br/>
            PREFIX agentRole: <https://w3id.org/oc/corpus/ar/>
            PREFIX responsibleAgent: <https://w3id.org/oc/corpus/ra/>
            PREFIX id: <https://w3id.org/oc/corpus/id/>
            
            SELECT DISTINCT ?journal_article
            ?publication_type ?title ?publication_year ?journal_name ?journal_issue_number ?journal_volume_number ?publisher_name ?doi ?pmid  ?url
            (GROUP_CONCAT(DISTINCT ?author_name; SEPARATOR=" | ") AS ?authors)
            (GROUP_CONCAT(DISTINCT ?cited_the_article; SEPARATOR=" | ") AS ?cited_the_articles)
            (GROUP_CONCAT(DISTINCT ?cited_by_article; SEPARATOR=" | ") AS ?cited_by_the_articles)
            
            
            WHERE{
              
              VALUES ?target_doi_literal{%s}
              
              # select journal articles
              ?journal_article rdf:type fabio:JournalArticle .
              ?journal_article datacite:hasIdentifier ?doiUri .
              ?doiUri datacite:usesIdentifierScheme datacite:doi .
              ?doiUri literal:hasLiteralValue ?target_doi_literal .
              
            
              # Publication Type
              BIND('Article'^^xsd:string AS ?publication_type)
            
              ### Title ###
              OPTIONAL{
                ?journal_article dcterm:title ?title .
              }
            
              ### Year ###
              OPTIONAL{
                ?journal_article fabio:hasPublicationYear ?publication_year .
              }
            
              ### Author ###
              OPTIONAL{
                ?journal_article pro:isDocumentContextFor ?author_uri .
                ?author_uri pro:withRole pro:author;
                            pro:isHeldBy ?author .
                ?author foaf:givenName ?author_firstname;
                        foaf:familyName ?author_lastname .
                BIND( CONCAT( STR(?author_lastname), " - ", STR(?author_firstname) ) AS ?author_name)
              }
            
              ### Publisher ###
              OPTIONAL{
                ?journal_article pro:isDocumentContextFor ?publisher_uri .
                ?publisher_uri pro:withRole pro:publisher;
                               pro:isHeldBy ?publisher .
                ?publisher foaf:name ?publisher_name .
              }
            
              ### Journal Name, Issue Nr., Volume ###
              OPTIONAL{
                ?journal_article frbr:partOf ?journal_issue .
                ?journal_issue fabio:hasSequenceIdentifier ?journal_issue_number .
            
                ?journal_issue frbr:partOf ?journal_volume .
                ?journal_volume fabio:hasSequenceIdentifier ?journal_volume_number .
            
                ?journal_volume frbr:partOf ?journal .
                ?journal dcterm:title ?journal_name .
              }
            
              ### DOI, URL, PMID ###
              OPTIONAL{
                ?journal_article datacite:hasIdentifier ?doiUri .
                ?doiUri datacite:usesIdentifierScheme datacite:doi .
                ?doiUri literal:hasLiteralValue ?doi .
              }
            
              OPTIONAL {
                ?journal_article datacite:hasIdentifier ?pmidUri .
                ?pmidUri datacite:usesIdentifierScheme datacite:pmid .
                ?pmidUri literal:hasLiteralValue ?pmid .
              }
            
              OPTIONAL {
                ?journal_article datacite:hasIdentifier ?UrlUri .
                ?UrlUri datacite:usesIdentifierScheme datacite:url .
                ?UrlUri literal:hasLiteralValue ?url .
              }
            
              ### Cited by ###
              #?cited_by_article is the articles that cites the ?journal article
              OPTIONAL{
                ?cited_by_article cito:cites ?journal_article;
                                  rdf:type fabio:JournalArticle .
              }
            
              ### Cited ###
              OPTIONAL{ 
                ?journal_article cito:cites ?cited_the_article;
                                 rdf:type fabio:JournalArticle .
              }
            
            } # /WHERE
            
            GROUP BY ?journal_article ?publication_type ?title ?publication_year ?journal_name ?journal_issue_number ?journal_volume_number ?publisher_name ?doi ?pmid ?url 
        """ % query_parameter

        return query