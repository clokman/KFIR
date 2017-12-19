#### VU ################################################################################################################

from step_2a_triple_creator_vu import triples_list

# IMPORTANT: CHANGE FILE NAME WITH EACH NEW VERSION IF THE FILE IS TO BE IMPORTED TO PROTEGE.
# Protege does not always understand that this is a new file if the file name is the same with a previously imported file.
output_file_path = "Output//vu_bib_100k_1.10.ttl"
# output_file_path = "Output//problematic_characters_test-0.1.ttl"
file_obj = open(output_file_path, "w")

for each_triple in triples_list:
    # TODO: this try-except block is a workaround and should be enhanced
    try:
        file_obj.write(each_triple)
        file_obj.write('\n')
    except:
        pass

print ('Success: The triples are written to the file "' + output_file_path + '".' )

# NOTE: Check the integrity of the produced .ttl file in command line
# > ttl <path to file>
# e.g.,
# > ttl .\pure_bib_head_100k_0.7.0.ttl
# If ttl validator is not installed, it can be obtained from:
# https://github.com/IDLabResearch/TurtleValidator
# (or, npm install -g turtle-validator)


# #### UVA ##############################################################################################################
#
# from step_2b_triple_creator_uva import triples_list
#
# # IMPORTANT: CHANGE FILE NAME WITH EACH NEW VERSION IF THE FILE IS TO BE IMPORTED TO PROTEGE.
# # Protege does not always understand that this is a new file if the file name is the same with a previously imported file.
# output_file_path = 'Output//uva_bib_100K_0.2.ttl'
# file_obj = open(output_file_path, "w")
# # file_obj = open("Output//pure_bib_limited_0.6.5.ttl", "w")  # use for test version
#
# for each_triple in triples_list:
#     # TODO: this try-except block is a workaround and should be enhanced
#     try:
#         file_obj.write(each_triple)
#         file_obj.write('\n')
#     except:
#         pass
#
# print ("Success: The triples are written to the specified file.")
#
# # NOTE: Check the integrity of the produced .ttl file in command line
# # > ttl <path to file>
# # e.g.,
# # > ttl .\pure_bib_head_100k_0.7.0.ttl
# # If ttl validator is not installed, it can be obtained from:
# # https://github.com/IDLabResearch/TurtleValidator
# # (or, npm install -g turtle-validator)
#
#
# #### OPEN CITATIONS ####################################################################################################
#
# output_file_path = 'Output//open_bib_full_0.2.ttl'
# from step_2c_triple_creator_oc import triples_list
#
# # IMPORTANT: CHANGE FILE NAME WITH EACH NEW VERSION IF THE FILE IS TO BE IMPORTED TO PROTEGE.
# # Protege does not always understand that this is a new file if the file name is the same with a previously imported file.
#
# file_obj = open(output_file_path, "w")
# # file_obj = open("Output//pure_bib_limited_0.6.5.ttl", "w")  # use for test version
#
# for each_triple in triples_list:
#     # TODO: this try-except block is a workaround and should be enhanced
#     try:
#         file_obj.write(each_triple)
#         file_obj.write('\n')
#     except:
#         pass
#
# print ('Success: The triples are written to the file "' + output_file_path + '".' )
#
# # NOTE: Check the integrity of the produced .ttl file in command line
# # > ttl <path to file>
# # e.g.,
# # > ttl .\pure_bib_head_100k_0.7.0.ttl
# # If ttl validator is not installed, it can be obtained from:
# # https://github.com/IDLabResearch/TurtleValidator
# # (or, npm install -g turtle-validator)
