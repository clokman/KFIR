#### VU ################################################################################################################

from step_2a_triple_creator_vu import triples_list
from step_1a_parser_vu import log_file

# IMPORTANT: CHANGE FILE NAME WITH EACH NEW VERSION IF THE FILE IS TO BE IMPORTED TO PROTEGE.
# Protege does not always understand that this is a new file if the file name is the same with a previously imported file.
#output_file_path = "Output//vu-1.20.ttl"
output_file_path = "Output//uva_vu_merged_100k_v1.9.ttl"
file_obj = open(output_file_path, "w")

for each_triple in triples_list:
    # TODO: this try-except block is a workaround and should be enhanced
    try:
        file_obj.write(each_triple)
        file_obj.write('\n')
    except:
        pass


print('Success: The triples are written to "%s."' % output_file_path)
print('A log of the operation is kept in "%s".' % log_file.input_file_path)

# NOTE: Check the integrity of the produced .ttl file in command line
# > ttl <path to file>
# e.g.,
# > ttl .\pure_bib_head_100k_0.1.0.ttl
# If ttl validator is not installed, it can be obtained from:
# https://github.com/IDLabResearch/TurtleValidator
# (or, npm install -g turtle-validator)