import csv
import re
from pprint import pprint
from preprocessor import *
from preprocessor.select_column import select_column
from biblio2rdf.bibliographyInstantiator import Bibliography
#### Clean  Open Citations CSV file from double quotes ###########

current_file_path = "open_citations_single_row_FULL.csv"
open_citations_raw_file = open(current_file_path, mode="r", encoding="utf8")
open_citations_raw_string = open_citations_raw_file.read()

open_citations_cleaned_string = re.sub(' ,', '_-_-_', open_citations_raw_string)
open_citations_cleaned_string = re.sub(', ', '-', open_citations_cleaned_string)
open_citations_cleaned_string = re.sub('_-_-_', ' ,', open_citations_cleaned_string)

open_citations_cleaned_string = re.sub(' "|" ', '', open_citations_cleaned_string)
#open_citations_cleaned_string = re.sub(' , ', '', open_citations_cleaned_string)

#between_quotes = False
#for i, each_character in enumerate(open_citations_cleaned_string):
#
#    if between_quotes:
#        if each_character == ",":
#            open_citations_cleaned_string[i] = "-"
#            print(open_citations_cleaned_string)
#
#    # first occurrence
#    if each_character == '\"' and not between_quotes:
#        between_quotes = True
#    elif each_character == '\"' and between_quotes:
#        between_quotes = False



#open_citations_cleaned_string = re.sub(' ', '_', open_citations_cleaned_string)
#open_citations_cleaned_string = re.sub(r'^_,', '-', open_citations_cleaned_string)
#open_citations_cleaned_string = re.sub('_', ' ', open_citations_cleaned_string)


open_citations_raw_file.close()

cleaned_file_path = "cleaned_temp.csv"
open_citations_cleaned_file = open(cleaned_file_path, mode="w", encoding="utf8")
open_citations_cleaned_file.write(open_citations_cleaned_string)
open_citations_cleaned_file.close()

################################################################

###

open_citations_import = list(csv.reader(open(cleaned_file_path, encoding="utf8"), delimiter=","))

open_citations_headers = get_headers(open_citations_import)
open_citations_data    = get_data(open_citations_import)

#print(open_citations_headers)
#column_summary('title', open_citations_import, True)

#print(select_column('title', open_citations_import))

#########

class CSV_Container():
    """

    Examples:
        my_csv_container = CSV_Container("referenceEntry", " | ")
        print(my_csv_container.entries)

        from pprint import pprint
        for each_entry_id, each_entry_data in my_csv_container.entries.items():
            print(str(each_entry_id) + ": " + str(each_entry_data))

        for each_entry_id, each_entry_data in my_csv_container.entries.items():
            print(each_entry_data['dois'])
    """

    def __init__(instance, id_column_header, joined_cell_separator_character):
        """Constructor for CSV_Container"""

        headers = get_headers(open_citations_import)
        data = get_data(open_citations_import)

        # get column number of id
        header_indexes_dictionary = {}
        for each_header in headers:
            header_indexes_dictionary[each_header] = get_header_index(each_header, open_citations_import)

        id_index = get_header_index(id_column_header, open_citations_import)

        instance.entries = {}

        for each_row in data:
            #print(each_row)
            # set id as entries key
            instance.entries[each_row[id_index]] = {}
            # and set field-value pairs as a sub-dictionary to each entry id key
            for each_header, each_header_index in header_indexes_dictionary.items():

                each_target_cell = each_row[each_header_index]
                if joined_cell_separator_character in each_target_cell:
                    each_target_cell = (each_target_cell.split(joined_cell_separator_character))
                    instance.entries[each_row[id_index]][each_header] = each_target_cell

                # if there is no aggregation in the cell
                else:
                    instance.entries[each_row[id_index]][each_header] = each_target_cell



open_citatons_csv_object =  CSV_Container(id_column_header="referenceEntry", joined_cell_separator_character=" | ")


open_citations_bibliography =  Bibliography()


conversion_arguments_list = [
      # [target_field_value in existing data,      formatting_algorithm,               desired_field_name in new object]
        ['each_entry_data["titles"]',              'pybtex_document_instance_name',       'b_document'],
        ['each_entry_data["titles"]',              'pybtex_document_label',               'b_document_label'],
        ['each_entry_data["dois"]',                'open_citations_list_minimizer',       'b_doi'],
        ['each_entry_data["authors"]',             'open_citations_author_instance_name', 'b_authors'],
        ['each_entry_data["authors"]',             'open_citations_author_label',         'b_author_labels'],
        ['each_entry_data["publications"]',        'pybtex_document_instance_name',       'b_publication'],
        ['each_entry_data["publications"]',        'pybtex_document_label',               'b_publication_label'],
        ['each_entry_data["publication_types"]',   'open_citations_list_minimizer_2',     'b_publication_type'],
        ['each_entry_data["types"]',               'open_citations_list_minimizer_2',     'b_type'],
        ['each_entry_data["years"]',               'open_citations_list_minimizer',       'b_publication_year'],
        ['each_entry_data["publishers"]',          'pybtex_document_instance_name',       'b_publisher'],
        ['each_entry_data["publishers"]',          'pybtex_document_label',               'b_publisher_label']
    ]

    # loop through individual reference entries in the parsed pybtex bib file
for each_entry_id, each_entry_data in open_citatons_csv_object.entries.items():
    # loop through each line in the conversion_arguments_list
    for each_argument_list in conversion_arguments_list:
        # try using the elements of each sub-list in conversion_arguments_list as arguments of .setFormattedEntry method
        # (try-except block is necessary, as each field may not exist for each entry)
        try:
            open_citations_bibliography.setFormattedEntry(each_entry_id, eval(each_argument_list[0]), each_argument_list[1], each_argument_list[2])
        except:
            # TODO: Restore this line (replace it with general except statement)
            # except KeyError:
            pass

#print(open_citations_bibliography.entries)


from step_1_bibtex_parser import pure_bibliography

#combined_bibliography = pure_bibliography.enrich(open_citations_bibliography, "b_doi")