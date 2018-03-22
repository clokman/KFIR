from triplicator.bibTools import Bibliography

######## Parse the csv file as a Bibliography object #########
oc_bibliography = Bibliography()
oc_bibliography.importCsv(path_of_file_to_import='Input//oc_articles_with_matching_dois_v1.3.csv',
                          csv_delimiter_character=',',
                          field_value_list_separator=' | ',
                          id_column_header='doi',
                          conversion_arguments_list='open citations',
                          cleaning_algorithm='default',
                          show_progress_bar=True)
oc_bibliography.preview(2)

############# Convert to n3 format (TTL/RDF) #################
from triplicator.rdfTools import Triples
oc_triples = Triples()
oc_triples.import_bibliography_object(oc_bibliography, desired_source_bibliography_name='OpenCitations')


################### Write to .ttl file ######################
from triplicator.rdfTools import RDF_File
oc_ttl_file = RDF_File('Output//oc_articles_with_matching_dois_v1.3.4.ttl')
oc_ttl_file.write_triples_to_file(oc_triples)
