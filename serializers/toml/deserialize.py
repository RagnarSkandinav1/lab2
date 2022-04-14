import re
from collections import deque
from typing import List

from serializers.exception.exceptions import DeserializationException


def deserialize(string: str) -> object:
    try:
        return __deserialize_dict(string)
    except Exception as e:
        if isinstance(e, DeserializationException):
            raise e
        else:
            __raise_exception()


def __deserialize_dict(string: str) -> dict:
    global_dictionary = {}

    lines = deque(string.splitlines())

    while lines:
        line = lines.popleft().strip()

        if not line:
            continue

        if line.startswith('['):
            lines.appendleft(line)
            break

        (key, value) = line.split('=')
        global_dictionary[key.strip()] = __deserialize_value(value)

    current_dictionary = None

    while lines:
        line = lines.popleft().strip()

        if not line:
            continue

        if line.startswith('[['):
            path = line[2:-2]
            path_tokens = __split_path(path)
            current_array = __create_dictionaries_last_array(global_dictionary, path_tokens)
            current_dictionary = {}
            current_array.append(current_dictionary)

        elif line.startswith('['):
            path = line[1:-1]
            path_tokens = __split_path(path)

            current_dictionary = __create_dictionaries(global_dictionary, path_tokens)

        else:
            (key, value) = line.split('=')
            current_dictionary[key.strip()] = __deserialize_value(value)

    return global_dictionary


def __deserialize_value(string: str) -> object:
    string = string.strip()

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

    if string.startswith("'") and string.endswith("'"):
        return string[1:-1]

    if string.startswith('[') and string.endswith(']'):
        return __deserialize_list(string)

    __raise_exception()


def __deserialize_list(string: str) -> list:
    array_values = string[1:-1].split(',')

    array = []

    for value in array_values:
        array.append(__deserialize_value(value))

    return array


def __split_path(string: str) -> List[str]:
    return string.split('.')


def __create_dictionaries(global_dictionary: dict, path_tokens: List[str]) -> dict:
    current_dictionary = global_dictionary

    for token in path_tokens:
        if token not in current_dictionary:
            current_dictionary[token] = {}

        current_dictionary = current_dictionary[token]

    return current_dictionary


def __create_dictionaries_last_array(global_dictionary: dict, path_tokens: List[str]) -> list:
    current_dictionary = global_dictionary

    for index in range(len(path_tokens) - 1):
        token = path_tokens[index]

        if token not in current_dictionary:
            current_dictionary[token] = {}

        current_dictionary = current_dictionary[token]

    last_token = path_tokens[len(path_tokens) - 1]
    if last_token not in current_dictionary:
        current_dictionary[last_token] = []

    return current_dictionary[last_token]


def __raise_exception():
    raise DeserializationException('Invalid toml passed')
