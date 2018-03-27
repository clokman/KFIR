import os
os.chdir('..')  # to be able to run file from both server environment and through 'Run' dialog in IDE
from triplicator.bibTools import Bibliography
from triplicator.rdfTools import Triples, RDF_File
from meta.consoleOutput import ConsoleOutput

console = ConsoleOutput('log.txt')
console.clear_log_file()

vu_bibliography = Bibliography()
vu_bibliography.importBibtex('acceptance_tests//test_data//VU_Pure_research_output-51017_cleaned_10k.bib', show_progress_bar=True) # PATH

uva_bibliography = Bibliography()
uva_bibliography.importBibtex('acceptance_tests//test_data//UvA_Pure_research_output-41217_cleaned_10k.bib', show_progress_bar=True) # PATH


oc_bibliography = Bibliography()
oc_bibliography.importCsv(path_of_file_to_import='acceptance_tests//test_data//oc_articles_with_matching_dois_v1.3.csv', # PATH
                          csv_delimiter_character=',',
                          field_value_list_separator=' | ',
                          id_column_header='doi',
                          conversion_arguments_list='open citations',
                          cleaning_algorithm='default',
                          show_progress_bar=True)

vu_bibliography.enrich_with(uva_bibliography,
                            field_to_match_in_bibliographies='b_doi',
                            method='merge')
console.log_message('VU bibtex file enriched with UvA bibtex file')

vu_bibliography.enrich_with(oc_bibliography,
                            field_to_match_in_bibliographies='b_doi',
                            method='left join')
console.log_message('VU bibtex file enriched with OpenCitations bibtex file')

# TODO: Turn n3 transformation and ttl writing steps to a single 'write_to_ttl' method for Bibliography (e.g., vu_bibliography.write_to_ttl())
# TODO: Source bibliography name for individual bibliographies inside must be preserved by allowing specification during parsing to Bibliography object and not during ttl conversion. (currently only one can be specified during ttl conversion)
### Convert to n3 format ###
merged_triples = Triples()
merged_triples.import_bibliography_object(vu_bibliography,
                                          desired_source_bibliography_name='vu_and_uva_enriched_with_opencitations',
                                          show_progress_bar=True)

### Write to ttl file ###
ttl_file = RDF_File('acceptance_tests//test_data//output//vu_and_uva_merged_and_enriched_with_opencitations_v0.4_10k.ttl')  # PATH
ttl_file.write_triples_to_file(merged_triples, show_progress_bar=True)

