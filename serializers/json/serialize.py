import collections


def serialize(obj: object) -> str:
    return __serialize_value(obj)


def __serialize_value(value: object) -> str:
    if value is None:
        return 'null'

    value_type = type(value)

    if value_type is bool:
        return str(value).lower()

    if value_type is int or value_type is float:
        return str(value)

    if value_type is str:
        return f'"{value}"'

    if isinstance(value, collections.Sequence):
        result = '['
        result += __serialize_array(value)
        result += ']'
        return result

    if isinstance(value, dict):
        result = '{'
        result += __serialize_dict(value)
        result += '}'
        return result

    result = '{'
    result += __serialize_dict(value.__dict__)
    result += '}'
    return result


def __serialize_array(value: collections.Sequence) -> str:
    result = ''

    for list_value in value:
        if len(result) > 1:
            result += ','

        result += __serialize_value(list_value)

    return result


def __serialize_dict(dictionary: dict) -> str:
    result = ""

    keys = dictionary.keys()

    for key in keys:
        if result:
            result += ','

        result += f'"{key}":'

        value = dictionary.get(key)

        result += __serialize_value(value)

    return result
