from triplicator.bibTools import Bibtex_File

my_bibtex_file = Bibtex_File('Input//vu_100k_feb.bib')
my_bibtex_file.convert_to_ttl(desired_version_suffix='v2.1_post_refactor', desired_source_bibliography_name='vu-100k-feb',
                              output_directory='Output')
