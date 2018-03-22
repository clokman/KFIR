"""Converts given .bib to .ttl """

from triplicator.bibTools import Bibtex_File

my_bibtex_file = Bibtex_File('Input//VU_Pure_research_output-51017.bib')
my_bibtex_file.convert_to_ttl(desired_version_suffix='v2.1_post_refactor', desired_source_bibliography_name='VU-Pure',
                              output_directory='Output')


# for testing with a smaller file:
#my_bibtex_file = Bibtex_File('Input//vu_100k_feb.bib')
#my_bibtex_file.convert_to_ttl(desired_version_suffix='v2.1_post_refactor', desired_source_bibliography_name='vu-100k-feb',
#                              output_directory='Output')
