# KFIR
Repository of the [Knowledge Flows in Interdisciplinary Research](http://www.networkinstitute.org/academy-assistants/academy-projects-17/#) project of VU Network Institute.

Is also the main repository for the packages 'triplicator' and 'preprocessor'. For descriptions of these individual modules, please see their directory. 
 
## Functionality 
![](KFIR_system_minimal.png)
## Requirements:
- Pyhon 3.x
- pybtex
- sparqlwrapper

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


See the ***examples*** directory for more examples.
Further documentation provided in docstrings within the code.

## Legal
Although short samples may be provided, bibliographic databases from VU and UvA are not included in this directory due to copyright reasons related to their respective owners. Data gathered from OpenCitations, however, are made fully available.


## Change Log
### OpenCitations enrichment and data merge ✅ 06/03/18 > 27/03/18


#### ⭐ New (4)
- [(8) Merge functionality fully implemented and tested](https://trello.com/c/NNy94TYB/30-8-merge-functionality-fully-implemented-and-tested)
- [(5) Implemented method to retrieve all entries with matching DOIs from OpenCitations](https://trello.com/c/h36euAFO/21-5-implemented-method-to-retrieve-all-entries-with-matching-dois-from-opencitations)
- [(5) All DOIs in bib files stored in a file](https://trello.com/c/Pl5QUor5/20-5-all-dois-in-bib-files-stored-in-a-file)
- [(21) Enrich method for OpenCitations and Pure implemented](https://trello.com/c/5darswd8/7-21-enrich-method-for-opencitations-and-pure-implemented)
- (8) Implemented methods for one-statement conversion of bib and csv files to ttl  

#### 👍 Enhancement (4)
- [(8) verbose_input parameter and the functionality removed form bib and csv parsing operations, so that it does not majorly slow down the processes if someone activates it by mistake](https://trello.com/c/AyD0pV06/27-8-verboseinput-parameter-and-the-functionality-removed-form-bib-and-csv-parsing-operations-so-that-it-does-not-majorly-slow-down)
- [(12) CSV file cleaning script improved (using already-existing cleaning scripts) so that it can be imported into .ttl without issues](https://trello.com/c/2cAvX18e/28-12-csv-file-cleaning-script-improved-using-already-existing-cleaning-scripts-so-that-it-can-be-imported-into-ttl-without-issues)
- [(8) Flexible search (instead of exact match search) is implemented in SPARQL query functionality](https://trello.com/c/a3zzmaQC/23-8-flexible-search-instead-of-exact-match-search-is-implemented-in-sparql-query-functionality)
- [(5) Example scripts folder updated and revised](https://trello.com/c/l31402yK/26-5-example-scripts-folder-updated-and-revised)
- (8) All functions in the project converted to their object-oriented equivalents

#### 🐛 Fixed (2)
- [(18) Fixed: Some author fields appearing empty](https://trello.com/c/7fZvyiV8/4-18-fixed-some-author-fields-appearing-empty)
- [(5) Publication type in ttl files made uniform across datasets (e.g., Journal Article and JournalArticle --> Article)](https://trello.com/c/eOO0h9dS/2-5-publication-type-in-ttl-files-made-uniform-across-datasets-eg-journal-article-and-journalarticle-article)

