"""Converts given .bib to .ttl """

from triplicator.bibTools import Bibtex_File

my_bibtex_file = Bibtex_File('Input//VU_Pure_research_output-51017.bib')
my_bibtex_file.convert_to_ttl(desired_version='v2.1_post_refactor', desired_source_bibliography_name='VU-Pure',
                              output_directory='Output')
