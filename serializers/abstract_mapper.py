class AbstractMapper:
    def dumps(self, obj: object) -> str:
        pass

    def dump(self, obj: object, filepath: str) -> None:
        pass

    def loads(self, string: str) -> object:
        pass

    def load(self, filepath: str) -> object:
        pass
