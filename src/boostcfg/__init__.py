"""File parser for config files from Boost.

The boostcfg parser is a Python module for parsing Boost config files that can be parsed
by the `parse_config_file
<https://www.boost.org/doc/libs/1_72_0/doc/html/boost/program_options/parse_co_1_3_32_9_8_1_1_11.html>`__
of :code:`boost::program_options`.

BoostConfigParser was especially designed for `Pawian
<https://panda-wiki.gsi.de/bin/view/PWA/PawianPwaSoftware>`__.
"""

from __future__ import annotations

from typing import Any

from . import lineparser


class BoostConfigParser:
    """Data structure that holds information of Boost config files."""

    def __init__(self, filename: str | None = None) -> None:
        self.__values: dict[str, Any] = {}
        self.__config_file: str | None = None
        if isinstance(filename, str):
            self.read_config(filename=filename, reset=True)

    def read_config(self, filename: str, reset: bool = True) -> None:
        """Parse a config line and to the internal `dict`."""
        self.__config_file = filename
        if reset:
            self.__values = {}
        with open(filename) as stream:
            for line in stream:
                self.append_value_from_line(line)

    def append_value_from_line(self, line: str) -> None:
        """Smartly append a key-value pair from a line."""
        if lineparser.is_empty(line):
            return
        (key, value) = lineparser.get_key_value_pair(line)
        converted_value = lineparser.string_to_value(value)
        self.append_value(key, converted_value)

    def append_value(self, key: str, value: Any) -> None:
        """Append a key-value pair.

        Append a key-value pair to the internal dictionary: convert existing string
        values to a list if a new value with the same key is added.
        """
        if key in self.__values:
            old_values = self.__values[key]
            if not isinstance(old_values, list):
                self.__values[key] = [old_values]
            self.__values[key].append(value)
        else:
            self.__values[key] = value

    def __getitem__(self, key: str) -> Any:
        return self.__values[key]

    @property
    def config_file(self) -> str | None:
        return self.__config_file
