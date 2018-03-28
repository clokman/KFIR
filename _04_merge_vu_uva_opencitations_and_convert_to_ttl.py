from triplicator.bibTools import Bibliography
from triplicator.rdfTools import Triples, RDF_File

vu_bibliography = Bibliography()
vu_bibliography.importBibtex('Input//VU_Pure_research_output-51017_cleaned.bib', show_progress_bar=True)

uva_bibliography = Bibliography()
uva_bibliography.importBibtex('Input//UvA_Pure_research_output-41217_cleaned.bib', show_progress_bar=True)

oc_bibliography = Bibliography()
oc_bibliography.importCsv(path_of_file_to_import='Input//oc_articles_with_matching_dois_v1.3.csv',
                          csv_delimiter_character=',',
                          field_value_list_separator=' | ',
                          id_column_header='doi',
                          conversion_arguments_list='open citations',
                          cleaning_algorithm='default',
                          show_progress_bar=True)

vu_bibliography.enrich_with(uva_bibliography,
                            field_to_match_in_bibliographies='b_doi',
                            method='merge')

vu_bibliography.enrich_with(oc_bibliography,
                            field_to_match_in_bibliographies='b_doi',
                            method='left join')

# TODO: Turn n3 transformation and ttl writing steps to a single 'write_to_ttl' method for Bibliography (e.g., vu_bibliography.write_to_ttl())
# TODO: Source bibliography name for individual bibliographies inside must be preserved by allowing specification during parsing to Bibliography object and not during ttl conversion. (currently only one can be specified during ttl conversion)
### Convert to n3 format ###
merged_triples = Triples()
merged_triples.import_bibliography_object(vu_bibliography,
                                          desired_source_bibliography_name='vu_and_uva_enriched_with_opencitations',
                                          show_progress_bar=True)

### Write to ttl file ###
ttl_file = RDF_File('Output//vu_and_uva_merged_and_enriched_with_opencitations_v01.ttl')
ttl_file.write_triples_to_file(merged_triples, show_progress_bar=True)

