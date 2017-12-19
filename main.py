from triplicator.bibliographyInstantiator import Bibliography

vu_bibliography = Bibliography()
vu_bibliography.importBib('Input//vu_100k.bib')
#vu_bibliography.importBib('Input//problematic_characters_test.bib')


#uva_bibliography = Bibliography()
#uva_bibliography.importBib('Input//uva_1k.bib', verbose_import=True)

#oc_bibliography = Bibliography()
#oc_bibliography.importCsv(path_of_file_to_import='Input//oc_100.csv',
#                          csv_delimiter_character=',',
#                          field_value_list_separator=' | ',
#                          id_column_header='referenceEntry',
#                          conversion_arguments_list='open citations',
#                          cleaning_algorithm='open citations',
#                          verbose_import=False)

