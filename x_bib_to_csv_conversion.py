# A .bib to .csv export script made in order to accelerate literature review process
frederik_bibliography = Bibliography()
frederik_bibliography.importBib('Input//csv_bibliographies//WOS_updated.bib')
frederik_bibliography.exportToCsv(output_file_path='Output//csv_to_bib_output//IDR_Literature_WOS_v0.3.csv',
                                  columns_to_ignore=['b_document', 'b_authors', 'b_topics', 'b_journal',
                                                   'b_publication_month', 'b_issue_number', 'b_volume',
                                                   'b_pages'],
                                  new_header_names=['Type', 'Title', 'Authors', 'Topics', 'Journal', 'Year', 'DOI',
                                                    'ISSN', 'Abstract', 'Note', 'ISBN']
)