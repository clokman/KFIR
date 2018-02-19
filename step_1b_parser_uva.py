from triplicator.bibliographyInstantiator import Bibliography
from preprocessor.Text_File import Text_File, Log_File

log_file = Log_File('log.txt')
log_file.clear_contents()

uva_bib_file = Text_File('Input//UvA_Pure_research_output-41217.bib')

uva_bib_file.clean_bibtex_file_and_output_cleaned_file(patterns_to_replace={
    '<': '--',
    '>': '--',
    '\{"\}': "'",  # to replace {"} with '
    '\\\\': '--',  # to remove '\' in expressions such as '\sqrt{s}' and rogue '\'s.  unsure why '\\' does not work
    '“': "'",
    '”': "'",
    '’': "'"
    }, show_progress_bar=True)


uva_bibliography = Bibliography()
uva_bibliography.importBib('Input/UvA_Pure_research_output-41217_cleaned.bib', show_progress_bar=True, verbose_import=False)
