from serializers.json.serialize import serialize
from tests.util.test_utils import TestObject


def test_serialize_list():
    expected = '[{"some":1,"object":"2"},{"another":3,"object":[]}]'
    array = [{'some': 1, 'object': '2'}, {'another': 3, 'object': []}]

    actual = serialize(array)

    assert actual == expected


def test_serialize_dictionary():
    expected = '{"some":1,"object":"2"}'
    obj = {'some': 1, 'object': '2'}

    actual = serialize(obj)

    assert actual == expected


def test_serialize_object():
    expected = '{"a":1,"b":"2","c":3.0}'
    obj = TestObject(1, '2', 3.0)

    actual = serialize(obj)

    assert actual == expected

