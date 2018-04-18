import os
if os.getcwd()[-7:] == 'scripts':
    os.chdir('..//')

from preprocessor.Text_File import Text_File
from preprocessor.string_tools import String


with open('Input//web_of_science_uva_vu//data_uvavu000001.ttl', encoding='utf8') as original_wos_file:
    with open('Input//web_of_science_uva_vu//data_uvavu000001_cleaned.ttl', mode='a', encoding='utf8') as cleaned_wos_file:

        for each_line in original_wos_file:
            each_line = String(each_line)
            each_line.purify(clean_from_non_ascii_characters=True,
                             clean_newline_characters=True,
                             remove_problematic_patterns=False)

            cleaned_wos_file.writelines(each_line)