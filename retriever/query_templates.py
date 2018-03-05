
class Query_Template():

    def get_dbpedia_entry_label(self, target_label):
        target_label = 'Example'

        query = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?label
            WHERE { <http://dbpedia.org/resource/%s> rdfs:label ?label }
        """ % target_label

        return  query


    def get_oc_article_by_doi(self, target_doi):
        """
        Examples:
            >>> my_query = Query_Template().get_oc_article_by_doi('342048723')
            >>> print(my_query[0:500])  # preview
            <BLANKLINE>
                        # v2.0
                        PREFIX cito: <http://purl.org/spar/cito/>
                        PREFIX dcterm: <http://purl.org/dc/terms/>
                        PREFIX datacite: <http://purl.org/spar/datacite/>
                        PREFIX literal: <http://www.essepuntato.it/2010/06/literalreification/>
                        PREFIX biro: <http://purl.org/spar/biro/>
                        PREFIX frbr: <http://purl.org/vocab/frbr/core#>
                        PREFIX c4o: <http://purl.org/spar/c4o/>
                        PREFIX pro: <http://purl.org/spar/pro/>
            <BLANKLINE>
        """

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

            WHERE{
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

        return query