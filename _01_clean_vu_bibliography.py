""" Cleans the VU bib file and writes the cleaned version to a file (output file name will be the input file path
suffixed with '_cleaned')
"""

from triplicator.bibTools import Bibtex_File

pattern_replacements_dictionary = {
    '<': '--',
    '>': '--',
    '\{"\}': "'",  # to replace {"} with '
    '\\\\': '--',  # to remove '\' in expressions such as '\sqrt{s}' and rogue '\'s.  unsure why '\\' does not work
    '“': "'",
    '”': "'",
    '’': "'"
}

vu_bibliography = Bibtex_File('Input//VU_Pure_research_output-51017.bib')
vu_bibliography.clean_bibtex_file_and_write_output_to_another_file(patterns_to_replace=pattern_replacements_dictionary,
                                                                   show_progress_bar=True)
