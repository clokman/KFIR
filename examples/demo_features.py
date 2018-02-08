from triplicator.bibliographyInstantiator import Bibliography
from preprocessor.string_tools import String
from preprocessor.csv_tools import CSV_Row, CSV_Line, CSV_Cell
##########################################################
################## VU & UVA BIBLIOGRAPHIES ###############
##########################################################

# import
vu_bibliography = Bibliography()
vu_bibliography.importBib('..//Input//vu//vu_5k.bib', verbose_import=True)

vu_bibliography.preview(10)
vu_bibliography.summarize()

# query
vu_bibliography.getEntriesByField('b_doi', '10.1177/1461444817724169')
vu_bibliography.getEntriesByField('b_authors', 'Werner_WG')

# RDF conversion
# --> [RUN] demo_triple_creator_vu.py <--


################# Underlying Functionality ###############
from triplicator.bibliographyInstantiator import Bibliography

# import
my_bibliography = Bibliography()
my_bibliography.importBib('demo.bib')
my_bibliography.preview()

# adding entries
my_bibliography = Bibliography()
my_bibliography.setEntry("01", "title", "A title")
my_bibliography.setEntry("02", "title", "Another title")
my_bibliography.preview()
my_bibliography.entries

# format standardization
my_formatted_bibliography = Bibliography()
my_formatted_bibliography.setFormattedEntry('01', 'this is a title ', 'pybtex_document_instance_name', 'x_document')
my_formatted_bibliography.entries
# --> demo_formatting.py <--
# --> standardizeCapitalization <--

# in progress
# vu_bibliography.index_bibid_doi_ocid
# vu_bibliography.enrich()


##########################################################
##################### OPEN CITATIONS #####################
##########################################################

# - *Preprocessor*: Versatile parsing and preprocesing library (bib<->csv<->rdf<->bib)
#   + Motivation: Simpler SPARQL queries, local processing
#   + The huge number of records expected due to long sparql output.
#   + Local processing: live parsing and merging


### SPARQL Queries:
# --> Input/open_citations/queries <--

### Preprocessor:
# - Live processing
# --> step_1c_parser_oc <--


################# Underlying Functionality ###############
from preprocessor.csv_tools import CSV_Row, CSV_Line, CSV_Cell

my_row = CSV_Line(' "a" , "b" , "c" ,').clean_from_newline_characters().\
    clean_head_and_tail_from_patterns(' ', 'head').\
    clean_head_and_tail_from_patterns(' ,', 'tail').\
    parse_line_and_CONVERT_to_CSV_Row(' , ').\
    clean_cell_heads_and_tails_from_characters('"')

print(my_row)

my_row.format_for_print_and_CONVERT_to_CSV_Line(column_separator=' , ',
                                                line_head=' ', line_tail=' ,',
                                                cell_wrapper='"')


String('-----STRING=======').clean_head_and_tail_iteratively_from_characters('-=')
String('ABC123').clip_at_index(4, remove='tail')


##########################################################
##################### OTHER FEATURES #####################
##########################################################

### CSV EXPORT ###
# A .bib to .csv export script made in order to accelerate literature review process
frederik_bibliography = Bibliography()
frederik_bibliography.importBib('..//Input//frederik//WOS_updated.bib')
frederik_bibliography.exportToCsv(output_file_path='demo.csv',
                                  columns_to_ignore=['b_document', 'b_authors', 'b_topics', 'b_journal',
                                                   'b_publication_month', 'b_issue_number', 'b_volume',
                                                   'b_pages'],
                                  new_header_names=['Type', 'Title', 'Authors', 'Topics', 'Journal', 'Year', 'DOI',
                                                    'ISSN', 'Abstract', 'Note', 'ISBN']
)

##########################################################
########################## +++ ###########################
##########################################################

# TESTS (esp. IN PREPROCESSOR)
# - Over 500

#Documentation
# - Sphinx

#Cleaner code than before
    # --> string_tools.py vs bibliographyInstantiator.py

# Error handling
# - CSV_Row(' "a", "b", "c" ,').clean_cell_heads_and_tails_from_characters('"')