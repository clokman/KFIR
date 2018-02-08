from preprocessor.csv_tools import CSV_File
ttl_file = CSV_File('Output//uva_1.11-1K.ttl', column_delimiter_pattern_in_input_file='> <')
ttl_file.preview()

ttl_file.set_cleaning_and_parsing_parameters(line_tail_pattern_to_remove=' .', cell_head_and_tail_characters_to_remove='<>')

ttl_file.set_output_formatting_parameters(line_tail=' .', cell_wrapper='')


ttl_file.clean_ttl_uri_strings()