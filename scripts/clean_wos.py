import os
if os.getcwd()[-7:] == 'scripts':
    os.chdir('..//')

from preprocessor.Text_File import Text_File
from preprocessor.string_tools import String
from meta.consoleOutput import ConsoleOutput

console = ConsoleOutput(log_file_path='log.txt')

input_file_path = 'Input//web_of_science_uva_vu//data_uvavu000001.ttl' # PATH

input_file = Text_File(input_file_path)
output_file_path = input_file.construct_output_file_name_with_postfix('_cleaned')

maximum_progress = input_file.get_no_of_lines_in_file()

pattern_replacements_dictionary = {
    "'": '',
    '"': '',
    '“': '',
    '”': '',
    '’': '',
    ',': '',
    ';': '',
    '-': '_',
    '—': '_',
    '\[': '',
    '\]': '',
    '\{': '',
    '\}': '',
    '\(': '',
    '\)': ''
}

patterns_to_be_ignored_if_lines_contain_them = [
    'dbpedia:'
    '<http://dbpedia.org/'
    'ns1:', 'ns2:', 'ns3:', 'ns4:', 'ns5:', 'ns6:', 'ns7:', 'ns8:', 'ns9:', 'ns10:', 'ns11:', 'ns12:', 'ns13:', 'ns14:',
    'ns15:', 'ns16:', 'ns17:', 'ns18:', 'ns19:', 'ns20:',
    'ns21:annotation', 'ns22:Annotation'
]

with open(input_file_path, encoding='utf8') as original_wos_file:
    with open(output_file_path, mode='a', encoding='utf8') as cleaned_wos_file:

        for i, each_line in enumerate(original_wos_file):
            each_line = String(each_line)

            if each_line.is_any_of_the_patterns_there(patterns_to_be_ignored_if_lines_contain_them):
                pass
            else:
                each_line.purify(clean_from_non_ascii_characters=True,
                                 clean_newline_characters=True,
                                 remove_problematic_patterns=False)

               #each_line.replace_patterns(pattern_replacements_dictionary)

                cleaned_wos_file.writelines(each_line)
            console.print_current_progress(i, maximum_progress, "Cleaning file '%s'" % input_file.input_file_path)

console.log_message("Cleaning of the file '%s' finished" % input_file.input_file_path)
console.log_message("The cleaned file path is '%s'" % output_file_path)