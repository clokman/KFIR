from triplicator.bibTools import Bibtex_File

my_bibtex_file = Bibtex_File('Input//vu_100k_feb.bib')
my_bibtex_file.convert_to_ttl(desired_version='2.1-objtest2', desired_source_label='vu')
