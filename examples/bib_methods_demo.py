"""
Instructions:
 - Run line by line in the console to see examples into workings of the methods.
 - IMPORTANT: The working directory of the console must be set to project root (i.e., KFIR), otherwise the scripts will likely NOT
    work (due to file path issues)
"""

from triplicator.bibTools import Bibtex_File, Bibliography

##########################################################
############# ONE-STEP CONVERSION TO RDF #################
##########################################################

### Convert given .bib to .ttl ###

my_bibtex_file = Bibtex_File('examples//example_data//demo.bib')
my_bibtex_file.convert_to_ttl(desired_version_suffix='v0.1', desired_source_bibliography_name='UvA-Pure',
                              output_directory='Output')



##########################################################
############ INDIVIDUAL CONVERSION STEPS #################
##########################################################

# These are some of the methods used in convert_to_ttl method.

################## Clean the bib file ####################
# patterns to clean from bib files
pattern_replacements_dictionary = {
    '<': '--',
    '>': '--',
    '\{"\}': "'",  # to replace {"} with '
    '\\\\': '--',  # to remove '\' in expressions such as '\sqrt{s}' and rogue '\'s.
    '“': "'",
    '”': "'",
    '’': "'"
}
demo_bibtex_file = Bibtex_File('examples//example_data//demo.bib')
demo_bibtex_file.clean_bibtex_file_and_output_cleaned_file(patterns_to_replace=pattern_replacements_dictionary,
                                                           show_progress_bar=True)

############ Parse the bib file into memory ###############
demo_bibliography = Bibliography()
demo_bibliography.importBibtex('examples//example_data/demo_cleaned.bib', verbose_import=True)

demo_bibliography.preview(10)
demo_bibliography.summarize()

# query
demo_bibliography.getEntriesByField('b_doi', '10.1016/j.cosust.2017.08.009')
demo_bibliography.getEntriesByField('b_authors', 'Van_Belleghem_F')


############# Convert to n3 format (TTL/RDF) #################
from triplicator.rdfTools import Triples
demo_triples = Triples()
demo_triples.import_bibliography_object(demo_bibliography, desired_source_bibliography_name='PureVU')


################### Write to .ttl file ######################
from triplicator.rdfTools import RDF_File
ttl_file = RDF_File('examples//example_data/demo_output.ttl')
ttl_file.write_triples_to_file(demo_triples)


##########################################################
############ FURTHER UNDERLYING FUNCTIONALITY ############
##########################################################

# Parsing a bibtex file to memory
my_bibliography = Bibliography()
my_bibliography.importBibtex('examples//example_data/demo.bib')
my_bibliography.preview()

# Adding entries
my_bibliography = Bibliography()
my_bibliography.setEntry("01", "title", "A title")
my_bibliography.setEntry("02", "title", "Another title")
my_bibliography.preview()
my_bibliography.entries

# Format standardization
my_formatted_bibliography = Bibliography()
my_formatted_bibliography.setFormattedEntry('01', 'this is a title ', 'pybtex_document_instance_name', 'x_document')
my_formatted_bibliography.entries


# --> Also see: formatting_demo.py <--
# --> Also see: method: standardizeCapitalization <--

