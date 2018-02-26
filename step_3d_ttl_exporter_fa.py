#### FINN & ARON ####################################################################################################

from step_2d_triple_creator_fa import triples_list

# IMPORTANT: CHANGE FILE NAME WITH EACH NEW VERSION IF THE FILE IS TO BE IMPORTED TO PROTEGE.
# Protege does not always understand that this is a new file if the file name is the same with a previously imported file.
output_file_path = "Output//finn_aron_1.0-DEMO.ttl"
#output_file_path = "Output//vu_full-0.10.ttl"
# output_file_path = "Output//problematic_characters_test-0.1.ttl"
file_obj = open(output_file_path, "w")

for each_triple in triples_list:
    # TODO: this try-except block is a workaround and should be enhanced
    try:
        file_obj.write(each_triple)
        file_obj.write('\n')
    except:
        pass

print ('Success: The triples were written to the file "' + output_file_path + '".' )
