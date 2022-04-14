from serializers.abstract_mapper import AbstractMapper
from serializers.json.deserialize import deserialize
from serializers.json.serialize import serialize


class JsonMapper(AbstractMapper):

    def dumps(self, obj: object) -> str:
        return serialize(obj)

    def dump(self, obj: object, filepath: str) -> None:
        result = self.dumps(obj)

        with open(filepath, 'w') as file:
            file.write(result)

    def loads(self, string: str) -> object:
        return deserialize(string)

    def load(self, filepath: str) -> object:
        with open(filepath, 'r') as file:
            file_content = file.read()

        return self.loads(file_content)
