"""Converts given .bib to .ttl """

from triplicator.bibTools import Bibtex_File

my_bibtex_file = Bibtex_File('Input//UvA_Pure_research_output-41217.bib')
my_bibtex_file.convert_to_ttl(desired_version_suffix='v0.1', desired_source_bibliography_name='UvA-Pure',
                              output_directory='Output')
