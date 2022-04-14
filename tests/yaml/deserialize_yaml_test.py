import pytest

from serializers.exception.exceptions import DeserializationException
from serializers.yaml.deserialize import deserialize


def test_deserialize_list():
    expected = [{'some': 1, 'object': None}, 'value', False]
    yaml = "- \n" \
           "  some: 1\n" \
           "  object: null\n" \
           "- 'value'\n" \
           "- false\n"

    actual = deserialize(yaml)

    assert actual == expected


def test_deserialize_dictionary():
    expected = {'some': {'dictionary': 'inside', 'test': 3.1}, 'ok': True}
    yaml = "some:\n" \
           "  dictionary: 'inside'\n" \
           "  test: 3.1\n" \
           "ok: true\n"

    actual = deserialize(yaml)

    assert actual == expected


def test_deserialize_dictionary__with_colons_in_string():
    expected = {'addr': '192.168.0.1:5432', 'username': 'user'}
    yaml = "addr: '192.168.0.1:5432'\n" \
           "username: 'user'\n"

    actual = deserialize(yaml)

    assert actual == expected


def test_deserialize_invalid_yaml():
    yaml = "{value}\n" \
           "22"
    with pytest.raises(DeserializationException):
        deserialize(yaml)
