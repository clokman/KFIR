from triplicator.bibliographyInstantiator import Bibliography
from preprocessor.Text_File import Text_File, Log_File
from meta.consoleOutput import ConsoleOutput

log_file = Log_File('log.txt')
log_file.clear_contents()

################# VU ####################

vu_bib_file = Text_File('Input//vu_100k_feb.bib')
#vu_bib_file = Text_File('Input//UvA_Pure_research_output-41217.bib')
#vu_bib_file = Text_File('Input//VU_Pure_research_output-51017.bib')

vu_bib_file.clean_bibtex_file_and_output_cleaned_file(patterns_to_replace={
    '<': '--',
    '>': '--',
    '\{"\}': "'",  # to replace {"} with '
    '\\\\': '--',  # to remove '\' in expressions such as '\sqrt{s}' and rogue '\'s.  unsure why '\\' does not work
    '“': "'",
    '”': "'",
    '’': "'"
    }, show_progress_bar=True)


vu_bibliography = Bibliography()
vu_bibliography.importBib('Input//vu_100k_feb_cleaned.bib', show_progress_bar=True)
#vu_bibliography.importBib('Input/UvA_Pure_research_output-41217_cleaned.bib', verbose_import=False)
#vu_bibliography.importBib('Input//VU_Pure_research_output-51017_cleaned.bib', verbose_import=False)


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
# vu_bibliography.enrich(uva_bibliography, field_to_match_in_bibliographies='b_doi', method='merge')
# print('enrichment completed')



################## Simple (only VU, no-merge) version on 8 Feb 2018 ####################3

# from triplicator.bibliographyInstantiator import Bibliography
# from preprocessor.Text_File import Text_File
#
#
# vu_bib_file = Text_File('Input//VU_Pure_research_output-51017.bib')
# vu_bib_file.clean_bibtex_file_and_output_cleaned_file(patterns_to_replace={
#     '<': '--',
#     '>': '--',
#     '\{"\}': "'",  # to replace {"} with '
#     '\\\\': '--',    # to remove '\' in expressions such as '\sqrt{s}' unsure why '\\' does not work
#     '/': '--',
#     })
#
# vu_bibliography = Bibliography()
# # a test bibliography that consists of many problematic entries gathered from source data
# vu_bibliography.importBib('Input//VU_Pure_research_output-51017_cleaned.bib', verbose_import=True)
#

# December 2017 import script:
# from triplicator.bibliographyInstantiator import Bibliography
#
# # VU bibliography
# vu_bibliography = Bibliography()
# vu_bibliography.importBib('Input//VU_Pure_research_output-51017-edit.bib', verbose_import=True)