class TestObject:

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __eq__(self, other):
        if isinstance(other, TestObject):
            return self.a == other.a \
                   and self.b == other.b \
                   and self.c == other.c

        if isinstance(other, dict):
            return self.a == other['a'] \
                   and self.b == other['b'] \
                   and self.c == other['c']

        return False
