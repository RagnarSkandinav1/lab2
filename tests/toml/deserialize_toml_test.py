import pytest

from serializers.exception.exceptions import DeserializationException
from serializers.toml.deserialize import deserialize


def test_deserialize_list():
    expected = {'array': [1, 2, 3, 4, 5]}
    string = "array = [1,2,3,4,5]"

    actual = deserialize(string)

    assert actual == expected


def test_deserialize_list_of_dictionaries():
    expected = {'array': [{'a': 1, 'b': 2, 'c': 3}, {'a': 4, 'b': 5, 'c': 6}, {'a': 7, 'b': 8, 'c': 9}]}
    string = "[[array]]\n"\
             "a = 1\n"\
             "b = 2\n"\
             "c = 3\n"\
             "\n"\
             "[[array]]\n"\
             "a = 4\n"\
             "b = 5\n"\
             "c = 6\n" \
             "\n" \
             "[[array]]\n"\
             "a = 7\n"\
             "b = 8\n"\
             "c = 9"

    actual = deserialize(string)

    assert actual == expected


def test_deserialize_dictionary():
    expected = {'ok': False, 'some': {'dictionary': 'inside', 'test': 3.8}}
    string = "ok = false\n" \
             "\n" \
             "[some]\n" \
             "dictionary = 'inside'\n" \
             "test = 3.8"

    actual = deserialize(string)

    assert actual == expected


def test_deserialize_invalid():
    string = "{main}\n" \
             "test = 3"

    with pytest.raises(DeserializationException):
        deserialize(string)


def test_deserialize_invalid_value():
    string = "test = [3"

    with pytest.raises(DeserializationException):
        deserialize(string)
