from triplicator.bibliographyInstantiator import Bibliography
from preprocessor.Text_File import Text_File


vu_bib_file = Text_File('Input//VU_Pure_research_output-51017-edit.bib')
vu_bib_file.clean_bibtex_file_and_output_cleaned_file(patterns_to_replace={
    '<': '--',
    '>': '--',
    '\{"\}': "'",  # to replace {"} with '
    '\\\\': '--',    # to remove '\' in expressions such as '\sqrt{s}' unsure why '\\' does not work
    '/': '--',
    })

uva_bib_file = Text_File('Input//UvA_Pure_research_output-41217-edit.bib')
uva_bib_file.clean_bibtex_file_and_output_cleaned_file(patterns_to_replace={
    '<': '--',
    '>': '--',
    '\{"\}': "'",  # to replace {"} with '
    '\\\\': '--',    # to remove '\' in expressions such as '\sqrt{s}' unsure why '\\' does not work
    '/': '--',
    })

vu_bibliography = Bibliography()
vu_bibliography.importBib('Input//VU_Pure_research_output-51017-edit_cleaned.bib', verbose_import=False)

uva_bibliography = Bibliography()
uva_bibliography.importBib('Input//UvA_Pure_research_output-41217-edit_cleaned.bib', verbose_import=False)

vu_bibliography.enrich(uva_bibliography, field_to_match_in_bibliographies='b_doi', method='merge')


# Simple (only VU, no-merge) version on 8 Feb 2018:
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