from serializers.pickle.mapper import PickleMapper
from tests.util.test_utils import TestObject

mapper = PickleMapper()


def test_dumping_list():
    expected = ['a', 'b', 3, '123123']

    dumped = mapper.dumps(expected)
    loaded = mapper.loads(dumped)

    assert loaded == expected


def test_dumping_dictionary():
    expected = {'a': 'b', 3: '123123'}

    dumped = mapper.dumps(expected)
    loaded = mapper.loads(dumped)

    assert loaded == expected


def test_dumping_object():
    expected = TestObject(1, True, 'some_value')

    dumped = mapper.dumps(expected)
    loaded = mapper.loads(dumped)

    assert loaded == expected
