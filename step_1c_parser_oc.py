from preprocessor.csv_tools import CSV_File
from triplicator.bibliographyInstantiator import Bibliography

# oc_csv = CSV_File('Input//open_citations//oc_yasgui_10k.csv',
#                   column_delimiter_pattern_in_input_file= ' , ',
#                   desired_cell_value_delimiter_pattern=' | ')

# oc_csv.live_clean_and_merge(1,
#                             clean_line_tails_from_pattern=' ,',
#                             clean_cell_heads_and_tails_from_characters='"'
#                             )

# clean, merge multi-row entries, and write to file
oc_csv = CSV_File('Input//open_citations//oc_10k_yasgui_with_citations.csv',
                  column_delimiter_pattern_in_input_file= ' , ',
                  desired_cell_value_delimiter_pattern=' | ')
oc_csv.live_clean_and_merge(id_column_index=1,
                            clean_line_tails_from_pattern=' ,',
                            clean_cell_heads_and_tails_from_characters='"'
                            )

#
# # parse the csv as a bib item
# oc_bibliography = Bibliography()
# oc_bibliography.importCsv(path_of_file_to_import='Input//open_citations//oc_10k_yasgui_with_citations_rows_merged.csv',
#                          csv_delimiter_character=',',
#                          field_value_list_separator=' | ',
#                          id_column_header='journal_article',
#                          conversion_arguments_list='open citations',
#                          cleaning_algorithm='open citations',
#                          verbose_import=True)
