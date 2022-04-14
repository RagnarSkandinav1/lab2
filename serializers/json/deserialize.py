import re

from serializers.exception.exceptions import DeserializationException


def deserialize(string: str) -> object:
    try:
        return __deserialize_value(string)
    except Exception as e:
        if isinstance(e, DeserializationException):
            raise e
        else:
            __raise_exception()


def __deserialize_value(string: str) -> object:
    string = string.strip()

    if string == 'null':
        return None

    if string == 'true':
        return True

    if string == 'false':
        return False

    if string.isdecimal():
        return int(string)

    if re.fullmatch(r'\d+\.\d+', string):
        return float(string)

    if string.startswith('"') and string.endswith('"'):
        return string[1:-1]

    if string.startswith('[') and string.endswith(']'):
        return __deserialize_list(string)

    if string.startswith('{') and string.endswith('}'):
        return __deserialize_dict(string)

    __raise_exception()


def __deserialize_list(string: str) -> list:
    string = string[1:-1]
    string = string.strip()

    if not string:
        return list()

    result_list = list()

    brackets = list()
    next_value_index = 0
    inside_string = False

    for current_index, char in enumerate(string):
        if char == '"':
            inside_string = not inside_string

        if inside_string:
            continue

        if char == '{' or char == '[':
            brackets.append(char)
            continue

        if char == '}':
            if brackets[-1] == '{':
                brackets.pop()
            else:
                __raise_exception()

        if char == ']':
            if brackets[-1] == '[':
                brackets.pop()
            else:
                __raise_exception()

        if char == ',' and len(brackets) == 0:
            string_value = string[next_value_index:current_index]
            value = __deserialize_value(string_value)
            result_list.append(value)

            next_value_index = current_index + 1

    string_value = string[next_value_index:]
    value = __deserialize_value(string_value)
    result_list.append(value)

    return result_list


def __deserialize_dict(string: str) -> dict:
    string = string[1:-1]
    string = string.strip()

    if not string:
        return dict()

    result_dictionary = dict()

    brackets = list()
    next_value_index = 0
    inside_string = False

    for current_index, char in enumerate(string):
        if char == '"':
            inside_string = not inside_string

        if inside_string:
            continue

        if char == '{' or char == '[':
            brackets.append(char)
            continue

        if char == '}':
            if brackets[-1] == '{':
                brackets.pop()
            else:
                __raise_exception()

        if char == ']':
            if brackets[-1] == '[':
                brackets.pop()
            else:
                __raise_exception()

        if char == ',' and len(brackets) == 0:
            element_pair = string[next_value_index:current_index]
            (name, value_string) = element_pair.split(':', 1)
            name = name.strip()[1:-1]
            result_dictionary[name] = __deserialize_value(value_string)

            next_value_index = current_index + 1

    element_pair = string[next_value_index:]
    (name, value_string) = element_pair.split(':', 1)
    name = name.strip()[1:-1]
    result_dictionary[name] = __deserialize_value(value_string)

    return result_dictionary


def __raise_exception():
    raise DeserializationException('Invalid json passed')
