"""Converts given .bib to .ttl """

from triplicator.bibTools import Bibtex_File

my_bibtex_file = Bibtex_File('Input//finn_aron//publications_finn_aron.bib')
my_bibtex_file.convert_to_ttl(desired_version='v2.1_post_refactor', desired_source_bibliography_name='VU-Finn')