#!/usr/bin/env python3

import argparse
import configparser
import re
import shutil

from serializers.factory import create_mapper


def extract_file_extension(path: str) -> str:
    try:
        return re.match(r'^.+\.(?P<extension>\w+)$', path).group('extension')
    except AttributeError as e:
        raise ValueError('Passed file is invalid or has no extension')


parser = argparse.ArgumentParser()

parser.add_argument('-f', '--from', type=str, help='Input file')
parser.add_argument('-t', '--to', type=str, help='Output file')
parser.add_argument('-c', '--config', type=str, help='Config location')

args = parser.parse_args()
from_ = args.__dict__['from']  # from is a reserved word
to = args.to

if args.config:
    config = configparser.ConfigParser()
    config.read(args.config)
    from_ = config['parser']['from']
    to = config['parser']['to']

if from_ and to:
    try:
        from_format: str = extract_file_extension(from_)
    except Exception as e:
        print('Failed to parse source path: ' + str(e))
        exit(1)

    try:
        to_format: str = extract_file_extension(to)
    except Exception as e:
        print('Failed to parse destination path: ' + str(e))
        exit(1)

    if from_format == to_format:
        shutil.copyfile(from_, to)
        exit(0)

    try:
        mapper_from = create_mapper(from_format.lower())
        mapper_to = create_mapper(to_format.lower())

        value = mapper_from.load(from_)
        mapper_to.dump(value, to)

    except Exception as e:
        print('Failed to map data from one file to another. Cause: ' + str(e))
        exit(1)

else:
    print('Specify source file and destination file. Like:')
    print('map --from a.json --to b.yaml')

    exit(1)
