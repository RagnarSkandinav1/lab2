import re

from serializers.exception.exceptions import DeserializationException


def deserialize(string: str) -> object:
    try:
        return __deserialize_value(string)
    except Exception as e:
        if isinstance(e, DeserializationException):
            raise e
        else:
            raise DeserializationException('Invalid yaml passed') from e


def __deserialize_value(string: str) -> object:
    strip_string = string.strip()

    if strip_string == 'null':
        return None

    if strip_string == 'true':
        return True

    if strip_string == 'false':
        return False

    if strip_string.isdecimal():
        return int(strip_string)

    if re.fullmatch(r'\d+\.\d+', strip_string):
        return float(strip_string)

    if strip_string.startswith('"') and strip_string.endswith('"'):
        return strip_string[1:-1]

    if strip_string.startswith("'") and strip_string.endswith("'"):
        return strip_string[1:-1]

    if strip_string == '[]':
        return []

    if strip_string == '{}':
        return {}

    if strip_string.startswith('-'):
        return __deserialize_list(string)

    return __deserialize_dict(string)


def __deserialize_list(string: str) -> list:
    base_indent: str = re.findall('^ *-', string)[0]
    base_indent_whitespace = base_indent.replace('-', ' ')

    result_list = list()
    temp_string = None

    lines = string.split('\n')

    for line in lines:
        line = line.rstrip()

        if not line:
            continue

        if line.startswith(base_indent):
            if temp_string:
                temp_string = temp_string.replace(base_indent, base_indent_whitespace)
                result_list.append(deserialize(temp_string))

            temp_string = ''

        if not line or not line.endswith('-'):
            temp_string += line
            temp_string += '\n'

    temp_string = temp_string.replace(base_indent, base_indent_whitespace)
    result_list.append(deserialize(temp_string))

    return result_list


def __deserialize_dict(string: str) -> dict:
    base_indent = re.findall('^ *', string)[0]
    nested_item_indent = base_indent + ' '

    result_dictionary = dict()
    temp_string = ''
    key = ''

    lines = string.split('\n')

    for line in lines:
        line = line.rstrip()

        if not line:
            continue

        if not line.startswith(nested_item_indent):
            if key and temp_string:
                result_dictionary[key] = deserialize(temp_string)

            temp_string = ''
            key = ''

        if line.endswith(':'):
            if key:
                result_dictionary[key] = None

            key = line[0:-1]
        else:
            if key:
                temp_string += line
                temp_string += '\n'
            else:
                (name, value_string) = line.split(':', 1)
                result_dictionary[name.strip()] = deserialize(value_string)

    if key and temp_string:
        result_dictionary[key] = deserialize(temp_string)

    return result_dictionary
