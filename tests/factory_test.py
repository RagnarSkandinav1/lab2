import pytest

from serializers.factory import create_mapper
from serializers.json.mapper import JsonMapper
from serializers.pickle.mapper import PickleMapper
from serializers.toml.mapper import TomlMapper
from serializers.yaml.mapper import YamlMapper


def test_create_json_mapper():
    mapper = create_mapper('json')

    assert isinstance(mapper, JsonMapper)


def test_create_yaml_mapper():
    mapper = create_mapper('yaml')

    assert isinstance(mapper, YamlMapper)


def test_create_toml_mapper():
    mapper = create_mapper('toml')

    assert isinstance(mapper, TomlMapper)


def test_create_pickle_mapper():
    mapper = create_mapper('pickle')

    assert isinstance(mapper, PickleMapper)


def test_create_mapper_with_invalid_type():
    with pytest.raises(ValueError):
        create_mapper('aaa')
