import pytest

from serializers.exception.exceptions import DeserializationException
from serializers.json.deserialize import deserialize


def test_deserialize_list():
    expected = [{'some': 1, 'object': None}, {'another': 3.5, 'object': []}]
    string = '[{"some":1,"object":null},{"another":3.5,"object":[]}]'

    actual = deserialize(string)

    assert actual == expected


def test_deserialize_dictionary():
    expected = {'some': 1, 'object': False, 'empty': {}}
    string = '{"some":1,"object":false,"empty":{}}'

    actual = deserialize(string)

    assert actual == expected


def test_deserialize_dictionary__with_commas_in_string():
    expected = {'some': 'value,a', 'object': 'value,b'}
    string = '{"some":"value,a","object":"value,b"}'

    actual = deserialize(string)

    assert actual == expected


def test_deserialize_dictionary__with_brackets_in_string():
    expected = {'some': 'value[}a', 'object': 'value{]b'}
    string = '{"some":"value[}a","object":"value{]b"}'

    actual = deserialize(string)

    assert actual == expected


def test_invalid_json__raises_exception():
    invalid_json = '{"some": "invalid", "json"}'

    with pytest.raises(DeserializationException):
        deserialize(invalid_json)


def test_invalid_brackets__raises_exception():
    invalid_json = '{"some": "invalid"]'

    with pytest.raises(DeserializationException):
        deserialize(invalid_json)
