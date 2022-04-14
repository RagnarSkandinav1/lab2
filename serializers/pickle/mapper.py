import pickle

from serializers.abstract_mapper import AbstractMapper
from serializers.exception.exceptions import DeserializationException


class PickleMapper(AbstractMapper):

    def dumps(self, obj: object) -> str:
        return pickle.dumps(obj).hex()

    def dump(self, obj: object, filepath: str) -> None:
        result = self.dumps(obj)

        with open(filepath, 'w') as file:
            file.write(result)

    def loads(self, string: str) -> object:
        try:
            return pickle.loads(bytes.fromhex(string))
        except Exception as e:
            raise DeserializationException('Invalid pickle passed') from e

    def load(self, filepath: str) -> object:
        with open(filepath, 'r') as file:
            file_content = file.read()

        return self.loads(file_content)
