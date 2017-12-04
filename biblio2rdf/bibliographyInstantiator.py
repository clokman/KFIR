class Bibliography:
    """
    A collection of objects and functions that gives control over naming and formatting of variables during
    bibliography to triple format conversion.
    """
    _class_instance_registry     = []   # will contain all instances created in this class
    _class_id_registry           = []   # will hold all instance ids created in this class
    _class_field_values_registry = {}   # will hold all field name-value pairs and entry ids associated with field values.
                                    # ...this enables fast searching for field values such as author names, etc.
                                    # ...across bibliographies.
    def __init__(instance):
        """
        Constructor for Bibliography Class Instance.
        Creates a 'Bibliography' class instance.

        Args:
            None

        Examples:
            >>> # import class and instantiate a Bibliography object.
            >>> from biblio2rdf.bibliographyInstantiator import Bibliography
            >>> my_bibliography = Bibliography()

            >>> # add entries to the instance
            >>> my_bibliography.setEntry("01", "author", "John Can Lokman")
            >>> my_bibliography.setEntry("01", "title", "A title")
            >>> my_bibliography.setEntry("02", "title", "Another title")
            >>> my_bibliography.entries
            {'01': {'author': 'John Can Lokman', 'title': 'A title'}, '02': {'title': 'Another title'}}
        """
        # adds the instance to the list of all instances of the class
        Bibliography._class_instance_registry.append(instance)

        # local equivalent of _class_field_values_registry. Does the same thing for the bibliography instance.
        instance._field_values_registry       = {}

        # hold all ids created within the bibliography instance. allows quick checking whether an id exists.
        instance._id_registry = []

        # dictionary for holding all field types and number of their occurrences
        instance._field_type_registry = {}

        # dictionary that holds all entries. this is where the bibliography data is held, including ids & field values.
        instance.entries      = {}


    def setEntry(instance, entry_id, field_name, field_value):
        """

        Args:
            entry_id (str): desired identifier for the entry to be created
            field_name (str): name of the field to be created (e.g., 'author')
            field_value (str): value of the field to be created (e.g., 'John Doe' or ['John Doe', 'Jane Doe'])

        Returns:
            Nothing, but it adds new entries to the Bibliography object instance.

        Examples:
            >>> # preparation: import class and instantiate a Bibliography object.
            >>> from biblio2rdf.bibliographyInstantiator import Bibliography
            >>> my_bibliography = Bibliography()

            >>> # add entries to the instance
            >>> my_bibliography.setEntry("01", "author", "John Can Lokman")
            >>> my_bibliography.setEntry("01", "title", "A title")
            >>> my_bibliography.setEntry("02", "title", "Another title")
            >>> my_bibliography.entries
            {'01': {'author': 'John Can Lokman', 'title': 'A title'}, '02': {'title': 'Another title'}}
        """
        # if the ID is a new entry
        if entry_id not in instance._id_registry:
            # add target id as key of a the output dictionary and a subdictionary to it as fields and values
            instance.entries[entry_id] = {field_name:field_value}
            # add an instance id to the instance._id_registry
            instance._id_registry.append(entry_id)

        # if the ID is NOT a new entry
        else:
            # call entry by id, and add value-key pair to it
            instance.entries[entry_id][field_name] = field_value

        instance.updateFieldTypesRegistry(entry_id, field_name, field_value)
        instance.updateFieldValuesRegistry(entry_id, field_name, field_value)

    #def formatValues(input_string, formatting_scheme):


    def setFormattedEntry(instance, desired_entry_id, target_field_value, formatting_algorithm, desired_field_name):
        """
        Extracts specified field values from a data source, formats it according to the specified algorithm, and adds
        the formatted values to the specified Bibliography class object. Works by simply passing the arguments to
        formatValues() function and .setEntry method. For modification of functionality, see that function or method
        instead; .setFormattedEntry is merely  proxy method built to serve as a shorthand. A fairly complrehensive
        example that demonstrates usage of different formatting algorithms is also provided in the examples of the
        curent method.

        Args:
            desired_entry_id: the identifier of the new entry to be created
            target_field_value:  the values in the existing source bibliography or data
            formatting_algorithm: one of the formatting algorithms in formatValues function. See formatValues function
                for a list of formatting algorithms.
            desired_field_name: the name of the field to be created

        Returns:
            if target_field_value is 'author' and formatting_algorithm is 'pybtex_author...' : list of authors
            if target_field_value is 'keywords' and formatting_algorithm is 'pybtex_author...': list of keywords
            all other scenarios: formatted string

        Examples:
            >>> # import class and instantiate a Bibliography object.
            >>> from biblio2rdf.bibliographyInstantiator import Bibliography
            >>> my_bibliography = Bibliography()

            >>> # import a sample .bib file and assign it to a variable
            >>> from biblio2rdf.pybtexImporter import Pybtex_import
            >>> pybtex_entries = Pybtex_import('test.bib').data.entries

            >>> # extract fields and their values (from pybtex object), format them,
            >>> # ... and add them to the Bibliography class object.
            >>> for each_entry_id, each_entry in pybtex_entries.items():
            ...     my_bibliography.setFormattedEntry(each_entry_id, each_entry.fields['title'], 'pybtex_document_instance_name', 'x_document')
            ...     my_bibliography.setFormattedEntry(each_entry_id, each_entry.fields['title'], 'pybtex_document_label', 'x_document_label')
            ...     my_bibliography.setFormattedEntry(each_entry_id, each_entry.persons['author'], 'pybtex_author_instance_name', 'x_author')
            ...     my_bibliography.setFormattedEntry(each_entry_id, each_entry.persons['author'], 'pybtex_author_label', 'x_author_label')
            ...     # some fields may exist for only some entries (for none in this sample .bib file)
            ...     # this try-except block will finish with exception because there is no 'keyword' field in the sample
            ...     # ... .bib file.
            ...     try:
            ...         my_bibliography.setFormattedEntry(each_entry_id, each_entry.fields['keyword'], 'pybtex_topic_instance_name', 'x_topics')
            ...         my_bibliography.setFormattedEntry(each_entry_id, each_entry.fields['keyword'], 'pybtex_topic_label', 'x_topic_labels')
            ...     except:
            ...         pass
            ...
            ...     try:
            ...         # 'pybtex_document_instance_name' and 'pybtex_document_label' formatting algorithms are suitable
            ...         # ... for use in other fields, like 'journal'
            ...         my_bibliography.setFormattedEntry(each_entry_id, each_entry.fields['journal'], 'pybtex_document_instance_name', 'x_journal')
            ...         my_bibliography.setFormattedEntry(each_entry_id, each_entry.fields['journal'], 'pybtex_document_label', 'x_journal_label')
            ...     except KeyError:
            ...         pass
            >>> print(my_bibliography.entries)
            {'56fafbf2574947cc9cbbfae578a0a36d': {'x_document': 'Book_with_one_author', 'x_document_label': 'Book with one author', 'x_author': ['Jaschke_AC'], 'x_author_label': ['Jaschke, AC']}, 'd79d00c790984ab08240e997d077c332': {'x_document': 'Article_with_5_authors_with_and_notation', 'x_document_label': "Article with 5 authors with 'and' notation", 'x_author': ['Lohr_A', 'Beunen_R', 'Savelli_H', 'Kalz_M', 'Ragas_A', 'Van_Belleghem_F'], 'x_author_label': ['Lohr, A', 'Beunen, R', 'Savelli, H', 'Kalz, M', 'Ragas, A', 'Van_Belleghem, F'], 'x_journal': 'Current_Opinion_in_Environmental_Sustainability', 'x_journal_label': 'Current Opinion in Environmental Sustainability'}, 'a8781aa0eae047d1826a658f3545ce3f': {'x_document': 'Article_with_3_authors_with_mixed_notation', 'x_document_label': 'Article with 3 authors with mixed notation', 'x_author': ['Mendoza_Rodriguez_JP', 'Wielhouwer_JL', 'Kirchler_ESMN'], 'x_author_label': ['Mendoza_Rodriguez, JP', 'Wielhouwer, JL', 'Kirchler, ESMN'], 'x_journal': 'Journal_of_Economic_Psychology', 'x_journal_label': 'Journal of Economic Psychology'}}
        """
        # if the current field exists for the current entry
        # format the extracted value (which is a string or list [e.g., if it is the values from the 'author' field])
        formatted_field_value = formatValues(target_field_value, formatting_algorithm)

        # add the now-formatted name to Bibliography object
        instance.setEntry(desired_entry_id, desired_field_name, formatted_field_value)

        # if the current field does not exist for the current entry

    ###################################################################################################################
    ################################################# QUERY FUNCTIONS #################################################
    ###################################################################################################################

    def getEntryById(instance, entry_id, field_name=""):
        """
        Searches bibliography instance registry for given entry id or (optionally) entry_id-field_name combination
        (e.g., '1234155125'-author), and returns a the matching entity.

        Args:
            entry_id (str): unique entry id of the bibliography entry
            field_name (str): name of the bibliography field. e.g., author, title.

        Returns:
            If field_name is not specified: The entry that matches with the provided entry_id.
            If field_name is specified: The value of the field of the entry which matches with the provided entry_id.

        Examples:
            >>> # Preparation:
            >>> from biblio2rdf.bibliographyInstantiator import Bibliography
            >>> bibx = Bibliography()
            >>> bibx.setEntry("01", "author", "John Can Lokman")
            >>> bibx.setEntry("01", "title", "Test Book 1")

            >>> # Example #1:
            >>> bibx.getEntryById("01")
            {'author': 'John Can Lokman', 'title': 'Test Book 1'}

            >>> # Example #2:
            >>> bibx.getEntryById("01", "title")
            'Test Book 1'
        """
        if field_name == "":
            return instance.entries[entry_id]
        else:
            return instance.entries[entry_id][field_name]


    def getEntriesByField(instance, field_name, field_value):
        """
        Searches the bibliography instance registry for given field name-value combination (e.g., title-my_title), and returns a list of matching
        bibliography entries.

        Args:
            field_name: Name of the field to be searched (e.g., "author").
            field_value: Value of the field that is being searched (e.g., "John Lokman"

        Returns:
            A list of bibliography entries.

        Examples:
            # Example 1

                >>> # preparation
                >>> from biblio2rdf.bibliographyInstantiator import Bibliography
                >>> bibx = Bibliography()
                >>> bibx.setEntry("01", "author", "John Can Lokman")
                >>> bibx.setEntry("01", "title", "Test Book 1")
                >>> bibx.setEntry("02", "author", "John Can Lokman")
                >>> bibx.setEntry("02", "title", "Test Book 2")

                >>> # method usage
                >>> bibx.getEntriesByField("author", "John Can Lokman")
                [{'author': 'John Can Lokman', 'title': 'Test Book 1'}, {'author': 'John Can Lokman', 'title': 'Test Book 2'}]

            # Example 2

                >>> # preparation:
                >>> from biblio2rdf.pybtexImporter import Pybtex_import
                >>> pybtex_entries = Pybtex_import("test.bib").data.entries
                >>> biby = Bibliography()
                >>> for each_entry_id, each_entry in pybtex_entries.items():
                ...     each_year = each_entry.fields["year"]
                ...     biby.setEntry(each_entry_id, "b_year",each_year)

                >>> # calling entries that has year 2017 using the method:
                >>> biby.getEntriesByField("b_year", "2017")
                [{'b_year': '2017'}, {'b_year': '2017'}, {'b_year': '2017'}]

                >>> # a similar operation without using the method:
                >>> for each_entry_id, each_entry_data in biby.entries.items():
                ...     print(each_entry_data["b_year"])
                2017
                2017
                2017

        """
        # Get matching ids from registry based on field name-value combination
        matching_ids_list = instance._field_values_registry[field_name][field_value]

        # Use matching ids that are returned to retrieve entities these ids correspond to
        matching_entries_list = []
        for each_id in matching_ids_list:
            matching_entries_list.append(instance.getEntryById(each_id))
        return matching_entries_list


    ###################################################################################################################
    ############################################ REGISTRY UPDATE FUNCTIONS ############################################
    ###################################################################################################################

    def updateFieldValuesRegistry(instance, entry_id, field_name, field_value):
        """
            Updates instance registry each time an entry is added to the bibliography instance. The registry allows
            fast searching entries in the bibliography.

            Args:
                 entry_id (str): id to be assigned to entry (e.g., '2341230u9078').
                 field_name(str): name of field (e.g., 'author')
                 field_value(str or list): value of the field (e.g., 'John Doe' )

            Returns:
                Nothing, but updates the instance._field_values_registry

            Examples:
                >>> # preparation
                >>> from biblio2rdf.bibliographyInstantiator import Bibliography
                >>> bibx = Bibliography()

                >>> # add first entry and see how instance registry is updated afterwards
                >>> bibx.setEntry("01", "author", "John Can Lokman")
                >>> bibx.setEntry("01", "title", "Test Book 1")
                >>> print(bibx._field_values_registry)
                {'author': {'John Can Lokman': ['01']}, 'title': {'Test Book 1': ['01']}}

                >>> # add second entry and see how instance registry is updated afterwards
                >>> bibx.setEntry("02", "title", "Test Book 2")
                >>> bibx.setEntry("02", "author", "Stefan Schlobach")
                >>> print(bibx._field_values_registry)
                {'author': {'John Can Lokman': ['01'], 'Stefan Schlobach': ['02']}, 'title': {'Test Book 1': ['01'], 'Test Book 2': ['02']}}

            TODO:
                - Input should be treated as a search string rather than an exact string, so, for instance, a partial
                    author name can also be searched.
        """
        # function must be able to accept a list of items, as this is sometimes the case (e.g., multiple authors
        # ...for author field).
        # Therefore, strings inputs are converted to lists to be compatible with the list processing facilities
        if type(field_value) == str:
            field_value_list = [field_value]

            # Debugger
            #print("input is this string:")
            #print(field_value_list)

        # Explicit statement. If the parameter is already a list, take it as it is
        elif type(field_value) == list:
            field_value_list = field_value

            # Debugger
            # print("input is this list:")
            # print(field_value_list)


        else:
            raise Exception("field_value' must be string or list.")


        for each_field_value in field_value_list:
            # if field_name (e.g., author) has never been added to the registry
            if field_name not in instance._field_values_registry:

                # Debugger
                #print("SCENARIO 1")
                #print("field_values_registry is currently:")
                #print(instance._field_values_registry)

                # Add dictionary entry for the field name-value pair and the entry id (e.g., {author:{"john x":[124515152])}
                # NOTE: Below line can instead use instance._field_type_registry for more efficient search. This has to be tested
                instance._field_values_registry[field_name] = {each_field_value: [entry_id]}

                # Debugger
                #print("field_name '" + str(field_name) + "' is not in registry")
                #print("the current field value is: '" + each_field_value + "' (and it is not in registry).")
                #print("field name and current field value is now added to registry with the following command:")
                #print("instance._field_values_registry[field_name] = {each_field_value: [entry_id]}")
                #print("the field_values_registry has now become:")
                #print(instance._field_values_registry)

            # if field name (e.g., 'author' field) is previously added to the registry...
            elif field_name in instance._field_values_registry:

                # Debugger
                #print("SCENARIO 2")
                #print("field_values_registry is currently:")
                #print(instance._field_values_registry)

                # ...but if field_value (e.g., author's name) has never been added to the registry
                if each_field_value not in instance._field_values_registry[field_name]:
                    # add this field value (e.g., author) and set its value to a LIST that contains current entry_id 
                    # so that this list can later be appended with other entry_ids.
                    # an example operation performed by the line below would be equivalent to:
                    # instance._field_values_registry[author] = {"John x": ["14578436002"]}
                    # which creates this dictionary entry:
                    # _field_values_registry:{ author:{ "John x": ["14578436002"] } }
                    instance._field_values_registry[field_name][each_field_value] = [entry_id]

                    # Debugger
                    #print("field_name '" + str(field_name) + "' has been found in the registry")
                    #print("current field value '" + each_field_value + "' has NOT been found in the registry")
                    #print("field name and current field value is now added to registry with the following command:")
                    #print("instance._field_values_registry[field_name] = {each_field_value: [entry_id]}")
                    #print("the field_values_registry has now become:")
                    #print(instance._field_values_registry)

                # if field_value (e.g., author's name) is previously added to the registry
                elif each_field_value in instance._field_values_registry[field_name]:
                    # Debugger
                    #print("SCENARIO 3")
                    #print("field_values_registry is currently:")
                    #print(instance._field_values_registry)

                    # append entry id to corresponding field value (e.g.,add entry_id to author name)
                    # an example operation performed by the line below would be equivalent to:
                    # instance._field_values_registry[author]["John x"].append["14578436002"]
                    # which creates this dictionary entry:
                    # _field_values_registry:{ author:{ "John x": ["some_previous_id", "14578436002"] } }
                    instance._field_values_registry[field_name][each_field_value].append(entry_id)

                    # Debugger
                    #print("field_name '" + str(field_name) + "' has been found in the registry")
                    #print("current field value '" + each_field_value + "' HAS been found in the registry")
                    #print("field name and current field value is now added to registry with the following command:")
                    #print("instance._field_values_registry[field_name] = {each_field_value: [entry_id]}")
                    #print("the field_values_registry has now become:")
                    #print(instance._field_values_registry)

            # Debugger
            #print("instance._field_values_registry is")
            #print(instance._field_values_registry)
            #print("")

    def updateFieldTypesRegistry(instance, entry_id, field_name, field_value):
        if field_name not in instance._field_type_registry:
            instance._field_type_registry[field_name] = 1
        else:
            instance._field_type_registry[field_name] += 1

            # two container variables for author (instance) names and author labels (which will later be needed by RDF format)


def replacePatternsAsPerDictionary(input_string, patterns_dictionary):
    '''
    Replaces patterns in an inputted string according to the key:value combinations in a dictionary. Useful for replacing
    long name segments such as "_-_" with "-" in instance names during their creation.

    Args:
        input_string (str): String to be processed
        patterns_dictionary(dict): A dictionary that contains the key:value combinations to be used in replacement.
             Keys in the patterns dictionary should be target patterns, while values of the dictionary should be
             the desired replacement patterns or characters.

    Returns:
        A string

    Examples:
        >>> patterns_dictionary = {"_-_" : "-",
        ...                        ": "  : "-" }
        >>> target_string = "Case_1_-_12:_Unknown"
        >>> formatted_string = replacePatternsAsPerDictionary(target_string, patterns_dictionary)
        >>> print(formatted_string)
        Case_1-12:_Unknown
    '''
    import re

    output_string = input_string

    # replace undesired characters with the desired ones (e.g., ':' -> '-') using dictionary_of_patterns_to_replace
    for each_target_pattern, each_replacement_pattern in patterns_dictionary.items():
        output_string = re.sub(each_target_pattern, each_replacement_pattern, output_string)

    return output_string


def standardizeCapitalization(input_string, algorithm):
    """
    Converts title case words (e.g., ' The ') to lowercase e.g., ' the '). Allows conversion algorithms for multiple
    scenarios (e.g., author names vs titles) and languages via keyword arguments of 'algorithm' parameter.

    Args:
        input_string (str): the string to be converted.

    Keyword Args:
        "English title" (algorithm):

    Returns:
        The converted string

    Examples:
        >>> from biblio2rdf.bibliographyInstantiator import standardizeCapitalization
        >>> standardizeCapitalization("Phantom Of The Opera", "en_title")
        'Phantom of the Opera'
    """
    import re

    formatted_string = input_string

    # convert title case to lowercase (DBpedia format)
    if algorithm is "en_title":
        formatted_string = re.sub(" In ", " in ", formatted_string)
        formatted_string = re.sub(" The ", " the ", formatted_string)
        formatted_string = re.sub(" A ", " a ", formatted_string)
        formatted_string = re.sub(" An ", " an ", formatted_string)
        formatted_string = re.sub(" As ", " as ", formatted_string)
        formatted_string = re.sub(" On ", " on ", formatted_string)
        formatted_string = re.sub(" At ", " at ", formatted_string)
        formatted_string = re.sub(" For ", " for ", formatted_string)
        formatted_string = re.sub(" With ", " with ", formatted_string)
        formatted_string = re.sub(" From ", " from ", formatted_string)
        formatted_string = re.sub(" By ", " by ", formatted_string)
        formatted_string = re.sub(" Of ", " of ", formatted_string)
        formatted_string = re.sub(" Vs ", " vs ", formatted_string)
        formatted_string = re.sub(" And ", " and ", formatted_string)

        formatted_string = re.sub(" Be ", " be ", formatted_string)
        formatted_string = re.sub(" Been ", " been ", formatted_string)
        formatted_string = re.sub(" Not ", " not ", formatted_string)
        formatted_string = re.sub(" Is ", " is ", formatted_string)
        formatted_string = re.sub(" Isn\'t ", " isn\'t ", formatted_string)
        formatted_string = re.sub(" Are ", " are ", formatted_string)
        formatted_string = re.sub(" Aren\'t ", " aren\'t ", formatted_string)
        formatted_string = re.sub(" Does ", " does ", formatted_string)
        formatted_string = re.sub(" Doesn\'t ", " doesn\'t ", formatted_string)
        formatted_string = re.sub(" Do ", " do ", formatted_string)
        formatted_string = re.sub(" Don\'t ", " don\'t ", formatted_string)
        formatted_string = re.sub(" Was ", " was ", formatted_string)
        formatted_string = re.sub(" Wasn\'t ", " wasn\'t ", formatted_string)
        formatted_string = re.sub(" Were ", " were ", formatted_string)
        formatted_string = re.sub(" Weren\'t ", " weren\'t ", formatted_string)
        formatted_string = re.sub(" Did ", " did ", formatted_string)
        formatted_string = re.sub(" Didn\'t ", " didn\'t ", formatted_string)
        # This list is not exhaustive

    else:
        raise Exception ('Unknown algorithm parameter: "' + algorithm + '". Please enter a valid capitalization algorithm such as "en_title".')

    return formatted_string


def formatValues(target_field, algorithm):
    """
    Formats the values in a given list or string according to the style specified by 'algorithm' parameter.
    All algorithms follow DBPedia naming conventions.

    Args:
        target_field(str or list): string or list to be formatted.
            For algorithm type 'pybtex_author_instance_name' the list contains 'person' objects.
        algorithm (str): formatting style

    Keyword Args:
        "pybtex_author_instance_name" (algorithm): takes my_pybtex_instance.persons['author'] field and outputs in the format
            ['Lastname1_Lastname1_FN1', 'Lastname2_Lastname2_FN2'] (e.g.,
            an input such as ["Van Belleghem, Frank", "Mendoza Rodriguez J.P."] would be formatted as
                             ["Van_Belleghem_F", "Mendoza_Rodriguez_JP"])

        "pybtex_author_label" (algorithm): takes my_pybtex_instance.persons['author'] field and outputs in the
            format ['Lastname1_Lastname1, FN1', 'Lastname2_Lastname2, FN2'] (e.g.,
            an input such as ["Van Belleghem, Frank", "Mendoza Rodriguez J.P."] would be formatted as
                             ["Van Belleghem, F", "Mendoza Rodriguez, JP"])

        "pybtex_document_instance_name" (algorithm): takes a given field's value
            (e.g., my_pybtex_instance.fields["title"]) (which is a string), and returns a formatted string that is
            suitable to be used as an instance name. During the operation, capitalization is standardized
            (e.g., 'In' -> 'in'), undesired characters (e.g., [,],*,^) and punctuation are removed, and spaces are
            replaced with underscores.

        "pybtex_document_label" (algorithm): takes a given field's value
            (e.g., my_pybtex_instance.fields["title"]) (which is a string), and returns a formatted string that is
            suitable to be used as a label.During the operation, capitalization is standardized
            (e.g., 'In' -> 'in').

        "pybtex_topic_instance_name" (algorithm): takes my_pybtex_instance.fields["keywords"] field's value
            (which is a string in the format of "keyword 1, keyword 2"), and returns a formatted string that is
            suitable to be used as a list of 'topics' (in the format of ["keyword_1", "keyword_2"]).During the
            operation, capitalization is standardized (e.g., 'In' -> 'in'), undesired characters (e.g., [,],*,^)
            and punctuation are removed, and spaces are replaced with underscores.

        "pybtex_topic_label" (algorithm): takes my_pybtex_instance.fields["keywords"] field's value
            (which is a string in the format of "keyword 1, keyword 2"), and returns a formatted string that is
            suitable to be used as a list of labels for 'topics' (in the format of ["keyword 1", "keyword 2"]).During the
            operation, capitalization is standardized (e.g., 'In' -> 'in').

    Raises:
        Keyword Error: Keyword for 'algorithm' parameter does not exist.

    Returns:
        A version of the inputted values that is formatted according the specified algorithm.
        Algorithms and their corresponding outputs:

            - "pybtex_author_instance_name": a list of strings
            - "pybtex_author_label" : a list of strings
            - "pybtex_document_instance_name" (algorithm): a string
            - "pybtex_topic_instance_name" (algorithm): a list of strings in the format of
                ["topic_string_1", "topic_string_2"]. (note that the input was a string of keywords, in the format of
                "topic string 1, topic string 2")

    Examples:
        >>> # preparation
        >>> from biblio2rdf.pybtexImporter import Pybtex_import
        >>> from biblio2rdf.bibliographyInstantiator import formatValues

        >>> # import a bib file with pybtex and and extract entries (i.e., {entry_id:entries} pairs)
        >>> pybtex_entries = Pybtex_import("test.bib").data.entries

        >>> # AUTHOR FORMATTING
        >>> # format all values (i.e., author names) in each entry's 'author' field
        >>> for each_id, each_entry in pybtex_entries.items():
        ...     formatValues(each_entry.persons["author"],"pybtex_author_instance_name")
        ...     formatValues(each_entry.persons["author"],"pybtex_author_label")
        ['Jaschke_AC']
        ['Jaschke, AC']
        ['Lohr_A', 'Beunen_R', 'Savelli_H', 'Kalz_M', 'Ragas_A', 'Van_Belleghem_F']
        ['Lohr, A', 'Beunen, R', 'Savelli, H', 'Kalz, M', 'Ragas, A', 'Van_Belleghem, F']
        ['Mendoza_Rodriguez_JP', 'Wielhouwer_JL', 'Kirchler_ESMN']
        ['Mendoza_Rodriguez, JP', 'Wielhouwer, JL', 'Kirchler, ESMN']

        >>> # AUTHOR FORMATTING + ADDING TO BIBLIOGRAPHY
        >>> # format all values (i.e., author names) in each entry's 'author' field...
        >>> # ...and this time add these formatted values to a Bibliography class instance
        >>> my_bibliography = Bibliography()
        >>> for each_id, each_entry in pybtex_entries.items():
        ...     # create a shorter name for 'author' field
        ...     each_author_field_values = each_entry.persons["author"]
        ...
        ...     # format values in 'author' fields
        ...     each_formatted_author_instance_names_list = formatValues(each_author_field_values, "pybtex_author_instance_name")
        ...     each_formatted_author_labels_list = formatValues(each_entry.persons["author"],"pybtex_author_label")
        ...
        ...     # add now-formatted entries to Bibliography object
        ...     my_bibliography.setEntry(each_id, "b_author", each_formatted_author_instance_names_list)
        ...     my_bibliography.setEntry(each_id, "b_author_labels", each_formatted_author_labels_list)
        >>>
        >>> # print the now-populated Bibliography object
        >>> my_bibliography.entries
        {'56fafbf2574947cc9cbbfae578a0a36d': {'b_author': ['Jaschke_AC'], 'b_author_labels': ['Jaschke, AC']}, 'd79d00c790984ab08240e997d077c332': {'b_author': ['Lohr_A', 'Beunen_R', 'Savelli_H', 'Kalz_M', 'Ragas_A', 'Van_Belleghem_F'], 'b_author_labels': ['Lohr, A', 'Beunen, R', 'Savelli, H', 'Kalz, M', 'Ragas, A', 'Van_Belleghem, F']}, 'a8781aa0eae047d1826a658f3545ce3f': {'b_author': ['Mendoza_Rodriguez_JP', 'Wielhouwer_JL', 'Kirchler_ESMN'], 'b_author_labels': ['Mendoza_Rodriguez, JP', 'Wielhouwer, JL', 'Kirchler, ESMN']}}

        >>> # DOCUMENT INSTANCE NAME FORMATTING
        >>> # Transform pybtex title string to document_instance_name:
        >>> pybtex_entries = Pybtex_import("test.bib").data.entries
        >>> my_bibliography = Bibliography()
        >>>
        >>> for each_entry_id, each_entry_data in pybtex_entries.items():
        ...     each_document_instance_name = formatValues(each_entry_data.fields["title"], "pybtex_document_instance_name")
        ...     my_bibliography.setEntry(each_entry_id, "document_instance_name", each_document_instance_name)
        >>> my_bibliography.entries
        {'56fafbf2574947cc9cbbfae578a0a36d': {'document_instance_name': 'Book_with_one_author'}, 'd79d00c790984ab08240e997d077c332': {'document_instance_name': 'Article_with_5_authors_with_and_notation'}, 'a8781aa0eae047d1826a658f3545ce3f': {'document_instance_name': 'Article_with_3_authors_with_mixed_notation'}}

        >>> # TOPIC FORMATTING
        >>> # transform pybtex keywords string to list of topics
        >>> # (this example depends on imports made in previous examples)
        >>> pybtex_entries = Pybtex_import("test.bib").data.entries
        >>> # test diagnostic. necessary because try-except block would succeed even if the code does nothing
        >>> no_of_keywords_processed = 0
        >>>
        >>> for each_pybtex_entry_id, each_pybtex_entry_data in pybtex_entries.items():
        ...    # if pybtex entry contains keywords
        ...    try:
        ...        # extract keywords
        ...        each_keyword_value_string = each_pybtex_entry_data.fields["keywords"]
        ...        # format and tokenize keywords string in order to transform it into a list of topics
        ...        each_formatted_keyword_list = formatValues(each_keyword_value_string, "pybtex_topic_instance_name")
        ...        # add the newly generated topics to the Bibliography instance
        ...        my_bibliography.setEntry(each_pybtex_entry_id, "b_topics", each_formatted_keyword_list)
        ...
        ...        # test diagnostic
        ...        no_of_keywords_processed = no_of_keywords_processed + 1
        ...    except:
        ...        pass
        >>>
        >>> # test diagnostic
        >>> if no_of_keywords_processed == 0:
        ...     raise Exception ("Test failed: No keywords processed inside the try-except block.")
    """
    import re
    # special characters to omit from strings
    # NOTE: currently, same characters are omitted for both labels and author names.
    # ...for richer labels, this can be changed in a future revision.
    pattern_of_characters_to_omit = "[.,;\'\"\(\)\{\}]"

    # special character patterns to replace in strings
    # in this dictionary, keys are target patterns and values are replacements
    # note the spaces in the patterns (i.e., in keys)
    dictionary_of_patterns_to_replace = {
        ": ": "-",
        " - ": "-"
    }


    # error handling for keywords of the 'algorithm' parameter is handled this way, as an 'else'
    # statement at the end of elif block for keywords does not produce the same result ('else' too broad?)
    # if the entered 'algorithm' parameter is unrecognized
    algorithm_keywords_list = ["pybtex_author_instance_name",
                               "pybtex_author_label",
                               "pybtex_document_instance_name",
                               "pybtex_document_label",
                               "pybtex_topic_instance_name",
                               "pybtex_topic_label",
                               "none"]

    if algorithm not in algorithm_keywords_list:
        raise Exception ('Unknown algorithm parameter: "' + algorithm + '". Please enter a valid capitalization algorithm.')
    #-------------------------------------------------------------------#
    #              FORMAT: AUTHOR INSTANCE NAME AND LABEL               #
    #-------------------------------------------------------------------#
    # algorithm for pybtex author field
    if algorithm is "pybtex_author_instance_name" or algorithm is "pybtex_author_label":
    # TODO: Initial letter of last names and first name abbreviations should always be capitalized, even if this is not the case in input

        # a more descriptive name for target_field
        inputted_author_field_value_list = target_field

        # two container variables for author (instance) names and author labels (which will later be needed by RDF format)
        each_formatted_author_instance_list = []
        each_formatted_author_label_list = []

        # for each "author" field value (which can hold multiple authors as a list) in the pybtex bib data
        for each_author in inputted_author_field_value_list:
            # extract and format each LAST NAME (if available)
            try:
                each_last_name = str(each_author.last()[0])
                each_last_name_formatted = re.sub(pattern_of_characters_to_omit, "", each_last_name)
                each_last_name_formatted = re.sub(" ", "_", each_last_name_formatted)


                # extract and format each FIRST NAME (if available)
                try:
                    # extract first name of a single author
                    each_first_names_string = str(each_author.first()[0])
                    # omit unwanted characters
                    each_first_names_string = re.sub(pattern_of_characters_to_omit, "", each_first_names_string)
                    # placeholder for output
                    each_abbreviated_first_names_string = ""

                    # for the first name's letters (e.g., "John", but "{John Some Middle Name}" is also possible)
                    for i, each_letter in enumerate(each_first_names_string):
                        # always add the first letter of a first name to abbreviated first name (i.e., the output)
                        if i == 0:
                            each_abbreviated_first_names_string = each_abbreviated_first_names_string + each_first_names_string[i]
                        # for the other letters that may be present in the first name string
                        else:
                            # if there are spaces or uppercase letter in the first name string
                            if " " in each_first_names_string or any(letter.isupper() for letter in each_first_names_string):
                                # add the character after space, or the capital letter, to the first name
                                if each_first_names_string[i-1] == " " or each_first_names_string[i].isupper() == True:
                                    each_abbreviated_first_names_string = each_abbreviated_first_names_string + each_first_names_string[i]
                                # otherwise, don't do anything
                                else:
                                    pass
                            # if there are no spaces of uppercase letters in the first name string, don't do anything additional
                            else:
                                pass
                # if a first name is not available, don't do anything
                except:
                    pass

            except:
                pass

            # add extracted last and first names to the output variables (as author instance names or as labels, ...
            # ...depending on the 'algorithm' parameter)
            if algorithm is "pybtex_author_instance_name":
                each_formatted_author_instance_list.append(each_last_name_formatted + "_" + each_abbreviated_first_names_string)
            elif algorithm is "pybtex_author_label":
                each_formatted_author_label_list.append(each_last_name_formatted + ", " + each_abbreviated_first_names_string)
                #each_formatted_author_label_list.append(each_last_name_formatted + ", " + each_first_name_formatted)

        # return either author instance names or author labels depending on which 'algorithm' parameter is entered
        if algorithm is "pybtex_author_instance_name":
            return each_formatted_author_instance_list
        elif algorithm is "pybtex_author_label":
            return each_formatted_author_label_list


    # -------------------------------------------------------------------#
    #              FORMAT: DOCUMENT INSTANCE NAME AND LABEL              #
    # -------------------------------------------------------------------#
    # if the task is title to document_instance_name conversion
    elif algorithm is "pybtex_document_instance_name" or algorithm is "pybtex_document_label":
        # in this case, the input (i.e., 'target_field') will be a string

        # standardize capitalization in the string (e.g., '  At ' -> ' at ')
        document_instance_name = standardizeCapitalization(target_field, "en_title")

        if algorithm is "pybtex_document_instance_name":
            # omit undesired characters from this string
            document_instance_name = re.sub(pattern_of_characters_to_omit, "", document_instance_name)
            # replace remaining undesired characters with the desired ones (e.g., ':' -> '-') using dictionary_of_patterns_to_replace
            document_instance_name = replacePatternsAsPerDictionary(document_instance_name, dictionary_of_patterns_to_replace)
            # replace spaces with underscores
            document_instance_name = re.sub(" ", "_", document_instance_name)

        return document_instance_name


    # ---------------------------------------------------------------------------#
    #                 FORMAT: TOPIC INSTANCE NAME AND TOPIC LABEL                #
    # ---------------------------------------------------------------------------#
    elif algorithm is "pybtex_topic_instance_name" or algorithm is "pybtex_topic_label":
        # tokenize string input (which is in the format of "topic string 1, topic string 2")
        # note that the split character is ", " and not ",". if space is not included, the first character of topics
        # end up being a space e.g., " topic 1" instead of "topic 1" .
        tokenized_topics_list = target_field.split(", ")

        # placeholder for final output
        formatted_topics_list = []

        for each_topic_string in tokenized_topics_list:
            # omit unwanted characters
            each_formatted_topic = re.sub(pattern_of_characters_to_omit, "", each_topic_string)
            # standardize capitalization in the string (e.g., '  At ' -> ' at ')
            each_formatted_topic = standardizeCapitalization(each_formatted_topic, "en_title")

            # if the task is to formatting the input as an instance name
            if algorithm is "pybtex_topic_instance_name":
                each_formatted_topic = each_formatted_topic.lower()
                # replace remaining unwanted characters/patterns with the ones in dictionary_of_patterns_to_replace
                each_formatted_topic = replacePatternsAsPerDictionary(each_formatted_topic,
                                                                      dictionary_of_patterns_to_replace)
                # replace spaces with underscores
                each_formatted_topic = re.sub(" ", "_", each_formatted_topic)
            # if the task is to format as a topic label
            elif algorithm is "pybtex_topic_label":
                # keep the spaces (i.e., " " character) in topic strings
                pass

            # add the formatted topics list to the output variable
            formatted_topics_list.append(each_formatted_topic)

        return formatted_topics_list

    elif algorithm is "none":
        # if no formatting is wanted, the target field values are returned as they are.
        return target_field