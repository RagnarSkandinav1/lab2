import collections

from typing import List, Tuple


def serialize(obj: object) -> str:
    return __serialize_value(obj, '')


def __serialize_value(value: object, field_name: str) -> str:
    if value is None:
        return ''

    value_type = type(value)

    if value_type is bool:
        return str(value).lower()

    if value_type is int or value_type is float:
        return str(value)

    if value_type is str:
        return f"'{value}'"

    if isinstance(value, collections.Sequence):
        return __serialize_array(value, field_name)

    if isinstance(value, dict):
        return __serialize_dict(value, field_name)

    return __serialize_dict(value.__dict__, field_name)


def __serialize_array(array: collections.Sequence, field_path: str) -> str:
    if not array:
        return '[]'

    if __should_serialized_as_table(array[0]):
        return __serialize_array_of_dicts(array, field_path)

    result = '['

    for value in array:
        if len(result) > 1:
            result += ','

        result += __serialize_value(value, field_path)

    result += ']'
    return result


def __serialize_array_of_dicts(array: collections.Sequence, field_path: str) -> str:
    result = ''

    for value in array:
        if result:
            result += '\n'

        result += f'[[{field_path}]]\n'
        result += __serialize_value(value, field_path).rstrip()
        result += '\n'

    return result


def __serialize_dict(dictionary: dict, field_path: str) -> str:
    result = ''

    # list[field name - dictionary]
    sub_dictionary_pairs: List[Tuple[str, dict]] = []

    for key in dictionary.keys():
        value = dictionary.get(key)

        if __should_serialized_as_table(value):
            if isinstance(value, dict):
                sub_dictionary_pairs.append((key, value))
            else:
                sub_dictionary_pairs.append((key, value.__dict__))

        elif __is_array_of_dicts(value):
            result += __serialize_array_of_dicts(value, __merge_field_path(field_path, key))

        else:
            serialized_value = __serialize_value(value, field_path)
            result += f'{key} = {serialized_value}\n'

    for sub_dictionary_pair in sub_dictionary_pairs:
        if result:
            result += '\n'

        (filed_name, sub_dictionary) = sub_dictionary_pair

        current_filed_name = __merge_field_path(field_path, filed_name)
        result += f'[{current_filed_name}]\n'
        result += __serialize_dict(sub_dictionary, current_filed_name).rstrip()
        result += '\n'

    return result


def __merge_field_path(path: str, field_name: str) -> str:
    if not path:
        return field_name

    return path + '.' + field_name


def __should_serialized_as_table(value: object) -> bool:
    value_type = type(value)

    if value_type is bool \
            or value_type is int \
            or value_type is float \
            or value_type is str \
            or isinstance(value, collections.Sequence):
        return False

    return True


def __is_array_of_dicts(value: object) -> bool:
    return isinstance(value, collections.Sequence)\
        and value\
        and __should_serialized_as_table(value[0])
