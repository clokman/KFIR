from triplicator.bibTools import Bibtex_File

my_bibtex_file = Bibtex_File('Input//vu_100k_feb.bib')
my_bibtex_file.convert_to_ttl(desired_version='2.1_post_refactor', desired_source_bibliography_name='vu-100k-feb',
                              output_directory='Output')
