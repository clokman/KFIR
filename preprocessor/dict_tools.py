class Registry():
    """
    >>> # create registry
    >>> my_registry = Registry()

    >>> # add content
    >>> my_registry.add(key='a', value='b').content
    {'a': ['b']}

    >>> # modify content directly (not recommended)
    >>> my_registry.content = {'m':['n', 'o'], 'x':['y'], 'z':['t']}
    >>> my_registry.content
    {'m': ['n', 'o'], 'x': ['y'], 'z': ['t']}

    >>> # key call
    >>> my_registry.get_values_from_key('x')
    ['y']

    >>> # iteration
    >>> for each_item in my_registry.content:
    ...     print(each_item)
    m
    x
    z

    >>> # dictionary methods
    >>> for each_key, each_value in my_registry.content.items():
    ...     print(each_key, each_value)
    m ['n', 'o']
    x ['y']
    z ['t']

    """

    def __init__(self):
        # will hold keys vs values as dictionary items. e.g., {key_x: value_1, key_y: value_2}
        self.content = {}

    def add(self, key, value):
        """
        If registry does not have a key for key, creates it and assigns value as value.
        If there is already a key in registry, appends the value to that entry.

        Returns:
            Registry object (self)

        Examples:
            >>> # prep
            >>> my_registry = Registry()

            >>> # add item
            >>> my_registry.add(key='a', value='b').content
            {'a': ['b']}

            >>> # add another item
            >>> my_registry.add(key='x', value=1).content
            {'a': ['b'], 'x': [1]}

            >>> # add a second value to a key
            >>> my_registry.add(key='x', value='3333').content
            {'a': ['b'], 'x': [1, '3333']}
        """
        registry = self.content

        # create key-value pair key is new, otherwise append value to existing key
        try:
            registry[key].append(value)
        except KeyError:
            registry[key] = [value]

        self.content = registry
        return self


    def get_values_from_key(self, key):
        """
        Returns a list of values of a key if it is present. Raises exception otherwise.

        Returns:
            list

        Examples:
            >>> # prep
            >>> my_registry = Registry()
            >>> my_registry.add(key='a', value='11').add(key='a', value=3333).content
            {'a': ['11', 3333]}

            >>> # get values
            >>> my_registry.get_values_from_key('a')
            ['11', 3333]

        """
        registry = self.content

        try:
            return registry[key]
        except IndexError:
            raise Exception("key '%s' not in registry." % key)
