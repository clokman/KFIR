import os
if os.getcwd()[-7:] == 'scripts':
    os.chdir('..//')

from preprocessor.Text_File import Text_File
from preprocessor.string_tools import String
from meta.consoleOutput import ConsoleOutput

console = ConsoleOutput(log_file_path='log.txt')
wos_file_used_for_logging = Text_File('Input//web_of_science_uva_vu//data_uvavu000001.ttl')  # PATH
maximum_progress = wos_file_used_for_logging.get_no_of_lines_in_file()

pattern_replacements_dictionary = {
    "'": '',
    '"': '',
    '“': '',
    '”': '',
    '’': '',
    ',': '',
    ';': '',
    '-': '',
    '—': '',
    '\[': '',
    '\]': '',
    '\{': '',
    '\}': '',
    '\(': '',
    '\)': ''
}

with open('Input//web_of_science_uva_vu//data_uvavu000001.ttl', encoding='utf8') as original_wos_file:  # PATH
    with open('Input//web_of_science_uva_vu//data_uvavu000001_cleaned.ttl', mode='a', encoding='utf8') as cleaned_wos_file:  # PATH

        for i, each_line in enumerate(original_wos_file):
            if 'dbpedia:' in each_line or '<http://dbpedia.org/' in each_line:
                pass
            else:
                each_line = String(each_line)
                each_line.purify(clean_from_non_ascii_characters=True,
                                 clean_newline_characters=True,
                                 remove_problematic_patterns=False)

                each_line.replace_patterns(pattern_replacements_dictionary)

                cleaned_wos_file.writelines(each_line)
            console.print_current_progress(i, maximum_progress, "Cleaning file '%s'" % wos_file_used_for_logging.input_file_path)

console.log_message("Cleaning of the file '%s' finished" % wos_file_used_for_logging.input_file_path)