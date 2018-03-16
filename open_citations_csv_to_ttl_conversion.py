from triplicator.bibTools import Bibliography


# clean, merge multi-row entries, and write to file
#oc_csv = CSV_File(input_file_path, column_delimiter_pattern_in_input_file =' , ')

#oc_csv.set_parsing_and_cleaning_parameters(line_head_pattern_to_remove='', line_tail_pattern_to_remove=' ,',
#                                           cell_head_and_tail_characters_to_remove='"')

#oc_csv.set_output_formatting_parameters(column_separator='same as input', cell_value_separator=' | ',
#                                        line_head=' ', line_tail=' ,',
#                                        cell_wrapper='"')

#oc_csv.live_clean_and_row_merge(0)


######## Parse the csv file as a Bibliography object #########
oc_bibliography = Bibliography()
oc_bibliography.importCsv(path_of_file_to_import='Input//oc_articles_with_matching_dois_v1.2.csv',
                          csv_delimiter_character=',',
                          field_value_list_separator=' | ',
                          id_column_header='doi',
                          conversion_arguments_list='open citations',
                          cleaning_algorithm='open citations',
                          show_progress_bar=True)
oc_bibliography.preview(2)

############# Convert to n3 format (TTL/RDF) #################
from triplicator.rdfTools import Triples
oc_triples = Triples()
oc_triples.import_bibliography_object(oc_bibliography, desired_source_bibliography_name='OpenCitations')


################### Write to .ttl file ######################
from triplicator.rdfTools import RDF_File
oc_ttl_file = RDF_File('Output//oc_articles_with_matching_dois_v1.2.ttl')
oc_ttl_file.write_triples_to_file(oc_triples)




