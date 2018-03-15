# KFIR
Repository of the [Knowledge Flows in Interdisciplinary Research](http://www.networkinstitute.org/academy-assistants/academy-projects-17/#) project of VU Network Institute.

Is also the main repository for the packages 'triplicator' and 'preprocessor'. For descriptions of these individual modules, please see their directory. 
 
## Requirements: 
- Pyhon 3.x
- pybtex
- sparqlwrapper

## Legal:
Although short samples may be provided, bibliographic databases from VU and UvA are not included in this directory due to copyright reasons related to their respective owners. Data gathered from OpenCitations, however, are made fully available.

## Quickstart

Convert .bib to .ttl:

    my_bibtex_file = Bibtex_File('demo.bib')
    my_bibtex_file.convert_to_ttl(desired_version_suffix='v0.1', 
                                  desired_source_bibliography_name='my-bib',
                                  output_directory='output')

Retrieve articles by DOIs from Open Citations:

    doi_list = ['10.1163/187607508X384689', '10.1017/S0954579416000572']
    oc_query = Open_Citations_Query()
    oc_query.retrieve_articles_by_dois(doi_list, show_progress_bar=True)
    oc_query.write_results_to_csv('retrieved_articles.csv')


See the ***examples*** directory for more examples