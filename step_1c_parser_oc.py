from preprocessor.csv_tools import CSV_File
from triplicator.bibliographyInstantiator import Bibliography


input_file_name_without_extension = 'oc_1.1_yasgui__2500'
input_file_path  = 'C://Users//Clokman//Google Drive//__Projects__//Code//KFIR//Input//open_citations//' + input_file_name_without_extension + '.csv'
merged_file_path = 'C://Users//Clokman//Google Drive//__Projects__//Code//KFIR//Input//open_citations//' + input_file_name_without_extension + '_rows_merged.csv'

# clean, merge multi-row entries, and write to file
oc_csv = CSV_File(input_file_path, column_delimiter_pattern_in_input_file =' , ')

oc_csv.set_cleaning_and_parsing_parameters(line_head_pattern_to_remove=' ', line_tail_pattern_to_remove=' ,',
                                           cell_head_and_tail_characters_to_remove='"')

oc_csv.set_output_formatting_parameters(column_separator='same as input', cell_value_separator=' | ',
                                        line_head=' ', line_tail=' ,',
                                        cell_wrapper='"')

oc_csv.live_clean_and_row_merge(1)


## parse the csv as a bib item
oc_bibliography = Bibliography()
oc_bibliography.importCsv(path_of_file_to_import=merged_file_path,
                         csv_delimiter_character=',',
                         field_value_list_separator=' | ',
                         id_column_header='journal_article',
                         conversion_arguments_list='open citations with citations',
                         cleaning_algorithm='open citations',
                         verbose_import=True)

oc_bibliography.preview(5)


# py query -- how to authenticate connection to the server through python?
vu_bib = Bibliography()
vu_bib.importBib('vu_1k.bib')

oc_bibliography.enrich('vu_1k.bib')




