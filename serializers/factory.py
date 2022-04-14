from serializers.abstract_mapper import AbstractMapper
from serializers.json.mapper import JsonMapper
from serializers.pickle.mapper import PickleMapper
from serializers.toml.mapper import TomlMapper
from serializers.yaml.mapper import YamlMapper


def create_mapper(mapper_type: str) -> AbstractMapper:
    if mapper_type == 'json':
        return JsonMapper()
    if mapper_type == 'yaml':
        return YamlMapper()
    if mapper_type == 'toml':
        return TomlMapper()
    if mapper_type == 'pickle':
        return PickleMapper()

    raise ValueError('Unsupported mapper type: ' + mapper_type)
