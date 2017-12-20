# KFIR
Repository of the [Knowledge Flows in Interdisciplinary Research](http://www.networkinstitute.org/academy-assistants/academy-projects-17/#) project of VU Network Institute.

Is also the main repository for the packages 'triplicator' and 'preprocessor'. For descriptions of these individual modules, please see their directory. 
 

## Requirements: 
- Pyhon 3.x
- pybtex

## Legal:
Although short samples may be provided, bibliographic databases from VU and UvA are not included in this directory due to copyright reasons related to their respective owners. Data gathered from OpenCitations, however, are made fully available.

# Change Log
## v1.2
2017.12.10
- Package name changed from 'bib2rdf' to 'triplicator'.
- Two-way .csv processing functionality added:
    - A .bib to .csv export method added (triplicator.bibliographyInstantiator.exportToCsv) added in order to accelerate 
    literature review process
    - A .csv to .bib conversion module added (triplicator.csvImporter) in order to import open citations data
- '{"}' characters in .bib files no longer cause issues in .ttl files. Each occurrence of this pattern is now replaced with a single quote.
- Standardization during import operations. Different author name inputs now author output name in a uniform format. (Now, all first names are abbreviated).
  (e.g., ["Van Belleghem, Frank", "Mendoza Rodriguez J.P."] are now formatted as
         ["Van_Belleghem_F", "Mendoza_Rodriguez_JP"])
  - was:
      ['Lohr_Ansje', 'Beunen_R', 'Savelli_Heidi', 'Kalz_Marco', 'Ragas_Ad', 'VanBelleghem_Frank']
      ['Lohr, Ansje', 'Beunen, R', 'Savelli, Heidi', 'Kalz, Marco', 'Ragas, Ad', 'VanBelleghem, Frank']
      ['MendozaRodriguez_JP', 'Wielhouwer_JL', 'Kirchler_Erich']
      ['MendozaRodriguez, JP', 'Wielhouwer, JL', 'Kirchler, Erich']
  - now:
      ['Lohr_A', 'Beunen_R', 'Savelli_H', 'Kalz_M', 'Ragas_A', 'Van_Belleghem_F']
      ['Lohr, A', 'Beunen, R', 'Savelli, H', 'Kalz, M', 'Ragas, A', 'Van_Belleghem, F']
      ['Mendoza_Rodriguez_JP', 'Wielhouwer_JL', 'Kirchler_E']
      ['Mendoza_Rodriguez, JP', 'Wielhouwer, JL', 'Kirchler, E']
- Further name standardization during import operations: Lowercase and uppercase letters should be matched across instance names (e.g., usage of 'and' or 'And') should be consistent
- Preprocessor package ported from https://github.com/clokman/DM-ML (Data mining and machine learning) and core functions are refactored from functional to object-oriented code. This package is primarily needed for .csv import functionality.
- Overall code structure improved for bibliographyInstantiator module, and several new methods added

## v1.1
- Code refactored from functional to object oriented
- Documentation completed
- Doctests added
- Add (to instance._field_registry) stats to measure how many DOIs etc exists in the bibliography
- Change "publication"  to "journal"
- Add labels
- Multi-author support
- Updated to Python 3
- Unicode character support added

# TODO
- Adding citations and references (see: open citations => bibResource:15088)
- Database enrichment (see frederik's article at 'Diigo to read', see Ali meetings & Skype links)
- Check citations in "Pybtex_import("biblio2rdf//test.bib").data.citations" (by using another bib file)
- Testing for all keyword capitalization scenarios for formatValues function
