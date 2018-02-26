from triplicator.bibliographyInstantiator import Bibliography
from triplicator.rdfTools import Triples, RDF_File
from preprocessor.Text_File import Text_File, Log_File

log_file = Log_File('log.txt')
log_file.clear_contents()

# Patterns to clean from bib files
pattern_replacements_dictionary = {
    '<': '--',
    '>': '--',
    '\{"\}': "'",  # to replace {"} with '
    '\\\\': '--',  # to remove '\' in expressions such as '\sqrt{s}' and rogue '\'s.  unsure why '\\' does not work
    '“': "'",
    '”': "'",
    '’': "'"
    }

# ### Clean the bib file ###
# bib_file = Text_File('Input//vu_100k_feb.bib')
# # UvA_Pure_research_output-41217.bib / VU_Pure_research_output-51017.bib / vu_100k_feb.bib
# bib_file.clean_bibtex_file_and_output_cleaned_file(patterns_to_replace=pattern_replacements_dictionary,
#                                                    show_progress_bar=True)

### Parse the bib file ###
bibliography = Bibliography()
# UvA_Pure_research_output-41217_cleaned.bib / VU_Pure_research_output-51017_cleaned.bib / vu_100k_feb_cleaned.bib
bibliography.importBib('Input//vu_100k_feb_cleaned.bib', show_progress_bar=True)

### Convert to n3 format ###
triples = Triples()
triples.import_bibliography_object(bibliography, desired_source_label='vu')

### Write to .ttl file
# uva_full_v2.1.ttl / vu_full_v2.1.ttl / vu_100k_feb_v2.1.ttl
ttl_file = RDF_File('Output//vu_100k_feb_v2.1.objtest.ttl')
ttl_file.write_triples_to_file(triples)



################# UVA ####################
# print('cleaning uva bib')
# #uva_bib_file = Text_File('Input//UvA_Pure_research_output-41217.bib')
# uva_bib_file = Text_File('Input//uva_100k_feb.bib')
# uva_bib_file.clean_bibtex_file_and_output_cleaned_file(patterns_to_replace={
#     '<': '--',
#     '>': '--',
#     '\{"\}': "'",  # to replace {"} with '
#     '\\\\': '--',  # to remove '\' in expressions such as '\sqrt{s}' and rogue '\'s. unsure why '\\' does not work
#     '“': "'",
#     '”': "'",
#     '’': "'"
#     }, show_progress_bar=True)
# print('cleaned uva bib')



# print('parsing cleaned uva bib')
# uva_bibliography = Bibliography()
# #uva_bibliography.importBib('Input//UvA_Pure_research_output-41217_cleaned.bib', verbose_import=False)
# uva_bibliography.importBib('Input//uva_100k_feb_cleaned.bib', verbose_import=True)
# print('uva bib parsed')


# print('enriching vu with uva')
# bibliography.enrich(uva_bibliography, field_to_match_in_bibliographies='b_doi', method='merge')
# print('enrichment completed')



################## Simple (only VU, no-merge) version on 8 Feb 2018 ####################3

# from triplicator.bibliographyInstantiator import Bibliography
# from preprocessor.Text_File import Text_File
#
#
# bib_file = Text_File('Input//VU_Pure_research_output-51017.bib')
# bib_file.clean_bibtex_file_and_output_cleaned_file(patterns_to_replace={
#     '<': '--',
#     '>': '--',
#     '\{"\}': "'",  # to replace {"} with '
#     '\\\\': '--',    # to remove '\' in expressions such as '\sqrt{s}' unsure why '\\' does not work
#     '/': '--',
#     })
#
# bibliography = Bibliography()
# # a test bibliography that consists of many problematic entries gathered from source data
# bibliography.importBib('Input//VU_Pure_research_output-51017_cleaned.bib', verbose_import=True)
#

# December 2017 import script:
# from triplicator.bibliographyInstantiator import Bibliography
#
# # VU bibliography
# bibliography = Bibliography()
# bibliography.importBib('Input//VU_Pure_research_output-51017-edit.bib', verbose_import=True)