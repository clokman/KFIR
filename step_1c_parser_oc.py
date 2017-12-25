from triplicator.bibliographyInstantiator import Bibliography

# OpenCitations bibliography
oc_bibliography = Bibliography()
oc_bibliography.importCsv(path_of_file_to_import='Input//oc_full.csv',
                         csv_delimiter_character=',',
                         field_value_list_separator=' | ',
                         id_column_header='referenceEntry',
                         conversion_arguments_list='open citations',
                         cleaning_algorithm='open citations',
                         verbose_import=True)
