"""File parser for config files from Boost.

The boostcfg parser is a Python module for parsing Boost config files that
can be parsed by the `parse_config_file
<https://www.boost.org/doc/libs/1_72_0/doc/html/boost/program_options/parse_co_1_3_32_9_8_1_1_11.html>`__
of :code:`boost::program_options`.

BoostConfigParser was especially designed for `Pawian
<https://panda-wiki.gsi.de/foswiki/bin/view/PWA/PawianPwaSoftware>`__.
"""

from . import lineparser


class BoostConfigParser:
    """Data structure that holds information of Boost config files."""

    def __init__(self, filename=None):
        self.__values = {}
        self.__config_file = None
        if isinstance(filename, str):
            self.read_config(filename=filename, reset=True)

    def read_config(self, filename, reset=True):
        """Parse a config line and to the internal `dict`."""
        self.__config_file = filename
        if reset:
            self.__values = {}
        with open(filename, "r") as stream:
            for line in stream.readlines():
                self.append_value_from_line(line)

    def append_value_from_line(self, line):
        """Smartly append a key-value pair from a line."""
        if lineparser.is_empty(line):
            return
        (key, value) = lineparser.get_key_value_pair(line)
        converted_value = lineparser.string_to_value(value)
        self.append_value(key, converted_value)

    def append_value(self, key, value):
        """Append a key-value pair.

        Append a key-value pair to the internal dictionary: convert existing
        string values to a list if a new value with the same key is added.
        """
        if key in self.__values:
            old_values = self.__values[key]
            if not isinstance(old_values, list):
                self.__values[key] = [old_values]
            self.__values[key].append(value)
        else:
            self.__values[key] = value

    def __getitem__(self, key):
        return self.__values[key]

    @property
    def config_file(self) -> str:
        return self.__config_file
