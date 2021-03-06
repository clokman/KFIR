class List(list):
    """
    >>> # object call
    >>> my_List = List([1,2,3,4,5])
    >>> my_List
    [1, 2, 3, 4, 5]

    >>> # string call
    >>> str(my_List)
    '[1, 2, 3, 4, 5]'

    >>> # modify content
    >>> my_List.content = ['a', 'b', 'c', 'd', 'e']
    >>> my_List
    ['a', 'b', 'c', 'd', 'e']

    >>> # index call
    >>> my_List[0]
    'a'
    >>> my_List[0] = None

    >>> # iteration
    >>> for each_item in my_List:
    ...     print(each_item)
    None
    b
    c
    d
    e

    >>> # length
    >>> len(my_List)
    5
    """

    def __init__(self, content):
        list.__init__(self)
        self.content = content

    ### overrides
    def __repr__(self):
        """Redirects object calls to 'self.content'"""
        return repr(self.content)
    def __str__(self):
        """Redirects string calls to 'self.content'"""
        return str(self.content)
    def __getitem__(self, index):
        """Redirects index calls to 'self.content'"""
        return self.content[index]
    def __setitem__(self, index, value):
        """Redirects modifications through index calls to 'self.content'"""
        self.content[index] = value
    def __iter__(self):
        return iter(self.content)
    def __len__(self):
        return len(self.content)


    def divide_to_sublists(self, max_sublist_length):
        """
        Divides the List object into sub-lists and returns a list with sub-lists.

        Args:
            max_sublist_length(int): Maximum size of each sublist

        Returns:
            list

        Examples:
            >>> my_List = List(['a', 'b', 1, 2, 'd', 'e', 3, 4, 'X'])
            >>> my_List.divide_to_sublists(2)
            [['a', 'b'], [1, 2], ['d', 'e'], [3, 4], ['X']]

            >>> doi_list = ['10.1016/j.adolescence.2016.09.008', '10.1186/s13561-016-0122-6', '10.1007/s00799-016-0182-6', '10.5194/gmd-2016-266', '10.1007/s00737-015-0531-2', '10.1103/RevModPhys.88.021003', 'https://doi.org/10.1101/167171', 'https://doi.org/10.1016/j.chb.2017.04.047', '10.1016/j.trb.2016.09.005', '10.1016/j.ancene.2016.01.001', '10.1111/adb.12322', '10.1017/njg.2016.45', '10.1080/1359432X.2016.1209489', '10.1117/1.JBO.21.6.066008', '10.5194/gmd-10-3329-2017', '10.1016/j.rser.2017.01.103', '10.1177/2050157916664559', '10.1007/978-3-319-45931-8_17', '10.1007/s11136-015-1171-8', '10.1145/2991079.2991121', '10.1093/cz/zow089', '10.1126/science.aac8167', '10.1007/s00586-016-4606-1', '10.1186/s12937-017-0229-6', '10.1007/s11357-016-9894-1', '10.1080/00130095.2015.1094371', '10.1016/j.epsl.2016.02.028', '10.1371/journal.pone.0168636', '10.1016/j.atmosres.2016.03.016', '10.1111/deci.12206', '10.1126/science.aad9634', '10.1103/PhysRevA.94.012506', '10.4103/0019-5545.196846', '10.1016/j.cedpsych.2017.01.006', '10.3324/haematol.2015.133470', '10.1057/978-1-137-50956-7', '10.1016/j.scico.2016.04.001', 'https://doi.org/10.1016/j.scico.2016.04.001', '10.1080/03081087.2015.1053425', '10.3758/s13423-017-1270-3', '10.1681/ASN.2015030287', '10.1016/j.avb.2016.05.006', '10.1177/0971333616689191', '10.1002/sej.1243', '10.1016/j.foreco.2017.06.023', '10.1103/PhysRevLett.118.071801', 'https://doi.org/10.1093/geront/gnv127', '10.1007/978-3-319-42324-1_16', '10.1109/JBHI.2015.2412656', '10.1016/j.jeem.2016.04.002', '10.1080/00207543.2015.1058982', '10.1038/mp.2016.100', '10.1080/03003930.2016.1194267', '10.1016/j.envint.2017.01.018', '10.1038/pr.2015.179', '10.1177/1753193416669263', '10.1016/j.tre.2016.11.003', '10.1021/acs.jpcc.5b12016', '10.1002/anie.201603510', '10.1073/pnas.1607005113', '(DOI) - 10.1111/cch.12521', '10.1017/S0016756815000886', '10.1080/1350293X.2015.1073507', '10.1152/jn.00701.2015', '10.1371/journal.pone.0170791', '10.1016/j.seares.2016.07.005', '10.1016/j.reseneeco.2016.03.003', '10.1007/s00531-017-1499-0', '10.1007/s41669-017-0014-7', '10.1093/acrefore/9780190228613.013.439', '10.14814/phy2.13201', '10.1016/j.jtrangeo.2016.10.013', '10.1523/JNEUROSCI.3658-16.2017', '10.1192/bjpo.bp.115.000166', '10.1136/bmjgh-2016-000109', '10.7554/eLife.20320.001', '10.1037/pas0000332', '10.1177/1474704916673841', '10.1057/978-1-137-58179-2', '10.1002/ejp.963', '10.1017/thg.2016.78', '10.1038/tpj.2016.32', '10.1016/j.jesp.2017.03.008', '10.1287/trsc.2015.0647', '10.1186/s13015-016-0087-3', '10.1016/j.neuroimage.2016.10.030', '10.1371/journal.pone.0169109', '10.1007/s11367-017-1358-z', '10.1080/1369183X.2015.1061425', '10.2196/mental.4614', '10.1002/arp.1564', '10.1021/acs.orglett.6b01023', '10.3847/1538-4357/aa6c47', 'http://www.socialevraagstukken.nl/veiligheid-creeer-je-met-geborgenheid/', '10.1186/s12888-016-0790-0', '10.1371/journal.pone.0155755', '10.1103/PhysRevLett.116.241801']
            >>> divided_doi_list = List(doi_list).divide_to_sublists(10)
            >>> for each_sublist in divided_doi_list:
            ...     print(len(each_sublist), each_sublist)
            10 ['10.1016/j.adolescence.2016.09.008', '10.1186/s13561-016-0122-6', '10.1007/s00799-016-0182-6', '10.5194/gmd-2016-266', '10.1007/s00737-015-0531-2', '10.1103/RevModPhys.88.021003', 'https://doi.org/10.1101/167171', 'https://doi.org/10.1016/j.chb.2017.04.047', '10.1016/j.trb.2016.09.005', '10.1016/j.ancene.2016.01.001']
            10 ['10.1111/adb.12322', '10.1017/njg.2016.45', '10.1080/1359432X.2016.1209489', '10.1117/1.JBO.21.6.066008', '10.5194/gmd-10-3329-2017', '10.1016/j.rser.2017.01.103', '10.1177/2050157916664559', '10.1007/978-3-319-45931-8_17', '10.1007/s11136-015-1171-8', '10.1145/2991079.2991121']
            10 ['10.1093/cz/zow089', '10.1126/science.aac8167', '10.1007/s00586-016-4606-1', '10.1186/s12937-017-0229-6', '10.1007/s11357-016-9894-1', '10.1080/00130095.2015.1094371', '10.1016/j.epsl.2016.02.028', '10.1371/journal.pone.0168636', '10.1016/j.atmosres.2016.03.016', '10.1111/deci.12206']
            10 ['10.1126/science.aad9634', '10.1103/PhysRevA.94.012506', '10.4103/0019-5545.196846', '10.1016/j.cedpsych.2017.01.006', '10.3324/haematol.2015.133470', '10.1057/978-1-137-50956-7', '10.1016/j.scico.2016.04.001', 'https://doi.org/10.1016/j.scico.2016.04.001', '10.1080/03081087.2015.1053425', '10.3758/s13423-017-1270-3']
            10 ['10.1681/ASN.2015030287', '10.1016/j.avb.2016.05.006', '10.1177/0971333616689191', '10.1002/sej.1243', '10.1016/j.foreco.2017.06.023', '10.1103/PhysRevLett.118.071801', 'https://doi.org/10.1093/geront/gnv127', '10.1007/978-3-319-42324-1_16', '10.1109/JBHI.2015.2412656', '10.1016/j.jeem.2016.04.002']
            10 ['10.1080/00207543.2015.1058982', '10.1038/mp.2016.100', '10.1080/03003930.2016.1194267', '10.1016/j.envint.2017.01.018', '10.1038/pr.2015.179', '10.1177/1753193416669263', '10.1016/j.tre.2016.11.003', '10.1021/acs.jpcc.5b12016', '10.1002/anie.201603510', '10.1073/pnas.1607005113']
            10 ['(DOI) - 10.1111/cch.12521', '10.1017/S0016756815000886', '10.1080/1350293X.2015.1073507', '10.1152/jn.00701.2015', '10.1371/journal.pone.0170791', '10.1016/j.seares.2016.07.005', '10.1016/j.reseneeco.2016.03.003', '10.1007/s00531-017-1499-0', '10.1007/s41669-017-0014-7', '10.1093/acrefore/9780190228613.013.439']
            10 ['10.14814/phy2.13201', '10.1016/j.jtrangeo.2016.10.013', '10.1523/JNEUROSCI.3658-16.2017', '10.1192/bjpo.bp.115.000166', '10.1136/bmjgh-2016-000109', '10.7554/eLife.20320.001', '10.1037/pas0000332', '10.1177/1474704916673841', '10.1057/978-1-137-58179-2', '10.1002/ejp.963']
            10 ['10.1017/thg.2016.78', '10.1038/tpj.2016.32', '10.1016/j.jesp.2017.03.008', '10.1287/trsc.2015.0647', '10.1186/s13015-016-0087-3', '10.1016/j.neuroimage.2016.10.030', '10.1371/journal.pone.0169109', '10.1007/s11367-017-1358-z', '10.1080/1369183X.2015.1061425', '10.2196/mental.4614']
            7 ['10.1002/arp.1564', '10.1021/acs.orglett.6b01023', '10.3847/1538-4357/aa6c47', 'http://www.socialevraagstukken.nl/veiligheid-creeer-je-met-geborgenheid/', '10.1186/s12888-016-0790-0', '10.1371/journal.pone.0155755', '10.1103/PhysRevLett.116.241801']


        """
        step_size = max_sublist_length
        input_list_length = len(self)

        divided_list = []
        current_slice_start = 0
        current_slice_end = step_size
        for i in range(0, input_list_length, step_size):
            divided_list.append(self[current_slice_start:current_slice_end])
            current_slice_start += step_size
            current_slice_end += step_size
        return divided_list


    def combine_items_if_their_combination_exists_in_external_list(self,
                                                                   fragmentation_signalling_character_at_either_end,
                                                                   external_list_to_compare_with,
                                                                   leave_erroneous_characters_in_place=False):
        """"
        Reconstructs fragments of of a string that is distributed to multiple elements by detecting the fragmentation
        using the fragmentation_signalling_character parameter.

        Args:
            fragmentation_signalling_character_at_either_end (str): Character to be used for detecting fragmentation at
                either end of the strings.
            external_list_to_compare_with (list)
            leave_erroneous_characters_in_place (bool): Includes in the output characters in the input dataset
                such as '' and '&' (i.e., the fragmentation_signalling_character itself). See 'Notes' for more.
                May cause errors if set to True.

        Notes:
            WARNING: This method may change the index positions of the original list due to reconstruction and
                removing of erroneous characters.

            Items that could cause errors, such as '' (causes index error) and '&' (the whole string is equal to the
                fragmentation_signalling_character) is removed. Characters such as ';' is purposefully not removed;
                such deeper cleaning functions is not in the scope of this method.

        See Also:
            dataframe_tools.combine_items_if_their_combination_exists_in_external_list()

        Returns:
            list_tools.List (as 'self')

        Examples:
            >>> from pprint import pprint

            >>> #===== INIT =============================================================================================
            >>> # Sample list of possible values:
            >>> wos_categories_list = ['Mathematical & Computational Biology', 'Architecture',
            ...                        'Statistics & Probability', 'Medicine, General & Internal']

            >>> # List to be processed:
            >>> # Note that 'Mathematical &' and 'Computational Biology' are one item divided in two.
            >>> my_list = ["Biochemical Research Methods",
            ...             "Biotechnology & Applied Microbiology",
            ...             "Computational Biology",
            ...             "Statistics & Probability",
            ...             "Computer Science",
            ...             "Interdisciplinary Applications",
            ...             "Mathematical &",
            ...             "& Internal",
            ...             "Health Care Sciences & Services",
            ...             "Primary Health Care",
            ...             "Medicine, General",
            ...             "",
            ...             " ",
            ...             "&",
            ...             ";"
            ... ]
            >>> #=======================================================================================================


            >>> #===== RECONSTRUCTION OF A SEPARATED ITEMS (AND PROCESSING OF PROBLEMATIC ITEMS) =======================
            >>> my_List = List(my_list)
            >>> my_List.combine_items_if_their_combination_exists_in_external_list(fragmentation_signalling_character_at_either_end="&", \
                                                                            external_list_to_compare_with=wos_categories_list)
            >>> pprint(my_List.content)  # Note that 'Mathematical & Computational Biology' and
            ...                          # 'Medicine, General & Internal' are constructed items.
            ['Biochemical Research Methods',
             'Biotechnology & Applied Microbiology',
             'Statistics & Probability',
             'Computer Science',
             'Interdisciplinary Applications',
             'Health Care Sciences & Services',
             'Primary Health Care',
             ' ',
             ';',
             'Medicine, General & Internal',
             'Mathematical & Computational Biology']
            >>> # ';' character is purposefully not removed; such deeper cleaning functions is not in the scope of
            >>> # this method. However, items that could cause errors, such as '' (causes index error) and '&' (the
            >>> # whole string is equal to the fragmentation_signalling_character) is removed.
            >>> #=======================================================================================================


            >>> #===== COMPETING CANDIDATE TAILS =======================================================================
            >>> # Init
            >>> wos_categories_list_2 = ['Mathematical & Computational Biology', 'Mathematical & Computational Chemistry']
            >>> my_list_2 = ["Biochemical Research Methods", "Biotechnology & Applied Microbiology",
            ...            "Computational Biology", "Statistics & Probability", "Computational Chemistry",
            ...            "Computer Science", "Interdisciplinary Applications", "Mathematical &"]
            >>> my_List_2 = List(my_list_2)

            >>> my_List_2.combine_items_if_their_combination_exists_in_external_list(fragmentation_signalling_character_at_either_end="&", \
                                                                       external_list_to_compare_with=wos_categories_list_2)
            WARNING: Automatic string reconstruction for the root string 'Mathematical &' skipped due more than one candidate existing for the tail part. These were the candidates: (2 items):
            Mathematical & Computational Biology
            Mathematical & Computational Chemistry

            >>> # Note that no item is constructed in this scenario.
            >>> my_List_2.content
            ['Biochemical Research Methods', 'Biotechnology & Applied Microbiology', 'Computational Biology', 'Statistics & Probability', 'Computational Chemistry', 'Computer Science', 'Interdisciplinary Applications', 'Mathematical &']
            >>> #=======================================================================================================


            >>> #===== NO MATCH FOUND IN COMPARISON LIST ===============================================================
            >>> # Init
            >>> wos_categories_list_3 = ['Geography', 'Physics']
            >>> my_list_3 = ["Biochemical Research Methods", "Biotechnology & Applied Microbiology",
            ...            "Computational Biology", "Statistics & Probability", "Computational Chemistry",
            ...            "Computer Science", "Interdisciplinary Applications", "Mathematical &"]
            >>> my_List_3 = List(my_list_3)

            >>> my_List_3.combine_items_if_their_combination_exists_in_external_list(fragmentation_signalling_character_at_either_end="&", \
                                                                        external_list_to_compare_with=wos_categories_list_3)

            >>> # Note that no item is constructed in this scenario.
            >>> my_List_3.content
            ['Biochemical Research Methods', 'Biotechnology & Applied Microbiology', 'Computational Biology', 'Statistics & Probability', 'Computational Chemistry', 'Computer Science', 'Interdisciplinary Applications', 'Mathematical &']
            >>> #=======================================================================================================


            >>> #===== NO SIGNALLING PATTERN FOUND IN TARGET LIST ======================================================
            >>> # Init
            >>> wos_categories_list_4 = ['Geography', 'Physics']
            >>> my_list_4 = ["Biochemical Research Methods", "Biotechnology & Applied Microbiology",
            ...            "Computational Biology", "Statistics & Probability", "Computational Chemistry",
            ...            "Computer Science", "Interdisciplinary Applications", "Mathematical"]
            >>> my_List_4 = List(my_list_4)

            >>> my_List_4.combine_items_if_their_combination_exists_in_external_list(fragmentation_signalling_character_at_either_end="&", \
                                                                         external_list_to_compare_with=wos_categories_list_4)

            >>> # Note that no item is constructed in this scenario.
            >>> my_List_4.content
            ['Biochemical Research Methods', 'Biotechnology & Applied Microbiology', 'Computational Biology', 'Statistics & Probability', 'Computational Chemistry', 'Computer Science', 'Interdisciplinary Applications', 'Mathematical']
            >>> #=======================================================================================================

        """
        from meta.consoleOutput import ConsoleOutput
        from warnings import warn

        console = ConsoleOutput(log_file_path='log.txt')

        input_list = self.content

        for k, each_item in reversed(list(enumerate(input_list))):

            item_is_likely_result_of_an_error = False  # and will likely cause an (hidden) error
            if len(each_item) < 1:
                item_is_likely_result_of_an_error = True
            if each_item == fragmentation_signalling_character_at_either_end:
                item_is_likely_result_of_an_error = True

            if item_is_likely_result_of_an_error:
                input_list.pop(k)

        # main loop of the method
        for i, each_item in reversed(list(enumerate(input_list))):  # reversing the list is necessary for using the .pop
                                                                    # method while iterating over the list

            item_is_first_section_of_a_defragmented_entity = False
            item_is_second_section_of_a_defragmented_entity = False

            if fragmentation_signalling_character_at_either_end == each_item[-1]:
                item_is_first_section_of_a_defragmented_entity = True

            if fragmentation_signalling_character_at_either_end == each_item[0]:
                item_is_second_section_of_a_defragmented_entity = True


            # if an item ends with the fragmentation_signalling_character
            if item_is_first_section_of_a_defragmented_entity or item_is_second_section_of_a_defragmented_entity:

                fragmented_string_part = input_list.pop(i)

                indices_of_possible_counterparts = []
                possible_counterparts = []
                for j, each_remaining_item in enumerate(input_list):

                    if item_is_first_section_of_a_defragmented_entity:
                        each_possible_combination = fragmented_string_part + ' ' + each_remaining_item

                    elif item_is_second_section_of_a_defragmented_entity:
                        each_possible_combination = each_remaining_item + ' ' + fragmented_string_part

                    else:
                        warn('Item "{item}" skipped due to being detected as both (or neither) the first and '
                                      'second parts of a fragmented string.'.format(item=fragmented_string_part))


                    if each_possible_combination in external_list_to_compare_with:

                        indices_of_possible_counterparts.append(j)
                        possible_counterparts.append(each_possible_combination)  # not functionally used; is for logging

                # if there is more than candidate for the tail part, put the popped part back to the list, and log this
                if len(indices_of_possible_counterparts) > 1:

                    # put the fragmented string back
                    input_list.append(fragmented_string_part)

                    console.log_list_with_caption("WARNING: Automatic string reconstruction for the root string "
                                                  "'{fragmented_string_part}' skipped due more than one candidate existing for the "
                                                  "tail part. These were the candidates:"
                                                  .format(fragmented_string_part=fragmented_string_part),
                                                  input_list=possible_counterparts
                    )

                # if there is only one candidate for the tail part, combine the both parts and add this version
                # to the list
                elif len(indices_of_possible_counterparts) == 1:

                    index_of_other_part = indices_of_possible_counterparts[0]
                    other_part = input_list.pop(index_of_other_part)

                    if item_is_first_section_of_a_defragmented_entity:
                        combined_string = fragmented_string_part + ' ' + other_part

                    elif item_is_second_section_of_a_defragmented_entity:
                        combined_string = other_part + ' ' + fragmented_string_part

                    else:
                        combined_string = ''  # no combination occurs

                        # put both parts back
                        input_list.append(fragmented_string_part)
                        input_list.append(other_part)

                        warn('Item "{item}" skipped due to being detected as both (or neither) the first and '
                                      'second parts of a fragmented string.'.format(item=fragmented_string_part))

                    if combined_string:
                        input_list.append(combined_string)

                # if no possible match within the comparison list is found, put the fragmented string back to the list
                else:
                    input_list.append(fragmented_string_part)

            # if no item ends with '&', do nothing
            else:
                pass

            self.content = input_list