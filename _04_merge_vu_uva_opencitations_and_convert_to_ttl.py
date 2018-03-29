from triplicator.bibTools import Bibliography
from triplicator.rdfTools import Triples, RDF_File
from meta.consoleOutput import ConsoleOutput

console = ConsoleOutput('log.txt')
console.clear_log_file()

# Uncomment if needed for diagnostic comparison purposes of the original and final data after the operation
# console.log_message('Starting to import VU Pure data to "vu_bibliography" Bibliography object')
# vu_bibliography = Bibliography()
# vu_bibliography.importBibtex('Input//VU_Pure_research_output-51017_cleaned.bib', show_progress_bar=True)  # PATH
# console.log_message('Success: VU Pure data imported to "vu_bibliography" Bibliography object')


console.log_message('Starting to import UvA Pure data to "uva_bibliography" Bibliography object')
uva_bibliography = Bibliography()
uva_bibliography.importBibtex('Input//UvA_Pure_research_output-41217_cleaned.bib', show_progress_bar=True)  # PATH
console.log_message('Success: UvA Pure data imported to "uva_bibliography" Bibliography object')


console.log_message('Starting to import OpenCitations data to "oc_bibliography" Bibliography object')
oc_bibliography = Bibliography()
oc_bibliography.importCsv(path_of_file_to_import='Input//oc_articles_with_matching_dois_v1.3.csv',  # PATH
                          csv_delimiter_character=',',
                          field_value_list_separator=' | ',
                          id_column_header='doi',
                          conversion_arguments_list='open citations',
                          cleaning_algorithm='default',
                          show_progress_bar=True)
console.log_message('Success: OpenCitations data imported to "oc_bibliography" Bibliography object')

console.log_message('Starting to initiate "enriched_bibliography" with VU Bibliography object')
enriched_bibliography = Bibliography()
# Initiates as the same with vu_bibliography... The previously created vu_bibliography variable is kept untouched
# (if not commented out above)in order to make post-operation comparisons between the original and the final data
# possible, in case they would be needed for diagnostic purposes
enriched_bibliography.importBibtex('Input//VU_Pure_research_output-51017_cleaned.bib', show_progress_bar=True)  # PATH
console.log_message('"Success: enriched_bibliography" initiated with VU Bibliography object')

console.log_message('Starting to merge "enriched_bibliography" with UvA Bibliography object')
enriched_bibliography.enrich_with(uva_bibliography,
                            field_to_match_in_bibliographies='b_doi',
                            method='merge')
console.log_message('Success: "enriched_bibliography" merged with UvA Bibliography object')

console.log_message('Starting to enrich "enriched_bibliography" with OpenCitations Bibliography object')
enriched_bibliography.enrich_with(oc_bibliography,
                            field_to_match_in_bibliographies='b_doi',
                            method='left join')
console.log_message('Success: "enriched_bibliography" enriched with OpenCitations Bibliography object')

# TODO: Turn n3 transformation and ttl writing steps to a single 'write_to_ttl' method for Bibliography (e.g., vu_bibliography.write_to_ttl())
# TODO: Source bibliography name for individual bibliographies inside must be preserved by allowing specification during parsing to Bibliography object and not during ttl conversion. (currently only one can be specified during ttl conversion)
### Convert to n3 format ###
console.log_message('Starting to convert "enriched_bibliography" to Triples object')
merged_triples = Triples()
merged_triples.import_bibliography_object(enriched_bibliography,
                                          desired_source_bibliography_name='vu_and_uva_enriched_with_opencitations',
                                          show_progress_bar=True)
console.log_message('Success: "enriched_bibliography" converted to Triples object')

### Write to ttl file ###
console.log_message('Starting to write the triples Object to .ttl')
ttl_file = RDF_File('Output//vu_and_uva_merged_and_enriched_with_opencitations_v0.3.ttl')  # PATH
ttl_file.write_triples_to_file(merged_triples, show_progress_bar=True)
console.log_message('Success: Triples Object written to .ttl file')
