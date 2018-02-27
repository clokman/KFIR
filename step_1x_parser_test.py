from triplicator.bibTools import Bibliography
from preprocessor.Text_File import Text_File


test_bib_file = Text_File('preprocessor//test_data//problematic_characters_test.bib')
# override automatically generated cleaned_file_path to separate from tests in preprocessor package, which also use the
# same automatically generated output file path (no harm would be done if this override is not made, but is made for
# cleaner separation of tests)
test_bib_file.cleaned_file_path = 'preprocessor//test_data//problematic_characters_test_cleaned_2.bib'

test_bib_file.clean_bibtex_file_and_output_cleaned_file(patterns_to_replace={
    '<': '--',
    '>': '--',
    '\{"\}': "'",  # to replace {"} with '
    '\\\\': '--',    # to remove '\' in expressions such as '\sqrt{s}' unsure why '\\' does not work
    '/': '--',
    })

test_bibliography = Bibliography()
# a test bibliography that consists of many problematic entries gathered from source data
test_bibliography.importBib('preprocessor//test_data//problematic_characters_test_cleaned_2.bib', verbose_import=True)
