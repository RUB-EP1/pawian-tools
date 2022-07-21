import pytest

from boostcfg import lineparser


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("errLogMode = trace", ("errLogMode", "trace")),
        ("  \tverbose	= true\n	  ", ("verbose", "true")),
        ("cloneParticle = pion+ pion+", ("cloneParticle", "pion+ pion+")),
        ("decay=Cano D*+ To D0 pion+  \t", ("decay", "Cano D*+ To D0 pion+")),
    ],
)
def test_get_key_value_pair(test_input, expected):
    assert lineparser.get_key_value_pair(test_input) == expected


@pytest.mark.parametrize("test_input", ["something", r" \tsome string # and comment"])
def test_get_faulty_key_value_pair(test_input):
    with pytest.raises(SyntaxError):
        lineparser.get_key_value_pair(test_input)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("\t don't ignore # and a comment", False),
        ("  \t# ignore whitespaces", True),
    ],
)
def test_is_commented(test_input, expected):
    assert lineparser.is_commented(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("   some text  ", False),
        ("# and a comment", True),
        ("  \t# ignore whitespaces", True),
    ],
)
def test_is_empty(test_input, expected):
    assert lineparser.is_empty(test_input) == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("", ""),
        ("No comments here", "No comments here"),
        ("before # after", "before "),
        ("\t don't ignore # and a comment", "\t don't ignore "),
        ("  \t# ignore whitespaces", "  \t"),
        ("before# after # and another", "before"),
        ("#Fully commented", ""),
    ],
)
def test_strip_comment(test_input, expected):
    assert lineparser.strip_comment(test_input) == expected
