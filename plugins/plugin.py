"""
Superclass of all plugins.
"""


class Plugin(object):
    def __init__(self, name, properties):
        self.__name = name
        self.__properties = properties

    @property
    def name(self):
        return self.__name

    @property
    def properties(self):
        return self.__properties

    def filter(self, msg):
        """
        Judge if message can pass this filter.

        Returns:
            Must return a bool value. True if message is handled inplace; False if not.
        """
        raise NotImplementedError('[Plugin.filter] needs to be implemented.')

    def handle_msg(self):
        """
        If [filter] returns True, we can now handle message using this method.
        """
        raise NotImplementedError('[Plugin.handle_msg] needs to be implemented.')

    def __str__(self):
        raise NotImplementedError('[Plugin.__str__] needs to be implemented.')
