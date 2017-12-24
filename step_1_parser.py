from triplicator.bibliographyInstantiator import Bibliography

# VU bibliography
vu_bibliography = Bibliography()
vu_bibliography.importBib('Input//VU_Pure_research_output-51017-edit.bib')
#vu_bibliography.importBib('Input//problematic_characters_test.bib')

# # UvA bibliography
# uva_bibliography = Bibliography()
# uva_bibliography.importBib('Input//UvA_Pure_research output-41217-edit.bib', verbose_import=True)

# # OpenCitations bibliography
# oc_bibliography = Bibliography()
# oc_bibliography.importCsv(path_of_file_to_import='Input//oc_100.csv',
#                          csv_delimiter_character=',',
#                          field_value_list_separator=' | ',
#                          id_column_header='referenceEntry',
#                          conversion_arguments_list='open citations',
#                          cleaning_algorithm='open citations',
#                          verbose_import=False)

# # Finn and Aron bibliography
# fa_bibliography = Bibliography()
# fa_bibliography.importBib('Input//finn_aron//publications_finn_aron_edit.bib')

