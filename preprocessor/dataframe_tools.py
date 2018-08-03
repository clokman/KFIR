"""
Methods for performing additional operations on pandas.DataFrames
"""

class Data_Frame(object):

    def __init__(self, pandas_dataframe):
        """
        Examples:
            >>> import pandas

            >>> # CREATE A DATA_FRAME INSTANCE =========================================================================
            >>> # Create a pandas.DataFrame
            >>> my_dataframe = pandas.DataFrame({
            ...      'wosKeywords': ['Clinical Neurology; Orthopedics','Biology; Mathematical & Computational Biology','Physics, Nuclear','Plant Sciences'],
            ...      'articleIds': ['wosres:WOS_000071013000007','wosres:WOS_000071018600001','wosres:WOS_000071021600006','wosres:WOS_000071040300005']
            ...     })
            >>> my_dataframe
                               articleIds                                    wosKeywords
            0  wosres:WOS_000071013000007                Clinical Neurology; Orthopedics
            1  wosres:WOS_000071018600001  Biology; Mathematical & Computational Biology
            2  wosres:WOS_000071021600006                               Physics, Nuclear
            3  wosres:WOS_000071040300005                                 Plant Sciences

            >>> # Initiate Data_Frame instance form pandas.DataFrame
            >>> my_Data_Frame = Data_Frame(my_dataframe)
            >>> my_Data_Frame.dataframe
                               articleIds                                    wosKeywords
            0  wosres:WOS_000071013000007                Clinical Neurology; Orthopedics
            1  wosres:WOS_000071018600001  Biology; Mathematical & Computational Biology
            2  wosres:WOS_000071021600006                               Physics, Nuclear
            3  wosres:WOS_000071040300005                                 Plant Sciences
            >>> #=======================================================================================================


            >>> # ERROR: INPUT MUST BE A PANDAS DATAFRAME ==============================================================
            >>> try:
            ...     my_Data_Frame = Data_Frame(1)
            ... except TypeError as exception:  # catch exception
            ...     print (exception)
            Parameter "1" must be of type <class 'pandas.core.frame.DataFrame'>, but is currently of type <class 'int'>
            >>> #=======================================================================================================
        """
        import pandas
        from preprocessor.string_tools import Parameter_Value
        Parameter_Value(pandas_dataframe).force_type(pandas.DataFrame)
        self.dataframe = pandas_dataframe

        self._index = {}  # for storing indexes created with indexing methods of this class
                          # (e.g., '_index_values_column_with_identifiers_column()')

    def tokenize_string_column(self, delimiter_pattern_in_literal_cells, string_column_name, id_column_name=None):
        """
        Tokenizes string literals by assigning one splitted part (e.g., keyword) per row. The input dataframe must have
        at most two columns: one column containing strings to be tokenized, and one column contaning ids(optional)

        Args:
            delimiter_pattern_in_literal_cells(str)
            string_column_name(str)
            id_column_name(str)

        Returns:
            Data_Frame (updated self)

        Examples:
            >>> import pandas

            >>> # TOKENIZING A SINGLE-COLUMN DATAFRAME =================================================================
            >>> # Make a single-column dataframe:
            >>> df = pandas.DataFrame({'the only column': ('a; b', 'c; d; e')})
            >>> my_Data_Frame = Data_Frame(df)
            >>> print(my_Data_Frame.dataframe)
              the only column
            0            a; b
            1         c; d; e

            >>> # Tokenize strings in single-column dataframe
            >>> my_Data_Frame.tokenize_string_column(string_column_name='the only column',
            ...                                      delimiter_pattern_in_literal_cells='; ')\
            .dataframe
              the only column
            0               a
            1               b
            2               c
            3               d
            4               e
            >>> #=======================================================================================================


            >>> # TOKENIZING A TWO-COLUMN DATAFRAME ====================================================================
            >>> # Create a simple dataframe
            >>> my_dataframe = pandas.DataFrame({
            ...      'literal_column':['literal one; literal two', 'literal three; literal four'],
            ...      'id_column': ['id 1', 'id 2']
            ... })

            >>> # Tokenize and view the dataframe
            >>> my_Data_Frame = Data_Frame(my_dataframe)
            >>> my_Data_Frame.tokenize_string_column(string_column_name='literal_column',
            ...                                                    id_column_name='id_column',
            ...                                                    delimiter_pattern_in_literal_cells='; ')\
               .dataframe
              id_column literal_column
            0      id 1    literal one
            1      id 1    literal two
            2      id 2  literal three
            3      id 2   literal four
            >>> #=======================================================================================================


            >>> # A REAL WORLD TWO-COLUMN EXAMPLE ======================================================================
            >>> # Create a dataframe
            >>> my_dataframe = pandas.DataFrame({'wosKeywords': ['Clinical Neurology; Orthopedics', 'Biology; Mathematical & Computational Biology', 'Physics, Nuclear', 'Plant Sciences'],
            ...                                  'articleId': ['wosres:WOS_000071013000007', 'wosres:WOS_000071018600001', 'wosres:WOS_000071021600006', 'wosres:WOS_000071040300005']})
            >>> my_Data_Frame = Data_Frame(my_dataframe)
            >>> my_Data_Frame.dataframe
                                articleId                                    wosKeywords
            0  wosres:WOS_000071013000007                Clinical Neurology; Orthopedics
            1  wosres:WOS_000071018600001  Biology; Mathematical & Computational Biology
            2  wosres:WOS_000071021600006                               Physics, Nuclear
            3  wosres:WOS_000071040300005                                 Plant Sciences

            >>> # Tokenize the string column
            >>> my_Data_Frame.tokenize_string_column(string_column_name='wosKeywords',
            ...                                                           id_column_name='articleId',
            ...                                                           delimiter_pattern_in_literal_cells='; ')\
                .dataframe
                                articleId                           wosKeywords
            0  wosres:WOS_000071013000007                    Clinical Neurology
            1  wosres:WOS_000071013000007                           Orthopedics
            2  wosres:WOS_000071018600001                               Biology
            3  wosres:WOS_000071018600001  Mathematical & Computational Biology
            4  wosres:WOS_000071021600006                      Physics, Nuclear
            5  wosres:WOS_000071040300005                        Plant Sciences
            >>> #=======================================================================================================


            >>> # EXCEPTION: DATAFRAME HAS TOO MANY COLUMNS ============================================================
            >>> # Create a simple dataframe
            >>> my_dataframe = pandas.DataFrame({
            ...      'literal_column':['literal one; literal two', 'literal three; literal four'],
            ...     'id_column': ['id 1', 'id 2'],
            ...     'third_column': ['abc', 'xyz']
            ... })
            >>> my_Data_Frame = Data_Frame(my_dataframe)
            >>> my_Data_Frame.dataframe
              id_column               literal_column third_column
            0      id 1     literal one; literal two          abc
            1      id 2  literal three; literal four          xyz

            >>> # Error: The input dataframe has too many columns:
            >>> try: my_Data_Frame.tokenize_string_column(string_column_name='literal_column',
            ...                                                         id_column_name='id_column',
            ...                                                         delimiter_pattern_in_literal_cells='; ')
            ... except IndexError as exception:  # catch exception
            ...     print (exception)
            'tokenize_string_column' method can only take a Pandas.DataFrame with two columns. The current number of columns is 3.
            >>> #=======================================================================================================

        """
        import pandas

        number_of_columns = self.dataframe.shape[1]
        if number_of_columns > 2:
            raise IndexError(
                "'tokenize_string_column' method can only take a Pandas.DataFrame with two columns. "
                "The current number of columns is %s." % number_of_columns)

        # get index positions of columns
        index_of_literal_column = self.dataframe.columns.get_loc(string_column_name)
        if id_column_name:
            index_of_id_column = self.dataframe.columns.get_loc(id_column_name)

        # tokenize literals at cell level
        literal_column = self.dataframe[string_column_name]
        splitted_literal_column = literal_column.str.split(delimiter_pattern_in_literal_cells)
        # update the column
        self.dataframe[string_column_name] = splitted_literal_column

        # create blank dataframe for output
        original_column_names = list(self.dataframe.columns)
        output_dataframe = pandas.DataFrame(columns=original_column_names)

        # create a new row for each tokenized literal
        for each_row_number, each_row in self.dataframe.iterrows():

            column_names = each_row.index.values
            row_values = each_row.values

            for each_literal in row_values[index_of_literal_column]:
                if id_column_name:
                    output_dataframe.loc[len(output_dataframe)] = (row_values[index_of_id_column], each_literal)
                else:
                    output_dataframe.loc[len(output_dataframe)] = (each_literal)

        self.dataframe = output_dataframe
        return self


    def purify_column(self, target_column_name):
        """
        Cleans the specified column from undesirable characters.

        Args:
            target_column_name(str): Column to be cleaned

        Returns:
            Data_Frame (updated self)

        Examples:
            >>> import pandas

            >>> # CLEAN A COLUMN =======================================================================================
            >>> # Create Data_Frame
            >>> my_dataframe = pandas.DataFrame({
            ...             'dirty_column':['{string} & one','String, "two"','[string] - three','(string) /\ four;'],
            ...             'id_column': ['id 1', 'id 2', 'id 3', 'id 4'],
            ...             'another_column': ['abc', 'mno', 'pqr', 'xyz']})
            >>> my_Data_Frame = Data_Frame(my_dataframe)
            >>> my_Data_Frame.dataframe
              another_column       dirty_column id_column
            0            abc     {string} & one      id 1
            1            mno      String, "two"      id 2
            2            pqr   [string] - three      id 3
            3            xyz  (string) /\ four;      id 4

            >>> # Clean the column
            >>> my_Data_Frame.purify_column('dirty_column')\
                             .dataframe
              another_column    dirty_column id_column
            0            abc  string and one      id 1
            1            mno     String, two      id 2
            2            pqr  string - three      id 3
            3            xyz     string four      id 4
            >>> #=======================================================================================================


            >>> # EXCEPTION: COLUMN MUST CONSIST OF STRINGS ============================================================
            >>> # Create a column that is made of integers
            >>> my_dataframe = pandas.DataFrame({
            ...      'integer_column':[1,
            ...                      2,
            ...                      3,
            ...                      4
            ...      ]
            ... })
            >>> my_Data_Frame = Data_Frame(my_dataframe)
            >>> my_Data_Frame.dataframe
               integer_column
            0               1
            1               2
            2               3
            3               4

            >>> # Fail to purify integer column
            >>> try:
            ...     my_Data_Frame.purify_column('integer_column')
            ... except Exception as exception:  # catch exception
            ...     print (exception)
            The target column "integer_column" must be of dtype "object". It is currently of dtype "int64".
            >>> #=======================================================================================================

        """
        from preprocessor.string_tools import String

        target_column = self.dataframe[target_column_name]

        # Target column must be made of strings
        self._force_column_type(target_column_name=target_column_name, dtype='object')  # 'O' stands for 'object'
                                                                    # a string columns is categorized as 'object'

        conversion_dictionary = {
            '/':'',
            ';':'',       # sometimes, a semicolon seems to be at the end of keywords (e.g.,instead of "kw1; kw2; kw3"
                                                                                                     # "kw1; kw2; kw3;")
            '&':'and',
            '\(|\)': '',  # ()
            '\[|\]': '',  # []
            '\{|\}': '',  # {}
            '  ':' '      # clean from double spaces (may occur after cleaning other characters)
        }

        # Purify each string in the column
        for i, each_item in enumerate(target_column):
            each_String = String(each_item)
            each_String.purify(clean_from_non_ascii_characters=True,
                               remove_problematic_patterns=True,
                               clean_newline_characters=True)
            each_String.replace_patterns(conversion_dictionary)
            target_column.loc[i] = each_String.content

        return self


    def collapse_dataframe_on_column(self, identifier_column_name, values_column_name):
        """
        Merges values of a column based on their corresponding ids in the identifier column. The collapsed column
        remains tokenized (i.e., it consists of lists that are an aggregation of cells)

        Args:
            identifier_column_name(str)
            values_column_name(str)

        Returns:
            Data_Frame (updated self)

        Examples:
            >>> import pandas

            >>> # INDEXING A TWO-COLUMN DATAFRAME ======================================================================
            >>> # Create a simple dataframe
            >>> my_dataframe = pandas.DataFrame({'strings': ['string one', 'string two', 'string three', 'string four'],
            ...                                      'ids': ['id 1', 'id 1', 'id 1', 'id 2']})
            >>> my_Data_Frame = Data_Frame(my_dataframe)
            >>> my_Data_Frame.dataframe
                ids       strings
            0  id 1    string one
            1  id 1    string two
            2  id 1  string three
            3  id 2   string four

            >>> my_Data_Frame.collapse_dataframe_on_column(identifier_column_name='ids', values_column_name='strings')\
                             .dataframe
                ids                                 strings
            0  id 1  [string one, string two, string three]
            1  id 2                           [string four]

            >>> # The collapsed column consists of lists
            >>> cell = my_Data_Frame.dataframe['strings'][0]
            >>> type(cell)
            <class 'list'>
        """
        # Indexing: Create a dictionary in the format of {'identifier': ['value 1', 'value 2', 'value 3']}
        self._index_values_column_with_identifiers_column(values_column_name, identifier_column_name)

        # Retrieve the created index
        target_index_entry_key = values_column_name  # this is the key of the related registry object in instance index

        new_dataframe = self._build_pandas_dataframe_from_index(target_index_entry_key, values_column_name, identifier_column_name)
        self._replace_content_and_reset_instance_attributes(new_dataframe)

        return self


    def combine_items_within_each_row_if_combination_exists_in_external_list(self,
                                                                             target_column_name,
                                                                             external_list_to_compare_with,
                                                                             fragment_signalling_pattern,
                                                                             fragment_signalling_pattern_index
         ):
        """


        Examples:
            >>> import pandas

            >>> my_dataframe = pandas.DataFrame({'wos_categories': [
            ...                                                     ["Mathematical &", "Computational Biology", "Statistics & Probability"],
            ...                                                     ["Interdisciplinary Applications", "Biochemical Research Methods"],
            ...                                                     ["Biotechnology & Applied Microbiology"]
            ...                                                    ],
            ...                                             'ids': ['id 1', 'id 2', 'id 3']})
            >>> my_Data_Frame = Data_Frame(my_dataframe)
            >>> my_Data_Frame.dataframe
                ids                                     wos_categories
            0  id 1  [Mathematical &, Computational Biology, Statis...
            1  id 2  [Interdisciplinary Applications, Biochemical R...
            2  id 3             [Biotechnology & Applied Microbiology]

            >>> my_Data_Frame.dataframe.loc[0, 'wos_categories']
            ['Mathematical &', 'Computational Biology', 'Statistics & Probability']

            >>> external_list = ['Mathematical & Computational Biology', 'Architecture', 'Statistics & Probability']

            >>> my_Data_Frame.combine_items_within_each_row_if_combination_exists_in_external_list(
            ...                                   external_list_to_compare_with=external_list,
            ...                                   target_column_name='wos_categories',
            ...                                   fragment_signalling_pattern='&',
            ...                                   fragment_signalling_pattern_index=-1)\
                             .dataframe
                ids                                     wos_categories
            0  id 1  [Statistics & Probability, Mathematical & Comp...
            1  id 2  [Interdisciplinary Applications, Biochemical R...
            2  id 3             [Biotechnology & Applied Microbiology]

            >>> my_Data_Frame.dataframe.loc[0, 'wos_categories']
            ['Statistics & Probability', 'Mathematical & Computational Biology']

        Notes:
            See 'preprocessor.list_tools.combine_items_if_their_combination_exists_in_external_list' method for further tests.


        """
        from preprocessor.list_tools import List

        target_column = self.dataframe[target_column_name]

        for i, each_row in enumerate(target_column):
            each_List_with_reconstructed_items = List(each_row)

            each_List_with_reconstructed_items.combine_items_if_their_combination_exists_in_external_list(
                fragment_signalling_pattern=fragment_signalling_pattern,
                fragment_signalling_pattern_index=fragment_signalling_pattern_index,
                external_list_to_compare_with=external_list_to_compare_with
            )

            target_column.loc[i] = each_List_with_reconstructed_items.content

        return self


    def _build_pandas_dataframe_from_index(self, target_index_entry_key, desired_values_column_name,
                                           desired_identifier_column_name):
        """

        Args:
            target_index_entry_key(str)

        Returns:
            pandas.DataFrame

        Examples:
            >>> import pandas

            >>> # GENERAL EXAMPLE ======================================================================================
            >>> # Create a simple dataframe
            >>> my_dataframe = pandas.DataFrame({'strings': ['string one', 'string two', 'string three', 'string four'],
            ...                                      'ids': ['id 1', 'id 1', 'id 1', 'id 2']})
            >>> my_Data_Frame = Data_Frame(my_dataframe)
            >>> my_Data_Frame.dataframe
                ids       strings
            0  id 1    string one
            1  id 1    string two
            2  id 1  string three
            3  id 2   string four

            >>> # Generate and view the index
            >>> my_Data_Frame._index_values_column_with_identifiers_column(values_column_name='strings',
            ...                                              identifier_column_name='ids')\
                             ._index['strings'].content  # output the index for viewing
            {'id 1': ['string one', 'string two', 'string three'], 'id 2': ['string four']}

            >>> # Replace the original dataframe with a collapsed one using the index:
            >>> my_Data_Frame._build_pandas_dataframe_from_index(target_index_entry_key='strings',
            ...                                                  desired_values_column_name='strings',
            ...                                                  desired_identifier_column_name='id')
                 id                                 strings
            0  id 1  [string one, string two, string three]
            1  id 2                           [string four]
            >>> #=======================================================================================================

        """
        import pandas

        # Check if and index is in place
        self._require_index_entry(target_index_entry_key)

        # Retrieve the Registry object from the instance index
        target_registry_object = self._index.pop(target_index_entry_key, None)  # pop also deletes the index..
                                                                               # ...(this is intended for saving memory)
        # Create the output dataframe
        new_dataframe = pandas.DataFrame(columns=[desired_identifier_column_name, desired_values_column_name])


        for each_key, each_values in target_registry_object.content.items():
            current_last_row = new_dataframe.shape[0]

            new_dataframe.loc[current_last_row, desired_identifier_column_name] = each_key
            new_dataframe.loc[current_last_row, desired_values_column_name] = each_values

        return new_dataframe


    def _require_index_entry(self, target_index_entry_key):
        """

        Args:
            target_index_entry_key:

        Returns:

        Examples:
            >>> # GENERAL EXAMPLES =====================================================================================
            >>> # Prep -------------------------------------------------------------------------------------------------
            >>> from preprocessor.dict_tools import Registry
            >>> import pandas

            >>> my_dataframe = pandas.DataFrame(columns=['Column A', 'Column B'])
            >>> my_Data_Frame = Data_Frame(my_dataframe)

            >>> my_registry = Registry()
            >>> my_registry.add(key='key a', value='value 1')\
                           .add(key='key a', value='value 2')\
                           .content
            {'key a': ['value 1', 'value 2']}

            >>> my_Data_Frame._index = {'index x': my_registry}  # manually injecting a Registry object to index
            >>>                                                 # (normally, this is done automatically)
            #-----------------------------------------------------------------------------------------------------------

            >>> # Valid index key call
            >>> my_Data_Frame._require_index_entry('index x')

            >>> # Exception: Index key is not in registry.
            >>> try:
            ...     my_Data_Frame._require_index_entry('wrong index key')
            ... except Exception as exception:  # catch exception
            ...     print (exception)
            There is no index entry in self._index dictionary that matches the key 'wrong index key'. An index may need to be first created with '_index_values_column_with_identifiers_column' method.

            #===========================================================================================================
        """

        from preprocessor.string_tools import Parameter_Value

        try:
            Parameter_Value.require_parameters(parameters_list=[self._index[target_index_entry_key]],
                                               parameter_names=['target_index_entry_key'])
        except KeyError:
            raise AttributeError("There is no index entry in self._index dictionary that matches the key '%s'. "
                                 "An index may need to be first created with"
                                 " '_index_values_column_with_identifiers_column' method."
                                 % target_index_entry_key)

    def _index_values_column_with_identifiers_column(self, values_column_name, identifier_column_name):
        """
        Generates and index in dict format and adds it to self._index as an entry. This entry can be called by using
        "self._index['values_column_name']"; it would return a "Registry" object whose content can be accessed using
        "my_registry_object.content"

        Args:
            values_column_name(str)
            identifier_column_name(str)

        Returns:
            Data_Frame (updated self)

        Examples:
            >>> import pandas

            >>> # INDEXING IN A TWO-COLUMN DATAFRAME ===================================================================
            >>> # Create a simple dataframe
            >>> my_dataframe = pandas.DataFrame({'strings':['string one', 'string two', 'string three', 'string four'],
            ...                                      'ids': ['id 1', 'id 1', 'id 1', 'id 2']})
            >>> my_Data_Frame = Data_Frame(my_dataframe)
            >>> my_Data_Frame.dataframe
                ids       strings
            0  id 1    string one
            1  id 1    string two
            2  id 1  string three
            3  id 2   string four

            >>> # Generate and view the index
            >>> my_Data_Frame._index_values_column_with_identifiers_column(values_column_name='strings',
            ...                                              identifier_column_name='ids')\
                             ._index['strings'].content  # output the index for viewing
            {'id 1': ['string one', 'string two', 'string three'], 'id 2': ['string four']}
            >>> #=======================================================================================================


            >>> # INDEXING USING TWO COLUMNS IN A THREE-COLUMN DATAFRAME ===============================================
            >>> # Create a simple dataframe
            >>> my_dataframe = pandas.DataFrame({'strings':['string one', 'string two', 'string three', 'string four'],
            ...                       'irreleveant_column': [1, 2, 3, 4],
            ...                                      'ids': ['id 1', 'id 1', 'id 1', 'id 2']})
            >>> my_Data_Frame = Data_Frame(my_dataframe)
            >>> my_Data_Frame.dataframe
                ids  irreleveant_column       strings
            0  id 1                   1    string one
            1  id 1                   2    string two
            2  id 1                   3  string three
            3  id 2                   4   string four

            >>>
            >>> my_Data_Frame._index_values_column_with_identifiers_column(values_column_name='strings',
            ...                                              identifier_column_name='ids')\
                             ._index['strings'].content  # output the index for viewing
            {'id 1': ['string one', 'string two', 'string three'], 'id 2': ['string four']}
            >>> #=======================================================================================================
        """
        from preprocessor.dict_tools import Registry
        local_index = Registry()
        # get index positions of columns
        position_of_keys_column = self.dataframe.columns.get_loc(identifier_column_name)
        position_of_values_column = self.dataframe.columns.get_loc(values_column_name)
        for each_row_number, each_series_object in self.dataframe.iterrows():
            current_row = each_series_object.values

            current_key = current_row[position_of_keys_column]
            current_value = current_row[position_of_values_column]

            local_index.add(current_key, current_value)

        index_entry_name = values_column_name
        self._index[index_entry_name] = local_index

        return self


    def _force_column_type(self, target_column_name, dtype):
        """

        Args:
            target_column_name(str)
            dtype(str)

        Kwargs:
            ... (dtype): any of pandas dtypes

        Returns:
            If the check is passed: nothing
            If the check is failed: Exception

        Examples:
            >>> import pandas

            >>> # MISC TESTING =========================================================================================
            >>> my_dataframe = pandas.DataFrame({'strings': ['string one', 'string two', 'string three', 'string four'],
            ...                                 'integers': [1, 2, 3, 4]})
            >>> my_Data_Frame = Data_Frame(my_dataframe)
            >>> my_Data_Frame.dataframe
               integers       strings
            0         1    string one
            1         2    string two
            2         3  string three
            3         4   string four

            >>> # Pass: Expected and actual types match each other
            >>> my_Data_Frame._force_column_type('strings', 'object')
            >>> my_Data_Frame._force_column_type('strings', 'O')  # 'O' is synonymous with 'object'. string columns are\
                                                                  # of type object
            >>> my_Data_Frame._force_column_type('integers', 'int64')

            >>> # Exception: Mismatch between expected and actual type
            >>> try:
            ...     my_Data_Frame._force_column_type('integers', 'object')
            ... except Exception as exception:  # catch exception
            ...     print (exception)
            The target column "integers" must be of dtype "object". It is currently of dtype "int64".
            >>> #=======================================================================================================

        """
        target_column = self.dataframe[target_column_name]
        # Target column must be made of strings
        if target_column.dtype != dtype:
            raise TypeError('The target column "%s" must be of dtype "%s". It is currently of dtype "%s".'
                            % (target_column_name, dtype, target_column.dtype))


    def _replace_content_and_reset_instance_attributes(self, pandas_dataframe):
        """

        Args:
            pandas_dataframe (pandas.DataFrame)

        Returns:
            Data_Frame (updated self)

        Examples:
        >>> import pandas

        >>> # GENERAL TESTING ======================================================================================
        >>> first_pandas_dataframe = pandas.DataFrame({'strings': ['string one', 'string two', 'string three', 'string four'],
        ...                                 'integers': [1, 2, 3, 4]})
        >>> my_Data_Frame = Data_Frame(first_pandas_dataframe)
        >>> my_Data_Frame.dataframe
           integers       strings
        0         1    string one
        1         2    string two
        2         3  string three
        3         4   string four

        >>> second_pandas_dataframe = pandas.DataFrame({'strings':['string one', 'string two', 'string three', 'string four'],
        ...                                      'ids': ['id 1', 'id 1', 'id 1', 'id 2']})
        >>> my_Data_Frame._replace_content_and_reset_instance_attributes(second_pandas_dataframe)\
                         .dataframe
            ids       strings
        0  id 1    string one
        1  id 1    string two
        2  id 1  string three
        3  id 2   string four
        """
        self.dataframe = pandas_dataframe
        self._index = {}
        return self
