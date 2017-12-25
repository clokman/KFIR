class Pybtex_import:
    """
    Parses the provided bibtex file into variables using the class constructor.

    Examples:
        # Example 1
        >>> # import package and class
            >>> from triplicator.pybtexImporter import Pybtex_import

            >>> # extract entries (i.e., dictionaries that has ids as keys and a sub-dictionary that contains fields
            >>> # and their values as values)
            >>> pybtex_entries = Pybtex_import("test.bib").data.entries

            >>> # parse different field names and values
            >>> for each_entry_id, each_entry in pybtex_entries.items():
            ...     print(each_entry.fields["title"])
            ...     try:
            ...         print(each_entry.fields["keywords"])
            ...     except:
            ...         pass
            Book with one author
            Article with 5 authors with 'and' notation
            Article with 3 authors with mixed notation
            Tax compliance, Auditing, Tax enforcement

        # Example 2
            >>> # parse author names (they are stored in a different object than field names and values)
            >>> # extract all author names from the imported bib file
            >>> for each_entry_id, each_entry in pybtex_entries.items():
            ...     print(each_entry.persons["author"])
            [Person('Jaschke, A.C.')]
            [Person('Lohr, Ansje'), Person('Beunen, R.'), Person('Savelli, Heidi'), Person('Kalz, Marco'), Person('Ragas, Ad'), Person('{Van Belleghem}, Frank')]
            [Person('{Mendoza Rodriguez}, J.P.'), Person('Wielhouwer, J.L.'), Person('Kirchler, Erich')]

        # Example 3
            >>> for each_entry_id, each_entry in pybtex_entries.items():
            ...    each_authors = (each_entry.persons["author"])
            ...    for each_author in each_authors:
            ...            print(each_author.last()[0])
            Jaschke
            Lohr
            Beunen
            Savelli
            Kalz
            Ragas
            {Van Belleghem}
            {Mendoza Rodriguez}
            Wielhouwer
            Kirchler
    """

    def __init__(self, bib_file_path):
        """
        Imports and holds the bibliography data as specified in pybtex package.

        Args:
            bib_file_path: The location of the bib file to be parsed.

        Returns:
            An instance that holds the bib data.

        Examples:
            >>> # Example 1
            >>> # import package and class
            >>> from triplicator.pybtexImporter import Pybtex_import

            >>> # extract entries (i.e., dictionaries that has ids as keys and a sub-dictionary that contains fields
            >>> # and their values as values)
            >>> pybtex_entries = Pybtex_import("test.bib").data.entries

            >>> # parse different field names and values
            >>> for each_entry_id, each_entry in pybtex_entries.items():
            ...     print(each_entry.fields["title"])
            ...     try:
            ...         print(each_entry.fields["keywords"])
            ...     except:
            ...         pass
            Book with one author
            Article with 5 authors with 'and' notation
            Article with 3 authors with mixed notation
            Tax compliance, Auditing, Tax enforcement

            >>> # Example 2
            >>> # parse author names (they are stored in a different object than field names and values)
            >>> # extract all author names from the imported bib file
            >>> for each_entry_id, each_entry in pybtex_entries.items():
            ...     print(each_entry.persons["author"])
            [Person('Jaschke, A.C.')]
            [Person('Lohr, Ansje'), Person('Beunen, R.'), Person('Savelli, Heidi'), Person('Kalz, Marco'), Person('Ragas, Ad'), Person('{Van Belleghem}, Frank')]
            [Person('{Mendoza Rodriguez}, J.P.'), Person('Wielhouwer, J.L.'), Person('Kirchler, Erich')]

            >>> # Example 3
            >>> for each_entry_id, each_entry in pybtex_entries.items():
            ...    each_authors = (each_entry.persons["author"])
            ...    for each_author in each_authors:
            ...            print(each_author.last()[0])
            Jaschke
            Lohr
            Beunen
            Savelli
            Kalz
            Ragas
            {Van Belleghem}
            {Mendoza Rodriguez}
            Wielhouwer
            Kirchler
        """

        # import and shorten bibtex parser function
        from pybtex.database.input import bibtex
        parser = bibtex.Parser()

        # Parse input file
        self.data = parser.parse_file(bib_file_path)

    # def removeUnbalancedEntries(self):
    #     # Turn each entry (and not just each line) in the .bib file into a string
    #     # (i.e., one string per entry, which contains multiple fields and their values)
    #     # This can be done via appending each line in-betweeen @ signs in the bib file to a variable
    #
    #     # Afterwards...
    #     for each_entry_string in XXX
    #         if balanced(each_entry_string):
    #             pass
    #             # if unbalanced
    #         else:
    #             # Delete string
    #
    #     balanced()
    #
    #     iparens = iter('(){}[]<>')
    #     parens = dict(zip(iparens, iparens))
    #     closing = parens.values()
    #
    #     def balanced(astr):
    #         """
    #          Code for balanced() by pillmuncher https://stackoverflow.com/questions/6701853/parentheses-pairing-issue
    #
    #         Returns:
    #             True if balanced, False if unbalanced.
    #         """
    #         stack = []
    #         for c in astr:
    #             d = parens.get(c, None)
    #             if d:
    #                 stack.append(d)
    #             elif c in closing:
    #                 if not stack or c != stack.pop():
    #                     return False
    #         return not stack
    #
