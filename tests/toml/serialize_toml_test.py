from serializers.toml.serialize import serialize
from tests.util.test_utils import TestObject


def test_serialize_list():
    expected = "array = [1,2,3,4,5]\n"
    # in toml no root array is possible, so we wrap it
    array = {'array': [1, 2, 3, 4, 5]}

    actual = serialize(array)

    assert actual == expected


def test_serialize_list_of_objects():
    expected = "[[array]]\n"\
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
               "c = 9\n"
    # in toml no root array is possible, so we wrap it
    array = {'array': [TestObject(1, 2, 3), TestObject(4, 5, 6), TestObject(7, 8, 9)]}

    actual = serialize(array)

    assert actual == expected


def test_serialize_dictionary():
    expected = "ok = true\n" \
               "\n" \
               "[some]\n" \
               "dictionary = 'inside'\n" \
               "test = 3\n"
    dictionary = {'some': {'dictionary': 'inside', 'test': 3}, 'ok': True}

    actual = serialize(dictionary)

    assert actual == expected


def test_serialize_object():
    expected = "a = 1\n" \
               "b = '2'\n" \
               "\n" \
               "[c]\n" \
               "a = 'test'\n" \
               "b = 3\n" \
               "c = true\n"
    obj = TestObject(1, '2', TestObject('test', 3, True))

    actual = serialize(obj)

    assert actual == expected
