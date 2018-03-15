"""
Instructions:
 - Run line by line in the console to see examples into workings of the methods.
 - IMPORTANT: The working directory of the console must be set to project root (i.e., KFIR), otherwise the scripts will likely NOT
    work (due to file path issues)
"""

from retriever.sparql_tools import Open_Citations_Query, DOI_String
from meta.consoleOutput import ConsoleOutput
from preprocessor.string_tools import String

########################################################
############ OPEN CITATIONS DEMO QUERY #################
########################################################

console = ConsoleOutput('log.txt')

# Read DOIs from a file
doi_list = []
with open('examples//example_data//doi_list_100.csv', encoding='utf8') as doi_file:
    for each_line in doi_file:
        each_line = String(each_line)
        each_line.clean_from_newline_characters()
        doi_list.append(str(each_line))

# Send query and write it to file
oc_query = Open_Citations_Query()
oc_query.retrieve_articles_by_dois(doi_list, show_progress_bar=True)
oc_query.write_results_to_csv('retrieved_oc_articles_with_matching_dois_test_100.csv')


#######################################################
############ UNDERLYING FUNCTIONALITY #################
#######################################################

############### DOI MANIPULATION ######################

# Generate alternative versions of a DOI
my_doi = DOI_String('10.1136/bmjgh-2016-000109')
my_doi.generate_alternative_versions_if_doi()

# Extract core doi, and create alternatives
my_doi = DOI_String('https://doi.org/10.1016/j.scico.2016.04.001')
my_doi.reduce_to_kernel()
my_doi.generate_alternative_versions_if_doi()

# Non-DOI input (nothing should happen except returning the input)
my_doi = DOI_String('http://www.socialevraagstukken.nl/veiligheid-creeer-je-met-geborgenheid/')
my_doi.reduce_to_kernel()
my_doi.generate_alternative_versions_if_doi()

# parse list from file (probably exists in ListData)
from retriever.sparql_tools import Open_Citations_Query
from meta.consoleOutput import ConsoleOutput
from preprocessor.string_tools import String


