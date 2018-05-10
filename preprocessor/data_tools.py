class Pandas_Dataframe():

    def __init__(self, dataframe):
        """
            Args:
                dataframe(pandas.DataFrame)
        """
        self.dataframe = dataframe


    def insert_dataframe_at_index(self, index, dataframe_to_insert):
        """
        Args:
            index(int): Index to insert the dataframe at.

        Examples:
            >>> import pandas, numpy
            >>> df1 = pandas.DataFrame(numpy.array([[1,2,3]]), columns=['Column A', 'Column B', 'Column C'])
            >>> df2 = pandas.DataFrame(numpy.array([[3,4,5]]), columns=['Column A', 'Column B', 'Column C'])
            >>> df3 = pandas.DataFrame(numpy.array([[6,7,8]]), columns=['Column A', 'Column B', 'Column C'])
            >>> my_dataframe = Pandas_Dataframe(df1)
            >>> my_dataframe.insert_dataframe_at_index(len(my_dataframe.dataframe), df2)\
                            .insert_dataframe_at_index(len(my_dataframe.dataframe), df3)\
                            .dataframe
               Column A  Column B  Column C
            0         1         2         3
            1         3         4         5
            2         6         7         8
        """
        base_dataframe = self.dataframe

        base_dataframe_head = base_dataframe.iloc[:index, ]
        base_dataframe_tail = base_dataframe.iloc[index:, ]

        combined_dataframe = base_dataframe_head.append(dataframe_to_insert)\
                                                .append(base_dataframe_tail)\
                                                .reset_index(drop=True)
        self.dataframe = combined_dataframe

        return self