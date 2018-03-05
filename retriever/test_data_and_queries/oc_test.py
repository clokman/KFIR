from retriever.sparql_tools import Sparql_Query

target_doi = '10.1186/s13034-015-0062-7'

query = """
    # v2.0
        
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
    ?title ?publication_year ?journal_name ?journal_issue_number ?journal_volume_number ?startEndPages ?publisher_name ?doi ?pmid  ?url
        (GROUP_CONCAT(DISTINCT ?author_name; SEPARATOR=" | ") AS ?authors)
        (GROUP_CONCAT(DISTINCT ?cited_the_article; SEPARATOR=" | ") AS ?cited_the_articles)
        (GROUP_CONCAT(DISTINCT ?cited_by_article; SEPARATOR=" | ") AS ?cited_by_the_articles)
    
        # The output names are in a different format than the camelCase, because they are intended for a Python script where underscore naming is the convention.
    
    WHERE{
      # This script queries fabio:JournalArticle
      # Example fabio:JournalArticle: http://opencitations.net/corpus/br/721330.html
      # It excludes other types, such as fabio:ReferenceEntry
      # Example fabio:ReferenceEntry: https://w3id.org/oc/corpus/br/9901
    
        # select journal articles
        ?journal_article rdf:type fabio:JournalArticle .
        ?journal_article datacite:hasIdentifier ?doiUri .
        ?doiUri datacite:usesIdentifierScheme datacite:doi .
        ?doiUri literal:hasLiteralValue '%s' .
        
        # Publication Type
        BIND( STR('Journal Article') AS ?publication_type)
    
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
    
        ### Start and End Page ###
        OPTIONAL{
            ?journal_article frbr:embodiment ?pageInfoBlankNode .
            ?pageInfoBlankNode prism:endingPage ?endingPage ;
                               prism:startingPage ?startingPage .
            BIND(
                IF (
                    EXISTS {?pageInfoBlankNode prism:startingPage ?startingPage} && EXISTS {?pageInfoBlankNode prism:endingPage ?endingPage},
                    CONCAT( STR(?startingPage), "--", STR(?endingPage) ),
                    IF (
                        EXISTS {?pageInfoBlankNode prism:startingPage ?startingPage} && NOT EXISTS {?pageInfoBlankNode prism:endingPage ?endingPage},
                        STR(?startingPage),
                        IF (
                            NOT EXISTS {?pageInfoBlankNode prism:startingPage ?startingPage} && EXISTS {?pageInfoBlankNode prism:endingPage ?endingPage},
                            STR(?endingPage),
                            ""
                        )#/IF
                    )#/IF
                ) #/IF
          
                AS ?startEndPages
            ) #/BIND
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
    
    GROUP BY ?journal_article ?title ?publication_year ?journal_name ?journal_issue_number ?journal_volume_number ?startEndPages ?publisher_name ?doi ?pmid ?url
    
    LIMIT 10 
""" % target_doi

sparql = Sparql_Query(input_query=query)
print('query is: ', sparql.query)
results = sparql.retrieve_results_from_endpoint(endpoint_address='http://opencitations.net/sparql', print_only=True)

print('\nDOI of first result:')
print(results[1]['doi'])

print('\nFirst result:')
print(results[1])


