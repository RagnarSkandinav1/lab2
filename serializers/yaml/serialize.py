import collections


def serialize(obj: object) -> str:
    return __serialize_value(obj, 0)


def __serialize_value(value: object, indent: int) -> str:
    if value is None:
        return 'null'

    value_type = type(value)

    if value_type is bool:
        return str(value).lower()

    if value_type is int or value_type is float:
        return str(value)

    if value_type is str:
        return f"'{value}'"

    if isinstance(value, collections.Sequence):
        result = '\n' if indent > 0 else ''
        result += __serialize_array(value, indent)
        return result

    if isinstance(value, dict):
        result = '\n' if indent > 0 else ''
        result += __serialize_dict(value, indent)
        return result

    result = '\n' if indent > 0 else ''
    result += __serialize_dict(value.__dict__, indent)
    return result


def __serialize_array(value: collections.Sequence, indent: int) -> str:
    if not value:
        return '[]'

    result = ''

    for list_value in value:
        serialized_value = __serialize_value(list_value, indent + 2).rstrip()
        result += f'{indent * " "}- {serialized_value}\n'

    return result


def __serialize_dict(dictionary: dict, indent: int) -> str:
    if not dictionary:
        return '{}'

    result = ''

    keys = dictionary.keys()

    for key in keys:
        result += f'{indent * " "}{key}: '

        value = dictionary.get(key)

        result += __serialize_value(value, indent + 2).rstrip()
        result += '\n'

    return result
