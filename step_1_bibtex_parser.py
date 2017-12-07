# TODO: Database enrichment (see frederik's article at 'Diigo to read', see Ali meetings & Skype links)
# TODO: Check citations in "Pybtex_import("biblio2rdf//test.bib").data.citations" (by using another bib file)
# TODO: Testing for all keyword capitalization scenarios for formatValues function
# TODO: Adding citations and references (see: http://145.100.59.37:3500/blazegraph/#explore:kb:bibResource:15088)

# DONE: Documentation
# DONE: Tests
# DONE: Further name standardization: Lowercase and uppercase letters should be matched across instance names (e.g., usage of 'and' or 'And') should be consistent
# DONE: Standardization. Different author name inputs now author output name in a uniform format. (Now, all first names are abbreviated).
#   (e.g., ["Van Belleghem, Frank", "Mendoza Rodriguez J.P."] are now formatted as
#          ["Van_Belleghem_F", "Mendoza_Rodriguez_JP"])
#   was:
#       ['Lohr_Ansje', 'Beunen_R', 'Savelli_Heidi', 'Kalz_Marco', 'Ragas_Ad', 'VanBelleghem_Frank']
#       ['Lohr, Ansje', 'Beunen, R', 'Savelli, Heidi', 'Kalz, Marco', 'Ragas, Ad', 'VanBelleghem, Frank']
#       ['MendozaRodriguez_JP', 'Wielhouwer_JL', 'Kirchler_Erich']
#       ['MendozaRodriguez, JP', 'Wielhouwer, JL', 'Kirchler, Erich']
#   now:
#       ['Lohr_A', 'Beunen_R', 'Savelli_H', 'Kalz_M', 'Ragas_A', 'Van_Belleghem_F']
#       ['Lohr, A', 'Beunen, R', 'Savelli, H', 'Kalz, M', 'Ragas, A', 'Van_Belleghem, F']
#       ['Mendoza_Rodriguez_JP', 'Wielhouwer_JL', 'Kirchler_E']
#       ['Mendoza_Rodriguez, JP', 'Wielhouwer, JL', 'Kirchler, E']
# DONE: Add (to instance._field_registry) stats to measure how many DOIs etc exists in the bibliography
# DONE: Change "publication"  to "journal"
# DONE: Add labels
# DONE: Multi-author support
# DONE: Object oriented refactoring
# DONE: Conversion to Python 3
# DONE: Dealing with unicode characters

# For compatibility with Python 3.x, if ran under 2.x
from __future__ import print_function

import re
from builtins import KeyError
from pprint import pprint
from biblio2rdf.pybtexImporter import Pybtex_import
from biblio2rdf.bibliographyInstantiator import Bibliography
from biblio2rdf.bibliographyInstantiator import formatValues

# import input data
pybtex_import_instance = Pybtex_import("Input//pure_bib_head_100K.bib")
pybtex_data = pybtex_import_instance.data
print("External .bib file imported into the input variable: '.pybtex_data'.")

# instantiate and assign the output object (which will be populated later)
pure_bibliography = Bibliography()
print("An output object is instantiated as the 'pure_bibliography' object.")


########################################################################
#  Transfer items from pybtex parsed dictionary to output dictionary   #
########################################################################

# In order to shorten the code, a list of arguments is given below, and then passed to the .setFormattedEntry method
# ... through a for loop. In the list, each line is a (sub-)list of three arguments to be passed.

# # Without the use of this shortening procedure, a function for each field should be written in try-except blocks
# # ... as following:
# for each_pybtex_entry_id, each_pybtex_entry in pybtex_data.entries.items():
#     # try-except blocks are necessary for use in for loops, as specified field may not always be present in an entry
#     try:
#         pure_bibliography.setFormattedEntry(each_pybtex_entry_id, each_pybtex_entry.fields['title'],
#                                             'pybtex_document_instance_name', 'b_document')
#     except:
#         pass

conversion_arguments_list = [
      # [target_field_value in existing data,      formatting_algorithm,               desired_field_name in new object]
        ['each_pybtex_entry.type',                'none',                             'b_type'],
        ['each_pybtex_entry.fields["title"]',     'pybtex_document_instance_name',    'b_document'],
        ['each_pybtex_entry.fields["title"]',     'pybtex_document_label',            'b_document_label'],
        ['each_pybtex_entry.persons["author"]',   'pybtex_author_instance_name',      'b_authors'],
        ['each_pybtex_entry.persons["author"]',   'pybtex_author_label',              'b_author_labels'],
        ['each_pybtex_entry.fields["keywords"]',  'pybtex_topic_instance_name',       'b_topics'],
        ['each_pybtex_entry.fields["keywords"]',  'pybtex_topic_label',               'b_topic_labels'],
        ['each_pybtex_entry.fields["journal"]',   'pybtex_document_instance_name',    'b_journal'],
        ['each_pybtex_entry.fields["journal"]',   'pybtex_document_label',            'b_journal_label'],
        ['each_pybtex_entry.fields["booktitle"]', 'pybtex_document_instance_name',    'b_parent_book'],
        ['each_pybtex_entry.fields["booktitle"]', 'pybtex_document_label',            'b_parent_book_label'],
        ['each_pybtex_entry.fields["publisher"]', 'pybtex_document_instance_name',    'b_publisher'],
        ['each_pybtex_entry.fields["publisher"]', 'pybtex_document_label',            'b_publisher_label'],
        ['each_pybtex_entry.fields["year"]',      'none',                             'b_publication_year'],
        ['each_pybtex_entry.fields["month"]',     'none',                             'b_publication_month'],
        ['each_pybtex_entry.fields["number"]',    'none',                             'b_issue_number'],
        ['each_pybtex_entry.fields["volume"]',    'none',                             'b_volume'],
        ['each_pybtex_entry.fields["pages"]',     'none',                             'b_pages'],
        ['each_pybtex_entry.fields["doi"]',       'none',                             'b_doi'],
        ['each_pybtex_entry.fields["issn"]',      'none',                             'b_issn'],
        ['each_pybtex_entry.fields["isbn"]',      'none',                             'b_isbn'],
        ['each_pybtex_entry.fields["edition"]',   'none',                             'b_edition'],
        ['each_pybtex_entry.fields["abstract"]',  'none',                             'b_abstract'],
        ['each_pybtex_entry.fields["note"]',      'none',                             'b_note']
    ]

# loop through individual reference entries in the parsed pybtex bib file
for each_pybtex_entry_id, each_pybtex_entry in pybtex_data.entries.items():
    # loop through each line in the conversion_arguments_list
    for each_argument_list in conversion_arguments_list:
        # try using the elements of each sub-list in conversion_arguments_list as arguments of .setFormattedEntry method
        # (try-except block is necessary, as each field may not exist for each entry)
        try:
            pure_bibliography.setFormattedEntry(each_pybtex_entry_id, eval(each_argument_list[0]), each_argument_list[1], each_argument_list[2])
        except KeyError:
            pass


    ########################################################################

# SERIES_TITLE AND ID -- To be implemented if needed
# This has to be kept out of the main loop, as series is not a field, but a whole bibliography entry themselves.
# They are not nested within individual entries, and are rather parallel to them.
# Some older code from previous versions, which extracts and converts series title:
#try:
#    # collection refers to a full reference entity, and this is why the title of the collection is nested quite deeper than other elements parsed before in this script
#    for series_id in pybtex_data.entries[each_pybtex_entry_id].collection.entries:
#        print series_id, each_pybtex_entry_id
#        #bibDictionary[each_pybtex_entry_id].append({"is_part_of_series_with_title":[each_pybtex_entry_id].fields["title"].encode("ascii",errors="ignore")
#        bibDictionary[each_pybtex_entry_id].append({"is_part_of_series_with_id":series_id})
#        #[each_pybtex_entry_id].fields["title"].encode("ascii",errors="ignore")
## field missing from bibliography
#except(KeyError):
#    pass


#######################
#  PRINT PROCEDURES   #
#######################

pprint(pure_bibliography.entries)

print("\nFields added added to bibliography:")
pprint(pure_bibliography._field_type_registry)


