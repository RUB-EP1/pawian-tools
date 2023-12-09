"""A collection of tools to parse lines in a Boost config file."""

from __future__ import annotations

__all__ = [
    "get_key_value_pair",
    "is_commented",
    "is_empty",
    "strip_comment",
    "string_to_value",
]


import re


def get_key_value_pair(line: str) -> tuple[str, str]:
    """Extract key and value from a line in a :code:`cfg` file.

    Extracts everything before an equal sign as the key, and everything after as the
    value.
    """
    new_line = strip_comment(line)
    matches = re.search(r"^\s*([^\s]+?)\s*=\s*([^\s]+.*?)\s*$", strip_comment(new_line))
    if matches is None:
        msg = f'Line "{new_line}" is not a key, value pair!'
        raise SyntaxError(msg)
    return matches[1], matches[2]


def is_commented(line: str) -> bool:
    """Check if a line starts with a comment sign (#), ignoring whitespaces."""
    return (bool)(re.match(r"\s*#", line))


def is_empty(line: str) -> bool:
    """Check if a line is empty or commented."""
    return (bool)(re.match(r"^\s*$", line)) or is_commented(line)


def strip_comment(line: str) -> str:
    """Remove everything before a comment sign (:code:`#`)."""
    matches = re.search(r"^[^#]*", line)
    if matches is None:
        msg = f"Line {line} is not valid"
        raise ValueError(msg)
    return matches[0]


def string_to_value(string: str) -> bool | float | int | str:
    """Attempt to convert a string to a `float` or `int`."""
    try:
        return int(string)
    except ValueError:
        try:
            return float(string)
        except ValueError:
            lower_string = string.lower()
            if lower_string == "true":
                return True
            if lower_string == "false":
                return False
            return string
