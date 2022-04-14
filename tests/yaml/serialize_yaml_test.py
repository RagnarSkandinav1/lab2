from serializers.yaml.serialize import serialize
from tests.util.test_utils import TestObject


def test_serialize_list():
    expected = "- \n" \
               "  some: 1\n" \
               "  object: '2'\n" \
               "- 'value'\n" \
               "- 3\n"
    array = [{'some': 1, 'object': '2'}, 'value', 3]

    actual = serialize(array)

    assert actual == expected


def test_serialize_dictionary():
    expected = "some: \n" \
               "  dictionary: 'inside'\n" \
               "  test: 3\n" \
               "ok: true\n"
    obj = {'some': {'dictionary': 'inside', 'test': 3}, 'ok': True}

    actual = serialize(obj)

    assert actual == expected


def test_serialize_object():
    expected = "a: 1\n" \
               "b: '2'\n" \
               "c: \n" \
               "  a: 'test'\n" \
               "  b: 3\n" \
               "  c: true\n"
    obj = TestObject(1, '2', TestObject('test', 3, True))

    actual = serialize(obj)

    assert actual == expected
