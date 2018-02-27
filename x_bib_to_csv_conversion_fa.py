# A .bib to .csv export script made in order to accelerate literature review process
from triplicator.bibTools import Bibliography

fa_bibliography = Bibliography()
fa_bibliography.importBib('Input//finn_aron//publications_finn_aron_edit.bib')
fa_bibliography.exportToCsv(output_file_path='Output//frederik//fa_v0.1.csv',
                                  columns_to_ignore=['b_document', 'b_authors', 'b_topics', 'b_journal',
                                                   'b_publication_month', 'b_issue_number', 'b_volume',
                                                   'b_pages'],
                                  new_header_names=['Type', 'Title', 'Authors', 'Topics', 'Journal', 'Year', 'DOI',
                                                    'ISSN', 'Abstract', 'Note', 'ISBN']
)