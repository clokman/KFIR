"""
Instructions:
 - Run line by line in the console to see examples into workings of the methods.
 - IMPORTANT: The working directory of the console must be set to project root (i.e., KFIR), otherwise the scripts will likely NOT
    work (due to file path issues)
"""

from triplicator.bibTools import Bibliography
from preprocessor.csv_tools import CSV_File, CSV_Line
from preprocessor.string_tools import String

###############################################################
#################### CLEANING AND PARSING #####################
###############################################################

# clean, merge multi-row entries, and write to file
oc_csv = CSV_File('examples//example_data//yasgui_formatted_100_rows.csv',
                  column_delimiter_pattern_in_input_file =' , ')

oc_csv.set_parsing_and_cleaning_parameters(line_head_pattern_to_remove=' ', line_tail_pattern_to_remove=' ,',
                                           cell_head_and_tail_characters_to_remove='"')

oc_csv.set_output_formatting_parameters(column_separator='same as input', cell_value_separator=' | ',
                                        line_head=' ', line_tail=' ,',
                                        cell_wrapper='"')

# Optional Step: Merging rows
# merge lines if they share the same id (i.e., if each entry occupies more than one row in the csv file,
# then merge this to one row)
oc_csv.live_clean_and_row_merge(index_position_of_id_column=1)


## parse the csv as a bib item
oc_bibliography = Bibliography()
oc_bibliography.importCsv(path_of_file_to_import='examples//example_data//yasgui_formatted_10_rows_rows_merged.csv',
                          csv_delimiter_character=',',
                          field_value_list_separator=' | ',
                          id_column_header='journal_article',
                          conversion_arguments_list='open citations',
                          cleaning_algorithm='default',
                          show_progress_bar=True)

oc_bibliography.preview(5)


###############################################################
################# UNDERLYING FUNCTIONALITY ####################
###############################################################

my_row = CSV_Line(' "a" , "b" , "c" ,').clean_from_newline_characters().\
    clean_head_and_tail_from_patterns(' ', 'head').\
    clean_head_and_tail_from_patterns(' ,', 'tail').\
    parse_line_and_CONVERT_to_CSV_Row(' , ').\
    clean_cell_heads_and_tails_from_characters('"')  # usage of chain methods/fluid interface is optional

print(my_row)

my_row.format_for_print_and_CONVERT_to_CSV_Line(column_separator=' , ',
                                                line_head=' ', line_tail=' ,',
                                                cell_wrapper='"')


String('-----STRING=======').clean_head_and_tail_iteratively_from_characters('-=')
String('ABC123').clip_at_index(4, remove='tail')


##########################################################
####################### CSV EXPORT #######################
##########################################################

demo_bibliography = Bibliography()
demo_bibliography.importBibtex('examples/example_data/IDR_Literature_WOS.bib')
demo_bibliography.exportToCsv(output_file_path='examples//example_data//demo_output.csv',
                              columns_to_ignore=['b_document', 'b_authors', 'b_topics', 'b_journal',
                                                'b_publication_month', 'b_issue_number', 'b_volume',
                                                'b_pages', 'b_pure_bibliography_id'],
                              new_header_names=['Type', 'Title', 'Authors', 'Topics', 'Journal', 'Year', 'DOI',
                                                'ISSN', 'Abstract', 'Note', 'ISBN'])