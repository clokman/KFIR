from preprocessor.legacy_functions.select_column import select_column


def preview_data(dataset, depth=0):
    """
    Transposes and prints data for easy previewing.

    :usage: function(dataset, depth_int)

    :param dataset:
        This is a database that contains headers.
        The database must have already been tokenized and to a variable.
    :param depth:
        The number of rows to print.
        (Rows will appear as lines next to column names in the transposed output).
    :returns: A line-by-line print of columns in a table. This is a transposed version of the table.
    :exception:
       01: User likely entered integer, string, or boolean instead of dataset.
    :example:
        >>> my_dataset = [["id", "number"],["John", 0], ["John", 12], ["Someone else", 7]]
        >>> preview_data(my_dataset)
        Transposed Table (Columns in original data => Rows in output)
        Displaying up to 4 values per column.
        =============================================================
        <BLANKLINE>
        id: 'John' 'John' 'Someone else'
        number: 0 12 7
        >>> preview_data(my_dataset, 5) # displays all columns 5 rows deep
        Transposed Table (Columns in original data => Rows in output)
        Displaying up to 5 values per column.
        =============================================================
        <BLANKLINE>
        id: 'John' 'John' 'Someone else'
        number: 0 12 7
    """

    #############################################################################################################

    # Check if input is a dataset
    if type(dataset) is str or type(dataset) is int or type(dataset) is bool:
        raise ValueError("01: Argument 1 must be a dataset.")

    # Import regex module for later use in function
    import re

    # If the number of rows to be displayed is not specified, set it to display all rows.
    if depth == 0:
        depth = len(dataset)

    # Select the number of rows specified by user
    # selected_rows = dataset[0:depth]
    column_headers = dataset[0]

    # Store each column in a list item
    extracted_columns = []
    for header in column_headers:
        extracted_columns.append(select_column(header, dataset))

    # Title and subtitle
    print("Transposed Table (Columns in original data => Rows in output)")
    print("Displaying up to " + str(depth) + " values per column.")
    print("=============================================================\n")

    # Print selected columns line by line, and clear unnecessary characters
    for i, column in enumerate(extracted_columns):
        output = str(column_headers[i]) + ": " + str(column[0:depth])
        output = re.sub("[\[\],]", "", output)
        print(output)
